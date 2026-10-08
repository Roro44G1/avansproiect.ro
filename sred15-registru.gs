/**
 * RADAR AI — Registrul de răspunsuri SRED-15 (PRE / POST)
 * Asociația AVANS PROIECT Sibiu, 2026
 *
 * Script Google Apps Script legat de foaia de calcul a registrului
 * (Extensii > Apps Script). Primește răspunsurile trimise din paginile
 * sred15-pre.html și sred15-post.html, le validează, calculează scorurile,
 * le stochează și generează analiza PRE-POST.
 *
 * Prima utilizare: rulați funcția configureaza(), apoi implementați
 * scriptul ca aplicație web (Execută ca: Eu; Cine are acces: Oricine).
 */

const CFG = {
  VERSIUNE: 'SRED-15 web 1.0 (2026)',
  ADRESA_SITE: 'https://avansproiect.ro/',
  PAGINA: { PRE: 'sred15-pre.html', POST: 'sred15-post.html' },
  DURATA_MINIMA_SEC: 90,          // sub acest timp, răspunsul primește observația „completare rapidă”
  LIMITA_GRUPA_10MIN: 150,        // număr maxim de trimiteri acceptate pe grupă în 10 minute
  RANDURI_GRUPE: 60,              // câte rânduri pregătite are foaia Grupe
  RANDURI_VALIDARE: 2000          // câte rânduri primesc listă derulantă în PRE / POST
};

const FOAIE = {
  GRUPE: 'Grupe',
  PRE: 'PRE',
  POST: 'POST',
  PERECHI: 'Perechi PRE-POST',
  RAPORT: 'Raport',
  ITEMI: 'Itemi',
  JURNAL: 'Jurnal'
};

const ITEMI = [
  'Mă pot adapta bine atunci când apar schimbări neașteptate în viața mea.',
  'Pot face față oricărei situații dificile care apare.',
  'Când am o problemă, încerc să văd și latura pozitivă sau amuzantă a situației.',
  'A trece prin situații stresante sau dificile mă face mai puternic/ă.',
  'Revin destul de repede după o boală, un accident sau altă experiență dificilă.',
  'Cred că îmi pot atinge obiectivele chiar dacă există obstacole sau piedici.',
  'Sub presiune, rămân concentrat/ă și gândesc limpede.',
  'Nu mă descurajez ușor atunci când eșuez sau fac greșeli.',
  'Mă consider o persoană puternică atunci când mă confrunt cu provocări sau dificultăți.',
  'Pot gestiona sentimentele neplăcute sau dureroase (tristețe, frică, furie, anxietate).',
  'Când văd online conținut care mă supără sau mă deranjează, știu cum să gestionez emoția (mă opresc, respir, ies din aplicație).',
  'Pot recunoaște când rețelele sociale sau telefonul îmi afectează negativ starea de spirit în cursul zilei.',
  'Cred că valoarea mea ca persoană nu depinde de numărul de like-uri, comentarii sau urmăritori online.',
  'Știu să verific dacă o informație sau o știre online este adevărată înainte de a o crede sau de a o distribui.',
  'Am cel puțin o persoană de încredere (prieten, coleg, părinte, profesor) la care pot apela când trec printr-o situație dificilă.'
];

const ANTET_RASP = ['Marcaj temporal', 'ID răspuns', 'Cod grupă', 'Grupa', 'Cod personal', 'Clasa', 'Sex']
  .concat(ITEMI.map(function (_, i) { return 'I' + (i + 1); }))
  .concat(['Scor P1 (0-40)', 'Scor P2 (5-25)', 'Scor total (5-65)', 'Nivel (scor total)', 'Durata (sec)',
    'Observații automate', 'Decizie psiholog', 'Cod corectat (psiholog)', 'ID client', 'Versiune']);

// Indicii coloanelor din foile PRE / POST (de la 0)
const K = {
  ts: 0, id: 1, grupaCod: 2, grupa: 3, cod: 4, clasa: 5, sex: 6, i1: 7,
  p1: 22, p2: 23, total: 24, nivel: 25, durata: 26, obs: 27, decizie: 28,
  codCorectat: 29, client: 30, versiune: 31
};

const ANTET_GRUPE = ['Cod grupă', 'Eticheta afișată elevilor', 'PRE deschis (DA/NU)', 'POST deschis (DA/NU)',
  'Observații interne', 'Link PRE', 'Link POST', 'Cod QR PRE', 'Cod QR POST'];

const MESAJ = {
  FORMAT: 'Cererea nu are formatul așteptat.',
  VALIDARE: 'Unele date nu au trecut verificarea registrului.',
  OCUPAT: 'Registrul este ocupat. Cererea va fi retrimisă automat.',
  GRUPA_INEXISTENTA: 'Codul grupei nu este recunoscut.',
  ETAPA_INCHISA: 'Chestionarul nu este deschis acum pentru această grupă.',
  LIMITA: 'Prea multe trimiteri pentru această grupă în ultimele minute.',
  FARA_PERECHE: 'Codul personal nu apare la evaluarea inițială a acestei grupe.',
  EROARE: 'Registrul nu a putut salva răspunsurile.'
};

const RE_COD = /^[A-Z](0[1-9]|[12][0-9]|3[01])[A-Z](0[1-9]|1[0-2])$/;
const RE_GRUPA = /^[A-Z0-9-]{2,20}$/;

/* ------------------------------------------------------------------ */
/* Puncte de intrare web                                              */
/* ------------------------------------------------------------------ */

