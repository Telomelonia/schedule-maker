from app.scheduler.solver import start_solver, get_current_solution, get_formatted_lessons, is_solver_running
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime

def pick_color(subject):
    color_map = {
        'Math': 'blue',
        'Physics': 'green',
        'Chemistry': 'red',
        'Spanish': 'yellow',
        'French': 'orange',
        'English': 'lime',
        'Biology': 'brown',
        'History': 'pink',
        'Geography':'cyan'
    }
    return color_map.get(subject, 'gray')

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

@main.route('/error')
def error():
    return render_template('error.html')
@main.route('/solver_status')
def solver_status():
    return jsonify({
        "is_running": is_solver_running(),
        "has_solution": get_current_solution() is not None
    })

@main.route('/get_solution')
def display_solution():
    solution = get_current_solution()
    if not solution:
        return jsonify({"error": "No solution available. Please start the solver first."})
    
    formatted_lessons = get_formatted_lessons(solution)
    
    subject_colors = {lesson['subject']: lesson['color'] for lesson in formatted_lessons}
    
    return jsonify({
        "lessons": formatted_lessons,
        "rooms": [room.name for room in solution.room_list],
        "teachers": solution.teacher_list,
        "student_groups": solution.student_group_list,
        "timeslots": [str(timeslot) for timeslot in solution.timeslot_list],
        "subject_colors": subject_colors
    })

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