const functions = require("firebase-functions");
const Anthropic = require("@anthropic-ai/sdk").default;
const fetch = require("node-fetch");
const { TextToSpeechClient } = require("@google-cloud/text-to-speech");
const { GoogleGenerativeAI } = require("@google/generative-ai");
const admin = require("firebase-admin");
if (!admin.apps.length) admin.initializeApp();

// ═══════════════════════════════════════
// 🔑 API 키는 .env 파일 또는 Google Cloud Secret Manager로 관리
// functions/.env 파일에 설정:
//   CLAUDE_KEY=sk-ant-...
//   ALADIN_KEY=ttb...
// ═══════════════════════════════════════

// CORS 헤더 설정
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

// OPTIONS 프리플라이트 처리
function handleCors(req, res) {
  if (req.method === "OPTIONS") {
    res.set(corsHeaders);
    res.status(204).send("");
    return true;
  }
  res.set(corsHeaders);
  return false;
}

// ═══════════════════════════════════════
// 📚 1. 책 기반 Q&A (Claude AI)
// ═══════════════════════════════════════
exports.askBook = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { question, bookData, chatHistory, studentName } = req.body;

    if (!question) {
      res.status(400).json({ error: "질문이 필요합니다." });
      return;
    }

    const apiKey = process.env.CLAUDE_KEY;
    if (!apiKey) {
      res.status(500).json({ error: "Claude API 키가 설정되지 않았습니다." });
      return;
    }

    const anthropic = new Anthropic({ apiKey });

    // 학생 이름에서 성 제거 + 친근한 호칭 생성
    const fullName = studentName || "친구";
    const koreanSurnames = ["김","이","박","최","정","강","조","윤","장","임","한","오","서","신","권","황","안","송","류","유","홍","전","고","문","양","손","배","백","허","노","남","하","곽","성","차","주","우","민","구","나","진","천","원","심","방","공","염","여","추","도","석","선","설","마","길","연","위","표","명","기","반","왕","금","옥","육","인","맹","제","모","탁","국","어","은","편"];
    const name = fullName.length >= 3 && koreanSurnames.includes(fullName.charAt(0)) ? fullName.slice(1) : fullName;
    // "건우" → "건우야", "민석" → "민석아"
    const lastChar = name.charAt(name.length - 1);
    const hasBatchim = lastChar && ((lastChar.charCodeAt(0) - 0xAC00) % 28 !== 0);
    const nickname = name + (hasBatchim ? "아" : "야");

    // 책 데이터를 시스템 프롬프트에 포함
    const systemPrompt = `너는 '콜레트 선생님'이야. 초등학교 6학년 학생 "${name}"의 독서 도우미 선생님이야.
${name}이가 읽은 책들의 내용을 바탕으로 질문에 답변해주는 밝고 활기찬 선생님이야.
학생을 부를 때는 항상 "${nickname}"처럼 친근하게 불러줘. "김건우", "건우" 같은 딱딱한 호칭 대신 "건우야", "지민아"처럼.

📚 ${name}이가 읽은 책 정보:
${bookData || "아직 읽은 책이 없습니다."}

답변 규칙:
1. 책의 내용을 근거로 답변하되, 어떤 책의 어떤 부분에서 나온 내용인지 알려줘.
2. 책에 없는 내용이라면 일반 지식으로 답변하되, "이건 책에는 없는 내용인데..." 라고 말해줘.
3. 초등학교 6학년이 이해할 수 있는 쉬운 말로 설명해줘.
4. 답변은 3~5문장, 최대 200자 이내로 간결하게 하고 반드시 완결된 문장으로 끝내.
5. 학생 이름을 부를 때 "${nickname}"처럼 친근하게 불러줘. "너"라고 하지 말고 항상 이름을 사용해. 예: "${nickname}, 좋은 질문이야!"
6. 친근하지만 격식 있는 선생님 말투를 사용해. 완전한 반말도 아니고 존댓말도 아닌, 학생을 가르치는 선생님의 말투야.
7. 한국어 맞춤법을 정확하게 지켜줘.
8. 이모지나 마크다운을 사용하지 마.`;

    // 이전 대화 히스토리 포함
    const messages = [];
    if (chatHistory && Array.isArray(chatHistory)) {
      chatHistory.forEach((msg) => {
        messages.push({
          role: msg.role === "user" ? "user" : "assistant",
          content: msg.text,
        });
      });
    }
    messages.push({ role: "user", content: question });

    const response = await anthropic.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 500,
      system: systemPrompt,
      messages: messages,
    });

    const aiText = response.content[0].text;

    res.json({
      answer: aiText,
      usage: {
        input_tokens: response.usage.input_tokens,
        output_tokens: response.usage.output_tokens,
      },
    });
  } catch (error) {
    console.error("askBook error:", error);
    res.status(500).json({ error: "AI 응답 생성 실패: " + error.message });
  }
});