function doGet(e) {
  const p = (e && e.parameter) || {};
  try {
    if (p.action === 'grupa') return json_(infoGrupa_(p.g, p.etapa));
    return json_({ ok: true, serviciu: 'SRED-15', versiune: CFG.VERSIUNE });
  } catch (err) {
    jurnal_('GET', p.g, 'Eroare: ' + err);
    return json_({ ok: false, cod: 'EROARE', mesaj: MESAJ.EROARE });
  }
}

function doPost(e) {
  let d;
  try {
    d = JSON.parse((e && e.postData && e.postData.contents) || '');
  } catch (err) {
    return json_({ ok: false, cod: 'FORMAT', mesaj: MESAJ.FORMAT });
  }
  try {
    return json_(proceseazaTrimitere_(d));
  } catch (err) {
    jurnal_(d && d.etapa, d && d.grupa, 'Eroare: ' + err);
    return json_({ ok: false, cod: 'EROARE', mesaj: MESAJ.EROARE });
  }
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function eroare_(cod) {
  return { ok: false, cod: cod, mesaj: MESAJ[cod] || MESAJ.EROARE };
}

/* ------------------------------------------------------------------ */
/* Primirea unui chestionar                                           */
/* ------------------------------------------------------------------ */

function proceseazaTrimitere_(d) {
  const etapa = d && (d.etapa === 'PRE' || d.etapa === 'POST') ? d.etapa : null;
  if (!etapa) return eroare_('FORMAT');

  // Câmp-capcană pentru roboți: elevii nu îl văd și nu îl completează.
  if (d.website) {
    jurnal_(etapa, d.grupa, 'Respins: câmp-capcană completat');
    return { ok: true, chitanta: 'OK' };
  }

  const v = valideaza_(d);
  if (v.erori.length) {
    jurnal_(etapa, d.grupa, 'Validare respinsă: ' + v.erori.join(', '));
    return { ok: false, cod: 'VALIDARE', campuri: v.erori, mesaj: MESAJ.VALIDARE };
  }

  const lock = LockService.getScriptLock();
  if (!lock.tryLock(25000)) return eroare_('OCUPAT');
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const grupa = cautaGrupa_(ss, v.grupa);
    if (!grupa) {
      jurnal_(etapa, v.grupa, 'Grupă inexistentă');
      return eroare_('GRUPA_INEXISTENTA');
    }
    if (!grupa.deschis[etapa]) {
      jurnal_(etapa, v.grupa, 'Etapă închisă');
      return eroare_('ETAPA_INCHISA');
    }
    if (!limitaOk_(v.grupa)) {
      jurnal_(etapa, v.grupa, 'Limită de trimiteri atinsă');
      return eroare_('LIMITA');
    }

    const foaie = ss.getSheetByName(FOAIE[etapa]);
    const date = foaie.getDataRange().getValues();

    // Retrimiterea aceluiași formular (aceeași cheie de client) nu creează rânduri noi.
    for (let r = 1; r < date.length; r++) {
      if (String(date[r][K.client]) === v.clientId) {
        return { ok: true, chitanta: chitanta_(date[r][K.id]), repetat: true };
      }
    }

    const obs = [];
    const existaDeja = date.some(function (row, r) {
      return r > 0 && normGrupa_(row[K.grupaCod]) === v.grupa &&
        normCod_(row[K.codCorectat] || row[K.cod]) === v.cod && !esteExclus_(row[K.decizie]);
    });
    if (existaDeja) obs.push('DUPLICAT: codul personal există deja în această grupă');

    if (etapa === 'POST') {
      const pre = ss.getSheetByName(FOAIE.PRE).getDataRange().getValues();
      const arePereche = pre.some(function (row, r) {
        return r > 0 && normGrupa_(row[K.grupaCod]) === v.grupa &&
          normCod_(row[K.codCorectat] || row[K.cod]) === v.cod && !esteExclus_(row[K.decizie]);
      });
      if (!arePereche) {
        if (d.confirmFaraPereche !== true) {
          return { ok: false, cod: 'FARA_PERECHE', cereConfirmare: true, mesaj: MESAJ.FARA_PERECHE };
        }
        obs.push('FĂRĂ PERECHE PRE: elevul și-a confirmat codul');
      }
    }

    if (v.durata !== null && v.durata < CFG.DURATA_MINIMA_SEC) obs.push('COMPLETARE RAPIDĂ: ' + v.durata + ' s');
    if (uniform_(v.raspunsuri)) obs.push('RĂSPUNS UNIFORM la itemii 1-10');

    const s = scoruri_(v.raspunsuri);
    const id = Utilities.getUuid();
    const rand = [new Date(), id, v.grupa, grupa.eticheta, v.cod, v.clasa, v.sex]
      .concat(v.raspunsuri)
      .concat([s.p1, s.p2, s.total, nivel_(s.total, 'total'), v.durata === null ? '' : v.durata,
        obs.join('; '), '', '', v.clientId, CFG.VERSIUNE]);
    foaie.appendRow(rand);
    return { ok: true, chitanta: chitanta_(id) };
  } finally {
    lock.releaseLock();
  }
}

function infoGrupa_(g, etapa) {
  const cod = normGrupa_(g);
  if (!RE_GRUPA.test(cod)) return eroare_('GRUPA_INEXISTENTA');
  const grupa = cautaGrupa_(SpreadsheetApp.getActiveSpreadsheet(), cod);
  if (!grupa) return eroare_('GRUPA_INEXISTENTA');
  const et = etapa === 'POST' ? 'POST' : 'PRE';
  return { ok: true, cod: cod, eticheta: grupa.eticheta, deschis: grupa.deschis[et] };
}

