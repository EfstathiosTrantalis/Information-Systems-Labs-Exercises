a_list = [10 , 12 , 14 , 14 , 16 , 28 , 28 , 30]
new_list=[]

def remove_duplicates(list,new):
    for item in list:
        if item not in new:
            new.append(item)  

remove_duplicates(a_list,new_list)

print("The first list is:",a_list)
print("The new list is:",new_list)

"""def sortList(list):
    list.sort(reverse=True)   The easiest way
"""
def sortList(list):
    
    for i in range(5,0,-1): 
        for item in range(i):
            if list[item] < list[item + 1]:
                x = list[item]
                list[item] = list[item + 1]
                list[item + 1] = x          
    
sortList(new_list)
print("The list in descending order is:", new_list)  

a_dict= {"a":10, "b":12, "c":14, "d":14, "e":16, "f":28, "g":28, "h":30}
new_dict = {}



def remove_dubblicate_dict(dict,new):
    for key,value in dict.items():
        if value not in new.values():
            new[key] = value

    print("The new dictionary is:",new)
            

print("The first dictionary is:",a_dict)        
remove_dubblicate_dict(a_dict,new_dict)



def sortDict(diction):
    
    l = list(diction.items())
    l.sort(reverse = True)
    new = dict(l)
    print("The dictionary in descending order is:", new)


sortDict(new_dict)