// ═══════════════════════════════════════
// 💬 2. 토론 AI 코치 (Claude AI)
// ═══════════════════════════════════════
exports.discussionCoach = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { userAnswer, topic, bookTitle, bookSummary, isDeep, studentName, chatHistory, roundNumber } = req.body;

    if (!userAnswer || !topic) {
      res.status(400).json({ error: "답변과 토론 주제가 필요합니다." });
      return;
    }

    const apiKey = process.env.CLAUDE_KEY;
    if (!apiKey) {
      res.status(500).json({ error: "Claude API 키가 설정되지 않았습니다." });
      return;
    }

    const fullName = studentName || "친구";
    // 성을 제거하고 이름만 사용 (예: "김건우" → "건우", "박지민" → "지민")
    const name = fullName.length >= 3 && ["김","이","박","최","정","강","조","윤","장","임","한","오","서","신","권","황","안","송","류","유","홍","전","고","문","양","손","배","백","허","노","남","하","곽","성","차","주","우","민","구","나","진","천","원","심","방","공","염","여","추","도","석","선","설","마","길","연","위","표","명","기","반","왕","금","옥","육","인","맹","제","모","탁","국","어","은","편"].includes(fullName.charAt(0)) ? fullName.slice(1) : fullName;
    // 친근한 호칭: "건우야" / "민석아"
    const lastChar2 = name.charAt(name.length - 1);
    const hasBatchim2 = lastChar2 && ((lastChar2.charCodeAt(0) - 0xAC00) % 28 !== 0);
    const nickname = name + (hasBatchim2 ? "아" : "야");
    const anthropic = new Anthropic({ apiKey });

    // 라운드 번호 (1=첫 답변, 2=두 번째, 3=마지막)
    const round = roundNumber || 1;

    // 라운드별 역할 지시
    let roundDirective;
    if (round === 1) {
      roundDirective = `[1라운드 — 탐색]
이것은 ${name}의 첫 번째 답변이야.
- 답변에서 흥미로운 부분을 하나 골라 "왜 그렇게 생각했어?" 또는 "그게 ~와 어떤 관계가 있을까?" 같은 꼬리 질문을 해줘.
- 칭찬은 구체적으로 하되 한 문장만. 나머지는 사고를 확장하는 질문에 집중해.
- 아이가 미처 생각 못한 다른 관점 하나를 짧게 힌트로 던져줘.`;
    } else if (round === 2) {
      roundDirective = `[2라운드 — 심화]
이것은 ${name}의 두 번째 답변이야. 이전 대화 맥락을 참고해.
- 1라운드에서 던진 질문에 잘 답했으면 한 단계 더 깊이 파고드는 질문을 해줘.
- "반대로 생각하면 어떨까?", "만약 ~라면 어떻게 될까?" 같은 반론이나 가정을 제시해줘.
- 책의 구체적인 내용이나 실제 사례를 연결해서 생각을 넓혀줘.`;
    } else {
      roundDirective = `[3라운드 — 정리]
이것은 ${name}의 마지막 답변이야. 이전 대화 맥락을 참고해.
- 세 번의 대화에서 ${name}의 생각이 어떻게 발전했는지 짧게 정리해줘.
- 처음 답변과 비교해서 깊어진 부분을 구체적으로 짚어줘.
- 이 주제에 대해 일상에서 더 생각해볼 수 있는 상황 하나를 제안하며 마무리해줘.
- 따뜻하고 격려하는 톤으로 끝내줘.`;
    }

    const systemPrompt = `너는 '칼 선생님'이야. 초등학교 6학년 학생 "${name}"의 독서 토론을 이끄는 선생님이야.
단순히 평가하는 게 아니라, 소크라테스 방식으로 질문을 통해 학생 스스로 더 깊이 생각하게 이끌어줘.
학생을 부를 때는 항상 "${nickname}"처럼 친근하게 불러줘.

📖 책: ${bookTitle}
📝 책 요약: ${bookSummary || ""}
❓ 토론 질문: ${topic.q}
💡 힌트: ${topic.hint}
난이도: ${isDeep ? "심화" : "기본"}
학생 이름: ${name}
현재 라운드: ${round}/3

${roundDirective}

말투 규칙:
- "${nickname}"처럼 친근하게 불러줘. "너"라고 하지 말고 항상 이름을 사용해.
- 친근한 선생님 말투. 예: "${nickname}, 좋은 생각이야!", "한번 생각해 볼까?"
- 감탄사를 자연스럽게 써줘. "오!", "와!", "흠, 재밌는 관점이네!"
- 틀린 부분은 밝은 분위기로 바로잡되, 답을 직접 알려주지 말고 질문으로 유도해.

작성 규칙:
- 전체 답변은 4~6문장, 최대 300자 이내. 음성으로 읽어주므로 간결해야 해.
- 반드시 마지막 문장을 완전히 끝내고 마무리해. 문장이 중간에 끊기면 절대 안 돼.
- 이모지나 마크다운(**굵은 글씨** 등)을 사용하지 마. 순수 텍스트로만 답변해.
- 한국어 맞춤법, 띄어쓰기, 조사 정확하게 지켜줘.`;

    // 대화 기록이 있으면 이전 맥락을 포함해서 전송
    let messages = [];
    if (chatHistory && Array.isArray(chatHistory) && chatHistory.length > 0) {
      // chatHistory: [{role: "user"|"ai", text: "..."}]
      for (const msg of chatHistory) {
        if (msg.role === "user") {
          messages.push({ role: "user", content: msg.text });
        } else if (msg.role === "ai" && msg.text) {
          messages.push({ role: "assistant", content: msg.text });
        }
      }
    }
    // 현재 답변 추가
    messages.push({ role: "user", content: userAnswer });

    // 연속된 같은 역할 메시지 병합 (Claude API 요구사항)
    const mergedMessages = [];
    for (const msg of messages) {
      if (mergedMessages.length > 0 && mergedMessages[mergedMessages.length - 1].role === msg.role) {
        mergedMessages[mergedMessages.length - 1].content += "\n" + msg.content;
      } else {
        mergedMessages.push({ ...msg });
      }
    }
    // 첫 메시지가 assistant이면 제거 (Claude API는 user로 시작해야 함)
    while (mergedMessages.length > 0 && mergedMessages[0].role === "assistant") {
      mergedMessages.shift();
    }

    const response = await anthropic.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 500,
      system: systemPrompt,
      messages: mergedMessages.length > 0 ? mergedMessages : [{ role: "user", content: userAnswer }],
    });

    res.json({
      feedback: response.content[0].text,
      usage: {
        input_tokens: response.usage.input_tokens,
        output_tokens: response.usage.output_tokens,
      },
    });
  } catch (error) {
    console.error("discussionCoach error:", error);
    res.status(500).json({ error: "AI 응답 생성 실패: " + error.message });
  }
});

