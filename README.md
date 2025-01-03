### XML Generator
- XML 產生器的設計我透過 python 的 Flask 套件寫了一個網頁來實作，網頁上包含了兩個檔案上傳的地方，可以上傳 txt 或是 csv 檔。
- 實作上，我利用了 python 的 `xml.etree.ElementTree` 來將**讀取的檔案內容轉換成 xml 的格式並產生一個 xml 檔案。**
- 操作上，使用者上傳檔案後，可以選擇檔案是透過什麼東西來做分隔（例如 `，` `.` `,` ，預設是使用`，`），選擇完後只要按下 **Generate XML 的按鈕**就可以產生 xml 檔案，這個檔案會被儲存在 **upload/ 的資料夾**裡，我也有提供一個按鈕**讓使用者將檔案手動下載到預設的下載目錄裡**。
  - 檔案產生後底下會有生成出的 xml 檔案的內容預覽。
- 兩個上傳的地方，左邊的那個是會給予生成的 xml 檔案已經設定好的 tag 和 attribute name，右邊的則是會自動依據上傳的檔案內容來生成 tag 和 attribute。
- 我使用的範例 txt 檔如下：
  ```txt
  0001，微積分，參考書，王大明，350
  0002，流浪狗太郎的故事，小說，遠藤初江，200
  0003，線性代數，教科書，李四，400
  ```

### How to use
- 在跟 `xml-generator.py` 同一目錄底下，執行以下指令
    `python xml-generator.py`，即可使用，必須確保環境中有 python


### 實作畫面
初始畫面如下：

![image](https://github.com/SunGj921028/xml-generator/blob/main/img/fig1.png)

- 使用左邊上傳，結果如下：

![image](https://github.com/SunGj921028/xml-generator/blob/main/img/fig2.png)

- 產生的 xml 檔案如下：

![image](https://github.com/SunGj921028/xml-generator/blob/main/img/fig3.png)

- 使用右邊上傳，結果如下：

![image](https://github.com/SunGj921028/xml-generator/blob/main/img/fig4.png)

- 產生的 xml 檔案如下：

![image](https://github.com/SunGj921028/xml-generator/blob/main/img/fig5.png)


