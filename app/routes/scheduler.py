from flask import Blueprint, render_template, request
from ..utils.scheduler_logic import create_schedule

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        teachers = request.form.getlist('teacher[]')
        time_slots = request.form.getlist('time_slots[]')
        classes_count = request.form.getlist('classes_count[]')
        schedules = create_schedule(teachers, time_slots, [int(count) for count in classes_count])
        return render_template('result.html', schedules=schedules)
    return render_template('index.html')
