import optapy
from optapy import constraint_provider, planning_entity, planning_id, planning_solution, planning_variable

print("OptaPy imported successfully")

@planning_entity
class TestEntity:
    def __init__(self, id):
        self.id = id

    @planning_id
    def get_id(self):
        return self.id

print("TestEntity defined successfully")

if __name__ == "__main__":
    print("Test completed")