from ortools.sat.python import cp_model

def solve_schedule(num_teachers, num_days, num_slots_per_day):
    model = cp_model.CpModel()

    # Create variables
    schedules = {}
    for teacher in range(num_teachers):
        for day in range(num_days):
            for slot in range(num_slots_per_day):
                schedules[(teacher, day, slot)] = model.NewBoolVar(f'schedule_t{teacher}_d{day}_s{slot}')

    # Add constraints
    for teacher in range(num_teachers):
        for day in range(num_days):
            model.Add(sum(schedules[(teacher, day, slot)] for slot in range(num_slots_per_day)) <= 1)

    # Solver configuration
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = [[None for _ in range(num_slots_per_day)] for _ in range(num_days)]
        for day in range(num_days):
            for slot in range(num_slots_per_day):
                for teacher in range(num_teachers):
                    if solver.Value(schedules[(teacher, day, slot)]):
                        result[day][slot] = teacher
        return result
    else:
        return None
