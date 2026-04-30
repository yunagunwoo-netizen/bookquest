// scripts/ocr_recommended_books.js
// 경기도교육청 추천도서 캡처 21장 → Claude vision으로 도서 리스트 추출
//
// 실행:
//   cd C:\dev\bookquest
//   node scripts/ocr_recommended_books.js
//
// 결과: ocr_results/extracted_books.json (마스터 리스트)
//       ocr_results/per_image/*.json (장별 결과)

const fs = require('fs');
const path = require('path');
const https = require('https');

// .env 로드 (functions/.env에서 CLAUDE_KEY 읽기)
function loadEnv() {
  const envPath = path.join(__dirname, '..', 'functions', '.env');
  const content = fs.readFileSync(envPath, 'utf-8');
  const env = {};
  content.split(/\r?\n/).forEach(line => {
    const m = line.match(/^([A-Z_]+)=(.+?)$/);
    if (m) env[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
  });
  return env;
}

const env = loadEnv();
const API_KEY = env.CLAUDE_KEY;
if (!API_KEY) {
  console.error('❌ CLAUDE_KEY 없음. functions/.env 확인하세요.');
  process.exit(1);
}
console.log(`🔑 키 prefix: ${API_KEY.slice(0, 20)}... (${API_KEY.length}자)`);

const SRC_DIR = path.join(__dirname, '..', 'recommended_lists_enlarged');
const OUT_DIR = path.join(__dirname, '..', 'ocr_results');
const PER_IMG_DIR = path.join(OUT_DIR, 'per_image');
fs.mkdirSync(OUT_DIR, { recursive: true });
fs.mkdirSync(PER_IMG_DIR, { recursive: true });

// 사용 모델 — Sonnet 4.6 (vision 정확도 높음)
const MODEL = 'claude-sonnet-4-6';

// Anthropic API 호출 (vision)
function callClaude(imageBase64, mediaType) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: MODEL,
      max_tokens: 4000,
      messages: [{
        role: 'user',
        content: [
          {
            type: 'image',
            source: { type: 'base64', media_type: mediaType, data: imageBase64 }
          },
          {
            type: 'text',
            text: `이 이미지는 경기도교육청 「초등 교과연계 추천도서 목록」입니다. 표 안의 모든 책을 정확히 추출하세요.

추출 규칙:
1. 표 헤더에서 학년(초1~초6) / 과목(국어·사회·과학·수학) 정보 파악
2. 각 행에서: 도서명, 저자, 출판사, 출판년도 추출
3. 한 글자도 빠뜨리지 말 것 — 작은 글씨도 모두
4. 헤더에 「초등 X학년」 표시 있으면 모든 책에 grade로 부여

JSON 형식으로만 응답 (설명 없이):
{
  "header_grade": 6,
  "header_subjects": ["국어", "사회", "과학"],
  "books": [
    {
      "subject": "수학",
      "title": "정확한 도서명",
      "author": "저자",
      "publisher": "출판사",
      "year": 2018
    }
  ]
}`
          }
        ]
      }]
    });

    const req = https.request({
      hostname: 'api.anthropic.com',
      path: '/v1/messages',
      method: 'POST',
      headers: {
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
        'content-length': Buffer.byteLength(body)
      }
    }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          return reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 500)}`));
        }
        try {
          const json = JSON.parse(data);
          const text = json.content[0].text;
          resolve({ text, usage: json.usage });
        } catch (e) {
          reject(new Error(`JSON parse: ${e.message}\nRaw: ${data.slice(0, 500)}`));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function extractJson(text) {
  // JSON 블록 추출 (코드펜스 제거)
  const fenced = text.match(/```(?:json)?\s*([\s\S]+?)```/);
  const raw = fenced ? fenced[1] : text;
  const m = raw.match(/\{[\s\S]+\}/);
  if (!m) throw new Error('JSON 못 찾음');
  return JSON.parse(m[0]);
}

async function processImage(filename) {
  const filepath = path.join(SRC_DIR, filename);
  const imageBase64 = fs.readFileSync(filepath).toString('base64');
  const mediaType = 'image/png';

  console.log(`\n📷 [${filename}]`);
  const start = Date.now();
  const { text, usage } = await callClaude(imageBase64, mediaType);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  let parsed;
  try {
    parsed = extractJson(text);
  } catch (e) {
    console.error(`❌ JSON 파싱 실패: ${e.message}`);
    fs.writeFileSync(path.join(PER_IMG_DIR, filename + '.raw.txt'), text);
    return null;
  }

  const bookCount = (parsed.books || []).length;
  console.log(`✅ ${bookCount}권 추출 (${elapsed}초, in=${usage.input_tokens} out=${usage.output_tokens})`);

  // 메타 정보 추가
  parsed._source_file = filename;
  parsed._extracted_at = new Date().toISOString();
  parsed._tokens = usage;

  fs.writeFileSync(
    path.join(PER_IMG_DIR, filename.replace('.png', '.json')),
    JSON.stringify(parsed, null, 2)
  );

  return parsed;
}

(async () => {
  const files = fs.readdirSync(SRC_DIR)
    .filter(f => f.endsWith('.png') && !f.startsWith('test_'))
    .sort();
  console.log(`\n총 ${files.length}장 처리 시작\n`);

  const allBooks = [];
  let totalIn = 0, totalOut = 0, ok = 0, fail = 0;

  for (const file of files) {
    try {
      const result = await processImage(file);
      if (result) {
        ok++;
        totalIn += result._tokens.input_tokens;
        totalOut += result._tokens.output_tokens;
        (result.books || []).forEach(b => {
          b._source = file;
          b._grade = result.header_grade;
          allBooks.push(b);
        });
      } else {
        fail++;
      }
    } catch (e) {
      console.error(`❌ ${file}: ${e.message}`);
      fail++;
    }
    // 분당 50회 rate limit 회피
    await new Promise(r => setTimeout(r, 1500));
  }

  console.log(`\n=== 종합 ===`);
  console.log(`성공: ${ok}장 / 실패: ${fail}장`);
  console.log(`총 추출 책: ${allBooks.length}권 (중복 포함)`);
  console.log(`토큰: input=${totalIn}, output=${totalOut}`);
  // Sonnet 4.6 가격: $3/MTok input, $15/MTok output (대략)
  const cost = (totalIn * 3 + totalOut * 15) / 1_000_000;
  console.log(`예상 비용: $${cost.toFixed(3)}`);

  // 마스터 파일 저장
  const master = {
    extracted_at: new Date().toISOString(),
    source_directory: SRC_DIR,
    total_images: files.length,
    success: ok,
    fail: fail,
    total_books_raw: allBooks.length,
    books: allBooks
  };

  fs.writeFileSync(
    path.join(OUT_DIR, 'extracted_books.json'),
    JSON.stringify(master, null, 2)
  );

  console.log(`\n✅ 저장: ocr_results/extracted_books.json (${allBooks.length}권)`);
  console.log(`📁 장별: ocr_results/per_image/`);
})();
