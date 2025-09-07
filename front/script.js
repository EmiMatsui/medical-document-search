// ★ ここをあなたの ngrok 公開URLに変更（末尾 / は不要）
// script.js の先頭
const API_BASE = window.API_BASE || "http://127.0.0.1:8000";


// ドラッグ＆ドロップ
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const pickBtn = document.getElementById("pickBtn");
const uploadResult = document.getElementById("uploadResult");

pickBtn?.addEventListener("click", () => fileInput.click());
fileInput?.addEventListener("change", () => {
  if (fileInput.files?.length) uploadFiles(fileInput.files);
});
["dragenter", "dragover"].forEach(ev =>
  dropZone?.addEventListener(ev, e => {
    e.preventDefault(); e.stopPropagation(); dropZone.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach(ev =>
  dropZone?.addEventListener(ev, e => {
    e.preventDefault(); e.stopPropagation();
    if (ev === "drop") {
      const files = e.dataTransfer?.files;
      if (files && files.length) uploadFiles(files);
    }
    dropZone.classList.remove("dragover");
  })
);

async function uploadFiles(fileList) {
  uploadResult.textContent = "アップロード中…";
  const formData = new FormData();
  [...fileList].forEach(f => formData.append("files", f)); // ←キー名は必ず "files"

  try {
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });

    // 失敗時はボディを文字列で読む（詳細を見る）
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Upload failed: ${res.status} - ${text}`);
    }

    const data = await res.json();
    const lines = (data.uploaded || []).map(u => `・#${u.id} ${u.original_name} (${u.size_bytes} bytes)`);
    uploadResult.innerHTML = ["✅ アップロード完了:", ...lines].join("<br>");
  } catch (e) {
    console.error(e);
    uploadResult.innerHTML = `<span style="color:red;">エラー: ${e.message}</span>`;
  }
}

