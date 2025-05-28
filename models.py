# class Person
# 속성: name, role, available_time


class Person:
    def __init__(self, name, role, available_time):
        self.name = name
        self.role = role
        self.available_time = available_time

    def __repr__(self):
        return f"Person(name={self.name}, role={self.role}, available_time={self.available_time})"