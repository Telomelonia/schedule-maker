import threading
import logging
from app.scheduler.optaplanner_scheduler import Lesson, TimeTable, define_constraints
from optapy import solver_manager_create
from optapy.types import SolverConfig, Duration
from app.scheduler.problem import generate_problem
from flask import session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#solver config
solver_config = SolverConfig().withEntityClasses(Lesson) \
    .withSolutionClass(TimeTable) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))
#manager
solver_manager = solver_manager_create(solver_config)

# Global variables to store the solution and solver status
current_solution = None
is_solving = False

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

# Callback function for best solution
def on_best_solution_changed(best_solution):
    global current_solution
    current_solution = best_solution

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

# Function to start the solver
def start_solver():
    global current_solution, is_solving
    if is_solving:
        logger.info("Solver is already running")
        return "Solver is already running"
    
    if current_solution is None:
        logger.info("Generating initial problem")
        current_solution = generate_problem(session.get('timeslots', []),session.get('rooms', []),session.get('lessons', []))
        current_solution.set_student_group_and_teacher_list()
    
    is_solving = True
    logger.info("Starting solver")
    def solve_async():
        global is_solving
        try:
            logger.info("Solver thread started")
            solver_manager.solveAndListen(0, lambda the_id: current_solution, on_best_solution_changed)
            logger.info("Solver finished")
        except Exception as e:
            logger.error(f"Error in solver thread: {str(e)}")
        finally:
            is_solving = False
    
    thread = threading.Thread(target=solve_async)
    thread.start()
    
    return "Solver started"

# Function to get the current solution
def get_current_solution():
    global current_solution
    return current_solution

# Function to check if the solver is currently running
def is_solver_running():
    global is_solving
    return is_solving

# Function to format all lessons
def get_formatted_lessons(solution):
    return [format_lesson_for_template(lesson) for lesson in solution.lesson_list]