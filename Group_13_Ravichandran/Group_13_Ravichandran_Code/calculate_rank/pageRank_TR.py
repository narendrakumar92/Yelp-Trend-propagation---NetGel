import numpy

#THe name of the file which has the test case Id
#fileNameId = 'UserId.txt'

#Name of the file having the adjacency matrix
fileNameAdj = 'Inputs/Adjacency_T'

#Name of the file containing the document term matrix
fileNameDocWord = 'Inputs/User_id_adj_ravi.out'


def returnMostInfluentialNode(adjMatrix, documentWordMatrix, i):

    noOfUsers=adjMatrix.shape[0]
    sumCol=documentWordMatrix[:, i].sum()
    pr_DocumentMatrix = documentWordMatrix[:, i]/sumCol
    resultMatrix = numpy.ones(noOfUsers, dtype=float)
    resultMatrix=resultMatrix/noOfUsers
    oldResultMatrix = numpy.zeros(noOfUsers, dtype=float)
   # pr_DocumentMatrix= pr_DocumentMatrix[:, i]
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

#with open(fileNameId, "r") as myfile:
 #   fileName = myfile.read()

docWordMatrix = numpy.loadtxt(fileNameDocWord, dtype=float)
for sr_No in range(0, 10):
    adjMatrix = numpy.loadtxt(fileNameAdj+str(sr_No), dtype=float)
    adjMatrix = rowNormalize(adjMatrix)
    adjMatrix = adjMatrix.transpose()
    result1, result2 = returnMostInfluentialNode(adjMatrix, docWordMatrix, 9)
    outputMatrix = numpy.column_stack((result1, result2))
    filename_T = 'Outputs/Result'+str(sr_No)
    numpy.savetxt(filename_T, outputMatrix, fmt='%f')