// ═══════════════════════════════════════
// 📖 3. 도서 추천 (알라딘 API + Claude)
// ═══════════════════════════════════════
exports.recommendBooks = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { readBooks, interests } = req.body;

    if (!readBooks || readBooks.length === 0) {
      res.status(400).json({ error: "읽은 책 정보가 필요합니다." });
      return;
    }

    const aladinKey = process.env.ALADIN_KEY;
    const claudeKey = process.env.CLAUDE_KEY;

    if (!aladinKey || !claudeKey) {
      res
        .status(500)
        .json({ error: "API 키가 설정되지 않았습니다." });
      return;
    }

    // 읽은 책에서 키워드 추출
    const keywords = readBooks.flatMap((book) => book.keywords || []);

    // 알라딘 API로 도서 검색 (키워드별로)
    const searchPromises = keywords.slice(0, 3).map(async (keyword) => {
      const url = `http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=${aladinKey}&Query=${encodeURIComponent(keyword)}&QueryType=Keyword&MaxResults=5&start=1&SearchTarget=Book&output=js&Version=20131101&CategoryId=50940`;
      try {
        const response = await fetch(url);
        const data = await response.json();
        return data.item || [];
      } catch (e) {
        console.error("알라딘 검색 실패:", keyword, e);
        return [];
      }
    });

    // 알라딘 베스트셀러도 가져오기 (청소년 카테고리)
    const bestsellerUrl = `http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=${aladinKey}&QueryType=Bestseller&MaxResults=5&start=1&SearchTarget=Book&output=js&Version=20131101&CategoryId=50940`;

    const [searchResults, bestsellerRes] = await Promise.all([
      Promise.all(searchPromises),
      fetch(bestsellerUrl)
        .then((r) => r.json())
        .then((d) => d.item || [])
        .catch(() => []),
    ]);

    // 검색 결과 합치기 + 중복 제거
    const allBooks = [...searchResults.flat(), ...bestsellerRes];
    const uniqueBooks = [];
    const seenIsbns = new Set();
    const readTitles = readBooks.map((b) => b.title.toLowerCase());

    for (const book of allBooks) {
      if (
        book.isbn13 &&
        !seenIsbns.has(book.isbn13) &&
        !readTitles.some((t) => book.title.toLowerCase().includes(t))
      ) {
        seenIsbns.add(book.isbn13);
        uniqueBooks.push({
          title: book.title,
          author: book.author,
          publisher: book.publisher,
          description: book.description,
          cover: book.cover,
          link: book.link,
          categoryName: book.categoryName,
          priceStandard: book.priceStandard,
        });
      }
    }

    // Claude에게 큐레이션 요청
    const anthropic = new Anthropic({ apiKey: claudeKey });

    const curationPrompt = `너는 초등학교 6학년 학생의 독서 큐레이터야.

학생이 읽은 책:
${readBooks.map((b) => `- "${b.title}": ${b.summary}`).join("\n")}

${interests ? `학생의 관심사: ${interests}` : ""}

아래 도서 목록에서 이 학생에게 가장 적합한 책 3권을 골라줘.
각 책에 대해 추천 이유를 2문장으로 설명해줘.

도서 목록:
${uniqueBooks
  .slice(0, 15)
  .map((b, i) => `${i + 1}. "${b.title}" (${b.author}) - ${b.description || "설명 없음"}`)
  .join("\n")}

반드시 아래 JSON 형식으로만 답변해:
[
  {"index": 번호, "reason": "추천 이유"},
  {"index": 번호, "reason": "추천 이유"},
  {"index": 번호, "reason": "추천 이유"}
]`;

    const aiResponse = await anthropic.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 500,
      messages: [{ role: "user", content: curationPrompt }],
    });

    let recommendations = [];
    try {
      const aiText = aiResponse.content[0].text;
      const jsonMatch = aiText.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        recommendations = parsed.map((rec) => ({
          ...uniqueBooks[rec.index - 1],
          reason: rec.reason,
        })).filter((r) => r.title);
      }
    } catch (e) {
      // AI 파싱 실패 시 상위 3권 반환
      recommendations = uniqueBooks.slice(0, 3).map((b) => ({
        ...b,
        reason: "읽은 책과 관련된 주제의 좋은 책입니다.",
      }));
    }

    res.json({
      recommendations,
      totalFound: uniqueBooks.length,
    });
  } catch (error) {
    console.error("recommendBooks error:", error);
    res.status(500).json({ error: "도서 추천 실패: " + error.message });
  }
});

