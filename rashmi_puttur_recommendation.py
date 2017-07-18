'''
Created on Apr 17, 2015

@author: Rashmi Puttur
'''
from __future__ import division

import sys
import math
from decimal import *
import collections
from collections import Counter



#Read program arguments
if(len(sys.argv) == 0):
    print("Please enter the appropriate number of arguments")
ratingsFile = sys.argv[1];
userId =  sys.argv[2];
neighborhood =  sys.argv[3];
resultNum =  sys.argv[4]

#Read contents from file
movies = []
users = []
ratings = []
with open(ratingsFile, 'r') as f:
    lines = f.read().splitlines();
ratingsList = [];
for i in lines:
    ratingsList.append(i.split('\t'));

#Obtain list of movies, users and ratings
for record in ratingsList:
    if(record[0] not in users):
        users.append(record[0])
        ratings.append(record[1])
    if(record[2] not in movies):
        movies.append(record[2])

#Store each record in a dictionary
userItemMatrix = {};
for eachItem in ratingsList:
    userItemMatrix[(eachItem[0]), (eachItem[2])] = (eachItem[1]);


#Obtain list of rated and unrated movies for the userId
unratedMovies = []
ratedMovies = []
for eachKey in userItemMatrix.keys():
    if(userId in eachKey):
        ratedMovies.append(eachKey[1])

for eachMovie in movies:
    if(eachMovie not in ratedMovies):
        unratedMovies.append(eachMovie)

#Compute Pearson Coeffecient
pearsonCorrelation = {}
prediction = {}
for i in unratedMovies:
    pearsonCorrelation = {}
    N = {}
    temp = []
    #Obtain j values
    for j in movies:
        u = []
        useri = []
        userj = []
        if(i != j):     #Not the same movies
            #Obtain set u
            for keyset in userItemMatrix.keys():
                if(keyset[1] == i):
                    if(keyset[0] not in useri):                   
                        useri.append(keyset[0])
                if(keyset[1] == j):
                    if(keyset[0] not in userj):                   
                        userj.append(keyset[0])
            u = set(useri) & set(userj)      
            #Obtain average rating for i and j
            avgi = 0.0
            avgj = 0.0
            numi = 0.0
            numj = 0.0
            if(len(u) > 1):
                for eachU in u:
                    for k in userItemMatrix.keys():
                        if(k[0] == eachU and k[1] == i):
                            numi  = Decimal(numi) + Decimal(userItemMatrix[k]);                                                            
                        if(k[0] == eachU and k[1] == j):                            
                            numj = Decimal(numj) + Decimal(userItemMatrix[k]);
                avgi = ((numi) / len(u))
                avgj = Decimal(Decimal(numj) / len(u))
                #Calculate the Pearson coeffecient              
                pnum = 0.0
                pdenomj = 0.0
                pdenomi = 0.0
                numi = 0.0
                numj = 0.0
                pdenom = 0.0
                for eachUser in u:
                    for eachK in userItemMatrix.keys():
                        if(eachK[0] == eachUser and eachK[1] == i):
                            numi = Decimal(Decimal(userItemMatrix[eachK]) - avgi);        
                        if(eachK[0] == eachUser and eachK[1] == j):
                            numj = Decimal(Decimal(userItemMatrix[eachK]) - Decimal(avgj));
                    
                    pnum = Decimal(Decimal(pnum) + Decimal(numi*numj));
                    #Obtain the denominator
                    pdenomi = Decimal(pdenomi) + Decimal((numi*numi));
                    pdenomj = Decimal(pdenomj) + Decimal((numj*numj));
                    pdenom = Decimal(math.sqrt(pdenomi*pdenomj));
                    if(pdenom == 0):
                        wij = (0.0)
                    else:
                        wij = pnum/pdenom;
                    pearsonCorrelation[j] = wij;
    #Obtain top N similarities
    temp = Counter(pearsonCorrelation).most_common(int(neighborhood))
    for m in temp:
        N[m[0]] = m[1]
    #Calculate unknown ratings
    num = 0.0
    denom = 0.0
    rating = 0.0
    prediction = {}
    for keySet in N.keys():      
        prioriRating = 0.0
        #Obtain ru,n
        for x in userItemMatrix:
            if(x[1] == keySet and x[0] == userId):
                prioriRating = Decimal(userItemMatrix[x])
        #Calculate numerator and denominator        
        if(prioriRating != 0.0):
            num = Decimal(num) + Decimal(Decimal(prioriRating)*Decimal(N[keySet]))
            denom = Decimal(denom) + Decimal(abs(N[keySet]))
    if( denom != 0):
        rating = round(Decimal(num / denom), 5)
        prediction[userId,i] = rating
        print(prediction)
        
        
            
        
                
                 
                
            



           
            
        
 

