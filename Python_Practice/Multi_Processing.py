from multiprocessing import Process

def func(*args):
    print(args)


if __name__ == "__main__":
    p = Process(target=func, args=[10,20])
    p.start()
    p.join()