// ═══════════════════════════════════════
// 🔊 4. TTS — ElevenLabs (1순위) → Chirp 3 HD (2순위) → OpenAI (3순위) → Neural2 (최종 폴백)
// ═══════════════════════════════════════
// .env 설정으로 엔진 전환:
//   TTS_ENGINE=elevenlabs → ElevenLabs 우선 (기본값)
//   TTS_ENGINE=chirp      → Chirp 3 HD 우선
//   TTS_ENGINE=openai     → OpenAI 우선
//   TTS_ENGINE=neural2    → Neural2만 사용
// ElevenLabs 음성: voice ID로 지정 (기본: 한국어 여성 "Aria")
// Chirp 3 HD 음성: ko-KR-Chirp3-HD-Achernar 등
// OpenAI 음성: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer
const ttsClient = new TextToSpeechClient();

// ElevenLabs 기본 설정
const ELEVENLABS_DEFAULT_VOICE = "9BWtsMINqrJLrRacOk9x";  // Aria (multilingual, 밝고 친근)
const ELEVENLABS_MODEL = "eleven_flash_v2_5";              // Flash v2.5 (저지연, 32개 언어)

exports.textToSpeech = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { text, voice } = req.body;

    if (!text) {
      res.status(400).json({ error: "텍스트가 필요합니다." });
      return;
    }

    const trimmedText = text.slice(0, 2500);
    const ttsEngine = (process.env.TTS_ENGINE || "elevenlabs").toLowerCase();
    const openaiKey = process.env.OPENAI_KEY || process.env.OPENAI_API_KEY;
    const elevenlabsKey = process.env.ELEVENLABS_KEY;

    // ── 1순위: ElevenLabs ──
    if (elevenlabsKey && (ttsEngine === "elevenlabs" || ttsEngine === "11labs")) {
      try {
        const voiceId = voice || ELEVENLABS_DEFAULT_VOICE;
        const ttsRes = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
          method: "POST",
          headers: {
            "xi-api-key": elevenlabsKey,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
          },
          body: JSON.stringify({
            text: trimmedText,
            model_id: ELEVENLABS_MODEL,
            voice_settings: {
              stability: 0.5,
              similarity_boost: 0.75,
              style: 0.3,
              use_speaker_boost: true,
            },
          }),
        });

        if (!ttsRes.ok) {
          const errBody = await ttsRes.text();
          throw new Error(`ElevenLabs ${ttsRes.status}: ${errBody.slice(0, 200)}`);
        }

        const arrayBuf = await ttsRes.arrayBuffer();
        const audioBase64 = Buffer.from(arrayBuf).toString("base64");
        res.json({ audio: audioBase64, format: "mp3", textLength: trimmedText.length, engine: "elevenlabs" });
        return;
      } catch (elErr) {
        console.warn("[TTS] ElevenLabs 실패, 다음 엔진으로 폴백:", elErr.message);
      }
    }

    // ── 2순위: Google Chirp 3 HD ──
    if (ttsEngine === "elevenlabs" || ttsEngine === "11labs" || ttsEngine === "chirp" || ttsEngine === "chirp3") {
      try {
        const chirpVoice = voice || "ko-KR-Chirp3-HD-Achernar";
        const [response] = await ttsClient.synthesizeSpeech({
          input: { text: trimmedText },
          voice: { languageCode: "ko-KR", name: chirpVoice },
          audioConfig: {
            audioEncoding: "MP3",
            speakingRate: 0.95,
            volumeGainDb: 2.0,
          },
        });
        const audioBase64 = response.audioContent.toString("base64");
        res.json({ audio: audioBase64, format: "mp3", textLength: trimmedText.length, engine: "chirp3-hd" });
        return;
      } catch (chirpErr) {
        console.warn("[TTS] Chirp 3 HD 실패, 다음 엔진으로 폴백:", chirpErr.message);
      }
    }

    // ── 3순위: OpenAI TTS ──
    if (openaiKey && ttsEngine !== "neural2") {
      try {
        const openaiVoices = ["alloy","ash","ballad","coral","echo","fable","nova","onyx","sage","shimmer"];
        const openaiVoice = openaiVoices.includes(voice) ? voice : "nova";

        const ttsRes = await fetch("https://api.openai.com/v1/audio/speech", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${openaiKey}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "tts-1",
            input: trimmedText,
            voice: openaiVoice,
            response_format: "mp3",
            speed: 0.95,
          }),
        });

        if (!ttsRes.ok) {
          const errText = await ttsRes.text();
          throw new Error(`OpenAI TTS ${ttsRes.status}: ${errText.slice(0, 200)}`);
        }

        const arrayBuf = await ttsRes.arrayBuffer();
        const audioBase64 = Buffer.from(arrayBuf).toString("base64");
        res.json({ audio: audioBase64, format: "mp3", textLength: trimmedText.length, engine: "openai" });
        return;
      } catch (openaiErr) {
        console.warn("[TTS] OpenAI 실패, Neural2로 폴백:", openaiErr.message);
      }
    }

    // ── 4순위: Google Neural2 (최종 폴백) ──
    const voiceName = voice || "ko-KR-Neural2-C";
    const [response] = await ttsClient.synthesizeSpeech({
      input: { text: trimmedText },
      voice: { languageCode: "ko-KR", name: voiceName },
      audioConfig: {
        audioEncoding: "MP3",
        speakingRate: 0.95,
        pitch: 1.0,
        volumeGainDb: 2.0,
      },
    });

    const audioBase64 = response.audioContent.toString("base64");
    res.json({ audio: audioBase64, format: "mp3", textLength: trimmedText.length, engine: "neural2" });
  } catch (error) {
    console.error("textToSpeech error:", error);
    res.status(500).json({ error: "음성 생성 실패: " + error.message });
  }
});

