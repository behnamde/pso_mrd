from collections import defaultdict
from distutils.log import error
from tkinter.messagebox import NO

class Graph:
    def __init__(self, graph=None) -> None :
        """Initializes a graph object. 

        Args: Defaults to None
            graph (dict, optional): If no dictionary or 
            None is given, a defaultdict will be used.
        """
        if graph is None or type(graph) != dict:
            graph = defaultdict(list)
        self._graph = graph
    
    def generateGraph(self, edges):
        """Creates a graph out of the input list of
        lists(queue).

        Args:
            edges (queue): a list of lists (queue)
            that includes the lists of pairs of the
            nodes that make edges of the graph.

        Returns:
            dict: a dictionary that represents
            the graph nodes as keys and connected 
            nodes to each node in lists as values.
        """
        
        # Adjacency lists of the graph 
        for edge in edges:
            node_a, node_b = edge[0], edge[1]
            self._graph[node_a].append(node_b)
            self._graph[node_b].append(node_a)
        return self._graph


    def bestPath(self, start, destination):
        """Finds the shortest path between two given
        node of the given graph if any.

        Args:
            start (int): node to start a path
            destination (int): node to end a path

        Returns:
            list: a list of nodes that make 
            a path between start and end including
            start point and end point
        """
        checked = []
        # In a breadth-first search, a queue is 
        # utilized to traverse the graph.
        queue = [[start]]
        
        if start == destination:
            print("The start and the destination"\
                "of the path are the same node")
            return
        
        # The queue is used to explore the graph
        # in a while loop
        while queue:
            path = queue.pop(0)
            node = path[-1]
            # If the current node hasn't been visited,
            # this condition is true.
            if node not in checked:
                neighbors = self._graph[node]
                # Iterate across the node's neighbors
                # in a for loop.
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    # If the destination node is a 
                    # neighbor, this condition must 
                    # be met.
                    if neighbor == destination:
                        return queue[-1]
                checked.append(node)

        else: 
            return f"There is no connection between"\
                "{start} and {destination}"

    def allPaths(self, start_end_nodes):
        """Provides list of all paths for start/end nodes
        
        Args:
            start_end_nodes (list): list of two lists
            _list_[0] contains the starts leaves
            _list_[1] contains the destinations leaves
            

        Returns:
            list: a list of all paths
        """ 
        starts = start_end_nodes[0]
        destinations = start_end_nodes[1]
        
        # an empty list to append path lists into it
        paths=[]
        paths.append(self.bestPath(starts[0],
                                     destinations[0]))
        # loop for iterate all start and end nodes
        # including the start node and the end one
        for start in starts:
            for destination in destinations:
                # append a path using given start-end
                # points
                paths.append(self.bestPath(start,
                                     destination))
                # if not path in paths:
                #     for item in paths:
                #         if not any(i in path 
                #                    for i in item):
                #             paths.append(path)
        return paths

    def maxCount(self, colored_nodes):
        """Counting maximum paths for given 
        colored_nodes that are start_end_nodes
        while there is no common node in the 
        two different path 

        Args:
            colored_nodes (queue): a list of all
            paths of colored nodes while one color
            is start and the other is end

        Returns:
            list: a list of 2 elements 
            _list_[0]: len(all uncommon paths' lists)
            _list_[1]: all uncommon paths' list
        """
        # path creator using colored nodes
        path_list = self.allPaths(colored_nodes)
        
        # preserved list for storing distinct paths
        new_list = []
        # check set for iterating the paths
        # each new dictinct path will store 
        # its elements here in a set
        # elements of first memeber of the 
        # input paths list will be preserved at first
        check_set = set(path_list[0])
        
        # first member of the list will be always unique
        new_list.append(path_list[0])
        
        # for loop to iterate the paths list
        for item in path_list:
            # check if any of nodes are in common or not
            if not any(i in item for i in check_set):
                # add new nodes to the check set
                for i in item:
                    check_set.add(i)
                # append the item to new list
                new_list.append(item)
            # if there is any node in common loop will start
            # again without doing anything
            else:
                pass
        
        return list((len(new_list), new_list))
    
    # def uncommonPathCount(self, start_end_nodes):
    #     return len(self.allPaths(start_end_nodes))

  
if __name__ == "__main__":
    test_cases = {'test_case_0': """6 2 2
1 2
2 3
4 2
5 7
6 5
4 5
1 3
7 6""",
'test_case_1': """18 4 3
1 3
3 2
4 3
5 4
6 5
5 19
7 6
8 6
9 4
10 9
11 10
12 10
13 9
18 13
14 13
15 14
16 15
17 15
1 2 7 8
18 16 12 19""",
'test_case_2': """20 5 6
1 3
3 4
2 3
4 5
4 9
5 6
5 19
6 7
6 8
19 20
19 21
9 10
9 13
10 11
10 12
13 18
13 14
14 15
15 16
15 17
1 2 7 8 21
11 12 16 17 18 20""",
'test_case_3': """25 5 5
1 3
3 4
2 3
4 5
4 9
5 6
5 19
6 7
6 8
6 21
19 20
9 10
9 13
10 11
10 12
13 18
13 14
14 15
14 22
15 16
15 17
22 24
22 23
23 25
1 2 7 8 21
11 12 16 18 25""",
'test_case_4': """25 7 6
1 3
3 4
2 3
4 5
4 9
5 6
5 19
6 7
6 8
6 21
19 20
9 10
9 13
10 11
10 12
13 18
13 14
14 15
14 22
15 16
15 17
22 24
22 23
23 25
1 2 7 8 21 24 17
11 12 16 18 25 20"""
}

    for key, test_case in test_cases.items():
        lines = test_case.split('\n')
        # print(lines)
        lenght = len(lines)
        final_list = [[int(item) for item in 
                       lines[i].split(' ')] 
                      for i in range(lenght)]
        edges = final_list[1:-2]
        colored_nodes = final_list[-2:]
        g = Graph()
        g.generateGraph(edges)
        print(f"max paths in {key} without any "\
            f"common node: {g.maxCount(colored_nodes)[0]}")
        print(g.maxCount(colored_nodes)[1])