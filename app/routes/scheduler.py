from flask import Blueprint, render_template, request
from app.scheduler.optaplanner_scheduler import create_schedule

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lectures = [
            {"id": f"L{i}", "course": request.form[f'course_{i}'], "teacher": request.form[f'teacher_{i}'], "duration": int(request.form[f'duration_{i}'])}
            for i in range(1, int(request.form['lecture_count']) + 1)
        ]
        rooms = request.form['rooms'].split(',')
        time_slots = range(int(request.form['time_slots']))
        
        schedule = create_schedule(lectures, time_slots, rooms)
        return render_template('result.html', schedule=schedule)
    return render_template('index.html')