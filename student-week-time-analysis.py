import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# 連接到 SQLite 資料庫
conn = sqlite3.connect('codinghere-20240208.db')

# 建立一個游標物件
cursor = conn.cursor()

# 查詢數據
cursor.execute('''
SELECT
    CASE       
        WHEN submits.cid = 'C000001' THEN '110-王老師計概一甲(1)'
        WHEN submits.cid = 'C000002' THEN '110-王老師計概一乙(1)'
        WHEN submits.cid = 'C000003' THEN '110-王老師運算思維與程式設計'
        WHEN submits.cid = 'C000005' THEN '110-王老師計概一甲(2)'
        WHEN submits.cid = 'C000006' THEN '110-王老師計概一乙(2)'
        WHEN submits.cid = 'C000009' THEN '111-王老師計概一甲(1)'
        WHEN submits.cid = 'C000010' THEN '111-王老師計概一乙(1)'
        WHEN submits.cid = 'C000011' THEN '111-王老師運算思維與程式設計'
        WHEN submits.cid = 'C000015' THEN '111-王老師計概一甲(2)'
        WHEN submits.cid = 'C000016' THEN '111-王老師計概一乙(2)'
        WHEN submits.cid = 'C000018' THEN '112-王老師計概一甲(1)'
        WHEN submits.cid = 'C000019' THEN '112-王老師計概一乙(1)'
        WHEN submits.cid = 'C000020' THEN '112-王老師運算思維與程式設計'
           ELSE 'Default Name'
           END AS custom_cid_name,
    users.name,
    STRFTIME('%Y-%m-%d', SUBSTR(submits.time_id, 1, 4) || '-' || SUBSTR(submits.time_id, 5, 2) || '-' || SUBSTR(submits.time_id, 7, 2))  AS week_number,
    AVG(submits.time_pt) AS average_time
FROM
    submits
JOIN
    users ON submits.uid = users.fid
JOIN
    courses ON submits.cid = courses.fid
WHERE
    submits.cid IN ('C000020')
    AND  SUBSTR(submits.time_id, 1, 4) || '-' || SUBSTR(submits.time_id, 5, 2) || '-' || SUBSTR(submits.time_id, 7, 2)  
               BETWEEN '2023-09-20' AND '2023-11-08'          
GROUP BY
    submits.cid, users.name;

''')

rows = cursor.fetchall()

# 輸出查詢結果
for row in rows:
    print(row)

# 關閉連接
conn.close()


