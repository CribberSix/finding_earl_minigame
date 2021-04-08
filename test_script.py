import yaml
import json

with open('./ressources/map/items.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data["2"])


#print(json.dumps(data, indent=1))  # pretty-print JSON with indents

l = [1,2]
print(l[1])
# print(l[2])

mylist = [1,2,3,4,5]
for i, x in enumerate(mylist):
    if i == 0:
        print("first item", x)
    elif i == len(mylist) -1 :
        print("last item", x)
    else:
        print(x)

mylist = ["This", "2dsfa", "that"]
print("iwthout", mylist.index("with"))

mylist = ["This", "with", "that"]
print("with", mylist.index("with"))