import optapy
from optapy import constraint_provider, planning_entity, planning_id, planning_solution, planning_variable

@planning_entity
class Lecture:
    def __init__(self, id, course, teacher, duration):
        self.id = id
        self.course = course
        self.teacher = teacher
        self.duration = duration
        self.time_slot = None
        self.room = None

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(int, value_range_provider_refs=["time_slots"])
    def get_time_slot(self):
        return self.time_slot

    def set_time_slot(self, time_slot):
        self.time_slot = time_slot

    @planning_variable(str, value_range_provider_refs=["rooms"])
    def get_room(self):
        return self.room

    def set_room(self, room):
        self.room = room

@planning_solution
class Schedule:
    def __init__(self, lectures, time_slots, rooms):
        self.lectures = lectures
        self.time_slots = time_slots
        self.rooms = rooms

    @optapy.problem_fact_collection_property(int)
    def get_time_slots(self):
        return self.time_slots

    @optapy.problem_fact_collection_property(str)
    def get_rooms(self):
        return self.rooms

    @optapy.planning_entity_collection_property(Lecture)
    def get_lectures(self):
        return self.lectures

@constraint_provider
def define_constraints(constraint_factory):
    return [
        # Room conflict: no two lectures in the same room at the same time
        constraint_factory.for_each(Lecture)
            .join(Lecture,
                  optapy.Joiners.equal(lambda l: l.time_slot),
                  optapy.Joiners.equal(lambda l: l.room),
                  optapy.Joiners.filtering(lambda l1, l2: l1.id != l2.id))
            .penalize("Room conflict", optapy.score.HardSoftScore.ONE_HARD),

        # Teacher conflict: no teacher can give two lectures at the same time
        constraint_factory.for_each(Lecture)
            .join(Lecture,
                  optapy.Joiners.equal(lambda l: l.time_slot),
                  optapy.Joiners.equal(lambda l: l.teacher),
                  optapy.Joiners.filtering(lambda l1, l2: l1.id != l2.id))
            .penalize("Teacher conflict", optapy.score.HardSoftScore.ONE_HARD),
    ]

def create_schedule(lectures_data, time_slots, rooms):
    lectures = [Lecture(l['id'], l['course'], l['teacher'], l['duration']) for l in lectures_data]
    problem = Schedule(lectures, time_slots, rooms)
    solver = optapy.solver_factory_create(Schedule).buildSolver()
    solution = solver.solve(problem)
    return solution.get_lectures()