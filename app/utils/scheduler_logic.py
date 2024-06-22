from constraint import Problem

def create_schedule(teachers, time_slots, num_classes):
    problem = Problem()
    
    # Convert string time slots into lists
    time_slot_lists = [slot.split(', ') for slot in time_slots]

    # Add variables for each teacher, where the domain is their available time slots
    for teacher, slots in zip(teachers, time_slot_lists):
        problem.addVariable(teacher, slots)

    # Add a constraint that no two teachers can have a class at the same time
    problem.addConstraint(lambda *args: len(set(args)) == len(args), teachers)

    # Try to find multiple solutions
    solutions = problem.getSolutions()
    return solutions[:5]  # Return top 5 solutions for simplicity
