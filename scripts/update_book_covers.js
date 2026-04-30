// scripts/update_book_covers.js
// covers/ 폴더 스캔 → BOOK_COVERS 객체 자동 생성 → app.html 교체
// 실행: node scripts/update_book_covers.js

const fs = require('fs');
const path = require('path');

// 1) covers/ 폴더 스캔
const COVERS_DIR = path.join(__dirname, '..', 'covers');
const files = new Set(fs.readdirSync(COVERS_DIR).filter(f => /\.(jpg|jpeg|png)$/i.test(f)));
console.log('[OK] covers/ 폴더 파일 수: ' + files.size);

// 2) app-data.js에서 169권 id + meta 추출
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

function extractIds(block) {
  const ids = [];
  const inside = block.slice(1, -1);
  let depth = 0, start = null;
  for (let i = 0; i < inside.length; i++) {
    const c = inside[i];
    if (c === '{') { if (depth === 0) start = i; depth++; }
    else if (c === '}') {
      depth--;
      if (depth === 0 && start !== null) {
        const obj = inside.slice(start, i + 1);
        const m = obj.match(/\bid:\s*(?:"([^"]+)"|(\d+))/);
        if (m) ids.push(m[1] || m[2]);
        start = null;
      }
    }
  }
  return ids;
}

const booksIds = extractIds(sliceGlobal('BOOKS'));
const currIds = extractIds(sliceGlobal('CURRICULUM_BOOKS'));
const s2Ids = extractIds(sliceGlobal('SEASON2_BOOKS'));
const allIds = [...booksIds, ...currIds, ...s2Ids];
console.log('[OK] app-data.js id 추출: ' + allIds.length + '권 (BOOKS ' + booksIds.length + ' + CURRICULUM ' + currIds.length + ' + SEASON2 ' + s2Ids.length + ')');

// 3) 각 id별로 표지 우선순위 결정
//    1순위: covers/{id}.jpg (알라딘에서 받은 새 표지)
//    2순위: covers/book{id}.jpg (BOOKS 기존)
//    3순위: img/book_cover_X.png (id 4·5의 외부 경로, 기존 코드에서 사용)
const mapping = {};
const stats = { new: 0, legacy: 0, external: 0, missing: 0 };

for (const id of allIds) {
  const newJpg = id + '.jpg';
  const newPng = id + '.png';
  const bookJpg = 'book' + id + '.jpg';
  if (files.has(newJpg)) {
    mapping[id] = 'covers/' + newJpg;
    stats.new++;
  } else if (files.has(newPng)) {
    mapping[id] = 'covers/' + newPng;
    stats.new++;
  } else if (files.has(bookJpg)) {
    mapping[id] = 'covers/' + bookJpg;
    stats.legacy++;
  } else {
    stats.missing++;
  }
}

// 특수: id 4·5는 img/book_cover_X.png 외부 경로 폴백 (기존 매핑 보존)
if (!mapping['4'] && fs.existsSync(path.join(__dirname, '..', 'img', 'book_cover_1.png'))) {
  mapping['4'] = 'img/book_cover_1.png'; stats.external++;
}
if (!mapping['5'] && fs.existsSync(path.join(__dirname, '..', 'img', 'book_cover_2.png'))) {
  mapping['5'] = 'img/book_cover_2.png'; stats.external++;
}

console.log('[OK] 매핑 결과:');
console.log('     - 신규 covers/{id}.jpg : ' + stats.new + '권');
console.log('     - 기존 covers/book{id}.jpg: ' + stats.legacy + '권');
console.log('     - 외부 img/* : ' + stats.external + '권');
console.log('     - 매핑 없음 (자물쇠 폴백): ' + stats.missing + '권');

// 4) 객체 직렬화 (한 줄 길어도 OK)
function keyFmt(id) {
  return /^\d+$/.test(id) ? id : '"' + id + '"';
}
// id 정렬: 숫자 먼저(BOOKS 1-13, SEASON2 2101-2316), 문자열(CURRICULUM C001-C108)은 나중
const sortedKeys = Object.keys(mapping).sort((a, b) => {
  const aNum = /^\d+$/.test(a), bNum = /^\d+$/.test(b);
  if (aNum && bNum) return Number(a) - Number(b);
  if (aNum && !bNum) return -1;
  if (!aNum && bNum) return 1;
  return a.localeCompare(b);
});
const entries = sortedKeys.map(id => keyFmt(id) + ': "' + mapping[id] + '"');
const newLine = '    const BOOK_COVERS = { ' + entries.join(', ') + ' };';

// 5) app.html 교체
const APP_PATH = path.join(__dirname, '..', 'app.html');
const appRaw = fs.readFileSync(APP_PATH);  // binary
const appSrc = appRaw.toString('utf-8');
const lineRegex = /^[ \t]*const BOOK_COVERS = \{[^\n]*\};/m;
const matchInfo = appSrc.match(lineRegex);
if (!matchInfo) {
  console.error('[ERR] app.html에서 BOOK_COVERS 라인을 찾지 못했어요.');
  process.exit(1);
}
const newAppSrc = appSrc.replace(lineRegex, newLine);
fs.writeFileSync(APP_PATH, newAppSrc, 'utf-8');
console.log('');
console.log('[OK] app.html 업데이트 완료 (BOOK_COVERS ' + entries.length + ' 매핑)');
console.log('');
console.log('다음 단계: cd C:\\dev\\bookquest && .\\deploy.ps1 "feat: BOOK_COVERS 매핑 자동 업데이트 — 알라딘 127권 + 누락 42권 자물쇠 폴백"');
