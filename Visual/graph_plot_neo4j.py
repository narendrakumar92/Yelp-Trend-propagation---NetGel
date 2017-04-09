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



plotted_ids = []
plotted_indeed = False
unavailable_nodes = []
# Creating relationships for highest user
def form_1_relations(highest_friend_user, users, level):
	global plotted_ids
	global plotted_indeed
	global unavailable_nodes
	num_of_nodes = 0
	edges_created = 0
	friends_ids = highest_friend_user.properties['friends'] #str.split(user.properties['friends'], ", ")
	num_of_nodes += 1
	print("No.:%d .. Friends count: %d" % (num_of_nodes, len(friends_ids)))
	friends = []

	for friend_user_id in friends_ids:
		friend_user_id.replace("'", "")
		if (friend_user_id in unavailable_nodes):
				continue
		else:
			if (friend_user_id in users.keys()):
				# To get different color changing node label
				node = users[friend_user_id]
				#friend_user = Node("Friend" + str(level), userId=node.properties['userId'], friends=node.properties['friends'])
				friend_user = Node("User", userId=node.properties['userId'], friends=node.properties['friends'])
				friend_edge = Relationship(highest_friend_user, str(level), friend_user)

				# Exception can occur if the edges were already created
				try:
					graph.create(friend_edge)
					edges_created += 1
				except ConstraintError:
					pass

				# Remove already handled users
				for pid in plotted_ids:
					if friend_user.properties['userId'] == pid:
						plotted_indeed = True
						break

				if plotted_indeed != True:
					friends += [friend_user]
					plotted_ids += [friend_user.properties['userId']]
				else:
					plotted_indeed = False
			else:
				unavailable_nodes.append(friend_user_id)

	print("Total edges created: %d" % edges_created)

	return friends



# Creating all relationships for influential users
def form_friend_relations(users_count, users):
	global plotted_ids
	global plotted_indeed
	num_of_nodes = 0
	edges_created = 0
	friends = []
	local_users = []

	# Extract the k most influential users, k = 3
	for i in sorted(users_count, reverse=True)[0:3]:
		local_users += [users_count[i]]
		plotted_ids += [users_count[i].properties['userId']]

	for level in range(1,4):
		print("LEVEL%d ------------------------------"%level)
		for user in local_users:
			friends_ids = user.properties['friends'] #str.split(user.properties['friends'], ", ")
			num_of_nodes += 1
			print("No.:%d .. Friends count: %d" % (num_of_nodes, len(friends_ids)))
			friends += form_1_relations(user, users, level)
			print("Num of friends: %d"%len(friends))
		
		local_users = friends

	print("Total edges created: %d" % edges_created)






clear_db()
#graph.schema.create_uniqueness_constraint('User', 'userId')

f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/Graphfriends.csv", encoding='utf8')
csv.field_size_limit(2147483647)
#f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/user_ids.csv", encoding='utf8')
all_rows = csv.reader(f)

highest_count_users = {}
all_users = {}
num_of_nodes = 30
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

form_friend_relations(highest_count_users, all_users)

exit()

# Old cases
highest_friend_count = 0
highest_friend_user = ""
all_users = {}
num_of_nodes = 30
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
		if len(friends_list) > highest_friend_count:
			highest_friend_count = len(friends_list)
			highest_friend_user = user
	else:
		break

#form_1_relations(highest_friend_user, all_users)

#form_relations(all_users)