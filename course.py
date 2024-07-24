import argparse
import os
import json
from time import sleep
from ignoreList import IGNORE_LIST_IDS
from tabulate import tabulate
from datetime import datetime, timedelta, time
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
import seaborn as sns

courseSelect = [
    "110-計概(一)甲",
    "110-計概(一)乙",
    "110-計概(二)甲",
    "110-計概(二)乙",
    "111-計概(一)甲",
    "111-計概(一)乙",
    "111-計概(二)甲",
    "111-計概(二)乙",
    "112-計概(一)甲",
    "112-計概(一)乙",
    "112-計概(二)甲",
    "112-計概(二)乙",
]

courseMap = {
    "110-計概(一)甲": "C000001",
    "110-計概(一)乙": "C000002",
    "110-計概(二)甲": "C000005",
    "110-計概(二)乙": "C000006",
    "111-計概(一)甲": "C000009",
    "111-計概(一)乙": "C000010",
    "111-計概(二)甲": "C000015",
    "111-計概(二)乙": "C000016",
    "112-計概(一)甲": "C000018",
    "112-計概(一)乙": "C000019",
    "112-計概(二)甲": "C000021",
    "112-計概(二)乙": "C000022",
}

DEBUG = False
XFIELDS = ['TST', 'TPS', 'TSC', 'TAC', 'TWA', 'TPE', 'TCE', 'TSS']
YFIELDS = ['PAS']
FIRST_TIME_THRESHOLD = 600
FIRST_IGNORE = 10

class CodingHere():
    folder = "groups"
    coursefile = os.path.join(folder, 'courses.json')
    submitsfile = os.path.join(folder, 'submits.json')
    answerfile = os.path.join(folder, 'answers.json')
    problemfile = os.path.join(folder, 'problems.json')

    def __init__(self):
        with open(self.coursefile, 'r') as file:
            self.courses = json.load(file)

        with open(self.submitsfile, 'r') as file:
            self.submits = json.load(file)

        with open(self.answerfile, 'r') as file:
            self.answers = json.load(file)

        with open(self.problemfile, 'r') as file:
            rawproblems = json.load(file)
            self.problems = [p for p in rawproblems if 'name' in p and p['name']=='基礎題庫'][0]['problems']
            self.problemsmap = {value['title']['zh']: key for key, value in self.problems.items()}

CH = CodingHere()

def color_text(txt, color, bgcolor=None):
    if bgcolor:
        return f'<span style="padding:2px 5px;color:{color};background-color:{bgcolor}">{txt}</span>'
    return f'<span style="padding:2px 5px;color:{color}">{txt}</span>'

def course_basic(course_name):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    output = f"{course_name}, "
    output += f"ID: {course['id']}, "
    output += f"Teachers: {', '.join([t['name'] for t in course['teachers']])}, "
    output += f"Assistants: {', '.join([a['name'] for a in course['assistants']]) if 'assistants' in course else 'None'}, "
    output += f"Compilers: {', '.join(course['compilers']) if 'compilers' in course else 'All'}\n"
    return output

def _course_students_raw(course):
    if 'students' not in course: return []
    result = []
    for key, value in  course['students'].items():
        if key not in IGNORE_LIST_IDS:
            value["id"] = key
            result.append(value)
    return result

def _course_students(course):
    if 'students' not in course: return "No students found\n"
    students = course['students']
    student_keys = [k for k in students.keys() if k not in IGNORE_LIST_IDS]
    students = [students[k] for k in student_keys]
    output = f"<div class='mylabel'> 學生人數：{len(students)}</div>"
    output += ", ".join([s['name'] for s in students])
    return output

def course_students(course_name):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    return _course_students(course)

def course_units(course_name):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    if 'units' not in course: return "No units found\n"
    units = course['units']
    output = f"<div class='mylabel'>課程單元數 : {len(units)}</div>"
    for unit in units:
        output += f"{color_text(unit['name'], '#FF007F')}: {unit['startDate']}-{unit['endDate']}, "
        probs = [p['title']['zh'] for p in unit['probs']]
        output += "[" + ", ".join(probs) + "]<br>"
    print(output)
    return output

