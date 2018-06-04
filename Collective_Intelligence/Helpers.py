def Dict_Print(Dict):
    for key, value in Dict.items():
        if not isinstance(value, dict):
            print ("    ",key, "--->", value)
        else:
            print (key)
            Dict_Print(value)