// ═══════════════════════════════════════
// ⚔️ 5. 아바타 Q&A 토론 배틀 (Gemini 2.5 Flash) v2 — tokens=8000, thinking=off
// ═══════════════════════════════════════
// Input: { myUid, oppUid, myPack, oppPack, mode }
// - myPack, oppPack: 클라이언트의 getAvatarKnowledgePack() 결과 문자열
// - mode: "watch"(유저 직접 관람) | "auto"(아바타 대리 배틀)
// Output: { battleId, rounds, winner, narration }
// Daily limit: 1회/일 (서버 검증 + 클라 검증 이중)
// ═══════════════════════════════════════

const BATTLE_DAILY_LIMIT = 1;

function getTodayKST() {
  // KST 기준 YYYY-MM-DD
  const now = new Date();
  const kst = new Date(now.getTime() + 9 * 60 * 60 * 1000);
  return kst.toISOString().slice(0, 10);
}

function buildBattlePrompt(myPack, oppPack, myName, oppName) {
  return `너는 어린이 독서 앱 "BookQuest"의 **아바타 토론 배틀 중계 엔진**이야.
두 아바타가 3라운드 배틀을 하는데, 결과는 양쪽 아바타의 독서 수준·강약점·완독 책 내용을 반영해서 **다양하게** 나와야 재미있어.

[규칙]
- 1~2라운드: Q&A 지식 대결 (책에서 출제). 아바타가 답을 모르는 책 질문이면 틀리게 답해도 됨.
- 3라운드: 자유 주제 미니 토론 (찬반 or 가치판단). 책 한정 X — 아바타가 쌓은 지식 기반 주장.
- 매 라운드 판정(my/opp/draw) + 짧은 판정 이유(1문장)
- 전체 승자는 2승 이상 또는 동점 시 draw
- **응답은 반드시 JSON 한 덩어리로만**. 주석·마크다운·설명 금지.
- 각 답변은 1~2문장, 초등학생이 이해 가능한 어휘로.

[아바타1 — 내 쪽]
이름표: ${myName}
${myPack}

[아바타2 — 상대 쪽]
이름표: ${oppName}
${oppPack}

[출력 JSON 스키마]
{
  "rounds": [
    {
      "type": "qa",
      "book": "책 제목 or 주제 키워드",
      "question": "질문 1문장",
      "myAnswer": "내 쪽 답변",
      "oppAnswer": "상대 답변",
      "judge": "my" | "opp" | "draw",
      "reason": "판정 근거 1문장"
    },
    { "type": "qa", "book": "...", "question": "...", "myAnswer": "...", "oppAnswer": "...", "judge": "...", "reason": "..." },
    {
      "type": "debate",
      "topic": "자유 주제 문장",
      "myStance": "찬성" | "반대" | "...",
      "oppStance": "찬성" | "반대" | "...",
      "myArgument": "주장 1~2문장",
      "oppArgument": "주장 1~2문장",
      "judge": "my" | "opp" | "draw",
      "reason": "판정 근거 1문장"
    }
  ],
  "winner": "my" | "opp" | "draw",
  "narration": "전투 전체를 흥미진진하게 요약하는 1~2문장 내레이션"
}`;
}

