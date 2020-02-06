from utils import Queue, Graph, base_url
import requests, json, os, pickle
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('API_KEY')
graph_verts = pickle.load(open('graph_vertices.p', 'rb'))
graph = Graph(graph_verts)


# def get_current_room():
#     auth = {'Authorization': f'Token {token}'}
#     response = requests.get(f"{base_url}/init", headers=auth)
    
#     if response.status_code == 200:
#         print('Success')
#     elif response.status_code == 404:
#         print('Not Found')

#     return json.loads(response.text)  #loads is for a string.  json.load is for a file.  

# current = get_current_room()
# room_id = current['room_id']
# mine_room_id = 207
# print(room_id)

def bfs_mine(graph,start_vert,end_vert):
    print(start_vert,end_vert)
    queue = Queue()
    queue.enqueue([start_vert])
    visited = set()

    while queue.size > 0:
        path = queue.dequeue()
        # print('path', path)
        vert = path[-1]
        # print('vert', vert)

        if vert not in visited:
            if vert == end_vert:
                return path
            visited.add(vert)

            # print('graph vert', list(graph.vertices[vert].values()))
            waze = list(graph.vertices[vert].values())
            for neighbor in waze:
                new_path = list(path)
                new_path.append(neighbor)
                queue.enqueue(new_path)

mine_room = 207
mining_room_path = bfs_mine(graph,55,207)

