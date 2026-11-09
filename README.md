# 國民法官新手村

用白話說明《國民法官法》的靜態網站，條文來自全國法規資料庫官方版本（民國 109 年 8 月 12 日公布）。學習用途，不是法律意見。

- 網站：啟用 GitHub Pages 後的網址（Settings → Pages → Deploy from a branch → main / root）
- 維護規則：見 [AGENTS.md](AGENTS.md)
- 條文核對：`python tools/check_quotes.py`
- 本機預覽：`python -m http.server`，再開啟 http://localhost:8000

這個儲存庫另外放有 RAG 作業用的 `rag-data.zip` 與 `vector_embedding.zip`。