exports.runAvatarBattle = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { myUid, oppUid, myPack, oppPack, myName, oppName, mode } = req.body || {};

    if (!myUid || !oppUid) {
      res.status(400).json({ error: "myUid, oppUid 가 필요합니다." });
      return;
    }
    if (!myPack || !oppPack) {
      res.status(400).json({ error: "myPack, oppPack 이 필요합니다." });
      return;
    }
    if (myUid === oppUid) {
      res.status(400).json({ error: "자기 자신과는 배틀할 수 없어요." });
      return;
    }

    const apiKey = process.env.GEMINI_KEY || process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
    if (!apiKey) {
      res.status(500).json({ error: "Gemini API 키가 설정되지 않았습니다." });
      return;
    }

    const db = admin.firestore();
    const today = getTodayKST();

    // 1) 일1회 제한 서버 검증 (유저 doc이 없으면 통과 — 신규 유저)
    const myRef = db.collection("users").doc(myUid);
    const mySnap = await myRef.get();
    const myData = mySnap.exists ? (mySnap.data() || {}) : {};
    if (myData.lastBattleDate === today && (myData.battleTodayCount || 0) >= BATTLE_DAILY_LIMIT) {
      res.status(429).json({ error: "오늘 배틀 기회를 이미 사용했어요. 내일 다시 도전해줘!" });
      return;
    }

    // 2) Gemini 호출
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash",
      generationConfig: {
        responseMimeType: "application/json",
        temperature: 0.9, // 다양성 확보
        maxOutputTokens: 8000, // 한국어 + thinking 토큰 여유
        thinkingConfig: { thinkingBudget: 0 }, // 2.5 Flash thinking 끄기 (속도·토큰 절약)
      },
    });

    const prompt = buildBattlePrompt(myPack, oppPack, myName || "내 아바타", oppName || "상대 아바타");
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    const finishReason = result.response.candidates?.[0]?.finishReason;

    let battle;
    try {
      battle = JSON.parse(text);
    } catch (e) {
      // 잘린 JSON 복구 시도: 마지막 완결된 } 위치까지 잘라서 파싱
      if (finishReason === "MAX_TOKENS") {
        throw new Error("Gemini 응답이 토큰 한도를 초과했어요. 잠시 후 다시 시도해줘!");
      }
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) throw new Error("Gemini JSON 파싱 실패(finish=" + finishReason + "): " + text.slice(0, 200));
      try {
        battle = JSON.parse(m[0]);
      } catch (e2) {
        throw new Error("Gemini JSON 파싱 실패(finish=" + finishReason + "): " + text.slice(0, 200));
      }
    }

    if (!Array.isArray(battle.rounds) || battle.rounds.length !== 3) {
      throw new Error("배틀 결과 형식 오류: rounds 가 3개가 아님");
    }
    if (!["my", "opp", "draw"].includes(battle.winner)) {
      // winner 누락 시 라운드 판정 집계로 보완
      const c = { my: 0, opp: 0, draw: 0 };
      battle.rounds.forEach(r => { if (c[r.judge] !== undefined) c[r.judge]++; });
      battle.winner = c.my > c.opp ? "my" : c.opp > c.my ? "opp" : "draw";
    }

    // 3) 배틀 문서 저장
    const battleRef = db.collection("battles").doc();
    await battleRef.set({
      myUid,
      oppUid,
      myName: myName || null,
      oppName: oppName || null,
      rounds: battle.rounds,
      winner: battle.winner,
      narration: battle.narration || "",
      mode: mode || "auto",
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      dateKST: today,
    });

    // 4) 양쪽 유저 통계 원자적 업데이트
    const batch = db.batch();
    const myWinInc = battle.winner === "my" ? 1 : 0;
    const myLoseInc = battle.winner === "opp" ? 1 : 0;
    const myDrawInc = battle.winner === "draw" ? 1 : 0;
    // 날짜가 바뀌었으면 count를 1로 리셋, 같은 날이면 +1
    const nextTodayCount = myData.lastBattleDate === today
      ? (myData.battleTodayCount || 0) + 1
      : 1;
    batch.set(
      myRef,
      {
        battleWins: admin.firestore.FieldValue.increment(myWinInc),
        battleLosses: admin.firestore.FieldValue.increment(myLoseInc),
        battleDraws: admin.firestore.FieldValue.increment(myDrawInc),
        weeklyBattleWins: admin.firestore.FieldValue.increment(myWinInc),
        lastBattleDate: today,
        battleTodayCount: nextTodayCount,
        lastBattleId: battleRef.id,
      },
      { merge: true }
    );
    const oppRef = db.collection("users").doc(oppUid);
    batch.set(
      oppRef,
      {
        battleWins: admin.firestore.FieldValue.increment(myLoseInc),
        battleLosses: admin.firestore.FieldValue.increment(myWinInc),
        battleDraws: admin.firestore.FieldValue.increment(myDrawInc),
        weeklyBattleWins: admin.firestore.FieldValue.increment(myLoseInc),
        lastOpponentBattleId: battleRef.id,
      },
      { merge: true }
    );
    await batch.commit();

    res.json({
      battleId: battleRef.id,
      rounds: battle.rounds,
      winner: battle.winner,
      narration: battle.narration || "",
      usage: result.response.usageMetadata || null,
    });
  } catch (error) {
    console.error("runAvatarBattle error:", error);
    res.status(500).json({ error: "배틀 생성 실패: " + error.message });
  }
});

// =============================================================
//  Interactive Battle (v1.4) — 직접 참여, 객관식 4지선다
// =============================================================
const BATTLE_PLAY_DAILY_LIMIT = 3;
const BATTLE_PLAY_COIN_COST = 30;

