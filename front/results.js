// ★ ここをあなたの ngrok 公開URLに変更（末尾 / は不要）
// results.js の先頭
const API_BASE = window.API_BASE || "http://127.0.0.1:8000";


const params = new URLSearchParams(location.search);
const q = params.get("q") || "";
const k = parseInt(params.get("k") || "4", 10);

const refinedEl = document.getElementById("refinedQuery");
const container = document.getElementById("resultsContainer");

(async () => {
  if (!q) {
    refinedEl.textContent = "クエリが指定されていません。";
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, k })
    });
    if (!res.ok) throw new Error(`API Error: ${res.status}`);

    const data = await res.json();
    refinedEl.textContent = data.refined_query || "(なし)";

    if (!data.results || !data.results.length) {
      container.textContent = "一致するドキュメントはありませんでした。";
      return;
    }
    container.innerHTML = data.results.map((r, i) => {
      const name = r["ファイル名"] || "";
      const dist = r["距離"] ?? "";
      const summary = (r["要約"] || "").replace(/\n/g, "<br>");
      return `
        <div class="result-card">
          <h4>${i + 1}. ${name}</h4>
          <div class="meta">距離: ${dist}</div>
          <div class="summary">${summary}</div>
        </div>
      `;
    }).join("");
  } catch (e) {
    refinedEl.textContent = "取得に失敗しました。";
    container.textContent = e.message;
    console.error(e);
  }
})();
