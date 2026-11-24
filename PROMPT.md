# ChatGPT 工單重現

將 evidence.json 與下列提示詞一併提供給 ChatGPT。將回覆另存為 UTF-8 的 tickets.tsv，不含表頭。

## 提示詞

針對附件的每個案例生成一行 TSV。依序輸出 id、decision、issues、行動代碼、繁體中文摘要，五欄以真正的 Tab 分隔。維持資料中的 id 和 decision，列出全部 issues，以逗號相連。沒有 issues 時輸出 -，行動為 ARCHIVE。相同行動只列一次，多項行動以逗號相連。

| 異常 | 行動 | 意義 |
|---|---|---|
| RPO | FIND_NEWER | 確認較新復原點 |
| RTO | RETIME | 記錄耗時並重演 |
| HASH | RECOPY | 取得另一份副本 |
| SQL | RECHECK_DB | 重做資料庫完整性檢查 |
| COUNT 或 SUM | RECONCILE | 與截點清冊對帳 |
| MISSING | LOCATE_COPY | 查明備份交付位置 |
| TIME_UNKNOWN | GET_TIMESTAMP | 補交含時區的時間戳記 |
| JOB_WARN | REVIEW_WARNING | 查核備份工作警告 |

摘要根據該案例的欄位寫出異常依據及待辦。復原點的上限為 240 分鐘，演練耗時上限為 30 分鐘。100 筆、50,500 為業務基準。時間欄位屬情境輸入。遇到缺漏請註明待補資料。輸出 12 行純文字，不加 Markdown 或說明文字。
