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
    submits.cid,
    STRFTIME('%W', SUBSTR(submits.time_id, 1, 4) || '-' || SUBSTR(submits.time_id, 5, 2) || '-' || SUBSTR(submits.time_id, 7, 2))  AS week_number,
    COUNT(*) AS submit_count,
    AVG(submits.time_pt) AS average_time
FROM
    submits
JOIN
    courses ON submits.cid = courses.fid
WHERE
    submits.cid IN ('C000018', 'C000019')
    AND  SUBSTR(submits.time_id, 1, 4) || '-' || SUBSTR(submits.time_id, 5, 2) || '-' || SUBSTR(submits.time_id, 7, 2)  
               BETWEEN '2023-09-11' AND '2024-01-09'              
GROUP BY
    submits.cid, week_number
ORDER BY
    submits.cid, week_number;
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
    ('C000018', '1', 4083, 464.1092334068087),
    ('C000018', '2', 1601, 390.33104309806373),
    ('C000018', '3', 348, 251.06896551724137),
    ('C000018', '4', 879, 435.26962457337885),
    ('C000018', '5', 1381, 679.5749456915279),
    ('C000018', '6', 1631, 803.3053341508277),
    ('C000018', '7', 2674, 733.376215407629),
    ('C000018', '8', 2607, 500.1933256616801),
    ('C000018', '9', 2097, 589.0324272770624),
    ('C000018', '10', 2687, 732.6382582806103),
    ('C000018', '11', 3147, 451.31998728948207),
    ('C000018', '12', 1518, 521.0237154150198),
    ('C000018', '13', 1739, 704.8447383553766),
    ('C000018', '14', 1207, 919.36454018227),
    ('C000018', '15', 209, 424.88516746411483),
    ('C000018', '16', 1427, 863.0665732305536),
    ('C000018', '17', 123, 203.5121951219512),
    ('C000018', '18', 1272, 1427.2185534591194),
    ('C000019', '1', 3096, 493.0439276485788),
    ('C000019', '2', 6383, 401.7642174526085),
    ('C000019', '3', 220, 217.1590909090909),
    ('C000019', '4', 1035, 353.0782608695652),
    ('C000019', '5', 1494, 607.8908969210174),
    ('C000019', '6', 2434, 843.6552999178307),
    ('C000019', '7', 2757, 723.4022488211824),
    ('C000019', '8', 3265, 653.6548238897396),
    ('C000019', '9', 1991, 670.6775489703666),
    ('C000019', '10', 3394, 570.6373011196229),
    ('C000019', '11', 3419, 491.95232524129864),
    ('C000019', '12', 5780, 320.6640138408305),
    ('C000019', '13', 2006, 731.8888334995015),
    ('C000019', '14', 1426, 828.8920056100982),
    ('C000019', '15', 66, 660.4242424242424),
    ('C000019', '16', 1431, 722.0335429769392),
    ('C000019', '17', 179, 452.6927374301676),
    ('C000019', '18', 1228, 1226.200325732899),
]

# 準備數據
class1_data = [(row[2], row[3]) for row in data if row[0] == 'C000018']
class2_data = [(row[2], row[3]) for row in data if row[0] == 'C000019']

class1_submissions, class1_average_time = zip(*class1_data)
class2_submissions, class2_average_time = zip(*class2_data)

weeks = range(1, 19)  # 假設一學期有18週

# 創建圖表
fig, ax1 = plt.subplots(figsize=(12, 6))

# 提交次數的柱狀圖
bar_width = 0.35
bar1 = ax1.bar(weeks, class1_submissions, bar_width, label='112-王老師計概一甲(1)提交次數', color='skyblue')
bar2 = ax1.bar([x + bar_width for x in weeks], class2_submissions, bar_width, label='112-王老師計概一乙(1)提交次數', color='lightcoral')
plt.xlabel('週')

# 平均時間的折線圖
ax2 = ax1.twinx()
line1, = ax2.plot(weeks, class1_average_time, label='112-王老師計概一甲(1)平均時間', marker='o', color='blue')
line2, = ax2.plot(weeks, class2_average_time, label='112-王老師計概一乙(1)平均時間', marker='o', color='red')

# 添加標籤和標題
ax1.set_ylabel('提交次數')
ax2.set_ylabel('平均時間(秒)')
plt.title('112-王老師計概一甲(1) 和 112-王老師計概一乙(1) 每週提交次數和平均時間(秒)')

# 旋轉x軸標籤以便於閱讀
plt.xticks(weeks)
plt.xticks(rotation=45)

# 添加圖例
lines = [bar1, bar2, line1, line2]
labels = [l.get_label() for l in lines]
plt.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.35, 1))

# 顯示圖表
plt.tight_layout()
plt.show()