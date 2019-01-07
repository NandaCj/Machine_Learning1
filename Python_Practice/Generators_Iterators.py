class Counter(object):
    def __init__(self, low, high):
        self.current = low
        self.high = high

    def __iter__(self):
        'Returns itself as an iterator object'
        return self

    def __next__(self):
        'Returns the next value till current is lower than high'
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1


c = Counter(5, 10)
def foo():
    for i in range(3):
        yield i


f = foo()

print("__Next__",f.__next__())
print("Next:",next(f))

for i in f:
    print(i)

# print("First")
# while True:
#     print(next(c))
#
#
# print("Second")
# for i in c:
#     print(i)


