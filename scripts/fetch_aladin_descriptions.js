// scripts/fetch_aladin_descriptions.js
// Fetch book descriptions/ISBN/publisher from Aladin OpenAPI
// for RECOMMENDED_BOOKS (R001-R096) + EXTRA_BOOKS (id 14-17)
//
// Usage (PowerShell):
//   $env:ALADIN_KEY = "ttb_xxx"; node scripts/fetch_aladin_descriptions.js
// Or:
//   node scripts/fetch_aladin_descriptions.js ttb_xxx
//
// Output:
//   ocr_results/aladin_meta.json
//     {
//       "R001": { description, isbn13, isbn, publisher, author, pubDate, title, link },
//       ...
//       "14":  { ... }, "15": { ... }, ...
//     }

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

let ALADIN_KEY = process.env.ALADIN_KEY || process.argv[2];

if (!ALADIN_KEY) {
  const envPath = path.join(__dirname, '..', 'functions', '.env');
  if (fs.existsSync(envPath)) {
    const envText = fs.readFileSync(envPath, 'utf-8').replace(/\x00+/g, '');
    const m = envText.match(/^\s*ALADIN_KEY\s*=\s*(.+?)\s*$/m);
    if (m) {
      ALADIN_KEY = m[1].replace(/^["\']|["\']$/g, '').trim();
      console.log('[INFO] Loaded ALADIN_KEY from functions/.env');
    }
  }
}

if (!ALADIN_KEY) {
  console.error('[ERR] ALADIN_KEY required.');
  console.error('  Get TTBKey at https://www.aladin.co.kr/ttb/wblog_manage.aspx');
  console.error('  Usage: $env:ALADIN_KEY = "ttb_xxx"; node scripts/fetch_aladin_descriptions.js');
  process.exit(1);
}

const appDataPath = path.join(__dirname, '..', 'app-data.js');
const src = fs.readFileSync(appDataPath, 'utf-8');

function sliceArray(name) {
  const m = src.match(new RegExp('const ' + name + '\\s*=\\s*\\['));
  if (!m) return '';
  const start = m.index + m[0].length - 1;
  let depth = 0, e = start;
  while (e < src.length) {
    const c = src[e];
    if (c === '[') depth++;
    else if (c === ']') { depth--; if (depth === 0) return src.slice(start, e + 1); }
    e++;
  }
  return src.slice(start);
}

function extractBooks(block, idPrefix) {
  const objects = [];
  const inside = block.slice(1, -1);
  let depth = 0, start = null;
  for (let i = 0; i < inside.length; i++) {
    const c = inside[i];
    if (c === '{') { if (depth === 0) start = i; depth++; }
    else if (c === '}') {
      depth--;
      if (depth === 0 && start !== null) {
        objects.push(inside.slice(start, i + 1));
        start = null;
      }
    }
  }
  return objects.map(obj => {
    const idStrM = obj.match(/\bid:\s*"([^"]+)"/);
    const idNumM = obj.match(/\bid:\s*(\d+)/);
    const titleM = obj.match(/\btitle:\s*"((?:[^"\\]|\\.)*)"/);
    const authorM = obj.match(/\bauthor:\s*"((?:[^"\\]|\\.)*)"/);
    const pubM = obj.match(/\bpublisher:\s*"((?:[^"\\]|\\.)*)"/);
    const id = idStrM ? idStrM[1] : (idNumM ? idNumM[1] : null);
    return {
      id,
      title: titleM ? titleM[1] : '',
      author: authorM ? authorM[1] : '',
      publisher: pubM ? pubM[1] : '',
    };
  }).filter(b => {
    if (!b.id) return false;
    if (idPrefix === 'R') return b.id.startsWith('R');
    if (idPrefix === 'EXTRA') {
      const n = parseInt(b.id, 10);
      return !isNaN(n) && n >= 14 && n <= 17;
    }
    return false;
  });
}

const recommended = extractBooks(sliceArray('RECOMMENDED_BOOKS'), 'R');
const extra = extractBooks(sliceArray('EXTRA_BOOKS'), 'EXTRA');
const allBooks = [...recommended, ...extra];

console.log(`[OK] RECOMMENDED: ${recommended.length} / EXTRA: ${extra.length} / total: ${allBooks.length}`);

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) {
          try { resolve(JSON.parse(data.replace(/[\x00-\x1F]/g, ''))); }
          catch(e2) { reject(e2); }
        }
      });
    }).on('error', reject);
  });
}