def _course_exams_raw(course, answers, problemsmap):
    if "exams" not in course: return []
    result = []
    for exam in course["exams"]:
        obj = {
            "id": exam["id"],
            "name": exam["name"],
            "tlimit": exam["tlimit"],
            "tscore": exam["tscore"],
        }
        questions = [e["title"]["zh"] for e in exam["probs"]]
        obj["problems"] = questions
        obj["pids"] = [problemsmap[q] for q in questions]
        exam_answers = [a for a in answers if a["examid"] == exam["id"]]
        obj["answers"] = len(exam_answers)
        answer_dates = list(set(a["date"] for a in exam_answers))
        obj["dates"] = answer_dates
        result.append(obj)
    if DEBUG:
        print("==========Exams==========")
        for exam in result:
            print("Exam: ", exam)
    return result

def _course_exams(course):
    if 'exams' not in course: return "No exams found\n"
    output = f"<div class='mylabel'>考試 : {len(course['exams'])}</div>"
    for exam in course['exams']:
        exam_answers = [a for a in CH.answers if a["examid"] == exam["id"]]
        answer_dates = list(set(a["date"] for a in exam_answers))
        dates_str = ", ".join(answer_dates)
        output += f"{color_text(exam['name'], '#FF007F')}: {dates_str}, ({'/'.join(exam['compilers'])}), "
        probs = [p['title']['zh'] for p in exam['probs']]
        output += "[" + ", ".join(probs) + "]<br>"
    return output

def course_exams(course_name):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    return _course_exams(course)

def exam_date(course, keyword):
    exams = course['exams']
    mexam = [exam for exam in exams if keyword in exam['name']][0]
    exam_answers = [a for a in CH.answers if a["examid"] == mexam["id"]]
    answer_dates = list(set(a["date"] for a in exam_answers))
    return answer_dates[0]

def course_submits(course_name, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE): # Homework submits
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    submits = [s for s in CH.submits if 'cid' in s and s['cid'] == cid]
    students = course['students']
    studnum = len([k for k in students.keys() if k not in IGNORE_LIST_IDS])
    units = course['units']
    split_submits = []
    unidates = [unit['startDate'] for unit in units]
    submit_counts = []
    average_submit_counts = []
    for unit in units:
        start_date = unit['startDate']
        end_time = unit['endDate']+"235959"
        pids = [p['id'] for p in unit['probs']]
        unit_submits = [s for s in submits if start_date <= s['created'] <= end_time and s['pid'] in pids]
        split_submits.append(unit_submits)
        submit_counts.append(len(unit_submits)/studnum)
        average_submit_counts.append(len(unit_submits)/len(pids)/studnum)

    spent_times = []
    for unit_submits in split_submits:
        submitstat = submits_stat(unit_submits, first_threshold, first_ignore)
        stimes = 0
        for k, v in submitstat.items():
            if 'TST' in k: stimes += v
        spent_times.append(stimes/len(submitstat)/studnum)

    unitdates = [datetime.strptime(date, '%Y%m%d').date() for date in unidates]
    # print("UNITDATES", unitdates)
    mdate = datetime.strptime(exam_date(course, '期中'), '%Y%m%d').date()
    # fdate = datetime.strptime(exam_date(course, '期末'), '%Y%m%d').date()
    plt.figure(figsize=(10, 6))
    plt.plot(unitdates, submit_counts, 'o-', label='Submit Counts')
    plt.legend()
    plt.gca().xaxis.set_major_locator(plt.LinearLocator())
    for i, count in enumerate(submit_counts):
        unit = units[i]
        plt.text(unitdates[i], count, f"{unit['name']}", ha='center', va='bottom')
    plt.xlabel('Units')
    plt.xticks(rotation=30)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(7))
    plt.ylabel('Submits / Seconds')
    plt.title('Homework Submits')
    plt.axvline(x=mdate, color='r', linestyle='--')
    plt.text(mdate, np.mean(submit_counts), f'Mid-Exam\n{mdate}', ha='center', va='bottom')

    plt.plot(unitdates, average_submit_counts, 'o-', color='g', label='Problem Submit Counts')
    plt.legend()

    plt.plot(unitdates, spent_times, '*-', color='r', label='Spent Times')
    plt.legend()
    # plt.axvline(x=fdate, color='r', linestyle='--')
    # plt.text(fdate, np.mean(submit_counts), f'Final-Exam\n{fdate}', ha='center', va='bottom')
    # plt.grid()

    # Add another y values with different scale
    # plt.twinx()
    # plt.ylabel('Average submit #')
    return plt
    if not os.path.exists('Fig'):
        os.makedirs('Fig')

    plt.savefig(f'Fig/{cid}_submits.png')
    return f'Fig/{cid}_submits.png'

