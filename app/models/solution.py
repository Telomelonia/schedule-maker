from optapy import solver_manager_create
from optapy.types import SolverConfig, Duration
from ipywidgets import Tab
from ipysheet import sheet, cell, row, column, cell_range
from domain import Lesson, TimeTable
from GenerateProblem import generate_problem
from constraints import define_constraints
import tkinter as tk
from tkinter import ttk

solver_config = SolverConfig().withEntityClasses(Lesson) \
    .withSolutionClass(TimeTable) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))


solution = generate_problem()
solution.set_student_group_and_teacher_list()

cell_map = dict()

def pick_color(subject):
    color_map = {
        'Math': 'blue',
        'Physics': 'green',
        'Chemistry': 'red',
        'Spanish': 'yellow',
        'French': 'orange',
        'English': 'purple',
        'Biology': 'brown',
        'History': 'pink',
        'Geography':'cyan'
    }
    return color_map.get(subject, 'gray')

def on_best_solution_changed(best_solution):
    global timetable
    global solution
    global cell_map
    solution = best_solution
    unassigned_lessons = []
    clear_cell_set = set()
    
    for (table_name, table_map) in cell_map.items():
        for (key, cell) in table_map.items():
            clear_cell_set.add(cell)
            
    for lesson in solution.lesson_list:
        if lesson.timeslot is None or lesson.room is None:
            unassigned_lessons.append(lesson, clear_cell_set)
        else:
            update_lesson_in_table(lesson, clear_cell_set)
            
    for cell in clear_cell_set:
            cell.value = ""
            cell.style["backgroundColor"] = "white"
            
    for (table_name, table_map) in cell_map.items():
        for (key, cell) in table_map.items():
            cell.send_state()

def update_lesson_in_table(lesson, clear_cell_set):
    global cell_map
    x = solution.timeslot_list.index(lesson.timeslot)
    room_column = solution.room_list.index(lesson.room)
    teacher_column = solution.teacher_list.index(lesson.teacher)
    student_group_column = solution.student_group_list.index(lesson.student_group)
    color = pick_color(lesson.subject)


    room_cell = cell_map['room'][(x, room_column)]
    teacher_cell = cell_map['teacher'][(x, teacher_column)]
    student_group_cell = cell_map['student_group'][(x, student_group_column)]
    
    clear_cell_set.discard(room_cell)
    clear_cell_set.discard(teacher_cell)
    clear_cell_set.discard(student_group_cell)

    room_cell.value = f"{lesson.subject}\n{lesson.teacher}\n{lesson.student_group}"
    room_cell.style["backgroundColor"] = color
    room_cell.send_state()

    teacher_cell.value = f"{lesson.room.name}\n{lesson.subject}\n{lesson.student_group}"
    teacher_cell.style["backgroundColor"] = color
    teacher_cell.send_state()

    student_group_cell.value = f"{lesson.room.name}\n{lesson.subject}\n{lesson.teacher}"
    student_group_cell.style["backgroundColor"] = color
    student_group_cell.send_state()

    
def create_table(table_name, solution, columns, name_map):
    global cell_map
    out = sheet(rows=len(solution.timeslot_list) + 1, columns=len(columns) + 1)
    header_color = "#22222222"
    cell(0,0, read_only=True, background_color=header_color)
    header_row = row(0, list(map(name_map, columns)), column_start=1, read_only=True,
                    background_color=header_color)
    timeslot_column = column(0,
            list(map(lambda timeslot: timeslot.day_of_week[0:3] + " " + str(timeslot.start_time)[0:10],
                             solution.timeslot_list)), row_start=1, read_only=True, background_color=header_color)

    table_cells = dict()
    cell_map[table_name] = table_cells
    for x in range(len(solution.timeslot_list)):
        for y in range(len(columns)):
            table_cells[(x, y)] = cell(x + 1, y + 1, "", read_only=True)
    return out
        
solver_manager = solver_manager_create(solver_config)

by_room_table = create_table('room', solution, solution.room_list, lambda room: room.name)
by_teacher_table = create_table('teacher', solution, solution.teacher_list, lambda teacher: teacher)
by_student_group_table = create_table('student_group', solution, solution.student_group_list,
                                      lambda student_group: student_group)

solver_manager.solveAndListen(0, lambda the_id: solution, on_best_solution_changed)

tab = Tab()
tab.children = [by_room_table, by_teacher_table, by_student_group_table]

tab.set_title(0, 'By Room')
tab.set_title(1, 'By Teacher')
tab.set_title(2, 'By Student Group')

tab