/* ------------------------------------------------------------------ */
/* Funcții pure: normalizare, validare, scorare                       */
/* ------------------------------------------------------------------ */

function normCod_(x) {
  return String(x === null || x === undefined ? '' : x)
    .toUpperCase()
    .replace(/[ĂÂ]/g, 'A').replace(/Î/g, 'I').replace(/[ȘŞ]/g, 'S').replace(/[ȚŢ]/g, 'T')
    .replace(/\s+/g, '');
}

function normGrupa_(x) {
  return String(x === null || x === undefined ? '' : x).trim().toUpperCase().replace(/\s+/g, '');
}

function esteExclus_(x) {
  return String(x === null || x === undefined ? '' : x).trim().toUpperCase() === 'EXCLUS';
}

function valideaza_(d) {
  const erori = [];
  const grupa = normGrupa_(d.grupa);
  if (!RE_GRUPA.test(grupa)) erori.push('grupa');
  const cod = normCod_(d.cod);
  if (!RE_COD.test(cod)) erori.push('cod');
  const clasa = String(d.clasa || '');
  if (['IX', 'X', 'XI', 'XII'].indexOf(clasa) < 0) erori.push('clasa');
  const sex = String(d.sex || '');
  if (['F', 'M'].indexOf(sex) < 0) erori.push('sex');
  const brute = Array.isArray(d.raspunsuri) ? d.raspunsuri : [];
  const r = brute.map(function (x) {
    return (x === null || x === undefined || x === '' || typeof x === 'boolean') ? NaN : Number(x);
  });
  const raspunsuriOk = r.length === 15 && r.every(function (x, i) {
    return Number.isInteger(x) && (i < 10 ? (x >= 0 && x <= 4) : (x >= 1 && x <= 5));
  });
  if (!raspunsuriOk) erori.push('raspunsuri');
  const clientId = String(d.clientId || '');
  if (!/^[A-Za-z0-9-]{8,64}$/.test(clientId)) erori.push('clientId');
  let durata = Number(d.durata);
  durata = (d.durata !== null && d.durata !== undefined && Number.isFinite(durata) && durata >= 0 && durata < 86400)
    ? Math.round(durata) : null;
  return { erori: erori, grupa: grupa, cod: cod, clasa: clasa, sex: sex, raspunsuri: r, clientId: clientId, durata: durata };
}

function scoruri_(r) {
  let p1 = 0, p2 = 0;
  for (let i = 0; i < 10; i++) p1 += Number(r[i]);
  for (let i = 10; i < 15; i++) p2 += Number(r[i]);
  return { p1: p1, p2: p2, total: p1 + p2 };
}

function nivel_(scor, componenta) {
  if (componenta === 'p1') return scor <= 15 ? 'redusă' : scor <= 25 ? 'moderată' : scor <= 35 ? 'bună' : 'ridicată';
  if (componenta === 'p2') return scor <= 10 ? 'conștientizare redusă' : scor <= 15 ? 'moderată' : scor <= 20 ? 'bună' : 'ridicată';
  return scor <= 25 ? 'scăzută' : scor <= 40 ? 'moderată' : scor <= 55 ? 'bună' : 'ridicată';
}

function uniform_(r) {
  for (let i = 1; i < 10; i++) if (r[i] !== r[0]) return false;
  return true;
}

function chitanta_(id) {
  const s = String(id).replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 8);
  return s.slice(0, 4) + '-' + s.slice(4);
}

function hamming1_(a, b) {
  if (a.length !== b.length) return false;
  let dif = 0;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) dif++;
  return dif === 1;
}

/* ------------------------------------------------------------------ */
/* Acces la foi                                                       */
/* ------------------------------------------------------------------ */

function cautaGrupa_(ss, cod) {
  const foaie = ss.getSheetByName(FOAIE.GRUPE);
  if (!foaie) return null;
  const v = foaie.getDataRange().getValues();
  for (let r = 1; r < v.length; r++) {
    if (normGrupa_(v[r][0]) === cod && cod) {
      return {
        cod: cod,
        eticheta: String(v[r][1] || cod),
        deschis: { PRE: esteDa_(v[r][2]), POST: esteDa_(v[r][3]) }
      };
    }
  }
  return null;
}

function esteDa_(x) {
  return x === true || String(x).trim().toUpperCase() === 'DA';
}

function limitaOk_(grupa) {
  const cache = CacheService.getScriptCache();
  const cheie = 'lim_' + grupa + '_' + Math.floor(Date.now() / 600000);
  const n = parseInt(cache.get(cheie) || '0', 10);
  if (n >= CFG.LIMITA_GRUPA_10MIN) return false;
  cache.put(cheie, String(n + 1), 700);
  return true;
}

function jurnal_(etapa, grupa, motiv) {
  try {
    const foaie = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(FOAIE.JURNAL);
    if (foaie && foaie.getLastRow() < 5000) {
      foaie.appendRow([new Date(), String(etapa || '').slice(0, 4), normGrupa_(grupa).slice(0, 20), String(motiv).slice(0, 200)]);
    }
  } catch (err) { /* jurnalul nu blochează niciodată primirea răspunsurilor */ }
}

/* ------------------------------------------------------------------ */
/* Meniu și configurare                                               */
/* ------------------------------------------------------------------ */

