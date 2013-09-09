import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

#load data
data = pd.read_table("D:/workspace/semantic-matching/Python/concept.dat")

#column names
dataCol = list(data.columns) 
dataIndex = list(data.index)
human = dataCol[0:5] #ranks of human
gsi = dataCol[5:10] #ranks of proposed algorithms 
other = dataCol[10:15] #ranks of other structure algorithms
algor = dataCol[5:15] #ranks of all the algorithms

humanData = []
for i in range(5):
    rank = np.array(data[human[i]])
    rank = 1-rank*1.0/max(rank)
    humanData.append(rank)

gsiData = []
for i in range(5):
    sim = np.array(data[gsi[i]])
    gsiData.append(sim)

algorData = []
for i in range(10):
    sim = np.array(data[algor[i]])
    algorData.append(sim)

otherData = []
for i in range(5):
    sim = np.array(data[other[i]])
    otherData.append(sim)

def computeCorrelation(group1,group2,data1,data2):
    result = {}
    for i in range(5):
        corList = []
        for j in range(5):
            cor = stats.stats.kendalltau(data1[i],data2[j])[0]
            corList.append(cor)
        result[group1[i]] = corList
    return result

result1 = computeCorrelation(human,gsi,humanData,gsiData)
result2 = computeCorrelation(human,other,humanData,otherData)
result3 = computeCorrelation(other,gsi,otherData,gsiData)
result4 = computeCorrelation(other,other,otherData,otherData)

frame1 = pd.DataFrame(result1,columns=human,index=gsi)
frame2 = pd.DataFrame(result2,columns=human,index=other)
frame3 = pd.DataFrame(result3,columns=other,index=gsi)
frame4 = pd.DataFrame(result4,columns=other,index=other)

plt.rc('figure',figsize=(10,10))
font_options = {'size' : 11}
plt.rc('font', **font_options)

fig,axes = plt.subplots(2, 2)
axes[0,0].set_xlabel('Proposed Algorithms', fontsize=12)
axes[0,0].set_ylabel('Rank Correlation', fontsize=12)
axes[0,0].set_title("Human and Proposed Algorithms", fontsize=14)
axes[0,0].set_ylim([0,1.5])
axes[0,0].legend(loc='best')
frame1.plot(kind='bar',grid=False, ax=axes[0,0], alpha=0.7)

axes[0,1].set_xlabel('Structured Based Algorithms', fontsize=12)
axes[0,1].set_ylabel('Rank Correlation', fontsize=12)
axes[0,1].set_title("Human and Structure Based Algorithms", fontsize=14)
axes[0,1].set_ylim([0,1.5])
axes[0,1].legend(loc='best')
frame2.plot(kind='bar',grid=False,ax=axes[0,1], alpha=0.7)

axes[1,0].set_xlabel('Proposed Algorithms', fontsize=12)
axes[1,0].set_ylabel('Rank Correlation', fontsize=12)
axes[1,0].set_title("Structure Based Algorithms and Proposed Algorithms", fontsize=14)
axes[1,0].set_ylim([0,1.5])
axes[1,0].legend(loc='best')
frame3.plot(kind='bar',grid=False,ax=axes[1,0], alpha=0.7)

axes[1,1].set_xlabel('Structured Based Algorithms', fontsize=12)
axes[1,1].set_ylabel('Rank Correlation', fontsize=12)
axes[1,1].set_title("Structure Based Algorithms", fontsize=14)
axes[1,1].set_ylim([0,1.5])
axes[1,1].legend(loc='best')
frame4.plot(kind='bar',grid=False,ax=axes[1,1], alpha=0.7)
plt.savefig('D:/workspace/semantic-matching/Python/human-algorithm.pdf',bbox_inches='tight')

