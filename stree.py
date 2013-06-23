#! usr/bin/python

class TTTree (object):
  """
  Class for 2-3 tree
  """
  class Node (object):
    """
    Class for nodes in 2-3 tree
    
      Methods:
        
        get_data([index])
        set_data(data)
        get_child([index])
        set_child(child)
        is_full()
    """
    def __init__ (self, max_child_number, data=None, child=None):
      self.__print('Node__init__(start)')
      self.max_number = max_child_number
        
      self.__print('Node__init__(1)')
      if data != None:
        self.set_data(data)
      else:
        self.data = None
      
      self.__print('Node__init__(2)')
      if child != None:
        self.set_child(child)
      else:
        self.child = None
      self.__print('Node__init__(end)')
        
    def set_data (self, data):
      if type(data) != type([]):
        self.data = [data]
      else:
        assert(len(data) < self.max_number)
        self.data = data
    
    def get_data (self, index=None):
      if index == None:
        return self.data
      
      else:
        try:
          return self.data[index]
        except (IndexError, TypeError):
          return None
  
    def set_child (self, child):
      self.__print('\nNode.set_child(start) child %s' % str(child))
      if type(child) != type([]):
        self.child = [child]
      else:
        assert(len(child) <= self.max_number)
        self.child = child
        if filter(lambda x: x!=None, self.child) == []:
          self.child = None
  
    def get_child (self, index=None):
      if index == None:
        return self.child
      else:
        try:
          return self.child[index]
        except (IndexError, TypeError):
          return None
  
    def is_full (self):
      return len(self.data) == (self.max_number - 1)
  
    def __print (self, information):
      pass
  
  def __init__ (self, key_function=(lambda x:x)):
    self.root = None
    self.keyfunc = key_function
    
  def is_empty (self):
    return self.root == None
  
  def find (self, data, parent=None):
    if self.is_empty() == True:
      return False, None
    
    # Search from root if parent not specified
    if parent == None:
      parent = self.root
    
    parent_data = parent.get_data()
    data_number = len(parent_data)
    childrend = parent.get_child()
    for i in range(0, data_number):
      if self.keyfunc(data) < self.keyfunc(parent_data[i]):
        try:
          return self.find(data, childrend[i])
        except (IndexError, TypeError):
          return False, parent
      elif self.keyfunc(data) == self.keyfunc(parent_data[i]):
        return True, parent
    try:
      return self.find(data, childrend[data_number])
    except (IndexError, TypeError):
      return False, parent

  def insert (self, data, parent=None):
    self.__print('\ninsert(start) data %s' % (str(data)))

    result = [False, None, None, None]
    # In case tree is empty, just put the node as root
    if self.is_empty() == True:
      self.root = self.Node(3, data=data)
      result[0] = True
      self.__print('\nroot %s' % (self.root.get_data()))
    else:
      # Insert from root if parent not specified
      if parent == None:
        parent = self.root
      
      parent_data = parent.get_data()
      data_number = len(parent_data)
      childrend = parent.get_child()
      
      self.__print('parent %s' % (str(parent_data)))

      # In case key is already existed, return False
      if (parent_data != None) and (self.keyfunc(data) in map(lambda x: self.keyfunc(x), parent_data)):
        self.__print_error('Key %s of data %s is already existed' % (str(self.keyfunc(data)), str(data)))
        result[0] = False