function onOpen() {
  SpreadsheetApp.getUi().createMenu('RADAR AI')
    .addItem('Generează analiza PRE-POST', 'genereazaAnaliza')
    .addItem('Recalculează scorurile (rânduri introduse manual)', 'recalculeazaScoruri')
    .addSeparator()
    .addItem('Șterge răspunsurile grupei TEST', 'stergeGrupaTest')
    .addItem('Configurează / repară structura registrului', 'configureaza')
    .addToUi();
}

function configureaza() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetTimeZone('Europe/Bucharest');

  // Grupe
  const g = foaie_(ss, FOAIE.GRUPE);
  if (!g.getRange(1, 1).getValue()) {
    g.getRange(1, 1, 1, ANTET_GRUPE.length).setValues([ANTET_GRUPE]);
    g.getRange(2, 1, 1, 5).setValues([['TEST', 'Grupă de test (ștergeți-o după verificare)', 'DA', 'DA',
      'Pentru verificarea instalării; vedeți meniul RADAR AI']]);
  }
  const formule = [];
  for (let r = 2; r <= CFG.RANDURI_GRUPE + 1; r++) {
    const linkPre = '=IF($A' + r + '="","","' + CFG.ADRESA_SITE + CFG.PAGINA.PRE + '?g="&ENCODEURL(UPPER(TRIM($A' + r + '))))';
    const linkPost = '=IF($A' + r + '="","","' + CFG.ADRESA_SITE + CFG.PAGINA.POST + '?g="&ENCODEURL(UPPER(TRIM($A' + r + '))))';
    const qrPre = '=IF($F' + r + '="","",HYPERLINK("https://quickchart.io/qr?size=600&margin=2&text="&ENCODEURL($F' + r + '),"Deschide codul QR"))';
    const qrPost = '=IF($G' + r + '="","",HYPERLINK("https://quickchart.io/qr?size=600&margin=2&text="&ENCODEURL($G' + r + '),"Deschide codul QR"))';
    formule.push([linkPre, linkPost, qrPre, qrPost]);
  }
  g.getRange(2, 6, CFG.RANDURI_GRUPE, 4).setFormulas(formule);
  const daNu = SpreadsheetApp.newDataValidation().requireValueInList(['DA', 'NU'], true).setAllowInvalid(false).build();
  g.getRange(2, 3, CFG.RANDURI_GRUPE, 2).setDataValidation(daNu);
  formateazaAntet_(g, ANTET_GRUPE.length);
  g.setColumnWidths(1, 1, 110); g.setColumnWidth(2, 260); g.setColumnWidths(3, 2, 150);
  g.setColumnWidth(5, 240); g.setColumnWidths(6, 2, 330); g.setColumnWidths(8, 2, 140);

  // PRE și POST
  [FOAIE.PRE, FOAIE.POST].forEach(function (nume) {
    const f = foaie_(ss, nume);
    if (!f.getRange(1, 1).getValue()) f.getRange(1, 1, 1, ANTET_RASP.length).setValues([ANTET_RASP]);
    formateazaAntet_(f, ANTET_RASP.length);
    f.setFrozenColumns(5);
    f.getRange(2, K.ts + 1, CFG.RANDURI_VALIDARE, 1).setNumberFormat('dd.MM.yyyy HH:mm:ss');
    const decizie = SpreadsheetApp.newDataValidation().requireValueInList(['INCLUS', 'EXCLUS'], true).setAllowInvalid(false).build();
    f.getRange(2, K.decizie + 1, CFG.RANDURI_VALIDARE, 1).setDataValidation(decizie);
    f.setColumnWidth(K.ts + 1, 150); f.setColumnWidth(K.id + 1, 120); f.setColumnWidth(K.grupa + 1, 180);
    f.setColumnWidths(K.i1 + 1, 15, 38); f.setColumnWidth(K.obs + 1, 320); f.setColumnWidth(K.decizie + 1, 130);
    f.setColumnWidth(K.codCorectat + 1, 160);
    const zona = f.getRange(2, 1, CFG.RANDURI_VALIDARE, ANTET_RASP.length);
    const colObs = litera_(K.obs + 1), colDec = litera_(K.decizie + 1);
    f.setConditionalFormatRules([
      SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$' + colDec + '2="EXCLUS"')
        .setBackground('#E6E6E6').setFontColor('#777777').setRanges([zona]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=$' + colObs + '2<>""')
        .setBackground('#FFF0E6').setRanges([zona]).build()
    ]);
    try {
      f.getProtections(SpreadsheetApp.ProtectionType.SHEET).forEach(function (p) { p.remove(); });
      const prot = f.protect().setDescription('Date colectate automat; modificați doar coloanele psihologului');
      prot.setWarningOnly(true);
      prot.setUnprotectedRanges([f.getRange(2, K.decizie + 1, CFG.RANDURI_VALIDARE, 2)]);
    } catch (err) { /* protecția este opțională */ }
  });

  // Itemi
  const it = foaie_(ss, FOAIE.ITEMI);
  it.clear();
  const randuriItemi = [['Nr.', 'Partea', 'Afirmația', 'Scala']].concat(ITEMI.map(function (t, i) {
    return i < 10
      ? [i + 1, 'Partea 1 — Cum mă raportez la dificultăți în viața mea', t, '0 = deloc adevărat ... 4 = aproape întotdeauna adevărat']
      : [i + 1, 'Partea 2 — Eu și viața mea digitală', t, '1 = deloc de acord ... 5 = complet de acord'];
  }));
  it.getRange(1, 1, randuriItemi.length, 4).setValues(randuriItemi);
  it.getRange(randuriItemi.length + 2, 1, 3, 1).setValues([
    ['Partea 1 este adaptată din Connor-Davidson Resilience Scale (CD-RISC-10; Campbell-Sills & Stein, 2007).'],
    ['Scor P1: 0-40 · Scor P2: 5-25 · Scor total: 5-65. Creștere semnificativă: POST ≥ PRE + 5 puncte.'],
    ['Versiunea formularului web: ' + CFG.VERSIUNE]
  ]);
  formateazaAntet_(it, 4);
  it.setColumnWidth(1, 50); it.setColumnWidth(2, 330); it.setColumnWidth(3, 620); it.setColumnWidth(4, 330);

  // Jurnal
  const j = foaie_(ss, FOAIE.JURNAL);
  if (!j.getRange(1, 1).getValue()) j.getRange(1, 1, 1, 4).setValues([['Marcaj temporal', 'Etapa', 'Cod grupă', 'Motiv']]);
  formateazaAntet_(j, 4);
  j.setColumnWidth(1, 150); j.setColumnWidth(4, 420);

  foaie_(ss, FOAIE.PERECHI);
  foaie_(ss, FOAIE.RAPORT);

  // Ordinea foilor și eliminarea foii goale implicite
  [FOAIE.GRUPE, FOAIE.PRE, FOAIE.POST, FOAIE.PERECHI, FOAIE.RAPORT, FOAIE.ITEMI, FOAIE.JURNAL].forEach(function (nume, i) {
    ss.setActiveSheet(ss.getSheetByName(nume));
    ss.moveActiveSheet(i + 1);
  });
  ss.getSheets().forEach(function (f) {
    if (Object.keys(FOAIE).map(function (k) { return FOAIE[k]; }).indexOf(f.getName()) < 0 && f.getLastRow() === 0) {
      ss.deleteSheet(f);
    }
  });
  ss.setActiveSheet(ss.getSheetByName(FOAIE.GRUPE));
  try { ss.toast('Registrul SRED-15 este configurat.', 'RADAR AI', 5); } catch (err) { /* rulare din editor */ }
}

