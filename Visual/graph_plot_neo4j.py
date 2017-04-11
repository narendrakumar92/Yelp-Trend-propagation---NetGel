import csv
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo import watch
from py2neo import ConstraintError



watch("httpstream")

graph = Graph("http://neo4j:admin@localhost:7474/db/data/")

def clear_db():
	graph.delete_all()
	
	# rel_list = list(graph.match(rel_type="KNOWS"))
	# if (len(rel_list) > 0):
	# 	tx = graph.begin()
	# 	tx.separate(rel_list)
	# 	tx.commit()


# Creating all relationships
def form_relations(users):
	unavailable_nodes = []
	print(len(users.keys()))
	num_of_nodes = 0
	edges_created = 0
	for user in users.values():
		friends_ids = user.properties['friends'] #str.split(user.properties['friends'], ", ")
		num_of_nodes += 1
		print("No.:%d .. Friends count: %d" % (num_of_nodes, len(friends_ids)))
		for friend_user_id in friends_ids:
			friend_user_id.replace("'", "")
			if (friend_user_id in unavailable_nodes):
				continue
			else:
				if (friend_user_id in users.keys()):
					friend_edge = Relationship(user, "KNOWS", users[friend_user_id])
					graph.create(friend_edge)
					edges_created += 1
				else:
					unavailable_nodes.append(friend_user_id)

	print("Total edges created: %d" % edges_created)


k_means = 2
twitter_propagation = 9
include_info_prop = True
info_count = 0
plotted_nodes = []
plotted_node_flag = False
unavailable_nodes = []
edges_created = 0
# Creating relationships for highest user
def form_1_relations(highest_friend_user, users, level, k_means_propagation = 0):
	global plotted_nodes
	global plotted_node_flag
	global unavailable_nodes
	global edges_created

	global info_count
	global include_info_prop
	friends_ids = highest_friend_user.properties['friends'] #str.split(user.properties['friends'], ", ")
	friends = []

	for friend_user_id in friends_ids:
		friend_user_id.replace("'", "")
		if (friend_user_id in unavailable_nodes):
				continue
		else:
			if (friend_user_id in users.keys()):
				if friend_user_id in plotted_nodes:
					continue
				# To get different color changing node label
				node = users[friend_user_id]
				if include_info_prop == True:
					#if info_count % k_means_propagation == 0:
					if k_means_propagation > 0:
						friend_user = Node("InformationPropagation", userId=node.properties['userId'], friends=node.properties['friends'])
					else:
						friend_user = Node("Friend" + str(level), userId=node.properties['userId'], friends=node.properties['friends'])
					k_means_propagation -= 1
					#info_count += 1
				else:
					friend_user = Node("Friend" + str(level), userId=node.properties['userId'], friends=node.properties['friends'])
				
				#friend_user = Node("User", userId=node.properties['userId'], friends=node.properties['friends'])
				
				friend_edge = Relationship(highest_friend_user, str(level), friend_user)

				# Exception can occur if the edges were already created
				try:
					graph.create(friend_edge)
					edges_created += 1
				except ConstraintError:
					pass

				# Elimate users whose nodes are already plotted
				if friend_user.properties['userId'] in plotted_nodes:
					plotted_node_flag = True
					break

				if plotted_node_flag != True:
					friends += [friend_user]
					plotted_nodes += [friend_user.properties['userId']]
				else:
					plotted_node_flag = False
			else:
				unavailable_nodes.append(friend_user_id)

	return friends


# Creating all relationships for influential users
def form_friend_relations(users_count_dict, users, k):
	global plotted_nodes
	global plotted_node_flag
	global edges_created
	global k_means
	num_of_nodes = 0
	friends = []
	local_users = []

	# Extract the k most influential users, k = 3
	for i in sorted(users_count_dict, reverse=True)[0:k]:
		local_users += [users_count_dict[i]]
		print(users_count_dict[i])
		plotted_nodes += [users_count_dict[i].properties['userId']]

	for level in range(1,3):
		print("LEVEL%d ------------------------------"% level)
		k_means_propagation = k_means
		#local_users.reverse()
		for user in local_users:
			friends_ids = user.properties['friends'] #str.split(user.properties['friends'], ", ")
			num_of_nodes += 1
			print("No.:%d .. Friends count: %d" % (num_of_nodes, len(friends_ids)))
			friends += form_1_relations(user, users, level, k_means_propagation)
		
		local_users = friends

	print("Total number of friends of %d-most influential users: %d"% (k,len(friends)))
	print("Total edges created: %d" % edges_created)


def get_total_count_friends(users, users_ids):
	highest_count_users = {}
	for user_id,user in users.items():
		count = 0
		friends_list = user.properties['friends']
		for friend_id in friends_list:
			if friend_id in users_ids:
				count += 1

		highest_count_users[count] = users[user_id]

	return highest_count_users


