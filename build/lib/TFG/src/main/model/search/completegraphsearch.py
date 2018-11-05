# AUTHOR: Juan Manuel Rey Escobar

import clingo
import time
from searchnode import SearchNode
from memory_profiler import memory_usage
from TFG.src.main.model.util.searchutils import expand
from TFG.src.main.model.util.atomutils import print_solution
from TFG.src.main.model.util.atomutils import decorate_action
from TFG.src.main.model.util.atomutils import get_solution_size

            
class CompleteGraphSearch:
    def __init__(self):
        self.domain = None
    
    def add_domain(self,domain):
        self.domain = domain
                    
    """ Searches for ALL possible plans """              

    def search(self, initial, fringe, actions, fluents, use_heuristic, bfs):
        """ Fringe: data structure for storing search nodes """
        fringe = fringe
        """ Maximum number of nodes in the fringe """
        max_size = 0
        """ Number of explored nodes """
        explored = 0
        """ Set of visited nodes """
        closed = set()
        """ Node which stores the initial state """
        root_node = SearchNode(initial, None, [], 0, 0, 0)
        fringe.push(root_node)
        """ The goal predicate """
        goal = clingo.Function("goal", [0])
        """ List of goal nodes """
        goal_nodes = []
        """ Minimun solution size """
        min_sol_size = 0
        """ The instant which marks the start of the execution """
        start = time.time()
        while 1:
            if max_size < fringe.size():
                max_size = fringe.size()
            """ Empty fringe means there are no solution """
            if (fringe.is_empty()):
                """ The instant which marks the end of the execution """
                end = time.time()
                """ The amount of memory usage in MB """
                memory = memory_usage()  

                if len(goal_nodes) == 0:
                    print('UNSATISFIABLE')
                    print('Execution time: ') ,
                    print(end - start) ,
                    print('s')
                    print('Memory usage: ') ,
                    print(memory[0]) ,
                    print('MB')
                    print('Explored states: ') ,
                    print(explored) 
                    print('Maximum number of nodes stored: ') ,
                    print(max_size) 
                    return 0
                else:
                    print('SATISFIABLE')
                    print('Solution found: ')
                    for element in goal_nodes[0].state:
                        if element != (clingo.Function(str(goal))):
                            print(clingo.Function(decorate_action(str(element)))) ,
                    print('')
                    print('Execution time: ') ,
                    print(end - start) ,
                    print('s')
                    print('Memory usage: ') ,
                    print(memory[0]) ,
                    print('MB')
                    print('Explored states: ') ,
                    print(explored)
                    print('Maximum number of nodes stored: ') ,
                    print(max_size) 
                    i = 1
                    for node in goal_nodes:
                        print('Plan ' + str(i) + ': ') ,
                        print_solution(node)
                        i += 1
                    return 1
            
            """ Recover fringe's first node """
            node = fringe.pop()
            """ We check if the recovered node is a posible solution """
            if (clingo.Function(str(goal))) in frozenset(node.state):
                if min_sol_size == 0:
                    min_sol_size = get_solution_size(node)
                if get_solution_size(node) == min_sol_size:
                    goal_nodes.append(node)
            """ If it is not a solution, then we have to store it in closed """
            if frozenset(node.state) not in closed:
                closed.add(frozenset(node.state))
                explored = explored + 1
                for child in expand(self.domain, node, actions, fluents, use_heuristic, bfs):
                    fringe.push(child)
