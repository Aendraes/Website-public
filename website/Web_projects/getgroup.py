from random import shuffle

def getgroups(groupstring,groupnumber):
    """Gets a group from randomized list."""
    group = groupstring.split(",")
    for person in range(len(group)):
        group[person] = group[person].strip()
    shuffle(group)
    grouplist=[]
    for x in range(groupnumber):
            grouplist.append(list())

    while len(group) > 0:
        x=0
        for y in range(groupnumber):
            try:
                grouplist[y].append(group[0])
                group.pop(0)
            except:
                break;
        x = x+1
    return grouplist