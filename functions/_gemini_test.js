require('dotenv').config({ path: '/sessions/stoic-trusting-brahmagupta/mnt/bookquest/functions/.env' });
const { GoogleGenerativeAI } = require('@google/generative-ai');

(async () => {
  try {
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash",
      generationConfig: { responseMimeType: "application/json", temperature: 0.8, maxOutputTokens: 500 }
    });
    const r = await model.generateContent('JSON 한 덩어리로만 답해: {"hello": "world", "model": "gemini-2.5-flash", "status": "ok"}');
    console.log('=== 응답 ===');
    console.log(r.response.text());
    console.log('=== usage ===');
    console.log(JSON.stringify(r.response.usageMetadata, null, 2));
  } catch (e) {
    console.error('❌ ERROR:', e.message);
  }
})();
