x#Python Script to implement the AdaBoost Algorithm 
import sys
import math

#Compute the Entropy
def computeEntropy(data, D):
    entropy = {}
    numP= {}
    numE ={}
    denom ={}
        
    for i in range(1,len(data[0])):       
        numP[i] = {}
        numE[i] ={}
        denom[i] = {}
        entropy[i] ={}
    
    #Compute the weighted probabilities
    col = 1
    row =0    
    while(col< len(data[0])):
        for row in range(0,len(data)):
            y = data[row][0]        
            if(data[row][col] in denom.get(col, {})):
                denom[col][data[row][col]] = denom[col][data[row][col]] + D[row]
            else:
                denom[col][data[row][col]] = D[row]     
            
            if(y == 'p'):
                if(data[row][col] in numP.get(col,{})):
                    numP[col][data[row][col]] = numP[col][data[row][col]] + D[row]
                else:
                    numP[col][data[row][col]] = D[row]
           
            elif(y == 'e'):
                if(data[row][col] in numE.get(col,{})):
                    numE[col][data[row][col]] = numE[col][data[row][col]] + D[row]  
                else:
                    numE[col][data[row][col]] = D[row]                
        col =col +1
    
    #Compute the entropy
    for col in range(1, len(data[0])):
        term1 = 0.0
        term2 = 0.0
        x1 = 0.0
        x2 = 0.0
        y1 = numP[col]
        y2 = numE[col] 
        for key in denom[col]:
            if(key in y1):
                x1 = numP[col][key]
            if(key in y2):
                x2 = numE[col][key]
            denominator = denom[col][key]
            if(x1 != 0):
                term1 = -(float(float(x1)/float(denominator)*(math.log((float(x1)/(float(denominator))), 2))))
            if(x2 !=0 ):
                term2 = -(float(float(x2)/float(denominator)*(math.log((float(x2)/(float(denominator))), 2)))) 
            entropy[col][key] = float((term1 + term2))
   
    pCount = 0.0
    eCount = 0.0
    d = 0.0
    
    for x in range(0,len(data)):
        d = d + D[x]
    
    for i in range(0,len(data)):
        c = data[i][0]
        if(c=='p'):
            pCount = pCount + D[i]
        elif(c=='e'):
            eCount = eCount + D[i]
    
    entropy['S'] = float(- 
                          ( 
                            float(float(float(pCount)/float(d))* float(float(math.log((float(pCount)/float(d)),2)))) + 
                            float(float(float(eCount)/float(d))* float(float(math.log((float(eCount)/float(d)),2))))
                           )           
                        ) 
    return entropy

#Compute information gain
def computeGain(entropy,data,D):
    gain = {}
    count = {}
    totals = {}
    
    for x in range(1,len(data[0])):
        totals[x] =0
        count[x] = {}
    
    for j in range(1, len(data[0])):
        for i in range(0, len(data)):
            totals[j] = totals[j] + D[i]
            
    for j in range(1, len(data[0])):
        for i in  range(0,len(data)):
            row = data[i][j]
            if(row in count[j]):
                count[j][row]  =  count[j][row] + D[i]
            else:
                count[j][row] = D[i]
    #Compute the gain
    for j in range(1, len(data[0])):
        temp = 0.0
        for keys in entropy[j].keys():
            temp = temp  + float((count[j][keys]/totals[j]) * entropy[j][keys])
        gain[j] = entropy['S'] - float(temp)  
    return gain  

def train(data, D,p,e):
    #Compute entropy and information gain
    entropy = computeEntropy(data, D)
    gain = computeGain(entropy, data, D)
    max = 0
    split = ''
    splitValues = []
    for key in gain.keys():
        if(gain[key] > max):
            max = gain[key]
            split = key
    for row in range(0,len(data)):
        if(data[row][split] not in splitValues):
            splitValues.append(data[row][split])
    return split, splitValues

#Function to obtain the classification
def classify(data,splitA, splitVal, D):
    ht = {}
    sumP = {}
    sumE = {}
    C= {}
    for v in splitVal:
        sumP[v] = 0.0
        sumE[v] = 0.0
        C[v] = ''
    
    for r in range(0,len(data)):     
        x = data[r][splitA]
        if(data[r][0] == 'p'):        
                sumP[x] =  sumP[x] + D[r]
        elif(data[r][0] =='e'):
                sumE[x] = sumE[x] + D[r]
    
    for row in range(0,len(data)): 
        r= data[row][splitA]
        wP = sumP[r]
        wE = sumE[r]
        if(wP >= wE):
            ht[row] = 'p'            
        else:
            ht[row] ='e'
            
    for y in splitVal:
        if(sumP[y] > sumE[y]):
            C[y] ='p'
        else:
            C[y] = 'e'
    C['Attr'] = splitA
    return ht, C

