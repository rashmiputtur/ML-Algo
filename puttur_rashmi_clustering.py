import sys
import math

#Read the command line arguments
File = ""
iterations = 0
initial = ""

if(len(sys.argv) ==0 ):
    print("Please enter the arguments")
else:
    File = sys.argv[1]
    k = sys.argv[2]
    iterations = sys.argv[3]
    initial = sys.argv[4]
       
#Read the initial points and input files 
dataFile = []
initialPoints = []
dataSet = []

with open(File, 'r') as f:
    dataFile = f.read().splitlines();
with open(initial, 'r') as f1:
    initialPoints = f1.read().splitlines();
  
#Compute distances to each centroid 
def computeDistances(point):
    distances = {}
    u1 = float(point[0])
    v1 = float(point[1])
    w1 = float(point[2])
    x1 = float(point[3])
    for eachCluster in initialPoints:     
        cluster = (str(eachCluster).split(','))
        u2 = float(cluster[0])
        v2 = float(cluster[1])
        w2 = float(cluster[2])
        x2 = float(cluster[3])
        label = cluster[4]
        term1 = float(((u1-u2)*(u1-u2)))
        term2 = float(((v1-v2) * (v1-v2)))
        term3 = float(((w1-w2) * (w1-w2)))
        term4 = float(((x1-x2) * (x1-x2)))
        term =  float(math.sqrt(term1 + term2 + term3 + term4))
        dist =  (math.sqrt(term))   
        distances[label] = dist
    return distances

#Compute centroid of a cluster
def centroid(cluster):   
    #Obtain class name
    label = ""
    setosaCount = 0
    virginicaCount = 0
    versicolorCount = 0
    count = {}
    pwidth = 0.0
    plength = 0.0
    swidth = 0.0
    slength = 0.0
    sLenCentroid = 0.0
    sWidCentroid = 0.0
    pLenCentroid = 0.0
    pWidCentroid = 0.0
    
    for x in cluster:
        if("Iris-setosa" in x):
            setosaCount = setosaCount + 1
        if("Iris-virginica" in x):
            virginicaCount = virginicaCount + 1
        if("Iris-versicolor" in x):
            versicolorCount =  versicolorCount + 1
    count["Iris-setosa"] = setosaCount
    count["Iris-virginica"] = virginicaCount
    count["Iris-versicolor"] = versicolorCount
    
    majority = max(setosaCount, versicolorCount, virginicaCount)
    for key in count.keys():
        if(count[key] == majority):
            label = key
   
    for eachPoint in cluster:
        temp = (str(eachPoint).split(','))
       
        slength = (slength) + float(temp[0])
        swidth = (swidth) + float(temp[1])
        plength = (plength) + float(temp[2])
        pwidth = (pwidth) + float(temp[3])
        
        sLenCentroid = float(slength/len(cluster))
        sWidCentroid = float(swidth/len(cluster))
        pLenCentroid = float(plength/len(cluster))
        pWidCentroid = float(pwidth/len(cluster))
        
    newCentroid = str(sLenCentroid) + ',' + str(sWidCentroid) + ',' + str(pLenCentroid) + ',' + str(pWidCentroid) + ',' +  label
    return  newCentroid
        
#k-means algorithm
i = 0
misplaced = []
setosa = []
versicolor = []
virginica = []
while(i < int(iterations)):
    setosa.clear()
    versicolor.clear()
    virginica.clear()
    #Assign each point to a cluster
    for eachLine in dataFile:
        label = ""  
        point = str(eachLine).split(',')
        finalstr = point[0] + ',' + point[1] + ',' + point[2] + ',' + point[3] + ',' + point[4];
        #Obtain different distances
        distances = computeDistances(point)
        minimum = (min(distances.values()))
        for keySet in distances.keys():
            if(distances[keySet] == minimum):
                label = keySet
        if("setosa" in label):
            setosa.append(finalstr)
        if("versicolor" in label):
            versicolor.append(finalstr)
        if("virginica" in label):
            virginica.append(finalstr)   
    
    #Calculate new centroid
    centroid1 = centroid(setosa);
    centroid2 = centroid(virginica);
    centroid3 = centroid(versicolor);
    initialPoints.clear()
    initialPoints.append(centroid1)
    initialPoints.append(centroid2)
    initialPoints.append(centroid3)
    i = i+1 
    
#Compute number of wrong assignments
for m in setosa:
    if(str(m).split(',')[4] != "Iris-setosa"):
        misplaced.append(m)

for n in versicolor:
    if(str(n).split(',')[4] != "Iris-versicolor"):
        misplaced.append(n)
    

for o in virginica:
    if(str(o).split(',')[4] != "Iris-virginica"):
        misplaced.append(o)
    

#Print results          
print("cluster : Iris-setosa")
for eachSetosa in setosa:
    print(eachSetosa)
print()
print("cluster : Iris-versicolor")
for eachVersicolor in versicolor:
    print(eachVersicolor)
print()
print("cluster : Iris-virginica")
for eachVirginica in virginica:
    print(eachVirginica)
print()
print("Number of points wrongly assigned")
print(len((misplaced)))

