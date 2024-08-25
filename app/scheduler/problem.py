from app.scheduler.optaplanner_scheduler import Timeslot, Room, Lesson, TimeTable
import datetime
from datetime import time

def generate_problem(timeslots_data, rooms_data, lessons_data):
    # Convert user-entered timeslots to Timeslot objects
    timeslot_list = []
    for i, timeslot in enumerate(timeslots_data):
        timeslot_list.append(
            Timeslot(i + 1, timeslot['weekday'], 
                     datetime.strptime(timeslot['start_time'], '%H:%M').time(), 
                     datetime.strptime(timeslot['end_time'], '%H:%M').time())
        )
    
    # Convert user-entered rooms to Room objects
    room_list = []
    for i, room in enumerate(rooms_data):
        room_list.append(Room(i + 1, room['name']))
    
    # Convert user-entered lessons to Lesson objects
    lesson_list = []
    for i, lesson in enumerate(lessons_data):
        lesson_list.append(Lesson(i + 1, lesson['subject'], lesson['teacher'], lesson['group']))
    
    # Example: Assign the first lesson to the first timeslot and room (can be expanded with logic)
    lesson = lesson_list[0]
    lesson.set_timeslot(timeslot_list[0])
    lesson.set_room(room_list[0])

    return TimeTable(timeslot_list, room_list, lesson_list)