function buildInteractivePrompt(myPack, oppPack, myName, oppName, miniDebateOwner) {
  const debateSection = miniDebateOwner === "me"
    ? `    {
      "type": "debate",
      "mode": "player",
      "topic": "자유 주제 한 문장",
      "myOptions": [
        { "text": "입장·주장 1 (1문장)", "score": 10~90 숫자 (주장 강도) },
        { "text": "입장·주장 2", "score": 10~90 },
        { "text": "입장·주장 3", "score": 10~90 },
        { "text": "입장·주장 4", "score": 10~90 }
      ],
      "oppStance": "상대가 고른 입장 1문장",
      "oppScore": 10~90 숫자,
      "oppReason": "상대가 왜 이 주장을 했는지 1문장 (상대 독서 수준 기반)"
    }`
    : `    {
      "type": "debate",
      "mode": "ai",
      "topic": "자유 주제 한 문장",
      "myStance": "내 아바타 입장",
      "oppStance": "상대 입장",
      "myArgument": "내 아바타 주장 1~2문장",
      "oppArgument": "상대 주장 1~2문장",
      "judge": "my" | "opp" | "draw",
      "reason": "판정 근거 1문장"
    }`;

  return `너는 어린이 독서 앱 "BookQuest"의 **직접 참여 배틀 문제 생성기**야.
아이가 자기 아바타를 조종해서 상대 아바타와 5라운드 대결한다.

[규칙]
- 라운드 1,2: Q&A 객관식 4지선다. 책에서 사실 기반 질문 출제 (내 아바타 또는 상대 아바타가 읽은 책 중에서).
- 각 Q&A 라운드에 정답 1개 + 그럴듯한 오답 3개. answerIdx 는 0~3 중 정답 위치.
- oppChoiceIdx 는 상대 아바타의 독서 수준·승률을 고려해서 정답 확률 결정 (레벨 높고 승많으면 정답 가능성 큼).
- 라운드 3,4: 문장 완성형. 책 내용 기반으로 미완성 문장 + 3개 보기 제시. 아이가 가장 적절한 마무리를 고른다.
  - sentence: "이 책에서 주인공이 용기를 낸 이유는 ___" 처럼 빈칸(___) 포함 미완성 문장.
  - completions: 3개 보기. 정답 1개 + 그럴듯한 오답 2개.
  - answerIdx: 0~2 중 정답 위치.
  - oppChoiceIdx: 상대 ���바타가 고르는 보기 (독서 수준 기반).
  - explanation: 왜 정답인지 1문장 설명.
  - 4지선다보다 **사고력이 필요한** 문장을 만들어. 단순 사실이 아니라 "왜?", "어떻게?", "무엇을 느꼈을까?" 같은 추론·감상 질문.
- 라운드 5: 미니토론: ${miniDebateOwner === "me" ? "아이가 4개 입장 중 선택" : "AI 자동 토론"}.
- 초등학생이 읽기 쉬운 어휘·1~2문장.
- **응답은 반드시 JSON 한 덩어리로만.** 주석·마크다운·설명 금지.

[아바타1 — 플레이어(아이)]
이름표: ${myName}
${myPack}

[아바타2 — 상대]
이름표: ${oppName}
${oppPack}

[출력 JSON 스키마]
{
  "rounds": [
    {
      "type": "qa",
      "book": "책 제목",
      "question": "질문 1문장",
      "choices": ["보기1", "보기2", "보기3", "보기4"],
      "answerIdx": 0~3,
      "oppChoiceIdx": 0~3,
      "explanation": "정답 설명 1문장 (교육적)"
    },
    {
      "type": "qa",
      "book": "...",
      "question": "...",
      "choices": ["...", "...", "...", "..."],
      "answerIdx": 0~3,
      "oppChoiceIdx": 0~3,
      "explanation": "..."
    },
    {
      "type": "complete",
      "book": "책 제목",
      "sentence": "미완성 문장 ___ 포함",
      "completions": ["마무리1", "마무리2", "마무리3"],
      "answerIdx": 0~2,
      "oppChoiceIdx": 0~2,
      "explanation": "정답 설명 1문장"
    },
    {
      "type": "complete",
      "book": "...",
      "sentence": "...",
      "completions": ["...", "...", "..."],
      "answerIdx": 0~2,
      "oppChoiceIdx": 0~2,
      "explanation": "..."
    },
${debateSection}
  ]
}`;
}