function foaie_(ss, nume) {
  return ss.getSheetByName(nume) || ss.insertSheet(nume);
}

function formateazaAntet_(f, nrCol) {
  f.getRange(1, 1, 1, nrCol).setFontWeight('bold').setBackground('#1F3864').setFontColor('#FFFFFF').setWrap(true)
    .setVerticalAlignment('middle');
  f.setFrozenRows(1);
}

function litera_(n) {
  let s = '';
  while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); }
  return s;
}

/* ------------------------------------------------------------------ */
/* Întreținere                                                        */
/* ------------------------------------------------------------------ */

function stergeGrupaTest() {
  const ui = SpreadsheetApp.getUi();
  if (ui.alert('Ștergeți toate răspunsurile cu codul de grupă TEST din PRE și POST?', ui.ButtonSet.YES_NO) !== ui.Button.YES) return;
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let n = 0;
  [FOAIE.PRE, FOAIE.POST].forEach(function (nume) {
    const f = ss.getSheetByName(nume);
    const v = f.getDataRange().getValues();
    for (let r = v.length - 1; r >= 1; r--) {
      if (normGrupa_(v[r][K.grupaCod]) === 'TEST') { f.deleteRow(r + 1); n++; }
    }
  });
  ss.toast('Rânduri șterse: ' + n, 'RADAR AI', 5);
}

/**
 * Completează scorurile pentru rândurile introduse manual (de exemplu,
 * chestionare pe hârtie transcrise în registru): necesită cod grupă,
 * cod personal și valorile I1-I15.
 */
function recalculeazaScoruri() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let n = 0;
  [FOAIE.PRE, FOAIE.POST].forEach(function (nume) {
    const f = ss.getSheetByName(nume);
    const v = f.getDataRange().getValues();
    if (v.length < 2) return;
    const grupe = {};
    for (let r = 1; r < v.length; r++) {
      const row = v[r];
      if (!row[K.grupaCod] && !row[K.cod]) continue;
      const rasp = [];
      for (let i = 0; i < 15; i++) rasp.push(row[K.i1 + i]);
      const nums = rasp.map(function (x) { return (x === '' || x === null) ? NaN : Number(x); });
      const ok = nums.every(function (x, i) { return Number.isInteger(x) && (i < 10 ? (x >= 0 && x <= 4) : (x >= 1 && x <= 5)); });
      if (!ok || row[K.total] !== '') continue;
      const s = scoruri_(nums);
      row[K.p1] = s.p1; row[K.p2] = s.p2; row[K.total] = s.total; row[K.nivel] = nivel_(s.total, 'total');
      row[K.grupaCod] = normGrupa_(row[K.grupaCod]);
      row[K.cod] = normCod_(row[K.cod]);
      if (!row[K.grupa]) {
        if (!(row[K.grupaCod] in grupe)) { const gr = cautaGrupa_(ss, row[K.grupaCod]); grupe[row[K.grupaCod]] = gr ? gr.eticheta : ''; }
        row[K.grupa] = grupe[row[K.grupaCod]];
      }
      if (!row[K.id]) row[K.id] = 'MANUAL-' + Utilities.getUuid().slice(0, 8).toUpperCase();
      if (!row[K.ts]) row[K.ts] = new Date();
      if (!row[K.versiune]) row[K.versiune] = 'introdus manual';
      row[K.obs] = row[K.obs] ? row[K.obs] : 'INTRODUS MANUAL';
      n++;
    }
    f.getRange(1, 1, v.length, v[0].length).setValues(v);
  });
  ss.toast('Rânduri completate: ' + n, 'RADAR AI', 5);
}

