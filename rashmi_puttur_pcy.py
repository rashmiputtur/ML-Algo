import sys
import copy
import itertools

#Required data structures and functions
itemsToIntegers = {}
IntegerRep = []
frequentItems = {}
candidate = {}
hashTable = {}
countOfItems = {}

#Read input from command prompt
with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()
supportThreshold = sys.argv[2]
bucketSize = sys.argv[3]

#Map items to integers 
myString = ",".join(lines)
Str = myString.split(',')

counter = 1
for eachStr in Str:
    if(not eachStr in itemsToIntegers):
        itemsToIntegers[eachStr] = counter
        counter = counter + 1


integerMapping = []
for eachLine in lines:
    integerMapping.clear()
    for key in itemsToIntegers.keys():
        if(key in eachLine):
            integerMapping.append(int(itemsToIntegers[key]))
    IntegerRep.append(copy.deepcopy(integerMapping))
     
#Generate all possible pairs in each basket
for rep in IntegerRep:
    allCombinations = itertools.combinations(rep, 2)
    for combination in allCombinations:
        sum = 0
        hashIndex = 0
        for eachItem in combination:
            sum = sum + eachItem
        hashIndex = sum % int(bucketSize)
        if(hashIndex in hashTable):
            hashTable[hashIndex] = hashTable[hashIndex] + 1
        else:
            hashTable[hashIndex] = 1

#Count of all items
for individual_items in Str:
        if(individual_items in countOfItems):
                countOfItems[individual_items] = countOfItems[individual_items] + 1
        else:
                countOfItems[individual_items] = 1 

#Generate the bit map
bitMap = []
for value in hashTable.values():
    if(value >= int(supportThreshold)):
        bitMap.append("1")
    else:
        bitMap.append("0")
        
#PCY Second Pass
def pcy_secondPass(items):
        count = 1
        frequentItems = items
        candidate = frequentItems.copy()
        original_items = list(items.keys())
        while(len(frequentItems) > 0):
            count = count + 1
            candidate.clear()
            frequentItems.clear()
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
                    if(num >= int(supportThreshold)):
                            checkCondition  = True

            if(checkCondition):
                    print()
                    print("Frequent Itemsets of size",count, ":")
                    for key in candidate.keys():
                        if(candidate[key] >= int(supportThreshold)):
                                frequentItems[key] = candidate[key]
                                print(str(' '+','.join(str(i) for i in key).strip("(,)")))
     
#Generate frequent items
itemNumbers = []
for i in range(len(bitMap)):
    if(bitMap[i] == 0):
        for eachInt in IntegerRep:
            for combi in itertools.combinations(eachInt, 2):
                checkSum = 0
                for eachCombi in combi:
                    checkSum = checkSum + eachCombi
                if(i == (checkSum % int(bucketSize))):
                    itemNumbers.append(eachCombi)

frequentItemNumbers = []
for num in itemsToIntegers.values():
    if(not num in itemNumbers):
        frequentItemNumbers.append(num)

flag = False
for item, itemNum in itemsToIntegers.items():
    if itemNum in frequentItemNumbers:
        flag = True
        
if(flag):
    print("Frequent Items of size 1: ")
    for item, itemNum in itemsToIntegers.items():
        if itemNum in frequentItemNumbers:
            if(countOfItems[item] >= int(supportThreshold)):
                print(item)
                frequentItems[item] = countOfItems[item]
else:
    print("No Frequent Items")
pcy_secondPass(frequentItems)               
                
        
        
        
        



