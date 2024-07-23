from flask import render_template, request, Blueprint
from datetime import time
from app.scheduler.optaplanner_scheduler import Timeslot, Room, Lesson, TimeTable

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate', methods=['POST'])
def generate():
    timeslot_day = request.form['timeslot_day']
    timeslot_start = request.form['timeslot_start']
    timeslot_end = request.form['timeslot_end']
    room_name = request.form['room_name']
    lesson_subject = request.form['lesson_subject']
    lesson_teacher = request.form['lesson_teacher']
    lesson_grade = request.form['lesson_grade']

    # Parse timeslot start and end times
    start_hour, start_minute = map(int, timeslot_start.split(':'))
    end_hour, end_minute = map(int, timeslot_end.split(':'))

    # Create Timeslot, Room, and Lesson objects
    timeslot = Timeslot(1, timeslot_day, time(start_hour, start_minute), time(end_hour, end_minute))
    room = Room(1, room_name)
    lesson = Lesson(1, lesson_subject, lesson_teacher, lesson_grade)

    # Set Timeslot and Room for the Lesson
    lesson.set_timeslot(timeslot)
    lesson.set_room(room)

    # Create lists and TimeTable object
    timeslot_list = [timeslot]
    room_list = [room]
    lesson_list = [lesson]
    timetable = TimeTable(timeslot_list, room_list, lesson_list)

    return render_template('result.html', timetable=timetable)
