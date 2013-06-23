#! usr/bin/python

class UnFdNode (dict):
  def __init__ (self, data=None, parent=None):
    super(UnFdNode, self).__init__()
    self.update({'data': data,
                 'parent': parent,
                 'count': 1})
  def get_data (self):
    return self['data']
  
  def get_parent (self):
    return self['parent']

  def set_parent (self, parent):
    #if self['parent'] != None:
    #  self['parent']['count'] = self['parent']['count'] - self['count']
    self['parent'] = parent
    #self['parent']['count'] = self['parent']['count'] + self['count']

  def get_count (self):
    return self['count']

  def set_count (self, count):
    self['count'] = count

class UnionFind (object):
  def __init__ (self):
    self.__all_nodes = {}

  def union (self, i, j):
    if i not in self.__all_nodes.keys():
      node_i = UnFdNode(data=i)
      self.__all_nodes.update({i: node_i})
    else:
      node_i = self.__all_nodes[i]
  
    if j not in self.__all_nodes.keys():
      node_j = UnFdNode(data=j)
      self.__all_nodes.update({j: node_j})
    else:
      node_j = self.__all_nodes[j]
  
    root_i = self.__find_root(node_i)
    root_j = self.__find_root(node_j)
    total_count = root_i.get_count() + root_j.get_count()
    if root_i.get_count() > root_j.get_count():
      root_i.set_count(total_count)
      root_j.set_parent(root_i)
    else:
      root_j.set_count(total_count)
      root_i.set_parent(root_j)
  
  def find (self, i):
    if self.__all_nodes.has_key(i):
      return self.__find_root(self.__all_nodes[i]).get_data()
    else:
      return None
  
  def is_in_the_same_set (self, i, j):
    if self.__all_nodes.has_key(i) and self.__all_nodes.has_key(j):
      return self.find(i) == self.find(j)
    else:
      return False
  
  def __find_root (self, node):
    stack = []
    root = node
    while root.get_parent() != None:
      stack.append(root)
      root = root.get_parent()
    #print stack
    if len(stack) > 1:
      for n in stack[:-1]:
        n.get_parent().set_count(n.get_parent().get_count() - n.get_count())
        n.set_parent(root)
    #map(lambda x: x.set_parent(root), stack)
    return root
    
  
if __name__ == '__main__':
  uf = UnionFind()
  uf.union(1,3)
  uf.union(3,5)
  uf.union(7,9)
  uf.union(11,13)
  uf.union(9,13)
  uf.union(13,5)

  #print uf.all_nodes
  """
  {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   5: {'count': 1, 'data': 5, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}
   }
  {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   5: {'count': 1, 'data': 5, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}}
  {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   5: {'count': 2, 'data': 5, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}}
  """
  
  #print find(13)
  #print find(5)
  #print uf.all_nodes == {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 5: {'count': 1, 'data': 5, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 13: {'count': 7, 'data': 13, 'parent': None}}
  """
  {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   5: {'count': 1, 'data': 5, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}}
  {1: {'count': 1, 'data': 1, 'parent': {'count': 1, 'data': 3, 'parent': {'count': 0, 'data': 5, 'parent': None}}}, 
   3: {'count': 1, 'data': 3, 'parent': {'count': 0, 'data': 5, 'parent': None}}, 
   5: {'count': 0, 'data': 5, 'parent': None}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 1, 'data': 9, 'parent': {'count': 1, 'data': 13, 'parent': {'count': 0, 'data': 5, 'parent': None}}}}, 
   9: {'count': 1, 'data': 9, 'parent': {'count': 1, 'data': 13, 'parent': {'count': 0, 'data': 5, 'parent': None}}}, 11: {'count': 1, 'data': 11, 'parent': {'count': 1, 'data': 13, 'parent': {'count': 0, 'data': 5, 'parent': None}}}, 13: {'count': 1, 'data': 13, 'parent': {'count': 0, 'data': 5, 'parent': None}}}
  {1: {'count': 1, 'data': 1, 'parent': {'count': 2, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   3: {'count': 2, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   5: {'count': 1, 'data': 5, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}}

  """

  uf.union(2,4)
  uf.union(6,8)
  uf.union(4,8)
  
  #print uf.all_nodes == {1: {'count': 1, 'data': 1, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 2: {'count': 1, 'data': 2, 'parent': {'count': 2, 'data': 4, 'parent': {'count': 4, 'data': 8, 'parent': None}}}, 3: {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 4: {'count': 2, 'data': 4, 'parent': {'count': 4, 'data': 8, 'parent': None}}, 5: {'count': 1, 'data': 5, 'parent': {'count': 3, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 6: {'count': 1, 'data': 6, 'parent': {'count': 4, 'data': 8, 'parent': None}}, 7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 8: {'count': 4, 'data': 8, 'parent': None}, 9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 13: {'count': 7, 'data': 13, 'parent': None}}

  """
  {1: {'count': 1, 'data': 1, 'parent': {'count': 2, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   2: {'count': 1, 'data': 2, 'parent': {'count': 2, 'data': 4, 'parent': {'count': 4, 'data': 8, 'parent': None}}}, 
   3: {'count': 2, 'data': 3, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   4: {'count': 2, 'data': 4, 'parent': {'count': 4, 'data': 8, 'parent': None}}, 
   5: {'count': 1, 'data': 5, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   6: {'count': 1, 'data': 6, 'parent': {'count': 4, 'data': 8, 'parent': None}}, 
   7: {'count': 1, 'data': 7, 'parent': {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}}, 
   8: {'count': 4, 'data': 8, 'parent': None}, 
   9: {'count': 2, 'data': 9, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   11: {'count': 1, 'data': 11, 'parent': {'count': 7, 'data': 13, 'parent': None}}, 
   13: {'count': 7, 'data': 13, 'parent': None}}
  """

  i, j = 4, 9
  print 'Test %d and %d: %s' % (i, j, uf.is_in_the_same_set(i, j) == False)
  i, j = 2, 6
  print 'Test %d and %d: %s' % (i, j, uf.is_in_the_same_set(i, j) == True)
  i, j = 1, 7
  print 'Test %d and %d: %s' % (i, j, uf.is_in_the_same_set(i, j) == True)

