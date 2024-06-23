from flask import Blueprint, render_template, request
from ..utils.planner_logic import solve_schedule

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')

@planner_bp.route('/', methods=['GET', 'POST'])
def planner():
    if request.method == 'POST':
        # Assume form data is collected here
        # You'll need to adjust this based on the actual form fields
        num_teachers = int(request.form.get('num_teachers', 3))
        num_days = int(request.form.get('num_days', 7))
        num_slots_per_day = int(request.form.get('num_slots_per_day', 10))

        # Call the scheduler
        schedule = solve_schedule(num_teachers, num_days, num_slots_per_day)
        return render_template('result.html', schedule=schedule)
    
    return render_template('planner.html')
