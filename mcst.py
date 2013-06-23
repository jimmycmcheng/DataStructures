#! usr/bin/python

from unfd import UnionFind
from bintree import MinHeap
from graph import *

class GraphCost (Graph):
  #def __init__ (self):
  #  super(GraphCost, self).__init__()
    
  def add_edge (self, n1, n2, cost):
    return super(GraphCost, self).add_edge(n1, n2, {'cost': cost})
  
  def generate_minimum_cost_spanning_tree (self):
    return self.__generate_minimum_cost_spanning_tree_kruskal()

  def __generate_minimum_cost_spanning_tree_kruskal (self):
    # Put all edge into Min Heap
    min_heap = MinHeap()
    map(lambda x: min_heap.insert(x.data['cost'], x), self.edges)

    union_find = UnionFind()
    selected_edges = []

    cost, edge = min_heap.delete()
    while len(selected_edges) < len(self.vertice) - 1:
      #print 'cost %d, (%d, %d)' % (cost, edge.end_nodes[0]['data'], edge.end_nodes[1]['data'])
      if union_find.is_in_the_same_set(edge.end_nodes[0]['data'], edge.end_nodes[1]['data']) == False:
        union_find.union(edge.end_nodes[0]['data'], edge.end_nodes[1]['data'])
        selected_edges.append(edge)
        #print 'Selected: ',
      cost, edge = min_heap.delete()

    return selected_edges

  def __generate_minimum_cost_spanning_tree_prim (self):
    selected_edges = []
    

if __name__ == '__main__':
  g1 = GraphCost()
  v1 = map(lambda x: g1.add_vertex(x), range(0, 7))
  e100 = g1.add_edge(v1[0], v1[1], 28)
  e101 = g1.add_edge(v1[0], v1[5], 10)
  e102 = g1.add_edge(v1[1], v1[2], 16)
  e103 = g1.add_edge(v1[1], v1[6], 14)
  e104 = g1.add_edge(v1[2], v1[3], 12)
  e105 = g1.add_edge(v1[3], v1[4], 22)
  e106 = g1.add_edge(v1[3], v1[6], 18)
  e107 = g1.add_edge(v1[4], v1[5], 25)
  e108 = g1.add_edge(v1[4], v1[6], 24)
  #g1.dfnlow(v1[3])
  #dfnlow_1 = map(lambda x: x['low'], v1) 
  #print dfnlow_1
  #print dfnlow_1 == dfnlow_2
  #print g1.min_heap
  #print map(lambda x: (x[0], (x[1].end_nodes[0]['data'], x[1].end_nodes[1]['data'])), g1.min_heap[1:])

  selected_edges = g1.generate_minimum_cost_spanning_tree()
  for edge in selected_edges:
    print 'cost %d, (%d, %d)' % (edge.data['cost'], edge.end_nodes[0]['data'], edge.end_nodes[1]['data'])

  print set(selected_edges) == set([e101, e104, e103, e102, e105, e107])
  #print set([e101, e104, e103, e102, e105, e107])




