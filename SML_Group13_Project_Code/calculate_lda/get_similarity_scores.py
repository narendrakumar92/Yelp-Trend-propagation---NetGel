from scipy import spatial
import numpy as np


def get_adj_index(k_idx_list):
	filename = "test_data.out"
	for line in open(filename):
		cluster_num = line.split(':')[-1]
	
	file_obj = open("Cluster_data" + cluster_num.strip() + ".txt","r")
	lines = file_obj.readlines()
	res = []
	for idx in k_idx_list:
		res += [int(lines[idx].split(':')[0])]

	print(res)
	return res


def get_similarity(index, k_users):

	npar = np.loadtxt('User_id_adj_ravi.out',dtype=int)
	data = npar.tolist()

	rand_data = data[index]
	dist = 0
	res_list = []
	for i in k_users:
		# Getting the similarity score from cosine distance and euclidean distance
		# dist = 1 - spatial.distance.cosine(rand_data, data[i])
		dist = spatial.distance.euclidean(rand_data, data[i])
		res_list += [dist]

	return res_list


def main():
	k = 5
	# Twitter rank
	k_twit_users = [6,13,18,37,8]

	# Random user
	rand_idx = 1010

	# Twitter rank
	twitter = get_similarity(rand_idx, k_twit_users)

	# k-means
	npar = np.loadtxt('KMeansResult.txt',dtype=float)
	k_idx_list = list(map(int, npar[:,1].tolist()))[0:k]
	k_k_means_users = get_adj_index(k_idx_list)
	print(k_k_means_users)
	k_means = get_similarity(rand_idx, k_k_means_users)

	for x in range(0,k):
		print("%d : %.3f .. %.3f"% (x,twitter[x],k_means[x]))


if __name__ == "__main__":
	main()