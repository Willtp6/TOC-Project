# TOC-Project-2022

## Spotify 音樂搜尋小幫手

### 簡介
* 基於 Spotify Web Api 的搜尋 chat bot 
* 可以記錄並重新設定 Spotify developer 的帳號資訊避免重複輸入
* 刪除、修改以及查看已記錄的帳號資訊
* 有登入紀錄後登入即可直接開始搜尋

### 使用流程說明
 * 需先至 Spotify developer 登入並取得 client ID 及 client secret
 * 輸入 spotify account login 來將資料紀錄，用於搜尋時呼叫 Spotify Web Api
 * 依序輸入 __藝人名、專輯名、歌曲名__ 即可得到30秒的試播以及完整版的連結

### 使用流程範例
![](https://i.imgur.com/FEkuXEg.jpg =x485)![](https://i.imgur.com/73hFvin.jpg =x485)
![](https://i.imgur.com/iIzNMTZ.jpg =x485)![](https://i.imgur.com/VIvHGct.jpg =x485)

### FSM-image
![](https://i.imgur.com/fhNIU5Y.png)