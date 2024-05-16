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
        WHEN cid = 'C000001' THEN '110-王老師計概一甲(1)'
        WHEN cid = 'C000002' THEN '110-王老師計概一乙(1)'
        WHEN cid = 'C000003' THEN '110-王老師運算思維與程式設計'
        WHEN cid = 'C000004' THEN '課程檢定'
        WHEN cid = 'C000005' THEN '110-王老師計概一甲(2)'
        WHEN cid = 'C000006' THEN '110-王老師計概一乙(2)'
        WHEN cid = 'C000007' THEN '翁老師計概一甲(1)'
        WHEN cid = 'C000008' THEN '翁老師計概一乙(1)'
        WHEN cid = 'C000009' THEN '111-王老師計概一甲(1)'
        WHEN cid = 'C000010' THEN '111-王老師計概一乙(1)'
        WHEN cid = 'C000011' THEN '111-王老師運算思維與程式設計'
        WHEN cid = 'C000012' THEN '黃老師運算思維與程式設計'
        WHEN cid = 'C000013' THEN '翁老師計概一甲(2)'
        WHEN cid = 'C000014' THEN '翁老師計概一乙(2)'
        WHEN cid = 'C000015' THEN '111-王老師計概一甲(2)'
        WHEN cid = 'C000016' THEN '111-王老師計概一乙(2)'
        WHEN cid = 'C000017' THEN '李老師計概一甲(1)'
        WHEN cid = 'C000018' THEN '112-王老師計概一甲(1)'
        WHEN cid = 'C000019' THEN '112-王老師計概一乙(1)'
        WHEN cid = 'C000020' THEN '112-王老師運算思維與程式設計'
        WHEN cid = 'playground' THEN 'playground'
        WHEN cid = 'C000021' THEN '112-王老師計概一甲(2)'
        WHEN cid = 'C000022' THEN '112-王老師計概一甲(2)'
        ELSE 'Default Name'
    END AS custom_cid_name, 
               COUNT(*) AS num_submissions, 
               AVG(time_pt) AS avg_time
               FROM submits
               WHERE time_pt IS NOT NULL
               GROUP BY cid;                                       
''')

# 提取結果中的課程 ID 和提交次數
submission_results = cursor.fetchall()
cid_submission = [result[0] for result in submission_results]
num_submissions = [result[1] for result in submission_results]

# 查詢平均時間
cursor.execute('''
    SELECT  CASE
        WHEN cid = 'C000001' THEN '110-王老師計概一甲(1)'
        WHEN cid = 'C000002' THEN '110-王老師計概一乙(1)'
        WHEN cid = 'C000003' THEN '110-王老師運算思維與程式設計'
        WHEN cid = 'C000004' THEN '課程檢定'
        WHEN cid = 'C000005' THEN '110-王老師計概一甲(2)'
        WHEN cid = 'C000006' THEN '110-王老師計概一乙(2)'
        WHEN cid = 'C000007' THEN '翁老師計概一甲(1)'
        WHEN cid = 'C000008' THEN '翁老師計概一乙(1)'
        WHEN cid = 'C000009' THEN '111-王老師計概一甲(1)'
        WHEN cid = 'C000010' THEN '111-王老師計概一乙(1)'
        WHEN cid = 'C000011' THEN '111-王老師運算思維與程式設計'
        WHEN cid = 'C000012' THEN '黃老師運算思維與程式設計'
        WHEN cid = 'C000013' THEN '翁老師計概一甲(2)'
        WHEN cid = 'C000014' THEN '翁老師計概一乙(2)'
        WHEN cid = 'C000015' THEN '111-王老師計概一甲(2)'
        WHEN cid = 'C000016' THEN '111-王老師計概一乙(2)'
        WHEN cid = 'C000017' THEN '李老師計概一甲(1)'
        WHEN cid = 'C000018' THEN '112-王老師計概一甲(1)'
        WHEN cid = 'C000019' THEN '112-王老師計概一乙(1)'
        WHEN cid = 'C000020' THEN '112-王老師運算思維與程式設計'
        WHEN cid = 'playground' THEN 'playground'
        WHEN cid = 'C000021' THEN '112-王老師計概一甲(2)'
        WHEN cid = 'C000022' THEN '112-王老師計概一甲(2)'
        ELSE 'Default Name'
    END AS custom_cid_name,  
            AVG(time_pt) AS avg_time
    FROM submits
    WHERE time_pt IS NOT NULL
    GROUP BY cid;
''')

# 提取結果中的課程 ID 和平均時間
time_results = cursor.fetchall()
cid_time = [result[0] for result in time_results]
avg_times = [result[1] for result in time_results]

# 關閉連接
conn.close()

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 替換成你的中文字體，如微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 視覺化提交次數和平均時間
plt.figure(figsize=(12, 7))

# 提交次數
plt.bar(cid_submission, num_submissions, color='skyblue', label='提交次數')
plt.xlabel('課程名稱')
plt.ylabel('提交次數')
plt.title('每門課程的提交次數及平均時間')

plt.xticks(rotation=90)
plt.tight_layout()
plt.legend(loc='upper right', bbox_to_anchor=(1, 1))

# 在每個柱子上方加入提交次數標籤
for i in range(len(cid_submission)):
    plt.text(cid_submission[i], num_submissions[i] + 0.1, str(num_submissions[i]), ha='center', va='bottom', fontsize=8)

# 創建第二個 y 軸
plt.twinx()
plt.plot(cid_time, avg_times, marker='o', color='orange', label='平均時間')
plt.ylabel('平均時間(秒)')

# 在每個點上方加入提交次數標籤
for i in range(len(cid_time)):
    plt.text(cid_time[i], avg_times[i] + 0.1, f"{avg_times[i]:.2f}",ha='center', va='top', fontsize=8)

plt.legend(loc='upper right', bbox_to_anchor=(1, 0.9))

plt.tight_layout()
plt.show()