#       # Try to put data here (in parent node)
#       elif self.__put_data(data, parent) == True:
#         result[0] = True
      
      # In case data full here, check where to insert
      else:
        self.__print('\ninsert(2) data %s parent %s' % (str(data), str(parent_data)))  
        if self.keyfunc(data) < self.keyfunc(parent_data[-1]):
          for i in range(0, data_number):
            self.__print('\ninsert(3) i %d' % (i))  
            if self.keyfunc(data) < self.keyfunc(parent_data[i]):
              try:
                result = self.insert(data, childrend[i])
              except (IndexError, TypeError):
                result[0:2] = [True, data]
              break
        else:
          try:
            result = self.insert(data, childrend[data_number])
          except (IndexError, TypeError):
            result[0:2] = [True, data]
                    
        self.__print('\ninsert(5) result %s' % (str(result)))  

      # Still a data cannot be inserted in subtree. 
      if (result[0] == True) and (result[1] != None):
        # Try to put data here
        if self.__put_data(result[1], parent, result[2:]) == True:
          result = [True, None, None, None]
        
        # It is full here. Split.
        else:
          result[1:] = self.__split(result[1], parent, result[2:])
      
        self.__print('\ninsert(7) result %s' % (str(result)))  

        if (parent == self.root) and (result[1] != None):
            self.root = self.Node(3, data=result[1], child=result[2:])
            result = [True, None, None, None]
          
    
    if parent == self.root:
      result = result[0]
          
    self.__print('\ninsert(end) result %s' % (str(result)))  
    return result

  def delete (self, key, parent=None):
    result = [False, None, False]
    # Return False in case tree is empty
    if self.is_empty() == True:
      return False, None
    
    if parent == None:
      parent = self.root
    
    parent_data = parent.get_data()
    parent_childrend = parent.get_child()
    
    # If key is included in this node
    if key in map(lambda x: self.keyfunc(x), parent_data):
      # If this is a leaf node 
      if parent_childrend == None:
        # If this node has more than one data, just remove it from the node
        for i in range(0, len(parent_data)):
          if key == self.keyfunc(parent_data[i]):
            result[0:2] = [True, parent_data.pop(i)]
            break
        
        parent.set_data(parent_data)
      
      # If this is not a leaf node, swap it to a leaf node
      else:
        if key == self.keyfunc(parent_data[0]):
          self.__swap_left(parent)
          result = self.delete(key, parent_childrend[0])
        else:
          self.__swap_right(parent)
          result = self.delete(key, parent_childrend[1]) 

    # If key is not included in this node
    else:
      # It is a leaf node implies searching is failed
      if parent_childrend == None:
        return False, None
      
      # Look forward to child
      else:
        if key < self.keyfunc(parent_data[-1]):
          for i in range(0, len(parent_data)):
            if key < self.keyfunc(parent_data[i]):
              result = self.delete(key, parent_childrend[i])
              break
        else:
          result = self.delete(key, parent_childrend[-1])

    # If data is found
    if result[0] == True:
      assert(result[1] != None)
      # If one child becomes empty, perform some restructure 
      if result[2] == True:
        # Key is found in subtree 0
        if self.keyfunc(result[1]) < self.keyfunc(parent_data[0]):
          parent_child_data = parent_childrend[1].get_data()
          # If child 1 is full, perform rotation
          if parent_childrend[1].is_full() == True:
            parent_childrend[0].set_data(parent_data[0])
            parent_data[0] = parent_child_data.pop(0)
            parent.set_data(parent_data)
            parent_childrend[1].set_data(parent_child_data)
          
          # Otherwise, if this node is full, merge self data 0 and child 1 as child 0 of this node 
          elif parent.is_full() == True:
            parent_childrend[0].set_data([parent_data.pop(0), parent_child_data.pop(0)])
            parent.set_data(parent_data)
            parent_childrend.pop(1)
            parent.set_child(parent_childrend)
            
          # Otherwise, merge self data 0 and child 1 into this node
          else:
            parent_data.extend(parent_child_data)
            parent.set_data(parent_data)
            parent.set_child(None)
            
        # Key is found in subtree 1
        elif self.keyfunc(result[1]) < self.keyfunc(parent_data[1]):
          parent_child_data = parent_childrend[0].get_data()
          # If child 0 is full, perform rotation
          if parent_childrend[0].is_full() == True:
            parent_childrend[1].set_data(parent_data[0])
            parent_data[0] = parent_child_data.pop()
            parent.set_data(parent_data)
            parent_childrend[0].set_data(parent_child_data)
          
          # Otherwise, if this node is full, merge self data 0 and child 0 as child 0 of this node 
          elif parent.is_full() == True:
            parent_childrend[1].set_data([parent_child_data.pop(), parent_data.pop(0)])
            parent.set_data(parent_data)
            parent.set_child(parent_childrend[1:])
            
          # Otherwise, merge self data 0 and child 0 into this node
          else:
            parent_data = parent_child_data + parent_data
            parent.set_data(parent_data)
            parent.set_child(None)

      # If this node becomes empty, set result[2] as True
      elif len(parent_data) == 0:
        result[2] = True
      

  def traverse_inorder (self, parent=None, delimiter=''):
    if self.is_empty():
      return ''
    
    if parent == None:
      parent = self.root
    
    return self.__inorder(parent, delimiter)
  
  def __inorder(self, parent, delimiter):
    if parent == None:
      return ''
    
    parent_data = '+'.join(map(lambda x:str(x), parent.get_data()))
    childrend = parent.get_child()
    if childrend == None:
      return parent_data
    elif len(childrend) == 1:
      return delimiter.join([self.__inorder(childrend[0], delimiter), parent_data])
    else:
      return delimiter.join([self.__inorder(childrend[0], delimiter), parent_data] + 
                            map(lambda x: self.__inorder(x, delimiter), childrend[1:]))
    
  def traverse_preorder (self, parent=None, delimiter=''):
    if self.is_empty():
      return ''
    
    if parent == None:
      parent = self.root
    
    return self.__preorder(parent, delimiter)
  
  def __preorder(self, parent, delimiter):
    if parent == None:
      return ''
    
    parent_data = '+'.join(map(lambda x:str(x), parent.get_data()))
    childrend = parent.get_child()
    if childrend == None:
      return parent_data
    else:
      return delimiter.join([parent_data] + 
                            map(lambda x: self.__preorder(x, delimiter), childrend))
    
  def traverse_postorder (self, parent=None, delimiter=''):
    if self.is_empty():
      return ''
    
    if parent == None:
      parent = self.root
    
    return self.__postorder(parent, delimiter)
  
  def __postorder(self, parent, delimiter):
    if parent == None:
      return ''
    
    parent_data = '+'.join(map(lambda x:str(x), parent.get_data()))
    childrend = parent.get_child()
    if childrend == None:
      return parent_data
    else:
      return delimiter.join(map(lambda x: self.__postorder(x, delimiter), childrend) + 
                            [parent_data])
    
  def __put_data (self, data, parent, childrend):
    self.__print('\nput_data(start) data %s parent %s childrend %s' % (str(data), str(parent.get_data()), str(childrend)))
    if parent.is_full() == True:
      return False
    
    else:
      parent_data = parent.get_data()
      parent_childrend = parent.get_child()
      
      self.__print('\nput_data(3) data %s parent_childrend %s' % (str(data), str(parent_childrend)))
      
      if parent_childrend == None:
        parent_childrend = [None, None]
      
      if parent_data == None:
        parent.set_data(data)
        return True
      
      if self.keyfunc(data) < self.keyfunc(parent_data[0]):
        parent.set_data([data] + parent_data)
        parent.set_child(childrend + [parent_childrend[1]])
      else:
        parent.set_data(parent_data + [data])
        parent.set_child([parent_childrend[0]] + childrend)

      self.__print('\nput_data(end) data %s parent %s childrend %s' % (str(data), str(parent.get_data()), str(parent.get_child())))

      return True

  def __split (self, data, parent, childrend):
    self.__print('\nsplit(start) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
    parent_data = parent.get_data()
    parent_child = parent.get_child()
    if parent_child == None:
      parent_child = [None] * 3
      
    if self.keyfunc(data) < self.keyfunc(parent_data[0]):
      self.__print('\nsplit(1) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
      new_node = self.Node(3, parent_data[1], child=parent_child[1:])
      parent.set_data(data)
      parent.set_child(childrend)
      data = parent_data[0]
      self.__print('\nsplit(3) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
    elif self.keyfunc(data) < self.keyfunc(parent_data[1]):
      self.__print('\nsplit(4) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
      new_node = self.Node(3, parent_data[1], child=[childrend[1], parent.get_child(2)])
      parent.set_data(parent_data[0])
      parent.set_child([parent.get_child(0), childrend[0]])
      self.__print('\nsplit(6) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
    else:
      self.__print('\nsplit(7) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))
      new_node = self.Node(3, data, child=childrend)
      parent.set_data(parent_data[0])
      parent.set_child(parent_child[0:2])
      data = parent_data[1]
      self.__print('\nsplit(9) parent %s data %s childrend %s' % (str(parent.get_data()), str(data), str(childrend)))

    self.__print('\nsplit(end) data %s parent %s %s new %s %s' % (str(data), str(parent.get_data()), str(parent.get_child()), str(new_node.get_data()), str(new_node.get_child())))

    return data, parent, new_node

  def __print (self, information):
    #print '%s' % str(information),
    pass

  def __print_error (self, information):
    print '\n[Error %s] %s' % (type(self).__name__, str(information))


if __name__ == '__main__':
  
  print 'Test of 2-3 tree'
  ttt = TTTree()
  ttt.insert(10)
  ttt.insert(40)
  ttt.insert(80)
  ttt.insert(20)
  ttt.insert(70)
  ttt.insert(30)
  ttt.insert(60)
  ttt.insert(50)
  ttt.insert(90)
  ttt.insert(0)

  print ttt.traverse_inorder(delimiter='') == '0+1020304050+607080+90',
  print ttt.traverse_preorder(delimiter='') == '40200+10307050+6080+90',
  print ttt.traverse_postorder(delimiter='') == '0+10302050+6080+907040'
 
















