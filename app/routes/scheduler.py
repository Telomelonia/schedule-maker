from flask import Blueprint, render_template, request
from ..utils.scheduler_logic import create_schedule, optimize_schedule

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        teachers = request.form.getlist('teacher[]')
        num_classes = request.form.getlist('num_classes[]')
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Prepare data for scheduling
        schedules_data = []
        for index, teacher in enumerate(teachers):
            availability = {}
            for day in days:
                start_times = request.form.getlist(f'{day}_start[]')
                end_times = request.form.getlist(f'{day}_end[]')
                if start_times[index] and end_times[index]:  # Ensure both times are provided
                    availability[day] = (start_times[index], end_times[index])
            if availability:  # Only add if there is some availability
                schedules_data.append((teacher, availability, int(num_classes[index])))

        # Generate schedules using the collected data
        schedule_matrix = create_schedule(schedules_data)
        optimized_matrix = optimize_schedule(schedule_matrix)

        return render_template('result.html', schedule=optimized_matrix)

    return render_template('index.html')
