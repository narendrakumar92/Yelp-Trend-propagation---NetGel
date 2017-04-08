import csv
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo import watch



watch("httpstream")

graph = Graph("http://neo4j:admin@localhost:7474/db/data/")

f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/Graphfriends.csv", encoding='utf8')
csv.field_size_limit(2147483647)
#f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/user_ids.csv", encoding='utf8')
all_rows = csv.reader(f)

users = {}
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
		users[user_id] = user
		num_of_nodes -= 1
	else:
		break

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
