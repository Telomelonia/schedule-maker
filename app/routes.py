from flask import Blueprint, render_template
from .solver_logic import setup_solver, solve_problem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    timetable = solve_problem()
    return render_template('index.html', timetable=timetable)
