from utils import *
import requests
import json
import random
import time
import pickle



def bfs(graph, current_room):
    queue = Queue()
    #push the starting vertex ID as list
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
            #check for target
            if "?" in graph.vertices[vert].values():
                path_dirs = []
                cur_idx = 0
                next_idx = 1
                last_room = path[-1]
                #print(path)    
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
                         
                return path_dirs
            # mark it is visited
            visited.add(vert)
            # then add all of its neighbors to the back of the queue
            for neighbor in graph.vertices[vert].values(): #self.get_neighbors(vert)
                if neighbor not in path:
                #copy path to avoid pass by reference
                    new_path = list(path) # make a copy
                    new_path.append(neighbor)
                    queue.enqueue(new_path)

adv_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
ep_status = 'status/'
ep_init = 'init/'
ep_move = 'move/'

param = {'Authorization': 'Token xxxx'}

# status_response = requests.post(adv_url+ep_status, headers=param)
# stat_r = status_response.text
# stat_res = json.loads(stat_r)

# cur_gold = stat_res['gold']
# cur_cd = stat_res['cooldown']
# cur_encumb = stat_res['encumbrance']
# cur_str = stat_res['strength']
# cur_spd = stat_res['speed']
# cur_bdy = stat_res['bodywear']
# cur_ft = stat_res['footwear']
# cur_inv = stat_res['inventory']
# cur_abl = stat_res['abilities']
# cur_stat = stat_res['status']
# time.sleep(cur_cd)


init_response = requests.get(adv_url+ep_init, headers=param)
init_res = init_response.text
ir = json.loads(init_res)


cur_room = ir['room_id']
cur_coords = ir['coordinates']
cur_exits = ir['exits']
cur_items = ir['items']
cur_cd = ir['cooldown']
time.sleep(cur_cd)

visited = set()
graph = Graph()

graph.add_vertex(cur_room, cur_exits)
visited.add(cur_room)

while len(visited) < 500:
    try:
        if cd > 500:
            print('uh-oh')
            break
    except:
        pass
    
    try:
        if cur_cd > 500:
            print('uh-oh')
            break
    except:
        pass
    
    while '?' in graph.vertices[cur_room].values():
        try:
            if cd > 500:
                print('uh-oh')
                break
        except:
            pass
        
        neighbors = graph.vertices[cur_room]
        dirs  = list(neighbors.keys())
        random.shuffle(dirs)
        for move in dirs:
            
            if neighbors[move] == '?':
                prev_room = cur_room
                
                # status_response = requests.post(adv_url+ep_status, headers=param)
                # stat_r = status_response.text
                # stat_res = json.loads(stat_r)
                
                # cur_cd = stat_res['cooldown']
                # time.sleep(cur_cd)


                move_response = requests.post(adv_url+ep_move, headers=param, json={'direction':move})
                move_resp = move_response.text
                mr = json.loads(move_resp)

                cd = mr['cooldown']
                
                if cd > 500:
                    print('uh-oh')
                    break

                time.sleep(cd)
                
                cur_room = mr['room_id']
                if cur_room not in visited:
                    visited.add(cur_room)
                cur_exits = mr['exits']
                
                if cur_room not in list(graph.vertices.keys()):
                    graph.add_vertex(cur_room, cur_exits)
                    graph.add_data(mr)
                graph.vertices[prev_room][move] = cur_room
                
                if move == 'n':
                    graph.vertices[cur_room]['s'] = prev_room
                if move == 's':
                    graph.vertices[cur_room]['n'] = prev_room
                if move == 'e':
                    graph.vertices[cur_room]['w'] = prev_room
                if move == 'w':
                    graph.vertices[cur_room]['e'] = prev_room

                prev_room = cur_room
                break
    
    if len(visited) == 500:
        break

    if '?' not in graph.vertices[cur_room].values():
        new_dirs = bfs(graph, cur_room)
        for move in new_dirs:
            
            if graph.vertices[cur_room][move] != '?':
                known_room_id = graph.vertices[cur_room][move]
                direction = {'direction': move, 'next_room_id': str(known_room_id)}
            else:
                direction = {'direction': move}

            prev_room = cur_room
            
            move_response = requests.post(adv_url+ep_move, headers=param, json=direction)
            move_resp = move_response.text
            mr = json.loads(move_resp)
            
            cur_room = mr['room_id']
            cur_cd = mr['cooldown']
            if cur_cd > 500:
                print('uh-oh')
                break
            time.sleep(cur_cd)

pkl1 = graph.vertices
pkl2 = graph.data
pickle.dump(pkl1, open('graph_vertices.p','wb'))
pickle.dump(pkl2, open('room_data.p','wb'))

