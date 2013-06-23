#! usr/bin/python
from graph import Digraph

def all_costs (adjacency_matrix):
  n = len(adjacency_matrix)
  a = []
  a.extend(adjacency_matrix)
  for k in range(0, n):
    new_a = []
    for i in range(0, n):
      new_a.append([])
      for j in range(0, n):
        new_a[i].append(min([a[i][j], a[i][k] + a[k][j]]))
        print '%6d' % new_a[i][j],
      print ''
    a = new_a
    print ''
    #dummy = input('Enter') 

class RoadNetwork (Digraph):
  def __init__ (self):
    super(RoadNetwork, self).__init__()
    self.__max_distance_value = 10
    self.places = {}
  
  def add_road (self, from_, to, distance):
    if from_ not in self.places:
      vertex_from = self.add_vertex(data={})
      self.__clear_vertex_data(vertex_from, {'name': from_})
      self.places.update({from_: vertex_from})
    else:
      vertex_from = self.places[from_]
  
    if to not in self.places:
      vertex_to = self.add_vertex(data={})
      self.__clear_vertex_data(vertex_to, {'name': to})
      self.places.update({to: vertex_to})
    else:
      vertex_to = self.places[to]
  
    self.add_edge(vertex_from, vertex_to, {'distance': distance})
    self.__max_distance_value += distance

  def shortest_path (self, from_):
    """
    Find the shortest path from specified place to all other reachable ones.
    Return a dictionary in the form of 
        {place_1: {'distance': distance_1, 'path': [intermediate_1, intermediate_2, intermediate_3, ...]},
         place_2: {'distance': distance_2, 'path': [intermediate_1, intermediate_2, intermediate_3, ...]},
         place_3: {'distance': distance_3, 'path': [intermediate_1, intermediate_2, intermediate_3, ...]},
         ...
        }
    """
    if from_ not in self.places:
      return None

    from_ = self.places[from_]

    # Initialization
    self.__initialize()
    
    from_data = from_.get_data()
    from_data.update({'distance': 0})
    result = {}

    while True:
      nearest = {'distance': self.__max_distance_value}
      from_data = from_.get_data()
      from_data.update({'found': True})
      #print 'Node %s distance %d path' % (from_data['name'], from_data['distance']),
      #print map(lambda x: x.get_data()['name'], from_data['path'])
      #print from_data['path']
      for adjacent, edge in from_.get_adjacent_edge():
        adjacent_data = adjacent.get_data()
        edge_data = edge.get_data()
        #print 'Check edge (%s, %s) distance %d' % (from_data['name'], adjacent_data['name'], edge_data['distance'])
        if adjacent_data['found'] != True and adjacent_data['distance'] > from_data['distance'] + edge_data['distance']:
          adjacent_data.update({'distance': from_data['distance'] + edge_data['distance'],
                                'path': from_data['path'] + [from_data['name']]})
        #print 'Adjacent %s distance %d' % (adjacent_data['name'], adjacent_data['distance'])

      #return {}

      for vertex in self.vertice:
        vertex_data = vertex.get_data()
        #print 'Choose: node %s distance %d (min distance %d)' % (vertex_data['name'], vertex_data['distance'], nearest['distance'])
        if vertex_data['found'] != True and vertex_data['distance'] < nearest['distance']:
          nearest = vertex_data
          from_ = vertex
      #return {}
      if nearest['distance'] == self.__max_distance_value:
        break
      else:
        result.update({nearest['name']: {'distance': nearest['distance'], 'path': nearest['path'] + [nearest['name']]}})


    return result


  def __initialize (self):
    for vertex in self.vertice:
      self.__clear_vertex_data(vertex)
          
  def __clear_vertex_data (self, vertex, default_data={}):
    data = vertex.get_data()
    data.update({'distance': self.__max_distance_value, 'found': False, 'path': []})
    data.update(default_data)