def course_predict(course_name, trainexam, testexam, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE, modelname="KNN"):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    submits = [s for s in CH.submits if 'cid' in s and s['cid'] == cid]
    answers = CH.answers
    problemsmap = CH.problemsmap
    sdata = student_data(course, submits, answers, problemsmap, first_threshold, first_ignore)
    sdata.fillna(0, inplace=True)
    df = sdata
    dcolumns = sdata.columns
    similar_columns = [col for col in dcolumns if 'PAS' in col]
    df['PAS'] = sdata[similar_columns].replace(-1, 0).sum(axis=1)
    ename_keywords = ['小考', '期中', '期末']
    exams = set()
    for keyword in ename_keywords:
        exams |= {ename for ename in df['ename'] if keyword in ename}
    for exam in exams:
        examscore = df.loc[df['ename'] == exam, 'PAS'].max(axis=0)
        df.loc[df['ename'] == exam, 'PAS'] = df.loc[df['ename'] == exam, 'PAS']*100/examscore

    df.fillna(0, inplace=True)
    traindata = df[df['ename'].str.contains(trainexam)]
    testdata = df[df['ename'].str.contains(testexam)]
    traincolpattern = r'P\d+'
    x_columns = [col for col in df.columns if re.match(traincolpattern, col)]
    xdata = traindata.loc[:, x_columns]
    ydata = traindata.loc[:, 'PAS']
    xdatamax = xdata.max()
    xdatamax[xdatamax == 0] = 1
    xdata = xdata/xdatamax
    # Create a RandomForestRegressor object
    if modelname == "KNN":
        model = KNeighborsRegressor()
    else:
        model = RandomForestRegressor()
    # Fit the model to the data
    model.fit(xdata, ydata)
    xtest = testdata.loc[:, x_columns]
    ytest = testdata.loc[:, 'PAS']

    xtestmax = xtest.max()
    xtestmax[xtestmax == 0] = 1
    xtest = xtest/xtestmax

    # y1est = np.full(len(ytest), ydata.mean())
    # mse1 = mean_squared_error(ytest, y1est, squared=False)
    y2est = model.predict(xtest)
    y2est = y2est
    # y2est = y2est/np.max(y2est)*100
    ypossible = np.array([n*100/7 for n in range(8)])
    # y2est = np.array([ypossible[np.abs(ypossible - y).argmin()] for y in y2est])
    mse2 = mean_squared_error(ytest, y2est, squared=False)
    # print(mse1, mse2)
    # print(ydata.mean())
    # print(int(np.mean(ytest)), int(np.min(ytest)), int(np.max(ytest)), list(map(float,ytest)))
    # print(int(np.mean(y1est)), int(np.min(y1est)), int(np.max(y1est)), list(map(float,y1est)))
    # print(int(np.mean(y2est)), int(np.min(y2est)), int(np.max(y2est)), list(map(float,y2est)))
    correlation = np.corrcoef(y2est, ytest)[0, 1]
    # print("Correlation of y2est and y_test:", correlation)
    plt1 = plt.figure(figsize=(8, 6))
    plt.scatter(y2est, ytest)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    # ytest = list(map(int, ytest*7/100+0.01))
    # y2est = list(map(int, y2est*7/100+0.01))
    # confusion_matrix(ytest, y2est)
    outstr = f"Correlation: {correlation:.2f}, MSE: {mse2:.2f}"
    ypossible = np.array([n*100/7 for n in range(8)])
    # y2est = np.array([ypossible[np.abs(ypossible - y).argmin()] for y in y2est])
    ytest = list(map(int, ytest*7/100+0.01))
    y2est = list(map(int, y2est*7/100+0.01))
    cmatrix = confusion_matrix(ytest, y2est)
    plt2, ax = plt.subplots(figsize=(8, 6))
    # plt2 = plt.figure(figsize=(8, 6))
    sns.heatmap(cmatrix, annot=True, fmt="d", cmap="Blues")
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    # ax.set_title('Confusion Matrix')
    # Move x-ticks and labels to the top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    # ax.xlabel('Predicted')
    # ax.ylabel('Actual')
    # ax.title('Confusion Matrix')
    # plt.xticks(rotation=30, ha='right')
    # plt.gca().xaxis.set_label_position('top')
    # print("Confusion Matrix: ", cmatrix)
    outstr = f"Correlation: {correlation:.2f}, MSE: {mse2:.2f}"
    return outstr, plt2, plt1
    outstr += "\n```\n" + str(cmatrix) + "\n```\n"
    return outstr, plt

