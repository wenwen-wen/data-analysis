import gradio as gr
from course import *
from mycss import css

def course_profile(course_name):
    return course_basic(course_name)

def show_course_students(course_name):
    return course_students(course_name)

def show_course_units(course_name):
    return course_units(course_name)

def show_course_exams(course_name):
    return course_exams(course_name)

def show_course_submits(course_name, first_threshold, first_ignore):
    return course_submits(course_name, first_threshold, first_ignore)

def course_model(course_name, trainexam, testexam, first_threshold, first_ignore, modelname):
    return course_predict(course_name, trainexam, testexam, first_threshold, first_ignore, modelname)

sindex = 0
slen = 0
gname = ""
gproblem = ""

def set_problem():
    return gproblem

def set_name():
    return gname

def course_inspect(course_name, studentname, pname):
    global sindex, slen, gname, gproblem
    code, stat1, stat2, slen, sindex = course_submit_inspect(course_name, studentname, pname, sindex)
    gproblem = stat1.split("\n")[1].split(":")[1].strip()
    gname = stat2.split("\n")[0].split(":")[1].strip()
    return code, stat1, stat2

def submit_start(course_name, studentname, pname):
    global sindex
    sindex = 0
    return course_inspect(course_name, studentname, pname)

def submit_prev(course_name, studentname, pname):
    global sindex
    sindex = sindex - 1
    if sindex < 0: sindex = 0
    return course_inspect(course_name, studentname, pname)

def submit_next(course_name, studentname, pname):
    global sindex
    sindex = sindex + 1
    if sindex >= slen: sindex = slen - 1
    return course_inspect(course_name, studentname, pname)

def submit_end(course_name, studentname, pname):
    global sindex
    sindex = slen - 1
    return course_inspect(course_name, studentname, pname)

with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
    gr.Markdown("<h1>CodingHere資料檢視系統</h1>")
    with gr.Row():
        coursename = gr.Dropdown(courseSelect, label="課程選擇", elem_classes="course")
        first_ignore = gr.Slider(0, 180, 10, label="提交最短時間", elem_classes="short")
        first_threshold = gr.Slider(0, 1800, 600, label="第一次最長時間", elem_classes="long")

    btn = gr.Button("執行", elem_classes="submit")

    with gr.Tab("課程資訊", elem_classes="short"):
        output = gr.Markdown(line_breaks=True)
        btn.click(course_profile, coursename, output)

        with gr.Tab("學生"):
            students = gr.Markdown(line_breaks=True)
            btn.click(show_course_students, coursename, students)

        with gr.Tab("課程單元"):
            units = gr.Markdown(line_breaks=True)
            btn.click(show_course_units, coursename, units)

        with gr.Tab("考試"):
            exams = gr.Markdown(line_breaks=True)
            btn.click(show_course_exams, coursename, exams)

        with gr.Tab("提交紀錄"):
            submits = gr.Plot()
            btn.click(show_course_submits, [coursename, first_threshold, first_ignore], submits)

    with gr.Tab("課程模型"):
        trainexam = gr.Radio(["小考", "小考|期中"], value="小考|期中", label="訓練考試" )
        testexam = gr.Radio(["期中測驗", "期末測驗", "期中考", "期末考"], value="期末測驗", label="測試考試")
        modelname = gr.Radio(["Random Forest", "KNN"], value="KNN", label="模型選擇")
        output1 = gr.Markdown(line_breaks=True)
        with gr.Row():
            output2 = gr.Plot()
            output3 = gr.Plot()
        btn.click(course_model, [coursename, trainexam, testexam, first_threshold, first_ignore, modelname], [output1, output2, output3])

    with gr.Tab("提交檢查"):
        with gr.Row():
            pname = gr.Textbox(label="問題名稱")
            studentname = gr.Textbox(label="學生姓名")
        with gr.Row():
            codeview = gr.Code(language='cpp')
            with gr.Column():
                with gr.Row():
                    bStart = gr.Button("<<")
                    bPrev = gr.Button("<")
                    bNext = gr.Button(">")
                    bEnd = gr.Button(">>")
                with gr.Row():
                    with gr.Column():
                        bProblem = gr.Button("設定問題")
                        output3 = gr.Markdown(line_breaks=True)
                    with gr.Column():
                        bName = gr.Button("設定名稱")
                        output4 = gr.Markdown(line_breaks=True)
        btn.click(course_inspect, [coursename, studentname, pname], [codeview, output3, output4])
        bStart.click(submit_start, [coursename, studentname, pname], [codeview, output3, output4])
        bPrev.click(submit_prev, [coursename, studentname, pname], [codeview, output3, output4])
        bNext.click(submit_next, [coursename, studentname, pname], [codeview, output3, output4])
        bEnd.click(submit_end, [coursename, studentname, pname], [codeview, output3, output4])
        bProblem.click(set_problem, outputs=pname)
        bName.click(set_name, outputs=studentname)


demo.launch()