from utils import *
import requests
import json
import random
import time
import pickle

complete_graph = Graph()
graph_verts = pickle.load(open('graph_vertices.p', 'rb'))
# room_data=pickle.load(open('room_data.p','rb'))
complete_graph.vertices = graph_verts

init_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
take_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
sell_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
move_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
status_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
examine_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'


param = {'Authorization': 'Token e79b12bf4f51c748e9edf3b395ad368c91c89ced'}

init_response = requests.get(init_url, headers=param)
init_res = init_response.text
ir = json.loads(init_res)
#cur_exits = ir['exits']
cur_room = ir['room_id']
cur_cd = ir['cooldown']
time.sleep(cur_cd)


status_response = requests.post(status_url, headers=param)
stat_res = status_response.text
sr = json.loads(stat_res)
cur_encumb = sr['encumbrance']
cur_cd = sr['cooldown']
time.sleep(cur_cd)


def bfs(graph, current_room):

    queue = Queue()
    # push the starting vertex ID as list
    queue.enqueue([current_room])
    # create an empty Set to store the visited vertices
    visited = set()

    # while the queue is not empty ...
    while queue.size() > 0:

        # dequeue the first vertex
        path = queue.dequeue()
        vert = path[-1]

        # if that vertex has not been visited ..
        if vert not in visited:

            # check for target
            if 55 in graph.vertices[vert].values():
                path_dirs = []
                cur_idx = 0
                next_idx = 1
                last_room = path[-1]
                # print(path)
                for room in path:
                    if room == last_room:
                        break
                    cur_room = path[cur_idx]
                    next_room = path[next_idx]
                    room_dirs = list(graph.vertices[cur_room].keys())

                    for d in room_dirs:

                        if graph.vertices[cur_room][d] == next_room:
                            path_dirs.append(d)
                            cur_idx += 1
                            next_idx += 1
                            break
                for direction in graph.vertices[vert]:
                    if graph.vertices[vert][direction] == 467:
                        path_dirs.append(direction)
                return path_dirs

            # mark it is visited
            visited.add(vert)

            # then add all of its neighbors to the back of the queue
            # self.get_neighbors(vert)
            for neighbor in graph.vertices[vert].values():
                if neighbor not in path:
                    # copy path to avoid pass by reference
                    new_path = list(path)  # make a copy
                    new_path.append(neighbor)
                    queue.enqueue(new_path)


dirs_to_well = bfs(complete_graph, cur_room)
for move in dirs_to_well:

    if complete_graph.vertices[cur_room][move] != '?':
        known_room_id = complete_graph.vertices[cur_room][move]
        direction = {'direction': move, 'next_room_id': str(known_room_id)}
    else:
        direction = {'direction': move}

    #prev_room = cur_room

    move_response = requests.post(move_url, headers=param, json=direction)
    move_resp = move_response.text
    mr = json.loads(move_resp)

    cur_room = mr['room_id']
    cur_cd = mr['cooldown']
    cur_items = mr['items']

    # if 'shiny treasure' in cur_items:
    #     if cur_encumb < 9:
    #         take = {"name": 'shiny treasure'}
    #         take_res = requests.post(take_url, headers=param, json=take)
    #         take_r = take_res.text
    #         tr = json.loads(take_r)
    #         cur_cd = tr['cooldown']
    #         time.sleep(cur_cd)
    #         cur_encumb += weight
    #         print('found treasure')

    if cur_cd > 500:
        print('uh-oh')
        break

    time.sleep(cur_cd)

if cur_room == 26:
    direction = {'direction': 'e', 'next_room_id': str(55)}
    move_response = requests.post(move_url, headers=param, json=direction)
    move_resp = move_response.text
    mr = json.loads(move_resp)

    cur_room = mr['room_id']
    cur_cd = mr['cooldown']
    time.sleep(cur_cd)


print('here')
print(cur_room)

examine = {'name': 'Well'}
examine_res = requests.post(examine_url, headers=param, json=examine)
examine_r = examine_res.text
er = json.loads(examine_r)
cd = er['cooldown']
message = er['description']
time.sleep(cd)
print(message)