def course_submit_inspect(course_name, studentname, pname, index):
    cid = courseMap[course_name]
    course = [c for c in CH.courses if c["id"] == cid][0]
    submits = [s for s in CH.submits if 'cid' in s and s['cid'] == cid]
    students = course['students']
    if studentname.upper() != '':
        sids = [id for id,s in students.items() if studentname in s['name']]
        submits = [s for s in submits if s['uid'] in sids]
    if pname.upper() != '':
        pids = [k for n,k in CH.problemsmap.items() if pname in n]
        submits = [s for s in submits if s['pid'] in pids]
    slen = len(submits)
    if index < len(submits):
        submit = submits[index]
    else:
        submit = submits[slen-1]
        index = slen-1
    code = submit['code']
    problem = CH.problems[submit['pid']]
    stat1 = f"Index: {index+1}/{slen}\n"
    stat1 += f"Problem: {problem['title']['zh']}\n"
    stat1 += f"Submit: {submit['created']}\n"
    stat1 += f"Score: {submit['score']}\n"
    stat1 += f"Status: {submit['status']}\n"
    if "time_pt" in submit: stat1 += f"PT: {submit['time_pt']} 秒\n"

    student = students[submit['uid']]
    if not student: return code, stat1, "", slen, index
    stat2 = f"Student: {student['name']}\n"
    answers = [a for a in CH.answers if a['courseid'] == cid and a['userid'] == submit['uid']]
    for answer in answers:
        exam = [e for e in course['exams'] if e['id'] == answer['examid']][0]
        if exam:
            stat2 += f"Exam: {exam['name']}, Score: {answer['score']}/{exam['tscore']}\n"
    return code, stat1, stat2, slen, index

def subtract_seconds_from_datetime(datetime_str, seconds):
    # Parse the datetime string to a datetime object
    datetime_obj = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')

    # Subtract the seconds
    new_datetime_obj = datetime_obj - timedelta(seconds=seconds)

    # Convert back to the original format and return
    return new_datetime_obj.strftime('%Y%m%d%H%M%S')

# def course_exams(course, answers, problemsmap):
#     if "exams" not in course: return []
#     result = []
#     for exam in course["exams"]:
#         obj = {
#             "id": exam["id"],
#             "name": exam["name"],
#             "tlimit": exam["tlimit"],
#             "tscore": exam["tscore"],
#         }
#         questions = [e["title"]["zh"] for e in exam["probs"]]
#         obj["problems"] = questions
#         obj["pids"] = [problemsmap[q] for q in questions]
#         exam_answers = [a for a in answers if a["examid"] == exam["id"]]
#         obj["answers"] = len(exam_answers)
#         answer_dates = list(set(a["date"] for a in exam_answers))
#         obj["dates"] = answer_dates
#         result.append(obj)
#     if DEBUG:
#         print("==========Exams==========")
#         for exam in result:
#             print("Exam: ", exam)
#     return result


def course_student_submits(course, student, submits): # Homework submits
    # print("COURSE", course['name'])
    # print("STUDENT", student)
    # print("SUBMITS", len(submits))
    result = [s for s in submits if 'cid' in s and s['uid'] == student['id'] and s['cid'] == course['id']]
    sorted_result = sorted(result, key=lambda x: x['created'])
    return sorted_result

def categorize_submits_by_pid(submits):
    submits_by_pid = {}
    submits.sort(key=lambda x: x['created'])
    for submit in submits:
        pid = submit['pid']
        if pid not in submits_by_pid:
            submits_by_pid[pid] = []
        submits_by_pid[pid].append(submit)
    return submits_by_pid

