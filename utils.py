base_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
init_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
take_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
sell_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/'
move_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
status_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
examine_url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/'

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size > 0:
            return self.queue.pop(0)
        else:
            return None
    @property
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
        self.data = []

    def load_data(self,dictionary):
        self.vertices = dictionary

    def add_vertex(self, vertex_id, dirs):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {i: "?" for i in dirs}

    def add_data(self, datum):
        self.data.append(datum)

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        If both exits, connect v1 to v2
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError('That vertex does not exist')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create an empty queue and enqueue the starting vertex ID
        queue = Queue()
        queue.enqueue(starting_vertex)
        # create an emtpy Set to stoe the visited vertices
        visited = set()
        # while the queue is not empty ...
        while queue.size() > 0:
            # dequeue the first vertex
            vert = queue.dequeue()
            # if that vertex has not been visited..
            if vert not in visited:
                # mark it as visited
                visited.add(vert)
                print(vert)
                # then add all of its neighbors to the back of the queue
                for neighbor in self.vertices[vert]: # self.get_neighbors(vert)
                    queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create an empty stack and push the starting vertex ID
        stack = Stack()
        stack.push(starting_vertex)
        # create an empty Set to store the visited vertices
        visited = set()
        # while the stack is not empty ...
        while stack.size() > 0:
            # pop the first vertex
            vert = stack.pop()
            # if that vertex has not been visited ..
            if vert not in visited:
                # mark it is visited
                visited.add(vert)
                print(vert)
                # then add all of its neighbors to the top of the stack
                for neighbor in self.vertices[vert]: #self.get_neighbors(vert)
                    stack.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        print(starting_vertex)
        for neighb_vert in self.vertices[starting_vertex]:
            if neighb_vert not in visited:
                self.dft_recursive(neighb_vert, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create an empty queue and enqueue A-PATH-TO the starting vertex ID
        # create a Set to store the visited vertices
        # while the queue is not empty ..
            # dequeue the first PATH
            # grab the last vertex from the PATH
            # if that vertex has not been visited ..
                # check if its the target
                    #if yes, return path
                #mark it as visited
                # add A PATH TO its neighbots to the back of the queue
                    # copt the path
                    # append the neighbor to the back
        
        
        # create an empty Queue 
        queue = Queue()
        #push the starting vertex ID as list
        queue.enqueue([starting_vertex])
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
                if vert == destination_vertex:
                    return path
                # mark it is visited
                visited.add(vert)
                # then add all of its neighbors to the top of the stack
                for neighbor in self.vertices[vert]: #self.get_neighbors(vert)
                    #copy path to avoid pass by reference
                    new_path = list(path) # make a copy
                    new_path.append(neighbor)
                    queue.enqueue(new_path)


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
         # create an empty stack 
        stack = Stack()
        #push the starting vertex ID as list
        stack.push([starting_vertex])
        # create an empty Set to store the visited vertices
        visited = set()
        # while the stack is not empty ...
        while stack.size() > 0:
            # pop the first vertex
            path = stack.pop()
            vert = path[-1]
            # if that vertex has not been visited ..
            if vert not in visited:
                #check for target
                if vert == destination_vertex:
                    return path
                # mark it is visited
                visited.add(vert)
                # then add all of its neighbors to the top of the stack
                for neighbor in self.vertices[vert]: #self.get_neighbors(vert)
                    #copy path to avoid pass by reference
                    new_path = list(path) # make a copy
                    new_path.append(neighbor)
                    stack.push(new_path)


    def dfs_recursive(self, starting_vertex, target, visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        if path is None:
            path = []
        
        visited.add(starting_vertex)
        path = path + [starting_vertex]
        if starting_vertex == target:
            return path
        for neighb_vert in self.vertices[starting_vertex]:
            if neighb_vert not in visited:
                new_path = self.dfs_recursive(neighb_vert, target, visited, path)
                if new_path:
                    return new_path
        return None
    
    def __repr__(self):
        return str(self.vertices)


