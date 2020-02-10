from utils import *
import requests,json,random,time,pickle,sys
from requests.exceptions import HTTPError
#must specify the token as an API_KEY in the .env file and pipenv install python-dotenv
# auth = get_auth()

g = graph.vertices

while len(visited) < 500:
  print(len(visited),'rooms visited')
  r = get_current_room()
  room_id = r['room_id']
  roomz = explore_exits(r)
  print('roomz from explore_exits()', roomz)
  for rz in roomz:
    visited.add(rz)
  g_roomz = {r_id:g[r_id] for r_id in roomz}
  print('graph of explored rooms for room id', room_id," : ", g_roomz)
  unexplored = {r_id:g[r_id] for r_id in g_roomz if '?' in g[r_id].values()}
  print('unexplored', unexplored)

  if len(unexplored):
    next_id,waze = random.choice([*unexplored.items()])
  else:
  print('all neighbors explored\n', graph)
  g_unexplored = {r_id:g[r_id] for r_id in g if '?' in g[r_id].values()}
  print('total graph unexplored', g_unexplored)
  traverse_id,trav_waze = random.choice([*g_unexplored.items()])
  graph.bfs(room_id,traverse_id)

  way = [w for w in g[room_id] if g[room_id][w] == next_id]
  print(way)
  if len(way):
    way = way[0]

  next = move(way)
  next_roomz = explore_exits(next)
  for nr in next_roomz:
    visited.add(nr)

print('rooms visited', len(visited), 'visited', visited)
print(graph)