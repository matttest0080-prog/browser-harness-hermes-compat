# Hermes 相容性發行版

這是 `matttest0080-prog` 維護的獨立相容性 fork，**不是 Browser Use 官方發行版**。

- 原始來源：browser-use/browser-harness `v0.1.13`，commit `c24e5072ee66f8499bacd663f4f4bcb089bc4492`。
- 保留原始程式、README、技能名稱與 MIT License（Copyright 2026 Browser Use）。
- 套件識別版本改為 `0.1.13.post1`，以免和原始 0.1.13 的 artifact 混淆。
- 唯一執行相依變更：Pillow 12.3.0 → 13.0.0（修補公開 critical GHSA-8g5g-8vmr-9782）；可選 MCP 2.1.1 → 2.3.0，與 Hermes 已審查的安全版本一致。
- 未修改 `src/` 的瀏覽器操作／daemon／IPC 實作；新增相容性測試、來源紀錄及只讀 CI。
- 上游 PyPI publisher 已改為相容性驗證 workflow；此 fork 不上傳 PyPI。GitHub release 提供 wheel、sdist、SHA256SUMS；消費端必須固定 artifact URL 與 SHA256，而非追蹤浮動 branch。

驗證包含 Python 3.11–3.14 的完整上游單元測試、Pillow JPEG 解碼／縮圖／遮罩、已安裝 wheel 的版本與 pip check，以及重建 wheel 的雜湊一致性。這些不等於真實 Chrome／Browser Use Cloud、模型品質或長期負載驗證。

待官方發行版可與安全 Pillow 相容後，應重新審查是否回歸官方 artifact，避免永久維護不必要的 fork。
