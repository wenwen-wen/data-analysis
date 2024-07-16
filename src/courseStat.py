import argparse
import os
import json
from ignoreList import IGNORE_LIST_IDS
from tabulate import tabulate
from datetime import datetime, timedelta, time
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

DEBUG = False
XFIELDS = ['TST', 'TPS', 'TSC', 'TAC', 'TWA', 'TPE', 'TCE', 'TSS']
YFIELDS = ['PAS']
FIRST_TIME_THRESHOLD = 600
FIRST_IGNORE = 10

def subtract_seconds_from_datetime(datetime_str, seconds):
    # Parse the datetime string to a datetime object
    datetime_obj = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')

    # Subtract the seconds
    new_datetime_obj = datetime_obj - timedelta(seconds=seconds)

    # Convert back to the original format and return
    return new_datetime_obj.strftime('%Y%m%d%H%M%S')

def course_students(course):
    if 'students' not in course: return []
    result = []
    for key, value in  course['students'].items():
        if key not in IGNORE_LIST_IDS:
            value["id"] = key
            result.append(value)
    return result

def show_course_units(course):
    if 'units' not in course: return
    for unit in course['units']:
        print(f"Unit: {unit['name']}, {unit['startDate']} - {unit['endDate']}")
        probs = [p['title']['zh'] for p in unit['probs']]
        print(f"Problems: {probs}")

def show_course_exams(course):
    if 'exams' not in course: return
    for exam in course['exams']:
        print(f"Exam: {exam['name']} ({exam['id']}), ({exam['tlimit']} / {exam['compilers']})")
        probs = [p['title']['zh'] for p in exam['probs']]
        print(f"Problems: {probs}")

def course_exams(course, answers, problemsmap):
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

def course_basic(course):
    print("Course ID: ", course['id'])
    print("Course Name: ", course['name'])
    print("Teachers: ", [t["name"] for t in course['teachers']])
    print("Assistants: ", [a["name"] for a in course['assistants']] if "assistants" in course else 'None')
    print("Compilers: ", course['compilers'] if "compilers" in course else 'All')
    print("Students: ", len(course_students(course)))
    print("Units: ", len(course['units']) if "units" in course else 0)
    show_course_units(course)
    print("Exams: ", len(course['exams']) if "exams" in course else 0)
    show_course_exams(course)

def course_student_submits(course, student, submits): # Homework submits
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

# XFIELDS = ['TST', 'TPS', 'TSC', 'TAC', 'TWA', 'TNA', 'TCE', 'TSS']
# YFIELDS = ['PAS']
# FIRST_TIME_THRESHOLD = 600
# Collect data for each student
def _student_data(student, exam, answer, submits, problemsmap):
    result = {"sid": student["id"], "sname": student["name"], "ename": exam["name"], "edate": answer["date"]}
    examdate = answer["date"]
    examstart = examdate + "091000"
    before_exam_submits = [s for s in submits if s["created"]<examstart]
    csubmits = categorize_submits_by_pid(before_exam_submits)
    result["TPS"] = len(csubmits)
    for pid, ss in csubmits.items():
        pss = pid_submits_stat(ss)
        for k, v in pss.items():
            result["P"+pid[4:]+k] = v
        result["PAS"+pid[4:]] = None

    for pid in exam["pids"]:
        result["PAS"+pid[4:]] = -1
        if pid in answer["submits"]:
            v = answer["submits"][pid]
            if v["correct"]: result["PAS"+pid[4:]] = 1

    return result

def pid_submits_stat(submits):
    tst, tsc, tac = 0, 0, 0
    sep_submits = separate_submits(submits)
    for ss in sep_submits:
        if 'time_pt' in ss[0]:
            if ss[-1]['time_pt'] < FIRST_IGNORE: continue # This is just a test
            delta = ss[0]['time_pt'] - FIRST_TIME_THRESHOLD
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
        if 'time_pt' in s and s['time_pt'] < FIRST_IGNORE: continue
        if s['status'] == 'AC': continue
        if s['status'] == 'PE' or s['status'] == 'NA': tna += 1
        elif s['status'] == 'CE': tce += 1
        else: twa += 1
        tss += 1

    result = {"TST": tst, "TSC": tsc, "TLS": len(sep_submits), "TAC": tac, "TWA": twa, "TNA": tna, "TCE": tce, "TSS": tss}
    return result

def separate_submits(submits):
    submits_lists = []
    current_list = []
    prev_time_pt = None
    for submit in submits:
        if prev_time_pt is None or submit['time_pt'] > prev_time_pt:
            current_list.append(submit)
        else:
            submits_lists.append(current_list)
            current_list = [submit]
        if 'time_pt' in submit: prev_time_pt = submit['time_pt']
    submits_lists.append(current_list)
    return submits_lists


def student_data(course, submits, answers, problemsmap):
    exams = course_exams(course, answers, problemsmap)
    students = course_students(course)
    records = []
    all_keys = set()
    for student in students:
        student_submits = course_student_submits(course, student, submits)
        for exam in exams:
            exam_answers = [a for a in answers if a["examid"] == exam["id"] and a["userid"] == student['id']]
            for a in exam_answers:
                sdata = _student_data(student, exam, a, student_submits, problemsmap)
                records.append(sdata)
                all_keys |= set(sdata.keys())

    for r in records:
        for k in all_keys:
            if k not in r: r[k] = None

    df = pd.DataFrame(records)
    df = df.reindex(sorted(df.columns), axis=1)
    df_sorted = df.sort_values(by='edate')
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process statistic data of a course")
    parser.add_argument("-c", "--courses", required=True, help="Course IDs (sep by comma)")
    parser.add_argument("-f", "--folder", required=True, help="Path to the json files")
    args = parser.parse_args()

    coursefile = os.path.join(args.folder, 'courses.json')
    submitsfile = os.path.join(args.folder, 'submits.json')
    answerfile = os.path.join(args.folder, 'answers.json')
    problemfile = os.path.join(args.folder, 'problems.json')

    with open(coursefile, 'r') as file:
        courses = json.load(file)

    with open(submitsfile, 'r') as file:
        submits = json.load(file)

    with open(answerfile, 'r') as file:
        answers = json.load(file)

    with open(problemfile, 'r') as file:
        problems = json.load(file)

    # process problems to make zh title map to key
    problems = [p for p in problems if 'name' in p and p['name']=='基礎題庫'][0]['problems']
    problemsmap = {value['title']['zh']: key for key, value in problems.items()}

    for course in courses:
        if course['id'] not in args.courses.split(','): continue
        course_stat(course, submits, answers, problemsmap)
        student_data(course, submits, answers, problemsmap)
