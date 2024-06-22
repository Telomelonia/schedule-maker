from constraint import Problem

def create_schedule(teacher, subject, num_classes):
    problem = Problem()
    times = ['Day{}-Slot{}'.format(day, slot) for day in range(1, 6) for slot in range(1, 4)]

    # Add variables for the teacher's schedule
    problem.addVariable(teacher, times)

    # Dummy constraint for demonstration
    problem.addConstraint(lambda x: x.endswith('1'), [teacher])  # Teacher prefers Slot 1

    # Retrieve solutions
    solutions = problem.getSolutions()
    return solutions
