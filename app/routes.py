from flask import render_template, request, Blueprint, redirect, url_for
from datetime import time
from app.scheduler.optaplanner_scheduler import generate_problem, Timeslot, Room, Lesson

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    timeslot_list = request.form.getlist('timeslot')
    room_list = request.form.getlist('room')
    lesson_list = request.form.getlist('lesson')
    # Convert timeslot_list and room_list to appropriate format
    timeslot_objects = []
    for timeslot in timeslot_list:
        id, day, start_hour, start_minute, end_hour, end_minute = timeslot.split(',')
        timeslot_objects.append(Timeslot(int(id), day, time(hour=int(start_hour), minute=int(start_minute)), time(hour=int(end_hour), minute=int(end_minute))))
    room_objects = [Room(int(id), name) for id, name in (room.split(',') for room in room_list)]
    lesson_objects = []
    for lesson in lesson_list:
        id, subject, teacher, student_group = lesson.split(',')
        lesson_objects.append(Lesson(int(id), subject, teacher, student_group))
    generate_problem(timeslot_objects, room_objects, lesson_objects)
    return redirect(url_for('index'))