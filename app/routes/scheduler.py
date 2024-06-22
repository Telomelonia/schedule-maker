from flask import Blueprint, render_template, request
from ..utils.scheduler_logic import create_schedule

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        teacher = request.form['teacher']
        subject = request.form['subject']
        num_classes = int(request.form['classesCount'])
        schedule = create_schedule(teacher, subject, num_classes)
        return render_template('result.html', schedule=schedule)
    return render_template('index.html')
