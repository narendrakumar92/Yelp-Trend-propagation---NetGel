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


spl_count = 0
plotted_nodes = []
plotted_node_flag = False
unavailable_nodes = []
edges_created = 0
# Creating relationships for highest user
def form_1_relations(highest_friend_user, users, level):
	global plotted_nodes
	global plotted_node_flag
	global unavailable_nodes
	global edges_created

	global spl_count
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

				if (highest_friend_user.properties['userId'] in plotted_nodes) and level == 3:
					print(plotted_node_flag)
					spl_count+=1
					print(spl_count)
					print(highest_friend_user.properties['userId'] + '_' + friend_user.properties['userId'])

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
	num_of_nodes = 0
	friends = []
	local_users = []

	# Extract the k most influential users, k = 3
	for i in sorted(users_count_dict, reverse=True)[0:k]:
		local_users += [users_count_dict[i]]
		plotted_nodes += [users_count_dict[i].properties['userId']]

	for level in range(1,3):
		print("LEVEL%d ------------------------------"% level)
		for user in local_users:
			friends_ids = user.properties['friends'] #str.split(user.properties['friends'], ", ")
			num_of_nodes += 1
			print("No.:%d .. Friends count: %d" % (num_of_nodes, len(friends_ids)))
			friends += form_1_relations(user, users, level)
		
		local_users = friends

	print("Total number of friends of %d-most influential users: %d"% (k,len(friends)))
	print("Total edges created: %d" % edges_created)


def get_highest_friends_count_users2(all_rows):
	highest_count_users = {}
	all_users = {}
	num_of_nodes = 60
	for row in all_rows:
		if num_of_nodes > 0:
			user_id = str.split(row[0], ":")
			row[0] = user_id[1]
			user_id = user_id[0]
			friends_list = row
			# user_id = row[5]
			# friends_list = row[7]
			user = Node("User", userId=user_id, friends=friends_list)
			all_users[user_id] = user
			num_of_nodes -= 1
			highest_count_users[len(friends_list)] = user
		else:
			break

	return highest_count_users, all_users

def get_highest_friends_count_users(all_rows):
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
			if 'TYwQtORbORzcX22xdYBx1g' in friends_list:
				print('^^^^^^^^^^^^')
				exit()
		if len(highest_count_users) == 5:
			print(len(all_users))
			break

	if 'TYwQtORbORzcX22xdYBx1g' in all_users:
		print('HERE')
		exit()

	return highest_count_users, all_users



def main():
    # my code here

	clear_db()
	#graph.schema.create_uniqueness_constraint('User', 'userId')

	f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/Graphfriends.csv", encoding='utf8')
	csv.field_size_limit(2147483647)
	#f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/user_ids.csv", encoding='utf8')
	all_rows = csv.reader(f)

	highest_count_users, all_users = get_highest_friends_count_users(reversed(list(all_rows)))
	form_friend_relations(highest_count_users, all_users, 5)

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