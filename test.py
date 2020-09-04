if __name__=="__main__":
    ttt = ['"40"', '"282"', '"Sprint Sprint 1"', None, '"future"', None, None, None]
    aaa = [1,3]
    aaa.sort(reverse=True)
    print(aaa)
    
    
    print(aaa)


    bb = {"test":"test", "test1":"test1"}
    cc = {"test4":"test2", "test1":"test3"}

    dd = {**bb, **cc}
    print(dd)


    bbbbb = [3,5]
    ddd = []
    ddd = [ *ddd, *aaa ]
    print(ddd)