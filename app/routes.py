from app.scheduler.solver import format_lesson_for_template,solution
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime


main = Blueprint('main', __name__)
@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        timeslots = []
        for i in range(int(request.form['timeslot_count'])):
            timeslots.append({
                'weekday': request.form[f'weekday_{i}'],
                'start_time': request.form[f'start_time_{i}'],
                'end_time': request.form[f'end_time_{i}']
            })

        rooms = []
        for i in range(int(request.form['room_count'])):
            rooms.append({
                'name': request.form[f'room_name_{i}']
            })

        lessons = []
        for i in range(int(request.form['lesson_count'])):
            lessons.append({
                'subject': request.form[f'subject_{i}'],
                'teacher': request.form[f'teacher_{i}'],
                'group': request.form[f'group_{i}']
            })

        time_per_lesson = int(request.form['time_per_lesson'])

        # Perform validation
        total_lesson_time = len(lessons) * time_per_lesson
        total_timeslot_duration = sum([
            (datetime.strptime(t['end_time'], '%H:%M') - datetime.strptime(t['start_time'], '%H:%M')).seconds / 60
            for t in timeslots
        ])

        if total_lesson_time <= total_timeslot_duration:
            # Store the data
            session['timeslots'] = timeslots
            session['rooms'] = rooms
            session['lessons'] = lessons
            
            # Redirect to a new route for processing
            return redirect(url_for('main.getdata'))
        else:
            return "Error: Not enough time slots for all lessons!"

    return render_template('index.html')

@main.route('/schedule')
def schedule():
    formatted_lessons = [format_lesson_for_template(lesson) for lesson in solution.lesson_list]
    return render_template('schedule.html', lessons=formatted_lessons, 
                           timeslots=solution.timeslot_list, 
                           rooms=solution.room_list, 
                           teachers=solution.teacher_list, 
                           student_groups=solution.student_group_list)

@main.route('/solve', methods=['POST'])
def solve():
    return jsonify({'status': 'Solving started'})

@main.route('/solution')
def get_solution():
    formatted_lessons = [format_lesson_for_template(lesson) for lesson in solution.lesson_list]
    return jsonify(formatted_lessons)

@main.route('/getdata')
def getdata():
    timeslots = session.get('timeslots', [])
    rooms = session.get('rooms', [])
    lessons = session.get('lessons', [])
    return render_template('getdata.html',timeslots=timeslots, rooms=rooms, lessons=lessons)

# @main.route('/process_schedule')
# def process_schedule():
#     # Retrieve the data from the session
#     timeslots = session.get('timeslots', [])
#     rooms = session.get('rooms', [])
#     lessons = session.get('lessons', [])
#     time_per_lesson = session.get('time_per_lesson', 0)

#     # Process the data (add your scheduling logic here)
#     # For example:
#     schedule = create_schedule(timeslots, rooms, lessons, time_per_lesson)

#     # Render a template with the processed data
#     return render_template('schedule.html', schedule=schedule)

# def create_schedule(timeslots, rooms, lessons, time_per_lesson):
#     # Implement your scheduling algorithm here
#     # This is just a placeholder function
#     return "Your schedule will be created here