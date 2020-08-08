from config import config 

def abcd(**args):
    print(len(args))
    for key, value in args.items():
        print(key, value)



if __name__=="__main__":
    
    abcd(arg1 = "abcd", arg2 = "efg")