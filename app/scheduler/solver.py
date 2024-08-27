from app.scheduler.optaplanner_scheduler import Duration, Lesson, TimeTable, define_constraints
from optapy import solver_manager_create
from optapy.types import SolverConfig
from flask import session
from app.scheduler.problem import generate_problem
#solver
solver_config = SolverConfig().withEntityClasses(Lesson) \
    .withSolutionClass(TimeTable) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solution = generate_problem()
solution.set_student_group_and_teacher_list()

solver_manager = solver_manager_create(solver_config)

# color
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
#store the best solution
def on_best_solution_changed(best_solution):
    global solution
    solution = best_solution
    session['solution'] = best_solution
# format the lesson data to show
def format_lesson_for_template(lesson):
    return {
        'subject': lesson.subject,
        'teacher': lesson.teacher,
        'student_group': lesson.student_group,
        'room': lesson.room.name if lesson.room else None,
        'timeslot': f"{lesson.timeslot.day_of_week[0:3]} {lesson.timeslot.start_time}" if lesson.timeslot else None,
        'color': pick_color(lesson.subject)
    }


