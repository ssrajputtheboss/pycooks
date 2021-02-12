#for finding value of a key in json
global attr_stack
attr_stack = []

def get(data , target):
    if isinstance( data , list ):
        for i in data  :
            k = get( i ,  target )
            if k!= None:
                return k
    if isinstance( data , dict ):
        for k in data.keys():
            if k == target:
                return data[k]
        for v in data.values():
            k = get( v ,  target )
            if k!= None:
                return k
def getaddr( data , target ):
    attr_stack = []
    addr = get_target_address( data , target )
    try:
        pass
    except:
        pass
def get_target_address( data , target ):
    if isinstance( data , list ):
        t=0
        for i in data :
            attr_stack.append(t)
            k = get_target_address( i ,  target )
            if k!= None:
                return k
            t+=1
            attr_stack.pop()
    if isinstance( data , dict ):
        for k in data.keys():
            attr_stack.append(k)
            if k == target:
                return attr_stack
            attr_stack.pop()
        for i,v in data.items():
            attr_stack.append(i)
            k = get_target_address( v ,  target )
            if k!= None:
                return k
            attr_stack.pop()
if __name__ == "__main__":
    data = eval(input())
    print(get(data,'temp'))
    print(getaddr(data,'temp'))
    print(data['main']['temp'])
