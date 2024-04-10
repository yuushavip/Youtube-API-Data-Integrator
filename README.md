# Youtube API 資料整合

Youtube 官方說明文件: [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)

使用 python 編寫，透過 Youtube 官方提供的 Web API 抓取資料，並轉成 csv 檔案保存至 `/data` 資料夾，需要先在 GCP 申請 Data API。

`youtube_api.ini`

認證相關設定，需要將 API KEY 輸入在對應的資料欄位中。

`youtube_task.yaml`

可以在 `task_list` 輸入執行目標頻道的 ID，並且自定義 `columns` 與相關參數。

---

# YouTube API Data Integration

**Official YouTube Documentation:** [https://developers.google.com/youtube/v3/getting-started](https://developers.google.com/youtube/v3/getting-started)

This project is written in Python and utilizes the official Youtube API to fetch data, which is then saved as CSV files in the /data folder. A Data API must first be applied for through GCP (Google Cloud Platform).

`youtube_api.ini`

This is for authentication settings. You will need to enter your API KEY in the corresponding field.

`youtube_task.yaml`

You can input the target channel IDs in `task_list` and customize `columns` and other params as needed.