/* ------------------------------------------------------------------ */
/* Analiza PRE-POST                                                   */
/* ------------------------------------------------------------------ */

function genereazaAnaliza() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const grupe = citesteGrupe_(ss);
  const pre = citesteRaspunsuri_(ss.getSheetByName(FOAIE.PRE));
  const post = citesteRaspunsuri_(ss.getSheetByName(FOAIE.POST));
  const rez = calculeazaAnaliza_(pre, post, grupe);
  scriePerechi_(ss, rez);
  scrieRaport_(ss, rez);
  try { ss.toast('Analiza PRE-POST a fost actualizată.', 'RADAR AI', 5); } catch (err) { /* rulare din editor */ }
  return rez;
}

function citesteGrupe_(ss) {
  const f = ss.getSheetByName(FOAIE.GRUPE);
  if (!f) return [];
  return f.getDataRange().getValues().slice(1)
    .filter(function (row) { return normGrupa_(row[0]); })
    .map(function (row) { return { cod: normGrupa_(row[0]), eticheta: String(row[1] || normGrupa_(row[0])) }; });
}

function citesteRaspunsuri_(foaie) {
  const v = foaie.getDataRange().getValues();
  const out = [];
  for (let r = 1; r < v.length; r++) {
    const row = v[r];
    if (!row[K.grupaCod] && !row[K.cod]) continue;
    const nums = [];
    for (let i = 0; i < 15; i++) {
      const x = row[K.i1 + i];
      nums.push((x === '' || x === null) ? NaN : Number(x));
    }
    const valid = nums.every(function (x, i) { return Number.isInteger(x) && (i < 10 ? (x >= 0 && x <= 4) : (x >= 1 && x <= 5)); });
    const ts = row[K.ts] instanceof Date ? row[K.ts].getTime() : (Date.parse(row[K.ts]) || 0);
    out.push({
      rand: r + 1,
      ts: ts,
      grupa: normGrupa_(row[K.grupaCod]),
      eticheta: String(row[K.grupa] || ''),
      cod: normCod_(row[K.codCorectat] || row[K.cod]),
      clasa: String(row[K.clasa] || ''),
      sex: String(row[K.sex] || ''),
      exclus: esteExclus_(row[K.decizie]),
      valid: valid,
      s: valid ? scoruri_(nums) : null
    });
  }
  return out;
}

function calculeazaAnaliza_(pre, post, grupeInfo) {
  function unice(lista) {
    const map = {}, dup = {};
    lista.filter(function (x) { return !x.exclus && x.valid && x.grupa && x.cod; })
      .sort(function (a, b) { return a.ts - b.ts || a.rand - b.rand; })
      .forEach(function (x) {
        const k = x.grupa + '|' + x.cod;
        if (map[k]) dup[k] = (dup[k] || 1) + 1; else map[k] = x;
      });
    return { map: map, dup: dup };
  }
  const A = unice(pre), B = unice(post);
  const perechi = [];
  Object.keys(A.map).sort().forEach(function (k) { if (B.map[k]) perechi.push({ pre: A.map[k], post: B.map[k] }); });

  const coduri = [], etichete = {};
  (grupeInfo || []).forEach(function (g) { if (coduri.indexOf(g.cod) < 0) { coduri.push(g.cod); etichete[g.cod] = g.eticheta; } });
  [A, B].forEach(function (X) {
    Object.keys(X.map).forEach(function (k) {
      const g = k.split('|')[0];
      if (coduri.indexOf(g) < 0) { coduri.push(g); etichete[g] = X.map[k].eticheta || g; }
    });
  });
  function numara(X, g) { return Object.keys(X.map).filter(function (k) { return k.split('|')[0] === g; }).length; }
  const peGrupe = coduri.map(function (g) {
    return {
      cod: g, eticheta: etichete[g] || g, nPre: numara(A, g), nPost: numara(B, g),
      st: statistici_(perechi.filter(function (p) { return p.pre.grupa === g; }))
    };
  }).filter(function (x) { return x.nPre || x.nPost; });
  const total = { nPre: Object.keys(A.map).length, nPost: Object.keys(B.map).length, st: statistici_(perechi) };

  const faraPereche = [];
  Object.keys(A.map).sort().forEach(function (k) { if (!B.map[k]) faraPereche.push({ grupa: A.map[k].grupa, cod: A.map[k].cod, doarIn: 'PRE' }); });
  Object.keys(B.map).sort().forEach(function (k) { if (!A.map[k]) faraPereche.push({ grupa: B.map[k].grupa, cod: B.map[k].cod, doarIn: 'POST' }); });
  faraPereche.forEach(function (f) {
    const alta = f.doarIn === 'PRE' ? 'POST' : 'PRE';
    f.sugestii = faraPereche.filter(function (o) { return o.doarIn === alta && o.grupa === f.grupa && hamming1_(o.cod, f.cod); })
      .map(function (o) { return o.cod; });
  });

  const duplicate = [];
  [['PRE', A], ['POST', B]].forEach(function (e) {
    Object.keys(e[1].dup).sort().forEach(function (k) {
      const p = k.split('|');
      duplicate.push({ grupa: p[0], cod: p[1], etapa: e[0], n: e[1].dup[k] });
    });
  });

  const niveluri = ['scăzută', 'moderată', 'bună', 'ridicată'];
  const distributie = niveluri.map(function (n) {
    return {
      nivel: n,
      pre: perechi.filter(function (p) { return nivel_(p.pre.s.total, 'total') === n; }).length,
      post: perechi.filter(function (p) { return nivel_(p.post.s.total, 'total') === n; }).length
    };
  });

  const excluse = pre.filter(function (x) { return x.exclus; }).length + post.filter(function (x) { return x.exclus; }).length;
  const invalide = pre.filter(function (x) { return !x.exclus && !x.valid; }).length + post.filter(function (x) { return !x.exclus && !x.valid; }).length;

  return { perechi: perechi, peGrupe: peGrupe, total: total, faraPereche: faraPereche, duplicate: duplicate,
    distributie: distributie, excluse: excluse, invalide: invalide };
}

