# Week2
* [specdata 資料夾底下內容請從課程網站下載](https://class.coursera.org/rprog-032/assignment/view?assignment_id=3)

## 常見問題
0.Error in read.table(file = file, header = header, sep = sep, quote = quote,  : 
  找不到物件 'files_full' 
  
  Ans: 可能是還沒下載 specdata



## 交作業的方式
用 command line 的方式的比較快。

* 首先要交作業之前，先 cd 到該作業的目錄。

* 然後開 R
  ```
  source("http://d396qusza40orc.cloudfront.net/rprog%2Fscripts%2Fsubmitscript1.R")
  ```

* 然後 source 你要交的檔案:
  ```
  source("submitscript1.R")
  ```

* 然後送出 
  ```
  submit()
  ```

送出之後會要你填帳號密碼以及課程 id，是正常的。