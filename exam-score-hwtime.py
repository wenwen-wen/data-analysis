import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import argparse

coursemap = {
    '110-王老師計概一甲(1)': 'C000001',
    '110-王老師計概一乙(1)': 'C000002',
    '110-王老師運算思維與程式設計': 'C000003',
    '110-王老師計概一甲(2)': 'C000005',
    '110-王老師計概一乙(2)': 'C000006',
    '111-王老師計概一甲(1)': 'C000009',
    '111-王老師計概一乙(1)': 'C000010',
    '111-王老師運算思維與程式設計': 'C000011',
    '111-王老師計概一甲(2)': 'C000015',
    '111-王老師計概一乙(2)': 'C000016',
    '112-王老師計概一甲(1)': 'C000018',
    '112-王老師計概一乙(1)': 'C000019',
    '112-王老師運算思維與程式設計': 'C000020',
}

midterm_exam = ['0418期中考', '乙班期中測驗', '期中測驗', '甲班期中測驗']
final_exam = ['乙班期末測驗', '期末測驗', '期末考', '甲班期末測驗']

def getCourseStudents(course):
    # get all userid from answers table with given courseid which is mapped from course name
    conn = sqlite3.connect('codinghere-20240208.db')
    cursor = conn.cursor()
    courseid = coursemap[course]
    cursor.execute('''
    SELECT DISTINCT users.name FROM answers JOIN users ON answers.userid = users.fid WHERE courseid = ?;
    ''', (courseid,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def getSubmitsFromCourseStudent(course, student):
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('codinghere-20240208.db')

    # 建立一個游標物件
    cursor = conn.cursor()

    # 
    seletct_sql = '''
    SELECT submits.* FROM submits JOIN users ON submits.uid = users.fid WHERE submits.cid = 'specific_cid' AND users.name = 'specific_user_name';
    '''
    sqlstr = seletct_sql.replace('specific_cid', coursemap[course]).replace('specific_user_name', student)

    cursor.execute(sqlstr)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    conn.close()
    return df

def getSameDateSubmitsForCourseStudent(csdataframe):
    csdataframe['date'] = csdataframe['created'].apply(lambda x: str(x)[:8])
    grouped_df = csdataframe.groupby('date').agg(list)
    return grouped_df
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--student', help='Specify the student name')
    parser.add_argument('-c', '--course', help='Specify the course name')

    args = parser.parse_args()
    # main(args)

    # test
    allstudents = getCourseStudents(args.course)

    for student in allstudents:
        print(student)
        submits = getSubmitsFromCourseStudent(args.course, student)
        dateSubmits = getSameDateSubmitsForCourseStudent(submits)

                # Initialize a new dictionary to store the sums
        dateSums = {}
        for date, times in dateSubmits['time_pt'].items():
            # Calculate the sum of the list for each date
            dateSums[date] = sum(times)
        
        print(dateSums)

        # Plot the dateSums
        plt.bar(dateSums.keys(), dateSums.values())
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.ylabel('Sum')
        plt.title('Sum of Times by Date')
        plt.show()

        break