async function searchAladin(query) {
  const url = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
    + '?ttbkey=' + ALADIN_KEY
    + '&Query=' + encodeURIComponent(query)
    + '&QueryType=Keyword&MaxResults=3&start=1&SearchTarget=Book'
    + '&output=js&Version=20131101&Cover=Big';
  const data = await fetchJson(url);
  return data.item || [];
}

async function lookupAladin(itemId) {
  // OptResult=fulldescription gets the fuller book description
  const url = 'http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx'
    + '?ttbkey=' + ALADIN_KEY
    + '&itemIdType=ItemId&ItemId=' + itemId
    + '&output=js&Version=20131101'
    + '&OptResult=fulldescription,authors';
  const data = await fetchJson(url);
  return (data.item && data.item[0]) || null;
}

async function findBookMeta(book) {
  const firstAuthor = (book.author || '').split(/[\u00b7,/]/)[0].split(' ')[0].trim();

  let items = [];
  if (firstAuthor) {
    items = await searchAladin((book.title + ' ' + firstAuthor).trim());
  }
  if (items.length === 0 && book.publisher) {
    items = await searchAladin((book.title + ' ' + book.publisher).trim());
  }
  if (items.length === 0) {
    items = await searchAladin(book.title);
  }
  if (items.length === 0) return null;

  const top = items[0];
  // Try to get richer description via ItemLookUp
  let fulldesc = '';
  try {
    if (top.itemId) {
      await new Promise(r => setTimeout(r, 200));
      const lookup = await lookupAladin(top.itemId);
      if (lookup) {
        fulldesc = lookup.fullDescription || lookup.fulldescription || '';
      }
    }
  } catch(e) {
    // ignore lookup failure, fall back to short description
  }

  return {
    title: top.title || '',
    author: top.author || '',
    publisher: top.publisher || '',
    pubDate: top.pubDate || '',
    isbn: top.isbn || '',
    isbn13: top.isbn13 || '',
    description: top.description || '',  // short description from search
    fullDescription: fulldesc,            // longer description from lookup
    cover: top.cover || '',
    link: top.link || '',
    categoryName: top.categoryName || '',
    itemId: top.itemId || null,
  };
}

async function main() {
  console.log(`[GO] Fetching descriptions for ${allBooks.length} books (rate: 400ms per book + 200ms lookup)`);
  console.log('');

  // Load existing meta if any (resume support)
  const outPath = path.join(__dirname, '..', 'ocr_results', 'aladin_meta.json');
  let result = {};
  if (fs.existsSync(outPath)) {
    try {
      result = JSON.parse(fs.readFileSync(outPath, 'utf-8'));
      console.log(`[INFO] Resuming — ${Object.keys(result).length} entries already cached`);
    } catch(e) {
      console.log('[WARN] existing aladin_meta.json corrupted, starting fresh');
      result = {};
    }
  }

  const missing = [];
  let fetched = 0, skipped = 0, failed = 0;

  for (let i = 0; i < allBooks.length; i++) {
    const book = allBooks[i];
    const id = book.id;
    const progress = '[' + String(i + 1).padStart(3) + '/' + allBooks.length + ']';

    if (result[id] && result[id].description) {
      console.log(progress + ' SKIP ' + id + ' (cached)');
      skipped++;
      continue;
    }

    const titleShort = book.title.length > 28 ? book.title.slice(0, 28) + '...' : book.title;
    process.stdout.write(progress + ' ' + id + '  ' + titleShort.padEnd(32));

    try {
      const meta = await findBookMeta(book);
      if (!meta) {
        console.log(' [FAIL] not found');
        missing.push({ id, title: book.title, reason: 'not_found' });
        failed++;
        await new Promise(r => setTimeout(r, 400));
        continue;
      }
      result[id] = meta;
      // Save incrementally
      fs.writeFileSync(outPath, JSON.stringify(result, null, 2));
      const descLen = (meta.fullDescription || meta.description || '').length;
      console.log(' OK (desc ' + descLen + ' chars)');
      fetched++;
    } catch (e) {
      console.log(' [FAIL] ' + e.message);
      missing.push({ id, title: book.title, reason: e.message });
      failed++;
    }

    await new Promise(r => setTimeout(r, 400));
  }

  console.log('');
  console.log('=== Done ===');
  console.log('  fetched: ' + fetched);
  console.log('  skipped (cached): ' + skipped);
  console.log('  failed: ' + failed);
  console.log('  saved to: ' + outPath);

  if (missing.length > 0) {
    const missingPath = path.join(__dirname, '..', 'ocr_results', 'aladin_meta_missing.json');
    fs.writeFileSync(missingPath, JSON.stringify(missing, null, 2));
    console.log('  missing list: ' + missingPath);
  }
  console.log('');
  console.log('Next: ask Claude to merge into app-data.js');
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
