li=[]
tu=[]
se=set()


li.append("first")
li.insert(0,"before first")
li2=["after first"]
li.extend(li2)

print(li)