
class Executor():
    def __init__(self, name, work_func):
        self.name = name
        self.work_func = work_func

    def work(self, value):
        self.work_func(value)
        
