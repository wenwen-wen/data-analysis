import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# 連接到 SQLite 資料庫
conn = sqlite3.connect('codinghere-20240208.db')

# 建立一個游標物件
cursor = conn.cursor()

#查詢數據
cursor.execute('''
SELECT 
    CASE       
        WHEN courseid = 'C000001' THEN '110-王老師計概一甲(1)'
        WHEN courseid = 'C000002' THEN '110-王老師計概一乙(1)'
        WHEN courseid = 'C000003' THEN '110-王老師運算思維與程式設計'
        WHEN courseid = 'C000005' THEN '110-王老師計概一甲(2)'
        WHEN courseid = 'C000006' THEN '110-王老師計概一乙(2)'
        WHEN courseid = 'C000009' THEN '111-王老師計概一甲(1)'
        WHEN courseid = 'C000010' THEN '111-王老師計概一乙(1)'
        WHEN courseid = 'C000011' THEN '111-王老師運算思維與程式設計'
        WHEN courseid = 'C000015' THEN '111-王老師計概一甲(2)'
        WHEN courseid = 'C000016' THEN '111-王老師計概一乙(2)'
        WHEN courseid = 'C000018' THEN '112-王老師計概一甲(1)'
        WHEN courseid = 'C000019' THEN '112-王老師計概一乙(1)'
        WHEN courseid = 'C000020' THEN '112-王老師運算思維與程式設計'
           ELSE 'Default Name'
           END AS custom_cid_name, 
    examname,
    SUBSTR(submits, 1, INSTR(submits, '#') - 1) AS problem,
    CAST(SUBSTR(submits, INSTR(submits, '#') + 1) AS INTEGER) AS time
FROM answers
    JOIN users ON answers.userid = users.fid
WHERE 
    courseid IN ('C000001', 'C000002' )
    AND examname IN ('0418期中考', '乙班期中測驗', '乙班期末測驗', 
        '期中測驗', '期末測驗', '期末考', '甲班期中測驗', '甲班期末測驗')
GROUP BY courseid, examname, problem, time
                ''')


rows = cursor.fetchall()

# 輸出查詢結果
for row in rows:
    print(row)

# 關閉連接
conn.close()

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 替換成你的中文字體，如微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# SQL 查詢结果
data = [
    ('110-王老師計概一甲(1)', '甲班期中測驗', 'BASE022', 130),
    
]

# 分組資料
class_a_midterm = [(d[2], d[3]) for d in data if d[1] == '甲班期中測驗']
class_a_final = [(d[2], d[3]) for d in data if d[1] == '甲班期末測驗']
class_b_midterm = [(d[2], d[3]) for d in data if d[1] == '乙班期中測驗']
class_b_final = [(d[2], d[3]) for d in data if d[1] == '乙班期末測驗']

# 繪製散點圖
plt.figure(figsize=(10, 6))  # 設定圖表大小

plt.scatter(*zip(*class_a_midterm), label='甲班期中考', color='blue', marker='o')
plt.scatter(*zip(*class_a_final), label='甲班期末考', color='green', marker='^')
plt.scatter(*zip(*class_b_midterm), label='乙班期中考', color='red', marker='s')
plt.scatter(*zip(*class_b_final), label='乙班期末考', color='orange', marker='x')

plt.xlabel('考試題目')
plt.ylabel('作答時間 (秒)')
plt.title('110-王老師計概一甲(1) 和 110-王老師計概一乙(1) 期中期末考考試題目及作答時間(秒)')
plt.legend(loc='upper center', bbox_to_anchor=(1.06, 1))
plt.grid(True)  # 添加網格線
plt.show()