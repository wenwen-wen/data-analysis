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

results = cursor.fetchall()

# 從查詢結果中分離數據
courses = [row[0] for row in results]
submissions = [row[1] for row in results]
avg_times = [row[2] for row in results]

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 替換成你的中文字體，如微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 建立圖表
fig, ax1 = plt.subplots(figsize=(12, 7))

# 繪製柱狀圖 (提交次數)
bars = ax1.bar(courses, submissions, color='skyblue', label='提交次數')
ax1.set_xlabel('課程名稱')
ax1.set_ylabel('提交次數')
ax1.tick_params(axis='y')
plt.xticks(rotation=90)

# 在柱狀圖上顯示提交次數
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height,
             f'{height:.0f}', ha='center', va='bottom', fontsize=8)
    
# 建立第二個 y 軸 (平均時間)
ax2 = ax1.twinx()
ax2.plot(courses, avg_times, color='coral', marker='o', linestyle='-', label='平均時間')
ax2.set_ylabel('平均時間(秒)')
ax2.tick_params(axis='y',)

# 在折線圖上顯示平均時間
for i, txt in enumerate(avg_times):
    ax2.annotate(f'{txt:.1f}', (courses[i], avg_times[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# 圖表標題和圖例
plt.title('每門課程的提交次數與平均時間(秒)')
fig.legend(loc="upper right", bbox_to_anchor=(0.93,0.95))

# 顯示圖表
plt.tight_layout()
plt.show()

# 關閉連接
conn.close()