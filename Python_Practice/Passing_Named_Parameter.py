def func(name, age, company="Hcl", nation="India"):
    print (name, age, company, nation)

def func2(*args):
    print (args)

func("Nandha", 26, "ACC", "TamilNadu")
func2("Nandha", 26, "ACC", "TamilNadu")