if __name__ == '__main__':
  am = [[0, 4, 11],
        [6, 0, 2],
        [3, 1000, 0]]
  all_costs(am)
  
  rn = RoadNetwork()
  rn.add_road('v0', 'v1', 50)
  rn.add_road('v0', 'v2', 10)
  rn.add_road('v0', 'v4', 45)
  rn.add_road('v1', 'v2', 15)
  rn.add_road('v1', 'v4', 10)
  rn.add_road('v2', 'v0', 20)
  rn.add_road('v2', 'v3', 15)
  rn.add_road('v3', 'v1', 20)
  rn.add_road('v3', 'v4', 35)
  rn.add_road('v4', 'v3', 30)
  rn.add_road('v0', 'v1', 50)
  rn.add_road('v5', 'v3', 3)
  #print len(rn.vertice)
  #print rn.vertice
  """
  [{'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb319d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31890>), ({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb319d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb318d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb319d0>), ({...}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({...}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31910>), ({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb319d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31b10>)]}, 
   {'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31890>), ({...}, <graph.GraphEdge object at 0x10fb318d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31910>), ({...}, <graph.GraphEdge object at 0x10fb31b10>)]}, <graph.GraphEdge object at 0x10fb319d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, 
   {'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31890>), ({...}, <graph.GraphEdge object at 0x10fb318d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31950>), ({...}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31910>), ({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31b10>)]}, <graph.GraphEdge object at 0x10fb319d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31a10>)]}, 
   {'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31890>), ({...}, <graph.GraphEdge object at 0x10fb318d0>), ({...}, <graph.GraphEdge object at 0x10fb31910>), ({...}, <graph.GraphEdge object at 0x10fb31b10>)]}, <graph.GraphEdge object at 0x10fb319d0>), ({...}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({...}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({...}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31ad0>)]}, 
   {'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31890>), ({...}, <graph.GraphEdge object at 0x10fb318d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31910>), ({...}, <graph.GraphEdge object at 0x10fb31b10>)]}, <graph.GraphEdge object at 0x10fb319d0>), ({...}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, 
   {'data': {'found': False, 'distance': 0, 'name': 'v5', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v3', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v1', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v2', 'path': []}, 'adjacent': [({'data': {'found': False, 'distance': 0, 'name': 'v0', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31890>), ({...}, <graph.GraphEdge object at 0x10fb318d0>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31910>), ({...}, <graph.GraphEdge object at 0x10fb31b10>)]}, <graph.GraphEdge object at 0x10fb319d0>), ({...}, <graph.GraphEdge object at 0x10fb31a10>)]}, <graph.GraphEdge object at 0x10fb31950>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31990>)]}, <graph.GraphEdge object at 0x10fb31a50>), ({'data': {'found': False, 'distance': 0, 'name': 'v4', 'path': []}, 'adjacent': [({...}, <graph.GraphEdge object at 0x10fb31ad0>)]}, <graph.GraphEdge object at 0x10fb31a90>)]}, <graph.GraphEdge object at 0x10fb31b50>)]}
  ]
  """
  #print rn.edges
  #print rn.places.keys()
  #print rn.places.values()
  #print map(lambda x: x.get_data()['name'], rn.places.values())
  
  result = rn.shortest_path('v0')
  #print len(result)
  print result
  print result == {'v1': {'distance': 45, 'path': ['v0', 'v2', 'v3', 'v1']}, 'v2': {'distance': 10, 'path': ['v0', 'v2']}, 'v3': {'distance': 25, 'path': ['v0', 'v2', 'v3']}, 'v4': {'distance': 45, 'path': ['v0', 'v4']}}
  """
  {'v1': {'distance': 45, 'path': ['v0', 'v2', 'v3']}, 
   'v2': {'distance': 10, 'path': ['v0']}, 
   'v3': {'distance': 25, 'path': ['v0', 'v2']}, 
   'v4': {'distance': 45, 'path': ['v0']}}
  """





