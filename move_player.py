import sys
from utils import Stack,Queue,Graph, base_url
import pickle, requests, json, random, time, os
from dotenv import load_dotenv
# from mining_room_path import mining_room_path
load_dotenv()
token = os.getenv('API_KEY')  #must specify the token as an API_KEY in the .env file and pipenv install python-dotenv
print(token)

graph_verts = pickle.load(open('graph_vertices.p', 'rb'))
island = Graph(graph_verts)

def send_move(data,cooldown=1):
    auth = {'Authorization': f"Token {token}"}
    time.sleep(cooldown)
    move_response = requests.post(f"{base_url}/move",headers=auth, json=data)
    next_room = move_response.json()
    next_cool = next_room['cooldown']
    time.sleep(next_cool)
    return next_room

current = island.get_current_room(token)
print("You are currently in room:", current['room_id'])

target_room = int(input("Enter the room_id of the room you like to move to: "),10)
print('target room', target_room, type(target_room))
if not island.vertices[target_room]:
    print('invalid room_id. Not found on the Island...')
    sys.exit()
else:
    mine_room = 207
    init_cooldown = current['cooldown']

    mining_room_path = island.bfs_move(current['room_id'],target_room)
    print('The path to get to your target room: ', mining_room_path)


    for i,path_id in enumerate(mining_room_path):
        try:
            next_id = mining_room_path[i+1]
        except:
            next_id = None
            break
    
        current = island.vertices[path_id]
        direction = {way:current[way] for way in current if current[way] == next_id}
        way = [*direction.keys()][0]
        next = [*direction.values()][0]
        data = {'direction':way, 'next_id': next}
        next_room = send_move(data,init_cooldown)
        print(next_room)

    















# for move in mine_room:
            
#     if complete_graph.vertices[cur_room][move] != '?':
#         known_room_id = complete_graph.vertices[cur_room][move]
#         direction = {'direction': move, 'next_room_id': str(known_room_id)}
#     else:
#         direction = {'direction': move}
# ​
#     #prev_room = cur_room
    
#     move_response = requests.post(move_url, headers=param, json=direction)
#     mr = move_response.json()
    
#     cur_room = mr['room_id']
#     cur_cd = mr['cooldown']
#     #cur_items = mr['items']
#     time.sleep(cur_cd)
# ​
# print(target, cur_room)



# init_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
# take_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
# sell_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
# move_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
# status_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
# examine_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'
# ​
# ​
# ​
# param = {'Authorization': 'Token 0a420d1c5e0e17faa8835f6b9bb35ef63ab4b502'}
# ​
# init_response = requests.get(init_url, headers=param)
# ir = init_response.json()
# cur_room = ir['room_id']
# cur_cd = ir['cooldown']
# time.sleep(cur_cd)
# ​
# complete_graph=Graph()
# graph_verts=pickle.load(open('graph_vertices.p','rb'))
# # room_data=pickle.load(open('room_data.p','rb'))
# complete_graph.vertices = graph_verts
# ​