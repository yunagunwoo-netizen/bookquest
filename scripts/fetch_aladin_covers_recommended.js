// scripts/fetch_aladin_covers_recommended.js
// Auto-fetch covers for RECOMMENDED_BOOKS (R001-R096) from Aladin OpenAPI
//
// Usage (PowerShell):
//   $env:ALADIN_KEY = "ttb_xxx_..."; node scripts/fetch_aladin_covers_recommended.js
// Or:
//   node scripts/fetch_aladin_covers_recommended.js ttb_xxx_...
//
// Get Aladin TTBKey: https://www.aladin.co.kr/ttb/wblog_manage.aspx
//
// Output:
//   covers/R001.jpg ~ covers/R096.jpg
//   covers_missing_R.json (failed list)

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
  console.error('');
  console.error('  Get TTBKey at: https://www.aladin.co.kr/ttb/wblog_manage.aspx');
  console.error('');
  console.error('  Usage:');
  console.error('    PowerShell:  $env:ALADIN_KEY = "ttb_xxx"; node scripts/fetch_aladin_covers_recommended.js');
  console.error('    Or:          node scripts/fetch_aladin_covers_recommended.js ttb_xxx');
  console.error('    Or add ALADIN_KEY=... to functions/.env');
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

function extractBooks(block) {
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
    const idM = obj.match(/\bid:\s*"([^"]+)"/);
    const titleM = obj.match(/\btitle:\s*"((?:[^"\\]|\\.)*)"/);
    const authorM = obj.match(/\bauthor:\s*"((?:[^"\\]|\\.)*)"/);
    const pubM = obj.match(/\bpublisher:\s*"((?:[^"\\]|\\.)*)"/);
    return {
      id: idM ? idM[1] : null,
      title: titleM ? titleM[1] : '',
      author: authorM ? authorM[1] : '',
      publisher: pubM ? pubM[1] : '',
    };
  }).filter(b => b.id && b.id.startsWith('R'));
}

const books = extractBooks(sliceArray('RECOMMENDED_BOOKS'));
console.log('[OK] Extracted ' + books.length + ' RECOMMENDED_BOOKS');

if (books.length !== 96) {
  console.warn('[WARN] Expected 96 books — please verify before continuing.');
}

const COVERS_DIR = path.join(__dirname, '..', 'covers');
fs.mkdirSync(COVERS_DIR, { recursive: true });

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

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return downloadFile(res.headers.location, dest).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error('HTTP ' + res.statusCode));
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve()));
      file.on('error', reject);
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

async function findCover(book) {
  const firstAuthor = (book.author || '').split(/[\u00b7,/]/)[0].split(' ')[0].trim();

  if (firstAuthor) {
    const items1 = await searchAladin((book.title + ' ' + firstAuthor).trim());
    if (items1.length > 0 && items1[0].cover) return items1[0].cover;
  }

  if (book.publisher) {
    const items2 = await searchAladin((book.title + ' ' + book.publisher).trim());
    if (items2.length > 0 && items2[0].cover) return items2[0].cover;
  }

  const items3 = await searchAladin(book.title);
  if (items3.length > 0 && items3[0].cover) return items3[0].cover;

  return null;
}

async function main() {
  console.log('[GO] Fetching Aladin covers for ' + books.length + ' books (rate: 300ms)');
  console.log('');
  const missing = [];
  let downloaded = 0, skipped = 0, failed = 0;

  for (let i = 0; i < books.length; i++) {
    const book = books[i];
    const id = book.id;
    const dest = path.join(COVERS_DIR, id + '.jpg');
    const progress = '[' + String(i + 1).padStart(3) + '/' + books.length + ']';

    if (fs.existsSync(dest) && fs.statSync(dest).size > 1000) {
      console.log(progress + ' SKIP ' + id);
      skipped++;
      continue;
    }

    const titleShort = book.title.length > 28 ? book.title.slice(0, 28) + '...' : book.title;
    process.stdout.write(progress + ' ' + id + '  ' + titleShort.padEnd(32));

    try {
      const coverUrl = await findCover(book);
      if (!coverUrl) {
        console.log(' [FAIL] not found');
        missing.push({ id: book.id, title: book.title, author: book.author, publisher: book.publisher, reason: 'not_found' });
        failed++;
        await new Promise(r => setTimeout(r, 300));
        continue;
      }
      await downloadFile(coverUrl, dest);
      console.log(' OK');
      downloaded++;
    } catch (e) {
      console.log(' [FAIL] ' + e.message);
      missing.push({ id: book.id, title: book.title, author: book.author, publisher: book.publisher, reason: e.message });
      failed++;
    }

    await new Promise(r => setTimeout(r, 300));
  }

  console.log('');
  console.log('=== Done ===');
  console.log('  downloaded: ' + downloaded);
  console.log('  skipped:    ' + skipped);
  console.log('  failed:     ' + failed);
  console.log('  saved to:   covers/R001.jpg ~ R096.jpg');

  if (missing.length > 0) {
    const missingPath = path.join(__dirname, '..', 'covers_missing_R.json');
    fs.writeFileSync(missingPath, JSON.stringify(missing, null, 2));
    console.log('');
    console.log('  missing list: ' + missingPath);
    console.log('  -> grab these manually and save as covers/Rxxx.jpg');
  }

  console.log('');
  console.log('Then run deploy.ps1 to publish.');
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
