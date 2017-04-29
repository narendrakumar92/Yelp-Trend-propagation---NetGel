import numpy

adjMatrix = numpy.loadtxt("Inputs/Adjacency_new.out", dtype=int)

TR_NodeIndex = [6, 13, 18, 37, 8]
K_MeansIndex = [676, 938, 998, 767, 659]

TR_IndexResult = []
K_MeansIndexResult=[]
for i in TR_NodeIndex:
    tempMatrix = adjMatrix[i,:]
    TR_IndexResult.append(numpy.count_nonzero(tempMatrix))

for j in K_MeansIndex:
    tempMatrix = adjMatrix[j, :]
    K_MeansIndexResult.append(numpy.count_nonzero(tempMatrix))

print(TR_IndexResult)
print(K_MeansIndexResult)