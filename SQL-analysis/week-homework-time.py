import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# 連接到 SQLite 資料庫
conn = sqlite3.connect('codinghere-20240208.db')

# 建立一個游標物件
cursor = conn.cursor()

data = [
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-09-25', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-10-02', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-10-09', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-10-16', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-10-23', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-10-31', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-11-06', 20],
  ['111-王老師計概一甲(1)', '洪金鋒', '2022-11-07', 20],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-12', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-24', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-25', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-26', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-27', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-09-28', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-03', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-04', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-05', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-07', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-11', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-14', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-17', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-22', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-10-31', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-11-03', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-11-04', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-11-05', 60],
  ['111-王老師計概一甲(1)', '湯光鈞', '2022-11-06', 60],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-09-18', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-09-24', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-10-01', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-10-02', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-10-14', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-10-17', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-10-23', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-11-06', 10],
  ['111-王老師計概一甲(1)', '蔡柏嶙', '2022-11-07', 10],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-12', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-19', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-25', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-26', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-27', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-29', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-09-30', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-06', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-07', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-10', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-13', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-14', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-15', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-16', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-17', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-18', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-19', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-30', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-10-31', 60],
  ['111-王老師計概一甲(1)', '許宇閎', '2022-11-05', 60],
  ['111-王老師計概一甲(1)', '陳奕廷', '2022-09-18', 0],
  ['111-王老師計概一甲(1)', '陳奕廷', '2022-09-25', 0],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-09-12', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-09-19', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-02', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-03', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-16', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-17', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-23', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-10-31', 60],
  ['111-王老師計概一甲(1)', '陳宗岷', '2022-11-06', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-09-12', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-09-19', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-09-26', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-10-03', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-10-04', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-10-11', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-10-17', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-10-31', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-11-04', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-11-05', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-11-06', 60],
  ['111-王老師計概一甲(1)', '陳芊妤（大芊）', '2022-11-07', 60],
  ['111-王老師計概一甲(1)', '魏若安', '2022-09-12', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-09-19', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-09-23', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-09-26', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-10-09', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-10-16', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-10-17', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-10-23', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-10-31', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-11-03', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-11-06', 20],
  ['111-王老師計概一甲(1)', '魏若安', '2022-11-07', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-09-12', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-09-25', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-10-02', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-10-09', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-10-16', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-10-23', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-11-05', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-11-06', 20],
  ['111-王老師計概一甲(1)', '黃為燁', '2022-11-07', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-09-19', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-09-25', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-02', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-09', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-16', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-17', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-22', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-23', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-10-31', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-11-06', 20],
  ['111-王老師計概一甲(1)', '黃聖驊', '2022-11-07', 20]
]

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 替換成你的中文字體，如微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

import matplotlib.dates as mdates
from datetime import datetime

# 建立學生的作答時間字典
student_data = {}
for d in data:
    course, student, date, score = d
    date = datetime.strptime(date, '%Y-%m-%d')
    if student not in student_data:
        student_data[student] = []
    student_data[student].append((date, score))

# 設定圖表大小
plt.figure(figsize=(15, 8))

# 設定 X 軸刻度和標籤
x_ticks = [
    datetime(2022, 9, 12),
    datetime(2022, 9, 19),
    datetime(2022, 9, 26),
    datetime(2022, 10, 3),
    datetime(2022, 10, 10),
    datetime(2022, 10, 17),
    datetime(2022, 10, 24),
    datetime(2022, 10, 31),
    datetime(2022, 11, 7)
]
x_labels = [date.strftime('%m/%d') for date in x_ticks]

# 繪製每一位學生的作答時間分佈圖

for i, (student, dates_scores) in enumerate(student_data.items()):
    dates, scores = zip(*dates_scores)
    colors = ['blue' if score >= 60 else 'red' for score in scores]
    plt.scatter(dates, [i] * len(dates), c=colors, s=30)

# 手動建立高分和低分的圖例物件
plt.scatter([], [], c='blue', s=30, label='高分群')
plt.scatter([], [], c='red', s=30, label='低分群')

# 設定圖表標題和軸標籤
plt.title('高分及低分群學生作業提交時間')
plt.xlabel('上課日期')
# plt.ylabel('學生')

# # 設定 Y 軸刻度和標籤
# plt.yticks(range(len(student_data)), student_data.keys())

# 移除 Y 軸刻度和標籤
plt.yticks([])  #

# 設定 X 軸刻度和格式
plt.xticks(x_ticks, x_labels)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# 顯示圖表
plt.legend(loc="upper right", bbox_to_anchor=(1.1,1))
plt.grid(True)  # 添加網格線
plt.show()
