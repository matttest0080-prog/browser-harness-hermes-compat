# Browser Harness — Hermes 獨立相容性發行版

這是 `matttest0080-prog` 維護的獨立相容性 fork，**不是 Browser Use 官方發行版**。PyPI 專案名稱為 **`browser-harness-hermes-compat`**，版本 `0.1.13.post1`；是否已發布應以 PyPI 的實際版本與 artifacts 為準，不以這份文件或尚未執行的 workflow 當成發布證據。

## 來源與授權

- 原始來源：browser-use/browser-harness `v0.1.13`，commit `c24e5072ee66f8499bacd663f4f4bcb089bc4492`。
- 保留 Browser Use 原始 MIT License（Copyright 2026 Browser Use）、上游 README 內容、技能名稱與來源署名。
- Python import 仍為 `browser_harness`；CLI 仍為 `browser-harness`／`browser-harness-mcp`；skill identity 仍為 `browser-use`。只有 distribution 名稱改成獨立 namespace，不能把它當成官方 `browser-harness` 的新版。
- Pillow 12.3.0 → 13.0.0，修補公開 critical `GHSA-8g5g-8vmr-9782`；可選 MCP 2.1.1 → 2.3.0，與 Hermes 已審查的安全版本一致。建置 backend 固定已修補的 setuptools 84.1.0。
- 瀏覽器操作／daemon／IPC 實作不變。為了正確的發行身份，版本讀取、PyPI 查詢、`uv tool upgrade`、更新快取及 MCP 安裝提示改指向本獨立 distribution，避免更新時誤裝官方舊版。沒有偽造官方 METADATA。
- 舊的 GitHub-only `v0.1.13.post1`／commit `f387133ecc9561128d18eabc4af6df143b2560d5` 仍是原 artifact，名稱為 `browser-harness`、wheel SHA256 `63a2fb36e398d8a764fb5961a70f0deb63dc60472ff0345b739105d17e2e059e`。不覆寫舊 tag／artifact；新的 PyPI 發行使用獨立 `pypi-v0.1.13.post1` tag 與新 distribution 名稱。

## 安裝與遷移

本套件與官方套件提供相同 import／CLI 檔案，**不要在同一個環境同時安裝兩個 distribution**。尤其不能先安裝新版、再移除舊版：pip 移除舊套件可能刪到同名模組或 CLI。

建議使用新的隔離環境，保留既有可用環境與服務：

```sh
python3 -m venv ~/.venvs/browser-harness-hermes-compat
~/.venvs/browser-harness-hermes-compat/bin/python -m pip install 'browser-harness-hermes-compat[mcp]==0.1.13.post1'
~/.venvs/browser-harness-hermes-compat/bin/python -m pip check
~/.venvs/browser-harness-hermes-compat/bin/browser-harness --version
```

若明確選擇在自己的 disposable 環境遷移，順序為先移除官方 `browser-harness`，再正常安裝本套件與執行 `pip check`；不使用 `--no-deps`、忽略錯誤或修改已建 wheel 的 METADATA。

## CI 與發布

- `.github/workflows/release.yml`：Python 3.11–3.14 的完整上游單元測試、Pillow JPEG／contact sheet／mask 正負控、獨立 distribution 查詢與 updater namespace 控制；以真實 wheel 安裝、`pip check`、實際 import 路徑、`twine check --strict` 及同 epoch wheel byte-identical 重建驗證。
- `.github/workflows/publish-pypi.yml`：只接受 `pypi-v*`，先驗證獨立專案名、相符版本、annotated tag 及預設維護分支 ancestry。全部四組 CI 成功後，只發布 CI 建出的 3.11 wheel／sdist；不在 publish job 重建或重寫 metadata。
- Publish job 獨享 `id-token: write`，使用 `pypi` environment 與 PyPI Trusted Publishing；無長期 PyPI token。CI build／PR 不取得發布憑證。
- PyPI 帳號的 Pending Publisher 設定：project `browser-harness-hermes-compat`、owner `matttest0080-prog`、repo `browser-harness-hermes-compat`、workflow `publish-pypi.yml`、environment `pypi`。入口：https://pypi.org/manage/account/publishing/ 。設定應由帳號擁有人完成，不將 token、密碼或 2FA 碼貼入 issue、PR 或聊天。

上述驗證不等於真實 Chrome／Browser Use Cloud、模型品質、全部作業系統或長期負載驗收。Hermes 與 Pi 2 的 registry 安裝、舊版遷移及五組鎖檔需在消費端另外驗證。

官方日後若發布與安全 Pillow 相容的正式 artifact，應重新審查是否回歸官方 distribution，避免永久維護不必要的 fork。
