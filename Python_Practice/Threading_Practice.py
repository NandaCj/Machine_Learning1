import threading

class Thread_Practice (threading.Thread):
    def __init__(self):
        super(Thread_Practice, self).__init__()

    def run(self):
        print ("RUN Function")
        for i in range(20):
            self.func()

    def func(self):
        print ("Func Running")

if __name__ == '__main__':
    Thread_Practice().start()