def func(**args):
    print(args.items())
if __name__=="__main__":
    data = {"a":"A", "b":"B"}
    
    func(**data)