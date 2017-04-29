import sys
import csv
from py2neo import Graph
from py2neo import Node, Relationship
from py2neo import watch
from py2neo import ConstraintError



watch("httpstream")

graph = Graph("http://neo4j:admin@localhost:7474/db/data/")

def clear_db():
	global graph
	graph.delete_all()


def get_friends_count_users(all_rows, num_of_nodes):
	all_users = {}
	all_user_ids = []
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
			all_users[user_id] = user
			all_user_ids += [user_id]
			num_of_nodes -= 1
		else:
			break

	#highest_count_users = get_total_count_friends(all_users, all_user_ids)
	#return highest_count_users, all_users
	return all_users, all_user_ids


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


def get_final_node_map(users, users_ids, k, levels):
	users_at_levels = [[] for i in range(levels)]
	idx = 0
	for level in range(1,levels+1):
		print('In level %d of node mapping' % level)	
		if level == 1:
			highest_count_users = get_total_count_friends(users, users_ids)
			# Get the influential users
			for i in sorted(highest_count_users, reverse=True)[0:k]:
				if len(users_at_levels) == 0:
					users_at_levels = [[highest_count_users[i]]]
				else:
					users_at_levels[idx] += [highest_count_users[i]]
		else:
			for user in users_at_levels[idx-1]:
				for user_id in users_ids:
					if user_id in user.properties['friends'] and user_id in users:
						users_at_levels[idx] += [users[user_id]]
						users.pop(user_id)

		idx+=1

	return users_at_levels


def create_edges_for_nodes(users_at_levels, levels, info_propagation_flag):
	global graph

	edges_created = 0
	idx = 0
	if levels > 1:
		for level in range(2,levels+1):
			print('In level %d of edge creation' % level)
			info_propagation = 70 * (idx + 1)
			print('Info prop: %f'%info_propagation)
			for next_user in users_at_levels[idx+1]:
				for user in users_at_levels[idx]:
					# Picking next set of users who are  friends with the current 'user'
					if (user != None) and (user != next_user) and (next_user.properties['userId'] in user.properties['friends']):
						if level > 2:
							temp_user =  graph.find_one("Friend" + str(level-2), property_key="userId", property_value=user.properties['userId'])
							# User is already converted to info-prop
							if temp_user == None:
								user =  graph.find_one("InformationPropagation", property_key="userId", property_value=user.properties['userId'])
							else:
								user = temp_user
								if (info_propagation_flag == True) and (info_propagation > 0):
									user.clear_labels()
									user.add_label('InformationPropagation')
									graph.push(user)
									info_propagation -= 1

						friend_user2 = Node("Friend" + str(level-1), userId=next_user.properties['userId'], friends=next_user.properties['friends'])
						friend_edge = Relationship(user, str(level-1), friend_user2)

						# Exception can occur if the edges were already created
						try:
							graph.create(friend_edge)
							edges_created += 1							
							if (info_propagation_flag == True) and (info_propagation > 0 and (idx == (levels - 2))):
								next_user =  graph.find_one("Friend" + str(level-1), property_key="userId", property_value=next_user.properties['userId'])
								next_user.clear_labels()
								next_user.add_label('InformationPropagation')
								graph.push(next_user)
								info_propagation -= 1
						except ConstraintError:
							pass

			idx+=1

	print("Total edges created: %d" % edges_created)


def main():

	clear_db()
#	f = open("C:/Users/Ravikiran357/Documents/Ravi/ASU/Sem-2/SML-CSE 575/Project/Dataset/Graphfriends.csv", encoding='utf8')
	f = open(sys.argv[1], encoding='utf8')
	csv.field_size_limit(2147483647)
	all_rows = csv.reader(f)
	num_of_nodes = 300
	all_users, all_user_ids = get_friends_count_users(reversed(list(all_rows)), num_of_nodes)
	num_of_influential_users = 1
	levels = 3
	info_propagation_flag = True
	users_at_levels = get_final_node_map(all_users, all_user_ids, num_of_influential_users, levels)
	create_edges_for_nodes(users_at_levels, levels, info_propagation_flag)

if __name__ == "__main__":
	main()


