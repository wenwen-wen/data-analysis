import gradio as gr
from course import *

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

with gr.Blocks() as demo:
    gr.Markdown("# Course Assistant")
    with gr.Row():
        coursename = gr.Dropdown(courseSelect, label="Select a course")
        first_threshold = gr.Slider(0, 1800, 600, label="First Threshold")
        first_ignore = gr.Slider(0, 180, 10, label="First Ignore")

    btn = gr.Button("Run")

    with gr.Tab("Course Profile"):
        output = gr.Markdown(line_breaks=True)
        btn.click(course_profile, coursename, output)

        with gr.Tab("Students"):
            students = gr.Markdown(line_breaks=True)
            btn.click(show_course_students, coursename, students)

        with gr.Tab("Units"):
            units = gr.Markdown(line_breaks=True)
            btn.click(show_course_units, coursename, units)

        with gr.Tab("Exams"):
            exams = gr.Markdown(line_breaks=True)
            btn.click(show_course_exams, coursename, exams)

        with gr.Tab("Submits"):
            submits = gr.Plot()
            btn.click(show_course_submits, [coursename, first_threshold, first_ignore], submits)

    with gr.Tab("Course Model"):
        trainexam = gr.Radio(["小考", "小考|期中"], value="小考|期中", label="Train Exam")
        testexam = gr.Radio(["期中測驗", "期末測驗", "期中考", "期末考"], value="期末測驗", label="Test Exam")
        modelname = gr.Radio(["Random Forest", "KNN"], value="KNN", label="Model Name")
        output1 = gr.Markdown(line_breaks=True)
        output2 = gr.Plot()
        btn.click(course_model, [coursename, trainexam, testexam, first_threshold, first_ignore, modelname], [output1, output2])


demo.launch()