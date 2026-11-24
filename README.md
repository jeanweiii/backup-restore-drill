# AI 輔助備份還原演練

本專案以 12 組模擬案例執行 SQLite 備份還原與驗證，對應 ISO/IEC 27001:2022 附錄 A.8.13。

## 實作流程

使用 Python 3.9 以上，在專案目錄執行 `python drill.py` 產生還原證據，再執行 `python check.py` 核對 `tickets.tsv`。`PROMPT.md` 說明如何用 ChatGPT 重新草擬工單。`sample/` 提供範例輸出。
