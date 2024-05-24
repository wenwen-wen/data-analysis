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
    submits.cid IN ('C000011', 'C000020')
    AND  SUBSTR(submits.time_id, 1, 4) || '-' || SUBSTR(submits.time_id, 5, 2) || '-' || SUBSTR(submits.time_id, 7, 2)  
               BETWEEN '2022-09-14' AND '2023-11-21'            
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
    ('C000011', '1', 220, 150.49545454545455),
    ('C000011', '2', 29, 72.55172413793103),
    ('C000011', '3', 12, 35.416666666666664),
    ('C000011', '4', 1473, 513.7569585879158),
    ('C000011', '5', 2171, 739.8507600184247),
    ('C000011', '6', 1538, 557.9785435630689),
    ('C000011', '7', 2130, 933.4868544600939),
    ('C000011', '8', 1982, 605.1140262361251),
    ('C000011', '9', 5304, 273.2535822021116),
    ('C000011', '10', 171, 272.5263157894737),
    ('C000020', '1', 85, 52.082352941176474),
    ('C000020', '2', 7, 77.71428571428571),
    ('C000020', '3', 538, 640.8494423791822),
    ('C000020', '4', 989, 594.7108190091001),
    ('C000020', '5', 1141, 378.4233128834356),
    ('C000020', '6', 923, 383.49837486457204),
    ('C000020', '7', 1714, 314.10618436406065),
    ('C000020', '8', 4141, 243.96860661675925),
    ('C000020', '9', 289, 421.3356401384083),
    ('C000020', '10', 437, 359.72768878718534),
]

# 準備數據
class1_data = [(row[2], row[3]) for row in data if row[0] == 'C000011']
class2_data = [(row[2], row[3]) for row in data if row[0] == 'C000020']

class1_submissions, class1_average_time = zip(*class1_data)
class2_submissions, class2_average_time = zip(*class2_data)

weeks = range(1, 11)  # 假設一學期有18週

# 創建圖表
fig, ax1 = plt.subplots(figsize=(12, 6))

# 提交次數的柱狀圖
bar_width = 0.35
bar1 = ax1.bar(weeks, class1_submissions, bar_width, label='111-王老師運算思維與程式設計', color='skyblue')
bar2 = ax1.bar([x + bar_width for x in weeks], class2_submissions, bar_width, label='112-王老師運算思維與程式設計', color='lightcoral')
plt.xlabel('週')

# 平均時間的折線圖
ax2 = ax1.twinx()
line1, = ax2.plot(weeks, class1_average_time, label='111-王老師運算思維與程式設計', marker='o', color='blue')
line2, = ax2.plot(weeks, class2_average_time, label='112-王老師運算思維與程式設計', marker='o', color='red')

# 添加標籤和標題
ax1.set_ylabel('提交次數')
ax2.set_ylabel('平均時間(秒)')
plt.title('111-王老師運算思維與程式設計 和 112-王老師運算思維與程式設計 每週提交次數和平均時間(秒)')

# 旋轉x軸標籤以便於閱讀
plt.xticks(weeks)
plt.xticks(rotation=45)

# 添加圖例
lines = [bar1, bar2, line1, line2]
labels = [l.get_label() for l in lines]
plt.legend(lines, labels, loc='upper left')

# 顯示圖表
plt.tight_layout()
plt.show()
