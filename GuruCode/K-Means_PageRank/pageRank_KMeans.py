import numpy


#file containing the Adjacency Matrix
fileNameAdj ='Inputs/Kmeans_Adjacency.out'

def returnMostInfluentialNode(adjMatrix, documentWordMatrix, i):

    noOfUsers=adjMatrix.shape[0]
    sumCol=documentWordMatrix[:, i].sum()
    pr_DocumentMatrix = documentWordMatrix[:, i]/sumCol
    resultMatrix = numpy.ones(noOfUsers, dtype=float)
    resultMatrix=resultMatrix/noOfUsers
    oldResultMatrix = numpy.zeros(noOfUsers, dtype=float)
    count = 0
    while not(numpy.array_equal(oldResultMatrix, resultMatrix)) and count <= 10000:
        count=count+1
        oldResultMatrix=resultMatrix
        resultMatrix=0.85*adjMatrix.dot(resultMatrix)+0.15*pr_DocumentMatrix

    return numpy.sort(resultMatrix)[::-1], numpy.argsort(-resultMatrix)


def rowNormalize(graphMatrix):
    for i in range(0,graphMatrix.shape[0]):
        if graphMatrix[i, :].sum() != 0:
            graphMatrix[i, :] = graphMatrix[i, :]/graphMatrix[i, :].sum()
    return graphMatrix


adjMatrix = numpy.loadtxt(fileNameAdj, dtype=float)
adjMatrix = rowNormalize(adjMatrix)
adjMatrix = adjMatrix.transpose()
docWordMatrix = numpy.ones(adjMatrix.shape, dtype=float)
result1, result2 = returnMostInfluentialNode(adjMatrix, docWordMatrix, 0)
outputMatrix = numpy.column_stack((result1, result2))
filename_T = 'Outputs/Result_KMeans'
numpy.savetxt(filename_T, outputMatrix, fmt='%f')
