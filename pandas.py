import pandas as pd
import sqlite3

# 連接到 SQLite 資料庫
conn = sqlite3.connect('codinghere-20240208.db')

# 建立一個游標物件
cursor = conn.cursor()

# 查詢數據
cursor.execute('''
        SELECT *
        FROM exams
        JOIN users
        WHERE users.name = '温彥丞';
''')


rows = cursor.fetchall()

# 輸出查詢結果
for row in rows:
    print(row)

# 關閉連接
conn.close()