def course_student_stat_by_date(course, student, submits, answers, problemsmap):
    print("Student ID: ", student['id'])
    print("Student Name: ", student['name'])
    student_submits = course_student_submits(course, student, submits)
    print("Total Submits: ", len(student_submits))
    # Categorize submits by problem ID

    # print(f"{pid}: {len(ss)}", end=", ")
    header = ["Time", "PID", "Score", "Status", "Time_pt"]
    data = [[s.get("created"), s.get("pid"), s.get("score"), s.get("status"), s.get("time_pt")] for s in student_submits]
    print(tabulate(data, headers=header))
    # Add any additional processing or analysis here
    print()
    exams = course_exams(course, answers, problemsmap)
    scores = []
    for exam in exams:
        print(f'Exam: {exam["name"]}, "TScore:", {exam["tscore"]}')
        student_answers = [a for a in answers if a["examid"] == exam["id"] and a["userid"] == student['id']]
        for a in student_answers:
            print(f"Date: {a['date']}, Score: {a['score']}, STime: {a['totaltime']}")
            # esubmits = []
            for k in sorted(a['submits'].keys()):
                v = a['submits'][k]
                # esubmits.append({"pid": k, "correct": v["correct"], "usetime": v["usetime"]})
                print(f"{k}: {v['correct']}, Time: {v['usetime']}")
            # scores.append(student_answers[0]["score"])


def course_student_stat_by_pid(course, student, submits, answers, problemsmap):
    print("Student ID: ", student['id'])
    print("Student Name: ", student['name'])
    student_submits = course_student_submits(course, student, submits)
    print("Total Submits: ", len(student_submits))
    # Categorize submits by problem ID

    submits_by_pid = categorize_submits_by_pid(student_submits)

    for pid, ss in submits_by_pid.items():
        # print(f"{pid}: {len(ss)}", end=", ")
        print("PID: ", pid)
        print("Total Submits: ", len(ss))
        header = ["Time", "PID", "Score", "Status", "Time_pt"]
        data = [[s.get("created"), s.get("pid"), s.get("score"), s.get("status"), s.get("time_pt")] for s in ss]
        print(tabulate(data, headers=header))
        # Add any additional processing or analysis here
    print()

def questions_ids(questions, problems):
    pass



def course_student_date_submits(course, student, date, submits):
    submits = course_student_submits(course, student, submits)
    submits = [s for s in submits if 'created' in s and s['created'].startswith(date)]
    submits = sorted(submits, key=lambda x: x['created'])
    header = ["Time", "PID", "Score", "Status", "Time_pt", "Start_Time"]
    data = [[s.get("created"), s.get("pid"), s.get("score"), s.get("status"), s.get("time_pt"), subtract_seconds_from_datetime(s['created'], s['time_pt'])] for s in submits]
    print(tabulate(data, headers=header))

def course_student_date_starts(course, student, date, submits, problemsmap):
    submits = course_student_submits(course, student, submits)
    submits = [s for s in submits if 'created' in s and s['created'].startswith(date)]
    submits = sorted(submits, key=lambda x: x['created'])
    result = []
    for s in submits:
        if 'time_pt' in s:
            datetime_obj = datetime.strptime(s['created'], '%Y%m%d%H%M%S')
            result.append(datetime_obj- timedelta(seconds=s['time_pt']))
    return result
    starts = sorted(set(result))
    starts = [s - timedelta(seconds=s.second % 10) for s in starts]
    starts = sorted(set(starts))
    return starts

def course_stat(course, submits, answers, problemsmap):
    print("==========Course Statistic==========")
    course_basic(course)
    # cexams = course_exams(course, answers, problemsmap)
    # course_student_stat_by_pid(course, course_students(course)[0], submits, answers, problemsmap)
    # course_student_date_submits(course, course_students(course)[0], "20220425", submits)
    # plot_date_starts(course, submits, "20220425", problemsmap)


def submits_stat(submits, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE):
    result = {}
    csubmits = categorize_submits_by_pid(submits)
    result["TPS"] = len(csubmits)
    for pid, ss in csubmits.items():
        pss = pid_submits_stat(ss, first_threshold, first_ignore)
        for k, v in pss.items():
            result["P"+pid[4:]+k] = v
    return result

def separate_submits(submits):
    submits_lists = []
    current_list = []
    prev_time_pt = None
    for submit in submits:
        if prev_time_pt is None or ('time_pt' in submit and submit['time_pt'] > prev_time_pt):
            current_list.append(submit)
        else:
            submits_lists.append(current_list)
            current_list = [submit]
        if 'time_pt' in submit: prev_time_pt = submit['time_pt']
    submits_lists.append(current_list)
    return submits_lists

