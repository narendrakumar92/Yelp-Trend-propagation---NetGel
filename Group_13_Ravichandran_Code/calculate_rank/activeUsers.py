import numpy

docWordMatrix = numpy.loadtxt('Inputs/User_id_adj_ravi.out', dtype=float)
with open("Inputs/user_list.out", "r") as ins:
    userMatrix = []
    for line in ins:
        userMatrix.append(line)

mat1 = docWordMatrix[:, 5]
matrixIndex = mat1.argsort()[-5:][::-1]
finalList=[]
for number in matrixIndex:
    finalList.append(userMatrix[number])

print(finalList)