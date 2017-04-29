import numpy

import sys
from calculate_run_details import read_run_details_file

# get run details hash from file
if len(sys.argv) == 1:
    run_file_name = 'run_details_1010_1_.out'
    run_number = '1'
else:
    run_file_name = sys.argv[1]
    run_number = sys.argv[2]
run_details_hash = read_run_details_file(run_file_name)


#Name of the file having the adjacency matrix
fileNameAdj = run_details_hash["run_details"][run_number]["adjacency_output_prefix"]

#Name of the file containing the document term matrix
fileNameDocWord = run_details_hash['userid_topic_scores_file_name']

#Name of result file
resultPrefix = run_details_hash["run_details"][run_number]["pagerank_output_prefix"]


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

    return resultMatrix


def rowNormalize(graphMatrix):
    for i in range(0,graphMatrix.shape[0]):
        if graphMatrix[i, :].sum() != 0:
            graphMatrix[i, :] = graphMatrix[i, :]/graphMatrix[i, :].sum()
    return graphMatrix


def main():
    docWordMatrix = numpy.loadtxt(fileNameDocWord, dtype=float)
    for sr_No in range(0, 10):
        adjMatrix = numpy.loadtxt(fileNameAdj+str(sr_No)+".out", dtype=float)
        adjMatrix = rowNormalize(adjMatrix)
        adjMatrix = adjMatrix.transpose()
        result1 = returnMostInfluentialNode(adjMatrix, docWordMatrix, 9)
        filename_T = resultPrefix+str(sr_No)+".out"
        numpy.savetxt(filename_T, result1, fmt='%f')



if __name__ == "__main__":
    print "Calculate Page Rank - Started"

    main()

    print "Calculate Page Rank - Ended"