exports.runInteractiveBattle = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { myUid, oppUid, myPack, oppPack, myName, oppName, miniDebateOwner } = req.body || {};

    if (!myUid || !oppUid) {
      res.status(400).json({ error: "myUid, oppUid 가 필요합니다." });
      return;
    }
    if (!myPack || !oppPack) {
      res.status(400).json({ error: "myPack, oppPack 이 필요합니다." });
      return;
    }
    if (myUid === oppUid) {
      res.status(400).json({ error: "자기 자신과는 배틀할 수 없어요." });
      return;
    }
    const owner = miniDebateOwner === "ai" ? "ai" : "me";

    const apiKey = process.env.GEMINI_KEY || process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
    if (!apiKey) {
      res.status(500).json({ error: "Gemini API 키가 설정되지 않았습니다." });
      return;
    }

    const db = admin.firestore();
    const today = getTodayKST();

    // 하루 3회 제한 서버 검증 (참여 모드 별도 카운트)
    const myRef = db.collection("users").doc(myUid);
    const mySnap = await myRef.get();
    const myData = mySnap.exists ? (mySnap.data() || {}) : {};
    if (myData.lastBattlePlayDate === today && (myData.battleTodayPlayCount || 0) >= BATTLE_PLAY_DAILY_LIMIT) {
      res.status(429).json({ error: "오늘 참여 배틀 3회를 모두 사용했어요. 내일 다시 도전!" });
      return;
    }

    // Gemini 호출
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash",
      generationConfig: {
        responseMimeType: "application/json",
        temperature: 0.85,
        maxOutputTokens: 8000,
        thinkingConfig: { thinkingBudget: 0 },
      },
    });

    const prompt = buildInteractivePrompt(
      myPack, oppPack,
      myName || "내 아바타",
      oppName || "상대 아바타",
      owner,
    );
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    const finishReason = result.response.candidates?.[0]?.finishReason;

    let battle;
    try {
      battle = JSON.parse(text);
    } catch (e) {
      if (finishReason === "MAX_TOKENS") {
        throw new Error("Gemini 응답이 토큰 한도를 초과했어요.");
      }
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) throw new Error("Gemini JSON 파싱 실패(finish=" + finishReason + "): " + text.slice(0, 200));
      battle = JSON.parse(m[0]);
    }

    if (!Array.isArray(battle.rounds) || battle.rounds.length !== 5) {
      throw new Error("참여 배틀 형식 오류: rounds가 5개가 아님 (got " + (battle.rounds?.length || 0) + ")");
    }

    // 각 라운드 검증 + 보정
    battle.rounds.forEach((r, i) => {
      if (r.type === "qa") {
        if (!Array.isArray(r.choices) || r.choices.length !== 4) {
          throw new Error(`라운드 ${i + 1}: choices 배열 4개 필요`);
        }
        r.answerIdx = Math.max(0, Math.min(3, Number(r.answerIdx) || 0));
        r.oppChoiceIdx = Math.max(0, Math.min(3, Number(r.oppChoiceIdx) || 0));
      } else if (r.type === "complete") {
        if (!Array.isArray(r.completions) || r.completions.length !== 3) {
          throw new Error(`라운드 ${i + 1}: completions 배열 3개 필요`);
        }
        if (!r.sentence) {
          throw new Error(`라운드 ${i + 1}: sentence 필드 필요`);
        }
        r.answerIdx = Math.max(0, Math.min(2, Number(r.answerIdx) || 0));
        r.oppChoiceIdx = Math.max(0, Math.min(2, Number(r.oppChoiceIdx) || 0));
      }
    });

    // 문서 저장 (판정은 프론트에서 아이 답변 받은 후 수행, 여기선 문제만 저장)
    const battleRef = db.collection("battles").doc();
    await battleRef.set({
      myUid,
      oppUid,
      myName: myName || null,
      oppName: oppName || null,
      rounds: battle.rounds,
      mode: "play",
      miniDebateOwner: owner,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      dateKST: today,
      status: "issued", // 아이가 답변 제출하면 "finished"로 업데이트
    });

    // 참여 카운트 원자적 업데이트 (승/패는 답변 제출 단계에서 별도 처리)
    const nextPlayCount = myData.lastBattlePlayDate === today
      ? (myData.battleTodayPlayCount || 0) + 1
      : 1;
    await myRef.set({
      lastBattlePlayDate: today,
      battleTodayPlayCount: nextPlayCount,
      lastBattleId: battleRef.id,
    }, { merge: true });

    res.json({
      battleId: battleRef.id,
      rounds: battle.rounds,
      miniDebateOwner: owner,
      coinCost: BATTLE_PLAY_COIN_COST,
      todayPlayCount: nextPlayCount,
      dailyLimit: BATTLE_PLAY_DAILY_LIMIT,
      usage: result.response.usageMetadata || null,
    });
  } catch (error) {
    console.error("runInteractiveBattle error:", error);
    res.status(500).json({ error: "참여 배틀 생성 실패: " + error.message });
  }
});

// 참여 배틀 결과 제출 (아이가 답변 완료 후)
exports.submitInteractiveResult = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    const { myUid, oppUid, battleId, winner, roundResults } = req.body || {};

    if (!myUid || !oppUid || !battleId) {
      res.status(400).json({ error: "myUid, oppUid, battleId 필요" });
      return;
    }
    if (!["my", "opp", "draw"].includes(winner)) {
      res.status(400).json({ error: "winner 값 오류" });
      return;
    }

    const db = admin.firestore();
    const battleRef = db.collection("battles").doc(battleId);
    const snap = await battleRef.get();
    if (!snap.exists) {
      res.status(404).json({ error: "배틀을 찾지 못했어요." });
      return;
    }
    const data = snap.data() || {};
    if (data.status === "finished") {
      res.status(409).json({ error: "이미 제출된 배틀입니다." });
      return;
    }

    // 배틀 문서 finalize
    await battleRef.set({
      winner,
      roundResults: Array.isArray(roundResults) ? roundResults : [],
      status: "finished",
      finishedAt: admin.firestore.FieldValue.serverTimestamp(),
    }, { merge: true });

    // 통계 업데이트 (참여 모드도 승/패 집계에 반영)
    const myRef = db.collection("users").doc(myUid);
    const oppRef = db.collection("users").doc(oppUid);
    const myWinInc = winner === "my" ? 1 : 0;
    const myLoseInc = winner === "opp" ? 1 : 0;
    const myDrawInc = winner === "draw" ? 1 : 0;

    const batch = db.batch();
    batch.set(myRef, {
      battleWins: admin.firestore.FieldValue.increment(myWinInc),
      battleLosses: admin.firestore.FieldValue.increment(myLoseInc),
      battleDraws: admin.firestore.FieldValue.increment(myDrawInc),
      weeklyBattleWins: admin.firestore.FieldValue.increment(myWinInc),
    }, { merge: true });
    batch.set(oppRef, {
      battleWins: admin.firestore.FieldValue.increment(myLoseInc),
      battleLosses: admin.firestore.FieldValue.increment(myWinInc),
      battleDraws: admin.firestore.FieldValue.increment(myDrawInc),
      weeklyBattleWins: admin.firestore.FieldValue.increment(myLoseInc),
    }, { merge: true });
    await batch.commit();

    res.json({ ok: true, winner });
  } catch (error) {
    console.error("submitInteractiveResult error:", error);
    res.status(500).json({ error: "결과 저장 실패: " + error.message });
  }
});
