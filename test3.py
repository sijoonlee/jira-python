def myfunc(obj):
    
    return obj["v"]



if __name__ == "__main__":
    a = {"v":1}
    b = {"v":2}
    c = {"v":3}
    x = map(myfunc, (a, b, c))

    print(x)

    #convert the map into a list, for readability:
    print(list(x))