
class Parent():
    def __init__(self):
        print("Inside Parent...")
        self.Parent_Name = 'Nandha'

    def get_parent_name(self):
        print("Parent Get Parent Method ")
        print(self.Parent_Name)

class Child(Parent):

    def __init__(self):
        print("Inside Child...")
        super().__init__()

    def get_parent_name(self):
        print("Child Get Parent Method ")
        print(self.Parent_Name)


if __name__ == "__main__":
    # Parent().get_parent_name()
    Child().get_parent_name()