function statistici_(pp) {
  const n = pp.length;
  if (!n) return { n: 0 };
  const d = pp.map(function (p) { return p.post.s.total - p.pre.s.total; });
  const m = medie_(d), sd = abatere_(d);
  const st = {
    n: n,
    mPre: medie_(pp.map(function (p) { return p.pre.s.total; })),
    mPost: medie_(pp.map(function (p) { return p.post.s.total; })),
    mDif: m, sdDif: sd,
    mPreP1: medie_(pp.map(function (p) { return p.pre.s.p1; })),
    mPostP1: medie_(pp.map(function (p) { return p.post.s.p1; })),
    mPreP2: medie_(pp.map(function (p) { return p.pre.s.p2; })),
    mPostP2: medie_(pp.map(function (p) { return p.post.s.p2; })),
    nCrestere: d.filter(function (x) { return x >= 5; }).length
  };
  st.pct = 100 * st.nCrestere / n;
  if (n >= 2 && sd > 0) {
    st.dz = m / sd;
    st.t = m / (sd / Math.sqrt(n));
    st.gl = n - 1;
    st.p = pT_(st.t, st.gl);
  }
  return st;
}

function medie_(a) { return a.reduce(function (s, x) { return s + x; }, 0) / a.length; }

function abatere_(a) {
  if (a.length < 2) return NaN;
  const m = medie_(a);
  return Math.sqrt(a.reduce(function (s, x) { return s + (x - m) * (x - m); }, 0) / (a.length - 1));
}

// Probabilitatea bilaterală pentru testul t (distribuția Student), prin funcția beta incompletă regularizată.
function pT_(t, gl) { return betai_(gl / 2, 0.5, gl / (gl + t * t)); }

function lnGamma_(x) {
  const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  if (x < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * x)) - lnGamma_(1 - x);
  x -= 1;
  let a = c[0];
  const t = x + 7.5;
  for (let i = 1; i < 9; i++) a += c[i] / (x + i);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}

function betacf_(a, b, x) {
  const MAXIT = 300, EPS = 3e-14, FPMIN = 1e-300;
  const qab = a + b, qap = a + 1, qam = a - 1;
  let c = 1, d = 1 - qab * x / qap;
  if (Math.abs(d) < FPMIN) d = FPMIN;
  d = 1 / d;
  let h = d;
  for (let m = 1; m <= MAXIT; m++) {
    const m2 = 2 * m;
    let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
    c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
    d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
    d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
    c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
    d = 1 / d;
    const del = d * c;
    h *= del;
    if (Math.abs(del - 1) < EPS) break;
  }
  return h;
}

