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

def show_course_submits(course_name):
    return course_submits(course_name)

with gr.Blocks() as demo:
    gr.Markdown("# Course Assistant")
    with gr.Row():
        coursename = gr.Dropdown(courseSelect, label="Select a course")
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
            btn.click(show_course_submits, coursename, submits)

    with gr.Tab():
        test = gr.Textbox("Enter your code here")


demo.launch()