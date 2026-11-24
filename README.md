# AI 輔助備份還原演練

本 PoC 對應 ISO/IEC 27001:2022 附錄 A.8.13「資訊備份」。使用 12 組虛構的訂單資料實際操作 SQLite 備份、還原、驗證，再由 ChatGPT 依證據草擬工單。

## 檔案

| 檔案 | 用途 |
|---|---|
| drill.py | 建立 12 個案例，執行還原檢查，輸出 JSON 與 CSV |
| check.py | 核對工單的案例、狀態、異常代碼及對應行動 |
| tickets.tsv | 報告所用的 12 筆 AI 工單 |
| PROMPT.md | 使用 ChatGPT 重做工單的操作指引與提示詞 |
| sample/evidence.json | 已驗證的參考證據 |
| sample/evidence.csv | 可用 Excel 開啟的參考證據 |
| sample/run.txt | 實際執行輸出 |

## 實作流程

1. 解壓縮或 clone 專案，在 VS Code 開啟專案資料夾。
2. 開啟終端機並切換至含有 drill.py 的目錄。使用 Python 3.9 以上，只需標準函式庫，無須安裝套件或設定 API 金鑰。
3. 執行以下指令。Windows 若使用 Python Launcher，可把 python 換成 py。Ubuntu 或 WSL 可使用 python3。

   ```sh
   python drill.py
   python check.py
   ```

4. 查看當次產生的 evidence.csv 或 evidence.json。暫存 SQLite 檔案會自動清理。
5. 如需重跑 AI 步驟，依 PROMPT.md 提供本次 evidence.json，再以新工單取代 tickets.tsv 並執行 check.py。建議先備份原始 TSV 以便比對。
6. 人工回查摘要中的數值和處理建議後，再決定分派相關工作。實務環境在修正後應重新演練。

## 判定條件

確認副本存在、還原副本 SHA-256 與備份基準相同，且 SQLite 完整性檢查通過。業務條件為 100 筆訂單、合計 50,500。復原點間隔上限 240 分鐘，演練耗時上限 30 分鐘，等於上限可接受。任一失敗條件判 FAIL。僅缺時間或存在工作警告判 REVIEW。其餘判 PASS。

## 實測結果

| 判定 | 筆數 |
|---|---:|
| PASS | 2 |
| FAIL | 8 |
| REVIEW | 2 |

11 筆顯示備份工作成功的案例中，有 9 筆需處理或複核。12 筆範例工單與 15 個異常代碼通過結構核對。程式檢查結構化欄位，摘要中的數值與語意仍由人工回查。

資料庫建立、備份複製、雜湊與 SQL 查詢皆實際執行。RPO 間隔和 RTO 耗時是情境輸入，用來測試門檻，正式演練應代入實際時間。此 PoC 使用模擬資料。

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [NIST SP 800-34 Rev. 1](https://doi.org/10.6028/NIST.SP.800-34r1)