def create_edges_for_nodes(users_at_levels, levels):
	edges_created = 0
	idx=0
	if levels > 1:
		for level in range(2,levels+1):
			print('In level %d of edge creation' % level)
			for next_user in users_at_levels[idx+1]:
				for user in users_at_levels[idx]:
					if user != next_user and (next_user.properties['userId'] in user.properties['friends']):

						#node = graph.find("Friend" + str(level-2), "userId", user.properties['userId'])
						

						if level > 2:
						# 	print(len(users_at_levels))
						# 	print(idx)
						# 	print(user in users_at_levels[idx])
						# 	print(user.properties['userId'])
							user =  graph.find_one("Friend1", property_key="userId", property_value=user.properties['userId'])
							# print(user)
							# m = graph.match_one(start_node=user)
							# print(m)
							# m = list(graph.match_one(end_node=user))
							# print(m)
							# print(m[0])
							# exit()
							user.remove_label('InformationPropagation')
							user.add_label("Friend" + str(level-2))
							#friend_user1 = Node("Friend" + str(level-2), userId=user.properties['userId'], friends=user.properties['friends'])
							#user = friend_user1
						friend_user2 = Node("Friend" + str(level-1), userId=next_user.properties['userId'], friends=next_user.properties['friends'])
						friend_edge = Relationship(user, str(level-1), friend_user2)

						# Exception can occur if the edges were already created
						try:
							graph.create(friend_edge)
							edges_created += 1
						except ConstraintError:
							#print(user.properties['userId'])
							pass

			idx+=1

	print("Total edges created: %d" % edges_created)

def get_final_node_map(users, users_ids, k, levels):
	users_at_levels = [[] for i in range(levels)]
	idx = 0
	for level in range(1,levels+1):
		print('In level %d of mapping' % level)	
		if level == 1:
			highest_count_users = get_total_count_friends(users, users_ids)
			# Get the influential users
			for i in sorted(highest_count_users, reverse=True)[0:k]:
				if len(users_at_levels) == 0:
					users_at_levels = [[highest_count_users[i]]]
				else:
					users_at_levels[idx] += [highest_count_users[i]]
		else:
			print(idx)
			print(len(users_at_levels))
			for user in users_at_levels[idx-1]:
				for user_id in users_ids:
					if user_id in user.properties['friends'] and user_id in users:
						users_at_levels[idx] += [users[user_id]]
						users.pop(user_id)

		idx+=1

	return users_at_levels


def get_friends_count_users(all_rows):
	all_users = {}
	all_user_ids = []
	num_of_nodes = 300
	for row in all_rows:
		if num_of_nodes > 0:
			user_id = str.split(row[0], ":")
			row[0] = user_id[1]
			user_id = user_id[0]
			friends_list = row
			# user_id = row[5]
			# friends_list = row[7]
			# user = Node("InfluentialUser", userId=user_id, friends=friends_list)
			user = Node("InformationPropagation", userId=user_id, friends=friends_list) 
			# print(user.labels())
			# exit()
			all_users[user_id] = user
			all_user_ids += [user_id]
			num_of_nodes -= 1
		else:
			break

	#highest_count_users = get_total_count_friends(all_users, all_user_ids)
	#return highest_count_users, all_users
	return all_users, all_user_ids

def get_known_highest_friends_count_users(all_rows):
	highest_count_users = {}
	all_users = {}
	for row in all_rows:
		user_id = str.split(row[0], ":")
		row[0] = user_id[1]
		user_id = user_id[0]
		friends_list = row
		# user_id = row[5]
		# friends_list = row[7]
		# Taken user is 1010
		if user_id == 'TYwQtORbORzcX22xdYBx1g':
			user = Node("RandomUser", userId=user_id, friends=friends_list)
		else:
			user = Node("InfluentialUser", userId=user_id, friends=friends_list)
		all_users[user_id] = user
		if user_id in ['folPdHjHOS0g5UxNSgtWVQ','z1QL9pkPgw08FwLiuqLX-w','DCnqvmdvbu04hTAv7DX-Mw','M_7cjIKGD3HfQ1G6SyjhkA','rNR390l5MgPHKsdeiS1F9w']:
			highest_count_users[len(friends_list)] = user
		if len(highest_count_users) == 5:
			print(len(all_users))
			break

	return highest_count_users, all_users



def main():
    # my code here

	clear_db()
	#graph.schema.create_uniqueness_constraint('User', 'userId')
	# graph.schema.create_uniqueness_constraint('Friend1', 'userId')
	# graph.schema.create_uniqueness_constraint('Friend2', 'userId')

	f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/Graphfriends.csv", encoding='utf8')
	csv.field_size_limit(2147483647)
	#f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/user_ids.csv", encoding='utf8')
	all_rows = csv.reader(f)

	all_users, all_user_ids = get_friends_count_users(reversed(list(all_rows)))
	# highest_count_users, all_users = get_friends_count_users(reversed(list(all_rows)))
	# highest_count_users, all_users = get_known_highest_friends_count_users(reversed(list(all_rows)))
	num_of_influential_users = 1
	levels = 3
	users_at_levels = get_final_node_map(all_users, all_user_ids, num_of_influential_users, levels)
	create_edges_for_nodes(users_at_levels, levels)

if __name__ == "__main__":
	main()


# Old cases
# highest_friend_count = 0
# highest_friend_user = ""
# all_users = {}
# num_of_nodes = 30
# for row in all_rows:
# 	if num_of_nodes > 0:
# 		user_id = str.split(row[0], ":")
# 		row[0] = user_id[1]
# 		user_id = user_id[0]
# 		friends_list = row
# 		# user_id = row[5]
# 		# friends_list = row[7]
# 		user = Node("User", userId=user_id, friends=friends_list)
# 		all_users[user_id] = user
# 		num_of_nodes -= 1
# 		if len(friends_list) > highest_friend_count:
# 			highest_friend_count = len(friends_list)
# 			highest_friend_user = user
# 	else:
# 		break

# form_1_relations(highest_friend_user, all_users)

# form_relations(all_users)