import sys
import itertools

#Required data structures and functions
items_to_integers = {}
frequent_items_pass1 = {}
candidate = {}

#Read input from command prompt
with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()
support_threshold = sys.argv[2]

#Map items to integers and count the individual items 
myString = ",".join(lines)
Str = myString.split(',')

for individual_items in Str:
        if(individual_items in items_to_integers):
                items_to_integers[individual_items] = items_to_integers[individual_items] + 1
        else:
                items_to_integers[individual_items] = 1

#Apriori Second Pass
def apriori_secondPass(items):
        count = 1
        frequent_items = items
        candidate = frequent_items.copy()
        original_items = list(items.keys())
        while(len(frequent_items) > 0):
            count = count + 1
            candidate.clear()
            frequent_items.clear()
            for candidate_itemSet in itertools.combinations(original_items, count):
                        for each_line in set(lines):
                                x = each_line.split(',')
                                if set(candidate_itemSet).issubset(set(x)):
                                        if((candidate_itemSet) in candidate):
                                                candidate[candidate_itemSet] = candidate[candidate_itemSet] + 1
                                        else:
                                                candidate[candidate_itemSet] = 1      
            checkCondition = False        
            for num in candidate.values():
                    if(num >= int(support_threshold)):
                            checkCondition  = True

            if(checkCondition):
                    print()
                    print("Frequent Itemsets of size",count, ":")
                    for key in candidate.keys():
                        if(candidate[key] >= int(support_threshold)):
                                frequent_items[key] = candidate[key]
                                print(str(' '+','.join(str(i) for i in key).strip("(,)")))

#frequent items of size 1

flag = False
for key in items_to_integers.keys():
        if(items_to_integers[key] >= int(support_threshold)):
                flag = True
if(flag):
    print("Frequent Itemsets of size 1 : ")
    for key in items_to_integers.keys():
        if(items_to_integers[key] >= int(support_threshold)):
                print(key)
                frequent_items_pass1[key] = items_to_integers[key]
else:
    print("No frequent items")
apriori_secondPass(frequent_items_pass1)
