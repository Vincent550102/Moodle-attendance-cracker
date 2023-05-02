# Moodle-attendance-cracker
使用前請先確認各服務的合理使用規範
## 如何使用

```
python main.py baseurl [-h] [-c course name] [-s sessid] [-w maxworker]
```
(-c 和 -s 擇一填寫)

example:
- 已知課程名稱(moodle 上顯示的名稱)
    ```
    python main.py https://moodle.ncku.edu.tw/mod/attendance/attendance.php -c "窩不想上課 (二)"
    ```
- 已知課程ID
    ```
    python main.py https://moodle.ncku.edu.tw/mod/attendance/attendance.php -c 1112_Z99999_1 
    ```
- 已知 sessid
    ```
    python main.py https://moodle.ncku.edu.tw/mod/attendance/attendance.php -s 200000
    ```

## 使用影片

TODO

