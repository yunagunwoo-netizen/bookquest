// scripts/fetch_aladin_covers.js
// 알라딘 ItemSearch API로 169권 책 표지 일괄 다운로드
// 실행 (PowerShell):
//   $env:ALADIN_KEY = "ttb_xxx_..."; node scripts/fetch_aladin_covers.js
// 또는:
//   node scripts/fetch_aladin_covers.js ttb_xxx_...

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const ALADIN_KEY = process.env.ALADIN_KEY || process.argv[2];
if (!ALADIN_KEY) {
  console.error('[ERR] ALADIN_KEY 필요. 환경변수 또는 첫 인자로 전달.');
  console.error('   PowerShell: $env:ALADIN_KEY = "ttb_xxx"; node scripts/fetch_aladin_covers.js');
  console.error('   또는:        node scripts/fetch_aladin_covers.js ttb_xxx');
  process.exit(1);
}

const appDataPath = path.join(__dirname, '..', 'app-data.js');
const src = fs.readFileSync(appDataPath, 'utf-8');

function sliceGlobal(name) {
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

function extractBooks(block, category) {
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
    const idMatch = obj.match(/\bid:\s*(?:"([^"]+)"|(\d+))/);
    const titleMatch = obj.match(/\btitle:\s*"((?:[^"\\]|\\.)*)"/);
    const authorMatch = obj.match(/\bauthor:\s*"((?:[^"\\]|\\.)*)"/);
    return {
      id: idMatch ? (idMatch[1] || idMatch[2]) : null,
      title: titleMatch ? titleMatch[1] : '',
      author: authorMatch ? authorMatch[1] : '',
      category,
    };
  }).filter(b => b.id);
}

const allBooks = [
  ...extractBooks(sliceGlobal('BOOKS'), 'BOOKS'),
  ...extractBooks(sliceGlobal('CURRICULUM_BOOKS'), 'CURRICULUM'),
  ...extractBooks(sliceGlobal('SEASON2_BOOKS'), 'SEASON2'),
];

console.log('[OK] 추출됨: ' + allBooks.length + '권 (BOOKS + CURRICULUM + SEASON2)');

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

async function findCover(book) {
  const firstAuthor = (book.author || '').split(/[·,/]/)[0].split(' ')[0].trim();
  const query = encodeURIComponent((book.title + ' ' + firstAuthor).trim());
  const url = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=' + ALADIN_KEY + '&Query=' + query + '&QueryType=Keyword&MaxResults=3&start=1&SearchTarget=Book&output=js&Version=20131101&Cover=Big';
  const data = await fetchJson(url);
  const items = data.item || [];
  if (items.length === 0) {
    const url2 = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=' + ALADIN_KEY + '&Query=' + encodeURIComponent(book.title) + '&QueryType=Keyword&MaxResults=3&start=1&SearchTarget=Book&output=js&Version=20131101&Cover=Big';
    const data2 = await fetchJson(url2);
    const items2 = data2.item || [];
    if (items2.length === 0) return null;
    return items2[0].cover || null;
  }
  return items[0].cover || null;
}

async function main() {
  console.log('[GO] 알라딘 표지 자동 수집 시작 (rate limit: 250ms 간격)');
  console.log('');
  const missing = [];
  let downloaded = 0, skipped = 0, failed = 0;

  for (let i = 0; i < allBooks.length; i++) {
    const book = allBooks[i];
    const id = book.id;
    const dest = path.join(COVERS_DIR, id + '.jpg');
    const progress = '[' + String(i+1).padStart(3) + '/' + allBooks.length + ']';

    if (fs.existsSync(dest) && fs.statSync(dest).size > 1000) {
      console.log(progress + ' SKIP ' + book.category + ' ' + id + ' (이미 있음)');
      skipped++;
      continue;
    }

    const titleShort = book.title.length > 28 ? book.title.slice(0, 28) + '...' : book.title;
    process.stdout.write(progress + ' ' + book.category.padEnd(11) + ' ' + String(id).padEnd(5) + ' ' + titleShort);

    try {
      const coverUrl = await findCover(book);
      if (!coverUrl) {
        console.log('  [FAIL] 표지 없음');
        missing.push({ ...book, reason: 'not_found' });
        failed++;
        await new Promise(r => setTimeout(r, 250));
        continue;
      }
      await downloadFile(coverUrl, dest);
      console.log('  OK');
      downloaded++;
    } catch (e) {
      console.log('  [FAIL] ' + e.message);
      missing.push({ ...book, reason: e.message });
      failed++;
    }

    await new Promise(r => setTimeout(r, 250));
  }

  console.log('');
  console.log('=== 완료 ===');
  console.log('OK 다운로드:         ' + downloaded);
  console.log('SKIP (이미 있음):    ' + skipped);
  console.log('FAIL 누락:           ' + failed);
  console.log('저장 위치:           covers/{id}.jpg');

  if (missing.length > 0) {
    const missingPath = path.join(__dirname, '..', 'covers_missing.json');
    fs.writeFileSync(missingPath, JSON.stringify(missing, null, 2));
    console.log('');
    console.log('누락 리스트: ' + missingPath);
    console.log('   → 이 책들은 직접 알라딘·교보문고에서 표지 받으세요');
  }

  console.log('');
  console.log('다음 단계: app.html의 BOOK_COVERS 매핑을 covers/{id}.jpg로 업데이트');
}

main().catch(e => {
  console.error('치명적 오류:', e);
  process.exit(1);
});
