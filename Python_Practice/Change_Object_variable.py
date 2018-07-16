class Test ():
    def __init__(self, host , port, x=10):
        self.host = host
        self.port = port
        print (self.host, self.port)

test = Test(port="10.0.10.113", host=22)

print (test.host, test.port)