def pid_submits_stat(submits, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE):
    tst, tsc, tac = 0, 0, 0
    sep_submits = separate_submits(submits)
    for ss in sep_submits:
        if 'time_pt' in ss[0]:
            if ss[-1]['time_pt'] < first_ignore: continue # This is just a test
            delta = ss[0]['time_pt'] - first_threshold
            if delta < 0: st = ss[-1]['time_pt']
            else: st = ss[-1]['time_pt'] - delta
            tst += st
        score = [s['score'] for s in ss]
        acss = [s for s in ss if s['status']=='AC']
        # print("SCORE"  , score)
        tsc += max(score)
        if acss:
            tac += 1

    twa, tna, tce, tss = 0, 0, 0, 0
    for s in submits:
        if 'time_pt' in s and s['time_pt'] < first_ignore: continue
        if s['status'] == 'AC': continue
        if s['status'] == 'PE' or s['status'] == 'NA': tna += 1
        elif s['status'] == 'CE': tce += 1
        else: twa += 1
        tss += 1

    result = {"TST": tst, "TSC": tsc, "TLS": len(sep_submits), "TAC": tac, "TWA": twa, "TNA": tna, "TCE": tce, "TSS": tss}
    return result

# XFIELDS = ['TST', 'TPS', 'TSC', 'TAC', 'TWA', 'TNA', 'TCE', 'TSS']
# YFIELDS = ['PAS']
# FIRST_TIME_THRESHOLD = 600
# Collect data for each student
def _student_data(student, exam, answer, submits, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE):
    result = {"sid": student["id"], "sname": student["name"], "ename": exam["name"], "edate": answer["date"]}
    examdate = answer["date"]
    examstart = examdate + "091000"
    before_exam_submits = [s for s in submits if s["created"]<examstart]
    csubmits = categorize_submits_by_pid(before_exam_submits)
    result["TPS"] = len(csubmits)
    for pid, ss in csubmits.items():
        pss = pid_submits_stat(ss, first_threshold, first_ignore)
        for k, v in pss.items():
            result["P"+pid[4:]+k] = v
        result["PAS"+pid[4:]] = None

    for pid in exam["pids"]:
        result["PAS"+pid[4:]] = -1
        if pid in answer["submits"]:
            v = answer["submits"][pid]
            if v["correct"]: result["PAS"+pid[4:]] = 1

    return result

def student_data(course, submits, answers, problemsmap, first_threshold=FIRST_TIME_THRESHOLD, first_ignore=FIRST_IGNORE):
    exams = _course_exams_raw(course, answers, problemsmap)
    students = _course_students_raw(course)
    records = []
    all_keys = set()
    for student in students:
        student_submits = course_student_submits(course, student, submits)
        for exam in exams:
            exam_answers = [a for a in answers if a["examid"] == exam["id"] and a["userid"] == student['id']]
            for a in exam_answers:
                sdata = _student_data(student, exam, a, student_submits, first_threshold, first_ignore)
                records.append(sdata)
                all_keys |= set(sdata.keys())

    for r in records:
        for k in all_keys:
            if k not in r: r[k] = None

    df = pd.DataFrame(records)
    df = df.reindex(sorted(df.columns), axis=1)
    df_sorted = df.sort_values(by='edate')
    return df_sorted
    df_sorted.to_csv(f"{course['id']}.csv", index=False)
    print("COLS:", list(df.columns))
    print("SHAPE", df.shape)
    print(f"Exported to {course['id']}.csv")



def plot_date_starts(course, submits, day, problemsmap):
    starts = []
    for student in course_students(course):
        sstarts = course_student_date_starts(course, student, day, submits, problemsmap)
        # print("Student ID: ", student['id'], "Starts: ", sstarts)
        starts += sstarts
    plot_datetime_histogram(starts)

def plot_datetime_histogram(dtimes):
    # Filter out datetimes before 8:00
    filtered_datetimes = [dt for dt in dtimes if dt.time() >= time(8, 0)]

    # Convert the array of datetime objects to a pandas Series
    datetime_series = pd.Series(filtered_datetimes)

    # Resample to '1T' for 1 minute frequency and count occurrences
    datetime_counts = datetime_series.dt.floor('1min').value_counts().sort_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    datetime_counts.plot(kind='line', marker='o')  # Change 'bar' to 'line' and add marker='o'
    plt.xlabel('Datetime (Minute)')
    plt.ylabel('Frequency')
    plt.title('Datetime Frequencies per Minute')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

