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
        pid,
        COUNT(*) AS num_records,
        AVG(time_pt) AS avg_time,
        CASE 
            WHEN cid = 'C000001' THEN '110-王老師計概一甲(1)'
            WHEN cid = 'C000002' THEN '110-王老師計概一乙(1)'
            WHEN cid = 'C000003' THEN '110-王老師運算思維與程式設計'
            WHEN cid = 'C000005' THEN '110-王老師計概一甲(2)'
            WHEN cid = 'C000006' THEN '110-王老師計概一乙(2)'
            WHEN cid = 'C000009' THEN '111-王老師計概一甲(1)'
            WHEN cid = 'C000010' THEN '111-王老師計概一乙(1)'
            WHEN cid = 'C000011' THEN '111-王老師運算思維與程式設計'
            WHEN cid = 'C000015' THEN '111-王老師計概一甲(2)'
            WHEN cid = 'C000016' THEN '111-王老師計概一乙(2)'
            WHEN cid = 'C000018' THEN '112-王老師計概一甲(1)'
            WHEN cid = 'C000019' THEN '112-王老師計概一乙(1)'
            WHEN cid = 'C000020' THEN '112-王老師運算思維與程式設計'
			
        END AS course_name
    FROM 
        submits
    WHERE 
        time_pt IS NOT NULL
        AND cid IN ('C000001', 'C000002')
    GROUP BY 
        pid, cid;
''')

# 提取查詢結果
rows = cursor.fetchall()

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 替換成你的中文字體，如微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 將結果轉換為 DataFrame
df = pd.DataFrame(rows, columns=['pid', 'num_records', 'avg_time', 'course_name'])

# 將結果按照題目（pid）合併
df_combined = df.groupby(['pid', 'course_name']).agg({'num_records': 'sum', 'avg_time': 'mean'}).reset_index()

# 定義顏色列表，每個課程一個顏色
colors = {'110-王老師計概一甲(1)': 'skyblue', '110-王老師計概一乙(1)': 'lightgreen'}

# 視覺化每一題的提交次數和平均時間
plt.figure(figsize=(12, 6))

# 按課程名稱迭代並繪製散點圖
for course_name, color in colors.items():
    course_data = df_combined[df_combined['course_name'] == course_name]
    plt.scatter(course_data['num_records'], course_data['avg_time'], color=color, label=course_name)

plt.xlabel('提交次數')
plt.ylabel('平均時間')
plt.title('110-王老師計概一甲(1)和110-王老師計概一乙(1)每題提交次數和平均時間')

# 添加圖例
plt.legend()

# 調整圖的外觀
plt.tight_layout()
plt.show()


