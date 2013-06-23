#! usr/bin/python

class GraphEdge (object):
  """
  Non-directed edge
  """
  def __init__ (self, n1, n2, data=None):
    self.end_nodes = (n1, n2)
    self.data = data

  def get_data (self):
    return self.data

class GraphVertex (dict):
  def __init__ (self, data=None):
    super(GraphVertex, self).__init__()
    self.update({'data': data,
                 'adjacent': []})

  def add_edge (self, edges):
    """
    adjacent is in the form of [edge1, edge2, edge3, ...]
    """
    #print self
    #print edges
    for edge in edges:
      #print edge.end_nodes
      if self in edge.end_nodes:
        nodes = list(edge.end_nodes)
        #print nodes
        nodes.remove(self)
        adjacent = nodes[0]
        self['adjacent'].append((adjacent, edge))

  def get_adjacent_edge (self):
    return self['adjacent']

  def get_adjacent (self):
    return map(lambda x: x[0], self['adjacent'])
  
  def get_data (self):
    return self['data']

class Graph (object):
  def __init__ (self):
    self.vertice = []
    self.edges = []

  def add_vertex (self, data=None):
    vertex = GraphVertex(data)
    self.vertice.append(vertex)
    return vertex

  def add_edge (self, n1, n2, data=None):
    if (n1 not in self.vertice) or (n2 not in self.vertice): 
      print 'Invalid edge'
      return None
    edge = GraphEdge(n1, n2, data)
    # Edge in graph is bi-directed (whilst in digraph is uni-directed)
    n1.add_edge([edge])
    n2.add_edge([edge])
    self.edges.append(edge)
    self.handle_edge(edge)
    return edge

  def dfs (self, vertex):
    vertex.update({'dfs': []})
    for adjacent in vertex.get_adjacent():
      if adjacent.has_key('dfs') == False:
        vertex['dfs'].append(adjacent)
        self.dfs(adjacent)

  def bfs (self, vertex=None):
    if vertex == None:
      vertex = self

    bfs_queue = [vertex]
    vertex.update({'bfs': []})
    while len(bfs_queue) > 0:
      vertext = bfs_queue.pop(0)
      for adjacent in vertext.get_adjacent():
        # adjacent is not visited yet
        if adjacent.has_key('bfs') == False:
          vertext['bfs'].append(adjacent)
          adjacent.update({'bfs': []})
          bfs_queue.append(adjacent)

  def dfnlow (self, vertex=None, dfn=[0]):
    if vertex == None:
      vertex = self

    vertex.update({'dfs': [], 'dfn': dfn[0], 'low': dfn[0]})
    for adjacent in vertex.get_adjacent():
      # adjacent is not visited yet
      if adjacent.has_key('dfs') == False:
        vertex['dfs'].append(adjacent)
        dfn[0] = dfn[0] + 1
        self.dfnlow(adjacent, dfn)

      if vertex not in adjacent['dfs']:
        vertex['low'] = min([vertex['low'], adjacent['low']])

  def handle_edge (self, edge):
    """
    Override to handle the new constructed edge
    """
    pass

  def handle_vertex (self, vertex):
    """
    Override to handle the new constructed vertex
    """
    pass

class Digraph (Graph):
  """
  Class of directed graphs
  """
  # Override add_edge method, since the edge in digraph is unidirected
  def add_edge (self, n1, n2, data=None):
    if (n1 not in self.vertice) or (n2 not in self.vertice): 
      print 'Invalid edge'
      return None
    edge = GraphEdge(n1, n2, data)
    n1.add_edge([edge])
    self.edges.append(edge)
    self.handle_edge(edge)
    return edge

  

if __name__ == '__main__':
  g2 = Graph()
  v2 = map(lambda x: g2.add_vertex(x), range(0, 10))
  e200 = g2.add_edge(v2[0], v2[1])
  e201 = g2.add_edge(v2[1], v2[2])
  e202 = g2.add_edge(v2[1], v2[3])
  e203 = g2.add_edge(v2[2], v2[4])
  e204 = g2.add_edge(v2[3], v2[4])
  e205 = g2.add_edge(v2[3], v2[5])
  e206 = g2.add_edge(v2[5], v2[6])
  e207 = g2.add_edge(v2[5], v2[7])
  e208 = g2.add_edge(v2[6], v2[7])
  e209 = g2.add_edge(v2[7], v2[8])
  e210 = g2.add_edge(v2[7], v2[8])
  e211 = g2.add_edge(v2[7], v2[9])
  g2.dfnlow(v2[3])
  dfnlow_2 = map(lambda x: x['low'], v2) 
  print dfnlow_2
  print [2, 0, 0, 0, 0, 5, 5, 5, 8, 9] == dfnlow_2
  