#Function to compute the error
def computeError(ht, data, D):
    count = 0.0
    for row in range(0,len(data)):
        if(data[row][0] != ht[row]):
            count = count + (D[row])
    epsilon = float(float(count) / float(len(data)))
    return epsilon

#Function to compute alpha
def computeAlpha(error):
    alpha = float(0.5* float( math.log((1-error)/error)))
    return alpha

#Function to update probability distributions
def updateProbabilityDistributions(D,alpha,prediction, data):
    sum=0.0
    #Compute Z Score
    for i in range(0, len(data)):
        ex = float(math.exp(-(alpha*classes[data[i][0]]*classes[prediction[i]])))
        sum = sum + ((D[i])*ex)
    Zscore = sum

    for row in range(0,len(data)):
        numerator = 0.0
        y= data[row][0]
        h= prediction[row]
        exponent = float(math.exp(-(alpha*classes[y]*classes[h])))
        oldD = D[row]
        numerator = oldD*exponent
        D[row] = numerator/Zscore        
    return D

#Function to obtain the final classifier
def finalClassifier(a,testing,predict):
    predictedClass = {}
    finalPrediction = {}
    
    for m in range(1, int(iterations) + 1):
        predictedClass[m] ={}
            
    for i in range(1, int(iterations) +1):
        for row in range(0,len(testing)):
            x = testing[row]
            currentPrediction = predict[i]
            attr = x[currentPrediction['Attr']]
            if(attr not in currentPrediction):
                currentPrediction[attr] = 'p' 
            predictedClass[i][row] = currentPrediction[attr]
    
    for r in range(0,len(testing)):
        sum = 0.0
        for t in range(1, int(iterations)):
            sum = sum  + float((a[t]* classes[predictedClass[t][r]]))
        if(sum<0):
            for k,v in classes.items():
                if(v==-1):
                    finalPrediction[r] = k
        elif(sum>0):
            for k,v in classes.items():
                if(v==1):
                    finalPrediction[r] = k
    return finalPrediction

#Function to compute testing accuracy
def computeAccuracy(test, predicted):
    num = 0
    for i in range(0,len(test)):
        if(test[i][0] != predicted[i]):
            num = num +1
    accuracy = (float(float(len(test) -num)/float(len(test)))) * 100
    return accuracy

#Function to compute the conditional probability
def computeConditionalProbability(data):
    p={}
    e={}
    
    pCount = 0;
    eCount = 0;
    for eachLine in data:
        if(eachLine[0] == 'p'):
            pCount = pCount+1
        elif(eachLine[0] == 'e'):
            eCount = eCount +1
    p['p'] = pCount
    e['e'] = eCount
    length = len(data) 
    #Initialize the dictionary
    for x in range(1,len(data[1])):
        p[x] = {};
        e[x] ={};

#Construct the conditional probability table   
    for i in range(1, length):
        row = data[i]
        clas = row[0]
        for j in range(1,len(row)):
            if(clas =='p'):
                if(row[j] in p[j]):
                    p[j][row[j]] = p[j][row[j]] + 1
                else:
                    p[j][row[j]] = 1
            elif(clas == 'e'):
                if(row[j] in e[j]):
                    e[j][row[j]] = e[j][row[j]] + 1
                else:
                    e[j][row[j]] = 1
    
    return p,e

#Obtain command line arguments
iterations  =0
trainData =""
testData =""
if(len(sys.argv)!=4):
    print "Enter the correct number of arguments"
else:
    iterations = sys.argv[1]
    trainData = sys.argv[2]
    testData = sys.argv[3]

#Read the input file 
with open(trainData, 'r') as f:
    lines=f.read().splitlines()
dataSet =[]
for eachLine in lines:
    dataSet.append(eachLine.split('\t'))
length = len(dataSet[0])

with open(testData, 'r') as f1:
    temp=f1.read().splitlines()
test =[]
for x in temp:
    test.append(x.split('\t'))

#Map class into integers 
classes = {}
classes['p'] = -1;
classes['e'] = 1;
p,e=computeConditionalProbability(dataSet)


#Initial probability distribution 
D= {}
m = len(dataSet)

for i in range(0,m):
    D[i]= float(float(1)/float(m))
        
accuracies={}
predictions ={}

#AdaBoost Algorithm
for t in range (1,int(iterations)+1):  
    #Train the weak learner using Dt
    splitAttr, splitAttrValues = train(dataSet,D,p,e)
    #Get weak classifier
    ht,C = classify(dataSet, splitAttr, splitAttrValues,D)
    predictions[t] = C
    #Determine the classification error
    et = computeError(ht,dataSet , D)
    #Compute alpha
    at = computeAlpha(et)
    accuracies[t] = at
    #Update Probability Distributions
    D = updateProbabilityDistributions(D, at, ht, dataSet)

#Final classifier output
output = finalClassifier(accuracies,test,predictions)

#Compute testing accuracy
acc = computeAccuracy(test, output)

#print output
print acc
for accuracy in accuracies:
    print accuracies[accuracy]
