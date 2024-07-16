import argparse
import json
import os

def ShowTimePT(submits):
    time_pt_date = '20240707202500'
    no_time_pt = [submit for submit in submits if 'time_pt' not in submit]
    with_time_pt = [submit for submit in submits if 'time_pt' in submit]
    for submit in with_time_pt:
        if submit['created'] < time_pt_date:
            time_pt_date = submit['created']
    print("==========Time_pt==========")
    print("With time_pt: ", len(with_time_pt))
    print("No time_pt: ", len(no_time_pt))
    print("Total: ", len(submits))
    print("Earliest time_pt: ", time_pt_date)

def ShowCompilers(submits):
    compilers = ['C', 'C++', 'Java', 'Python']
    c_submits = [s for s in submits if ('lang' not in s) or s['lang'].lower() == 'c']
    cpp_submits = [s for s in submits if s['lang'].lower() == 'cpp']
    java_submits = [s for s in submits if s['lang'].lower() == 'java']
    python_submits = [s for s in submits if s['lang'].lower() == 'py']
    print("==========Compilers==========")
    print("C: ", len(c_submits))
    print("C++: ", len(cpp_submits))
    print("Java: ", len(java_submits))
    print("Python: ", len(python_submits))
    print("Total: ", len(submits))

def ShowCourses(submits, coursefile):
    if coursefile:
        with open(coursefile, 'r') as file:
            courses = json.load(file)
    else:
        courses = None
    c_submits = {}
    total = 0
    for s in submits:
        if 'cid' not in s: continue # it is an exam submit
        if s['cid'] not in c_submits: c_submits[s['cid']] = []
        c_submits[s['cid']].append(s)
        total += 1
    print("==========Courses==========")
    print("Course IDs: ", c_submits.keys())
    print("Total Courses: ", len(c_submits.keys()))
    cids = sorted(list(c_submits.keys()))
    total_timepts = 0
    for cid in cids:
        subs = c_submits[cid]
        subs_timept = [s for s in subs if 'time_pt' in s]
        total_timepts += len(subs_timept)
        if courses:
            course = [c for c in courses if c['id'] == cid]
            if len(course)>0: cname = course[0]['name']
            else: cname = 'Playground'
            print(f"Course {cid}: {cname}, {len(subs)}, with time_pt: {len(subs_timept)}")
        else:
            print(f"Course {cid}: {len(subs)}, with time_pt: {len(subs_timept)}")
    print("Total Homework Submits (No CID): ", total)
    print("Total Homework Submits with Timepts: ", total_timepts)

def main(infile, coursefile):
    with open(infile, 'r') as file:
        submits = json.load(file)
    ShowTimePT(submits)
    ShowCompilers(submits)
    ShowCourses(submits, coursefile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Statistic Data of Submits")
    parser.add_argument("folder", help="Path to the json folder")
    args = parser.parse_args()

    if args.folder.endswith('/'):
        args.folder = args.folder[:-1]

    submitsfile = os.path.join(args.folder, 'submits.json')
    coursesfile = os.path.join(args.folder, 'courses.json')
    main(submitsfile, coursesfile)