function betai_(a, b, x) {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const bt = Math.exp(lnGamma_(a + b) - lnGamma_(a) - lnGamma_(b) + a * Math.log(x) + b * Math.log(1 - x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf_(a, b, x) / a : 1 - bt * betacf_(b, a, 1 - x) / b;
}

/* ------------------------------------------------------------------ */
/* Scrierea rezultatelor                                              */
/* ------------------------------------------------------------------ */

function r2_(x) { return (x === undefined || x === null || !isFinite(x)) ? '—' : Math.round(x * 100) / 100; }
function r1_(x) { return (x === undefined || x === null || !isFinite(x)) ? '—' : Math.round(x * 10) / 10; }
function rp_(x) {
  if (x === undefined || x === null || !isFinite(x)) return '—';
  return x < 0.001 ? '< 0,001' : Math.round(x * 1000) / 1000;
}

function scriePerechi_(ss, rez) {
  const f = foaie_(ss, FOAIE.PERECHI);
  f.clear();
  const antet = ['Cod grupă', 'Grupa', 'Cod personal', 'Clasa', 'Sex', 'PRE P1', 'PRE P2', 'PRE total',
    'POST P1', 'POST P2', 'POST total', 'Dif. P1', 'Dif. P2', 'Dif. total', 'Creștere ≥ 5 puncte', 'Nivel PRE', 'Nivel POST'];
  const randuri = rez.perechi.map(function (p) {
    const a = p.pre, b = p.post;
    return [a.grupa, a.eticheta || b.eticheta, a.cod, a.clasa, a.sex, a.s.p1, a.s.p2, a.s.total, b.s.p1, b.s.p2, b.s.total,
      b.s.p1 - a.s.p1, b.s.p2 - a.s.p2, b.s.total - a.s.total, (b.s.total - a.s.total) >= 5 ? 'DA' : 'NU',
      nivel_(a.s.total, 'total'), nivel_(b.s.total, 'total')];
  });
  const tot = [antet].concat(randuri);
  f.getRange(1, 1, tot.length, antet.length).setValues(tot);
  formateazaAntet_(f, antet.length);
  f.setColumnWidth(2, 200);
}

function scrieRaport_(ss, rez) {
  const f = foaie_(ss, FOAIE.RAPORT);
  f.clear();
  const W = 19;
  const rows = [], antete = [], titluri = [];
  function add(arr) { const r = arr.slice(0, W); while (r.length < W) r.push(''); rows.push(r); return rows.length; }
  function gol() { add([]); }

  titluri.push(add(['Raport de evaluare SRED-15 — comparația PRE-POST']));
  add(['Generat la: ' + Utilities.formatDate(new Date(), 'Europe/Bucharest', 'dd.MM.yyyy, HH:mm')]);
  add(['Se analizează doar perechile valide (același cod personal în aceeași grupă). Rândurile marcate EXCLUS nu intră în calcul; la răspunsuri duplicate se folosește prima completare.']);
  add(['Rânduri excluse de psiholog: ' + rez.excluse + ' · rânduri incomplete ignorate: ' + rez.invalide]);
  gol();

  const st = rez.total.st;
  titluri.push(add(['Indicatorul de impact']));
  if (st.n) {
    add(['Procentul participanților cu creștere semnificativă (POST ≥ PRE + 5 puncte): ' + String(r1_(st.pct)).replace('.', ',') +
      '% (' + st.nCrestere + ' din ' + st.n + ' elevi evaluați PRE și POST).']);
  } else {
    add(['Nu există încă perechi PRE-POST valide.']);
  }
  gol();

  titluri.push(add(['Rezultate pe grupe']));
  antete.push(add(['Grupa', 'Cod grupă', 'PRE completate', 'POST completate', 'Perechi valide', 'Medie PRE (total)',
    'Medie POST (total)', 'Diferență medie', 'Abatere std. a diferenței', 'Cohen dz', 't (perechi)', 'gl', 'p (bilateral)',
    'Creștere ≥ 5 (n)', 'Creștere ≥ 5 (%)', 'Medie PRE P1', 'Medie POST P1', 'Medie PRE P2', 'Medie POST P2']));
  function rand(et, cod, nPre, nPost, s) {
    return [et, cod, nPre, nPost, s.n, r2_(s.mPre), r2_(s.mPost), r2_(s.mDif), r2_(s.sdDif), r2_(s.dz), r2_(s.t),
      s.gl === undefined ? '—' : s.gl, rp_(s.p), s.n ? s.nCrestere : '—', r1_(s.pct), r2_(s.mPreP1), r2_(s.mPostP1),
      r2_(s.mPreP2), r2_(s.mPostP2)];
  }
  rez.peGrupe.forEach(function (g) { add(rand(g.eticheta, g.cod, g.nPre, g.nPost, g.st)); });
  const rTotal = add(rand('Total', '', rez.total.nPre, rez.total.nPost, st));
  add(['t, gl și p: testul t pentru eșantioane perechi, cu titlu orientativ. SRED-15 este un instrument de screening educațional, nu un instrument clinic.']);
  gol();

  titluri.push(add(['Distribuția pe niveluri a scorului total (perechi valide)']));
  antete.push(add(['Nivel', 'Interval', 'PRE (n)', 'PRE (%)', 'POST (n)', 'POST (%)']));
  const intervale = { 'scăzută': '5-25', 'moderată': '26-40', 'bună': '41-55', 'ridicată': '56-65' };
  rez.distributie.forEach(function (d) {
    add([d.nivel, intervale[d.nivel], d.pre, st.n ? r1_(100 * d.pre / st.n) : '—', d.post, st.n ? r1_(100 * d.post / st.n) : '—']);
  });
  gol();

  titluri.push(add(['Coduri fără pereche (de verificat de psiholog)']));
  antete.push(add(['Cod grupă', 'Cod personal', 'Există doar în', 'Posibilă potrivire (diferă printr-un caracter)']));
  if (rez.faraPereche.length) {
    rez.faraPereche.forEach(function (x) { add([x.grupa, x.cod, x.doarIn, x.sugestii.join(', ')]); });
  } else {
    add(['Nu există coduri fără pereche.']);
  }
  add(['Pentru o potrivire confirmată, scrieți codul corect în coloana „Cod corectat (psiholog)” din foaia PRE sau POST și regenerați analiza.']);
  gol();

  titluri.push(add(['Răspunsuri duplicate']));
  antete.push(add(['Cod grupă', 'Cod personal', 'Etapa', 'Număr de completări']));
  if (rez.duplicate.length) {
    rez.duplicate.forEach(function (x) { add([x.grupa, x.cod, x.etapa, x.n]); });
  } else {
    add(['Nu există duplicate.']);
  }

  f.getRange(1, 1, rows.length, W).setValues(rows);
  titluri.forEach(function (r) { f.getRange(r, 1).setFontWeight('bold').setFontSize(12).setFontColor('#1F3864'); });
  antete.forEach(function (r) {
    f.getRange(r, 1, 1, W).setFontWeight('bold').setBackground('#EBF3FB').setWrap(true).setVerticalAlignment('middle');
  });
  f.getRange(rTotal, 1, 1, W).setFontWeight('bold');
  f.setColumnWidth(1, 220);
  f.setColumnWidths(2, W - 1, 105);
}
