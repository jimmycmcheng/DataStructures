#! usr/bin/python

class BinaryTree (object):
  """
  Class of basic binary tree
  
    Method:
    
      is_empty()
      insert_left()
      insert_right()
      traverse_inorder()
      traverse_preorder()
      traverse_postorder()
    
  """
  class Node (object):
    """
    Class of a basic node in binary trees 
    """
    def __init__ (self, left_child=None, 
                        right_child=None, 
                        data=None):
      self.left_child = None
      self.right_child = None
      self.data = None
      self.set_data(data)
      self.set_left_child(left_child)
      self.set_right_child(right_child)
    
    def is_data_empty (self):
      return self.data == None
    
    def set_data (self, data):
      self.data = data
  
    def get_data (self, default=None):
      if self.is_data_empty() == True:
        return default
      else:
        return self.data
    
    def has_left_child (self):
      return self.left_child != None
    
    def set_left_child (self, node):
      self.left_child = node
    
    def get_left_child (self):
      return self.left_child
    
    def has_right_child (self):
      return self.right_child != None
    
    def set_right_child (self, node):
      self.right_child = node
    
    def get_right_child (self):
      return self.right_child
  
  def __init__ (self, node=None):
    self.root = node

  def insert_left (self, data, parent=None, right=False):
    """
    Insert left child of the specified node
      Parameter:
        right -- specify how to treat the old left child of parent (if exists)
                 True for putting the old left child as a right child of the new child
                 False for putting the old left child as a left child of the new child
    """
    assert((self.root != None) or (parent == None))
    
    child = self.Node(data=data)

    # If tree is empty, fill data into root node
    if self.root == None:
      self.root = child
    
    else:
      # parent not specified means add a node as a child of root
      if parent == None:
        parent = self.root
    
      if right == False:
        child.set_left_child(parent.get_left_child())
      else:
        child.set_right_child(parent.get_left_child())
      parent.set_left_child(child)

    return child

  def insert_right (self, data, parent, left=False):
    """
    Insert right child of the specified node. It CANNOT be used to 
    add the first node of tree

      Parameter:
        left -- specify how to treat the old right child of parent (if exists)
                True for putting the old right child as a left child of the new child
                False for putting the old right child as a right child of the new child
    """
    assert(self.root != None)
    
    child = self.Node(data=data)

    # parent not specified means add a node as a child of root
    if parent == None:
      parent = self.root
  
    if left == False:
      child.set_right_child(parent.get_right_child())
    else:
      child.set_left_child(parent.get_right_child())
    parent.set_right_child(child)

    return child

  def is_empty (self):
    """
    Return True if tree is empty
    """
    return self.root == None

  def traverse_inorder (self, delimiter=''):
    """
    Perform the inorder traversal. Return the string which is the concatenation of node data
    with separator 'delimiter' 
    """
    return self.__traverse_inorder_recursive(self.root, delimiter)

  def traverse_preorder (self, delimiter=''):
    """
    Perform the preorder traversal. Return the string which is the concatenation of node data
    with separator 'delimiter'   
    """
    return self.__traverse_preorder_recursive(self.root, delimiter)

  def traverse_postorder (self, delimiter=''):
    """
    Perform the postorder traversal. Return the string which is the concatenation of node data
    with separator 'delimiter'   
    """
    return self.__traverse_postorder_recursive(self.root, delimiter)

  def __traverse_inorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([self.__traverse_inorder_recursive(node.get_left_child(), delimiter),
                      str(node.get_data()),
                      self.__traverse_inorder_recursive(node.get_right_child(), delimiter)])

  def __traverse_preorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([str(node.get_data()),
                      self.__traverse_preorder_recursive(node.get_left_child(), delimiter),
                      self.__traverse_preorder_recursive(node.get_right_child(), delimiter)])

  def __traverse_postorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([self.__traverse_postorder_recursive(node.get_left_child(), delimiter),
                      self.__traverse_postorder_recursive(node.get_right_child(), delimiter),
                      str(node.get_data())])

class BinarySearchTree (BinaryTree):
  """
  Class of binary search tree.
  
    Methods:
    
      search()
      insert()  
  """
  
  
  def __init__ (self, key_function=(lambda x:x)):
    super(BinarySearchTree, self).__init__()
    self.key_function = key_function
  
  def search (self, key, node=None):
    """
    Search for 'key'.
    Return a three-element tuple. The first element is a boolean showing 
    whether 'key' is found or not, the second is the data of the last-searched node,
    and the third is the last-searched node
    """
    # Search from root if node is not specified
    if node == None:
      node = self.root
      
    data = node.get_data()
    
    if key == self.key_function(data):
      return True, data, node
    elif key > self.key_function(data):
      if node.get_right_child() == None:
        return False, data, node
      else:
        return self.search(key, node.get_right_child())
    else:
      if node.get_left_child() == None:
        return False, data, node
      else:
        return self.search(key, node.get_left_child())

  def insert (self, data):
    """
    Insert data into tree.
    Return a two-element tuple. The first element is a boolean showing whether 
    the insertion is success or not (data key is already existed result in False),
    and the second is the inserted node
    """
    is_found, node = self.search(data)[::2]
    if is_found == True:
      return False, None
    else:
      if node.is_data_empty() == True:#get_data() == None:
        node.set_data(data)
        return True, node
      elif self.key_function(data) > self.key_function(node.get_data()):
        if node.get_right_child() == None:
          return True, node.insert_right(data)
        else:
          print node
          return False, None
      else:
        if node.get_left_child() == None:
          return True, node.insert_left(data)
        else:
          print node
          return False, None

class AvlTree (BinarySearchTree):
  """
  Class of AVL tree. AVL tree is a balanced binary search tree such that it provides
  better worst case of searching.
  
    Usage:
      avl_tree = AvlTree([key_function])
      avl_tree.insert(data)
      data = avl_tree.search(key)
  """
  
  class Node (BinaryTree.Node):
    """
    Class of nodes in AVL tree. 
    In addition to BinaryTree.Node, it adds the field bf (balance factor) 
    and the method swap_data() 
    """
    def __init__ (self, left_child=None, 
                        right_child=None, 
                        data=None,
                        bf=0):
      super(AvlTree.Node, self).__init__(left_child, right_child, data)
      self.bf = bf
    
    def swap_data (self, other_node):
      """
      Swap data and bf with other_node's
      """
      # Swap data
      data = self.get_data()
      self.set_data(other_node.get_data())
      other_node.set_data(data)
      # Swap bf
      self.bf, other_node.bf = other_node.bf, self.bf

  def __init__ (self, key_function=(lambda x:x)):
    super(AvlTree, self).__init__(key_function)
    #self.key_function = key_function

  def insert (self, data, parent=None):
    """
    Insert a data into AVL tree.
    In addition to inserting a node into tree, it takes some overhead to restructure for 
    maintaining balance
    Return True if the height of tree is grown
    """

    self.__print('\ninsert(%s)' % (str(data)))
    
    
    # parent not specified means adding data from root
    if parent == None:
      parent = self.root

    # Tree is now empty, put data in root
    if self.is_empty() == True:
      self.insert_left(data)
      self.root.bf = 0
      grow = True

    # key of data is less than parent, make data as the left child of parent 
    # in case parent has no left child, or go on to check the left child
    elif self.key_function(data) < self.key_function(parent.get_data()):
      self.__print('parent %s bf %d' % (parent.get_data(), parent.bf))
      #if child == None:
      if parent.has_left_child() == False:
        child = self.insert_left(data, parent)
        child.bf = 0

        # Since parent has no left child, parent.bf must not be +1        
        assert(parent.bf != 1)
        
        # The height of left subtree is grown (0->1). Increase parent.bf by one 
        # and then check if the height of subtree is grown
        parent.bf += 1
        if parent.bf == 1:
          grow = True
        else:
          grow = False
      
      # Parent already has left child
      else:
        child = parent.get_left_child()
        # Insert data to left subtree
        grow = self.insert(data, child)
        
        # In case the height of left subtree is grown, update parent.bf
        if grow == True:
          if parent.bf == -1:
            parent.bf = 0
            grow = False
          elif parent.bf == 0:
            parent.bf = 1
            grow = True
          else:
            grow = self.__left_rotate(parent)
            parent.bf = 0

      self.__print('\n--> parent %s bf %d' % (parent.get_data(), parent.bf))
      
    # key of data is larger than parent, make data as the right child of parent 
    # in case parent has none, or go on to check the right subtree
    elif self.key_function(data) > self.key_function(parent.get_data()):
      self.__print('parent %s bf %d' % (parent.get_data(), parent.bf))
      #if child == None:
      if parent.has_right_child() == False:
        child = self.insert_right(data, parent)
        child.bf = 0

        # Since parent has no right child, parent.bf must not be -1        
        assert(parent.bf != -1)
        
        # The height of right subtree is grown (0->1). Decrease parent.bf by one 
        # and then check if the height of subtree is grown
        parent.bf -= 1
        if parent.bf == -1:
          grow = True
        else:
          grow = False
      
      # Parent already has right child
      else:
        child = parent.get_right_child()
        # Insert data to right subtree
        grow = self.insert(data, child)
        
        # In case the height of right subtree is grown, update parent.bf
        if grow == True:
          if parent.bf == 1:
            parent.bf = 0
            grow = False
          elif parent.bf == 0:
            parent.bf = -1
            grow = True
          else:
            grow = self.__right_rotate(parent)
            parent.bf = 0

      self.__print('\n--> parent %s bf %d' % (parent.get_data(), parent.bf))
    
    # Key value is the same with parents
    else:
      self.__print_error('Key %s of data %s is already exist' % (str(self.key_function(data)), str(data)))
      grow = False
      
    return grow 
  
  def __left_rotate (self, parent):
    """
    Left rotate
    """
    assert(parent.has_left_child() == True)
    
    left_child = parent.get_left_child()

    assert(left_child.bf != 0)
    
    # Perform LL rotate
    if left_child.bf == 1:
      grow = self.__ll_rotate(parent)
    # Perform LR rotate
    elif left_child.bf == -1:
      grow = self.__lr_rotate(parent)
    else:
      pass
    return grow
  
  def __right_rotate (self, parent):
    """
    Left rotate
    """
    assert(parent.has_right_child() == True)
    right_child = parent.get_right_child()
    assert(right_child.bf != 0)
    # Perform RR rotate
    if right_child.bf == 1:
      grow = self.__rl_rotate(parent)
    # Perform RL rotate
    elif right_child.bf == -1:
      grow = self.__rr_rotate(parent)
    else:
      pass
    return grow
  
  def __ll_rotate (self, parent):
    """
    LL rotate
    """
    self.__print('\n__llr %s' % (parent.get_data()))
    #             A(+2)                                     B(0)
    #          /         \                             /           \ 
    #         /           \             LL            /             \
    #      B(+1)          +--+ -       rotate      +--+ -           A(0)  
    #    /      \         |Ar| |      ------->     |Bl| |         /      \ 
    #   /        \        |  | h                   |  | h        /        \
    # +--+ -    +--+ -    |  | |                   |  | |      +--+ -    +--+ -
    # |Bl| |    |Br| |    +--+ -                   +--+ -      |Br| |    |Ar| |
    # |  | h    |  | h                             |  | 1      |  | h    |  | h
    # |  | |    |  | |                             +--+ -      |  | |    |  | |
    # +--+ -    +--+ -                                         +--+ -    +--+ -
    # |  | 1                                      
    # +--+ -
    child = parent.get_left_child()
    parent.set_left_child(child.get_left_child())
    child.set_left_child(child.get_right_child())
    child.set_right_child(parent.get_right_child())
    parent.set_right_child(child)
    parent.swap_data(child)
    child.bf = 0
    parent.bf = 0
    
    # Height before insertion is h+1 and after is still h+1
    return False
  
  def __rr_rotate (self, parent):
    """
    RR rotate
    """
    self.__print('\n__rrr %s' % (parent.get_data()))

    # Symmetric to LL rotate 
    child = parent.get_right_child()
    parent.set_right_child(child.get_right_child())
    child.set_right_child(child.get_left_child())
    child.set_left_child(parent.get_left_child())
    parent.set_left_child(child)
    parent.swap_data(child)
    child.bf = 0
    parent.bf = 0
    
    # Height before insertion is h+1 and after is still h+1
    return False
  
  def __lr_rotate (self, parent):
    """
    LR rotate
    """
    self.__print('\n__lrr %s' % (parent.get_data()))
    #                    A(+2)                                              C(0)                   
    #               /             \                                    /            \              
    #              /               \                                  /              \             
    #         B(-1)                +--+ -                         B(0)                A(-1)        
    #     /           \            |Ar| |                       /      \            /      \       
    #    /             \           |  | h+1       LR           /        \          /        \      
    # +--+ -           C(+1)       |  | |        rotate      +--+ -    +--+ -    +--+ -    +--+ -  
    # |Bl| |         /      \      +--+ -       ------->     |Bl| |    |Cl| |    |Cr| |    |Ar| |  
    # |  | h+1      /        \                               |  | h+1  |  | h    |  | h    |  | h+1
    # |  | |      +--+ -    +--+ -                           |  | |    |  | |    |  | |    |  | |  
    # +--+ -      |Cl| |    |Cr| |                           +--+ -    +--+ -    +--+ -    +--+ -  
    #             |  | h    |  | h                                     |  | 1                      
    #             |  | |    |  | |                                     +--+ -                      
    #             +--+ -    +--+ -                           
    #             |  | 1                                     
    #             +--+ -                                     
    child = parent.get_left_child()
    grandchild = child.get_right_child()
    assert(grandchild.bf != 0)
    child.set_right_child(grandchild.get_left_child())
    grandchild.set_left_child(grandchild.get_right_child())
    grandchild.set_right_child(parent.get_right_child())
    parent.set_right_child(grandchild)
    parent.swap_data(grandchild)
    
    if parent.bf == 1:
      child.bf = 0
      grandchild.bf = -1
    else:
      child.bf = 1
      grandchild.bf = 0
    parent.bf = 0
    
    # Height before insertion is h+3 and after is still h+3
    return False
    
  def __rl_rotate (self, parent):
    """
    RL rotate
    """
    self.__print('\n__rlr %s' % (parent.get_data()))

    # Symmetric to LR rotate                                      
    child = parent.get_right_child()
    grandchild = child.get_left_child()
    assert(grandchild.bf != 0)
    child.set_left_child(grandchild.get_right_child())
    grandchild.set_right_child(grandchild.get_left_child())
    grandchild.set_left_child(parent.get_left_child())
    parent.set_left_child(grandchild)
    parent.swap_data(grandchild)
    
    if parent.bf == 1:
      child.bf = -1
      grandchild.bf = 0
    else:
      child.bf = 0
      grandchild.bf = 1
    parent.bf = 0
    
    # Height before insertion is h+3 and after is still h+3
    return False
    
  
  def __print (self, information):
    #print information,
    pass
  
  def __print_error (self, information):
    print '\n[Error %s] %s' % (type(self).__name__, str(information))


class Leftist (BinaryTree):
    
  class __Node (BinaryTree.Node):
    def __init__ (self, left_child=None, 
                        right_child=None, 
                        parent=None, 
                        data=None, 
                        key_function=(lambda x:x)):
      self.__kf = key_function
      self.__parent = None
      self.shortest = None
      self.key = None
      super(Leftist._Leftist__Node, self).__init__(data=data, left_child=left_child, right_child=right_child)
    
    def set_data (self, data):
      super(Leftist._Leftist__Node, self).set_data(data)
      self.key = None
      if data != None:
        self.key = self.__kf(data)
      self.shortest = self.__derive_shortest()

    def set_left_child (self, node):
      super(Leftist._Leftist__Node, self).set_left_child(node)
      self.shortest = self.__derive_shortest()
      if node != None:
        node.set_parent(self)
    
    def set_right_child (self, node):
      super(Leftist._Leftist__Node, self).set_right_child(node)
      self.shortest = self.__derive_shortest()
      if node != None:
        node.set_parent(self)
    
    def set_parent (self, node):
      self.__parent = node
      
    def get_parent (self):
      return self.__parent
    
    def __derive_shortest (self):
      """
      Derive shortest value
      """
      if self.data == None:
        return 0
      
      if (self.right_child == None) or (self.left_child == None):
        return 1
      
      return 1 + min([self.left_child.shortest, self.right_child.shortest])

  def __init__ (self, node=None):
    assert((node == None) or (type(node) == type(self.__Node())))    
    super(Leftist, self).__init__(node)
    
  def insert (self, data, key_function=(lambda x:x)):
    node = self.__Node(data=data, key_function=key_function)
    if self.is_empty() == True:
      self.root = node
    else:
      temp_leftist = Leftist(node)
      self.combine(temp_leftist)
  
  def delete (self):
    if self.is_empty() == True:
      return None
  
    result = self.root.get_data()
    temp_leftist = Leftist(self.root.get_left_child())
    temp_leftist.combine(Leftist(self.root.get_right_child()))
    self = temp_leftist
    return result
    
  def combine (self, other_leftist):
    assert(type(other_leftist) == type(Leftist()))
    self.__print('\ncombine()')
    
    if other_leftist.is_empty() == True:
      return
    
    if self.is_empty() == True:
      self.root = other_leftist.root
      return
    
    self.__print('\nCombining %d shortest %d, %d shortest %d' % (self.root.key, self.root.shortest, other_leftist.root.key, other_leftist.root.shortest))
    
    if self.root.key <= other_leftist.root.key:
      right_child = self.root.get_right_child()
      if right_child == None:
        self.root.set_right_child(other_leftist.root)
        self.__print('\n')
        if self.root.get_left_child() != None:
          self.__print('\nleft shortest %d' % (self.root.get_left_child().shortest))
        if self.root.get_right_child() != None: 
          self.__print('right shortest %d' % (self.root.get_right_child().shortest)) 
        self.__print('shortest %d' % (self.root.shortest))
      else:
        temp_leftist = Leftist(right_child) 
        temp_leftist.combine(other_leftist)
        self.root.set_right_child(temp_leftist.root)
    else:
      right_child = other_leftist.root.get_right_child()
      if right_child == None:
        other_leftist.root.set_right_child(self.root)
      else:
        temp_leftist = Leftist(right_child)
        temp_leftist.combine(self)
        other_leftist.root.set_right_child(temp_leftist.root)
      self.root = other_leftist.root

    self.__print('\nAfter combine %d shortest %d' % (self.root.key, self.root.shortest))
    
    left_child = self.root.get_left_child()
    right_child = self.root.get_right_child()
    if right_child == None:
      pass
    elif (left_child == None) or (left_child.shortest < right_child.shortest):
      self.root.set_left_child(right_child)
      self.root.set_right_child(left_child)

  def __print (self, information):
    #print information,
    pass

class BinaryTreeList (object):
  """

  """
  def __init__ (self, tree=[]):
    #super(Heap, self).__init__([''] + tree)
    #super(BinaryTreeList, self).__init__([None])
    #self = ['']
    #print self
    self.data = [None]
    self.data.extend(tree)

  def is_empty (self):
    return len(self.data) <= 1

  def traverse_inorder (self, node=1, delimiter=''):
    if node >= len(self.data):
      return delimiter
    else:
      return delimiter.join([self.traverse_inorder(node=node*2, delimiter=delimiter),
                      str(self.data[node]),
                      self.traverse_inorder(node=node*2+1, delimiter=delimiter)])

  def traverse_preorder (self, node=1, delimiter=''):
    if node >= len(self.data):
      return delimiter
    else:
      return delimiter.join([str(self.data[node]),
                      self.traverse_preorder(node=node*2, delimiter=delimiter),
                      self.traverse_preorder(node=node*2+1, delimiter=delimiter)])

  def traverse_postorder (self, node=1, delimiter=''):
    if node >= len(self.data):
      return delimiter
    else:
      return delimiter.join([self.traverse_postorder(node=node*2, delimiter=delimiter),
                      self.traverse_postorder(node=node*2+1, delimiter=delimiter),
                      str(self.data[node])])


class Heap (BinaryTreeList):
  """
  Heap Class

    Usage:

      heap = MaxHeap(rule)                    # Construct a Heap defined by the specified rule
                                              #   The rule function is prototyped as
                                              #     boolean rule (child, parent)
      
      heap.insert(value[, object])            # Insert a node with value
       
      value, object = heap.delete()           # Return the (value, object) pair of maximum value.
                                              #   object is None if not available
                                              #   (None, None) is returned if the heap is empty           
  """
  def __init__ (self, rule):
    super(Heap, self).__init__()
    self.__rule = rule
    #self.data = self

  def size (self):
    return len(self.data) - 1

  def insert (self, value, object_=None):
    self.data.append((value, object_))
    return self.tidy_up(len(self.data)-1)

  def delete (self, value=None, object_=None):
    result = (None, None)
    if (value == None) and (self.is_empty() == True):
      return result

    if value != None:
      self.data.appen((value, object_))

    node = 1
    result = self.data[1]
    #print 'delete(): %d' % value
    last = self.data.pop()
    if self.is_empty() == False:
      self.data[1] = last
      #print self
      node = self.tidy_up(1)

    #print 'delete(): %d' % value
    if value != None:
      result += (node,)

    return result

  def tidy_up (self, node):
    #print 'tidy_up(): node=%d' % node
    temp_node = node

    # Upward
    if temp_node != 1:
      #while temp_node > 1 and self.data[temp_node] > self.data[temp_node/2]:
      while temp_node > 1 and self.__rule(self.data[temp_node/2][0], self.data[temp_node][0]):
        self.data[temp_node], self.data[temp_node/2] = self.data[temp_node/2], self.data[temp_node]
        temp_node = temp_node / 2

    # Downward
    else:
      while True:
        if len(self.data) <= temp_node*2:
          # Have no child
          break
        elif len(self.data) <= (temp_node*2+1):
          # Have left child only
          if self.__rule(self.data[temp_node][0], self.data[temp_node*2][0]):
            self.data[temp_node], self.data[temp_node*2] = self.data[temp_node*2], self.data[temp_node]
            temp_node = temp_node * 2
          break  
        #print 'tidy_up(): temp_node=%d' % temp_node

        if self.__rule(self.data[temp_node][0], self.data[temp_node*2][0]) == True:
          if self.__rule(self.data[temp_node*2+1][0], self.data[temp_node*2][0]) == True:
            self.data[temp_node], self.data[temp_node*2] = self.data[temp_node*2], self.data[temp_node]
            temp_node = temp_node * 2
          else:
            self.data[temp_node], self.data[temp_node*2+1] = self.data[temp_node*2+1], self.data[temp_node]
            temp_node = temp_node * 2 + 1
        elif self.__rule(self.data[temp_node][0], self.data[temp_node*2+1][0]): 
          self.data[temp_node], self.data[temp_node*2+1] = self.data[temp_node*2+1], self.data[temp_node]
          temp_node = temp_node * 2 + 1
        else:
          break

    return temp_node

class MaxHeap (Heap):
  """
  MaxHeap Class

    Usage:

      max_heap = MaxHeap()                        # Construct a MaxHeap
      
      max_heap.insert(value[, object])            # Insert a node with value
       
      value, object = max_heap.delete()           # Return the (value, object) pair of maximum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
  """
  def __init__ (self, key=(lambda x:x)):
    super(MaxHeap, self).__init__(rule=lambda c,p:key(p)>=key(c))

class MinHeap (Heap):
  """
  MinHeap Class

    Usage:

      min_heap = MinHeap()                        # Construct a MinHeap
      
      min_heap.insert(value[, object])            # Insert a node with value
       
      value, object = min_heap.delete()           # Return the (value, object) pair of maximum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
  """
  def __init__ (self, key=(lambda x:x)):
    super(MinHeap, self).__init__(rule=(lambda c,p:key(p)<key(c)))

class Deap (object):
  """
  Deap Class

    Usage:

      d = Deap()                                  # Construct a Deap
      
      d.insert(data)                              # Insert a node with value
       
      key, data = d.delete_min()                  # Return the (value, object) pair of minimum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
       
      key, data = d.delete_max()                  # Return the (value, object) pair of maximum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
  """
  def __init__ (self, key=(lambda d:d)):
    #super(Deap, self).__init__(rule=None)
    #self.data = self
    self.__min_heap = MinHeap()
    self.__max_heap = MaxHeap()
    self.__kf = key

  def insert (self, data):
    self.__print('\ninsert(%d)' % self.__kf(data))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))

    # Decide which heap to add
    length_min = len(self.__min_heap.data)
    length_max = len(self.__max_heap.data)
    assert(length_min >= length_max)
    if length_min == length_max:
      # Will add to min heap
      heap = self.__min_heap
      other_heap = self.__max_heap
      correspond = length_min / 2
      rule = lambda h,c: self.__kf(h) <= self.__kf(c) 
    else:
      # Will add to max heap
      heap = self.__max_heap
      other_heap = self.__min_heap
      correspond = length_max
      rule = lambda h,c: self.__kf(h) > self.__kf(c) 
    
    self.__print('\n[2] correspond %d' % correspond)

    # Compare to correspondence and swap if necessary
    if (correspond > 0) and (rule(data, other_heap.data[correspond][1]) == False):
      data, other_heap.data[correspond] = other_heap.data[correspond][1], (self.__kf(data), data)
      other_heap.tidy_up(correspond)
    
    self.__print('\n[4] data %d' % self.__kf(data))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    
    # Tidy up!
    heap.insert(self.__kf(data), data)

    self.__print('\n[E] data %d' % self.__kf(data))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    

  def delete_min (self):
    self.__print('\ndelete_min()')
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    
    result = None

    # Deap is empty
    if self.__min_heap.is_empty() == True:
      return result
    
    # There is only one node in deap
    if self.__max_heap.is_empty() == True:
      result = self.__min_heap.data.pop()[1]
      return result
      
    # Take the root of min heap
    result = self.__min_heap.data[1][1]
    
    # Pop the last node of (min + max heap) and put it in the root of min heap
    length_min = len(self.__min_heap.data)
    length_max = len(self.__max_heap.data)
    assert(length_min >= length_max)
    if length_min == length_max:
      # Pop node from max heap
      node = self.__max_heap.data.pop()[1]
      length_max -= 1
    else:
      # Pop node from min heap
      node = self.__min_heap.data.pop()[1]
      length_min -= 1

#     # Deap is empty now     
#     if self.__min_heap.is_empty() == True:
#       return result

    self.__print('\n[2] node %d' % self.__kf(node))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))

    self.__min_heap.data[1] = (self.__kf(node), node)
    
    # Tidy up min heap from root
    new_node = self.__min_heap.tidy_up(1)
    
    self.__print('\n[2] new_node %d' % new_node)
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))

    # Compare to correspondence and swap if necessary
    if new_node < length_max:
      correspond = new_node
    else:
      correspond = new_node / 2
    
    if (correspond > 0) and (self.__kf(self.__min_heap.data[new_node]) > self.__kf(self.__max_heap.data[correspond])):
      self.__min_heap.data[new_node], self.__max_heap.data[correspond] = self.__max_heap.data[correspond], self.__min_heap.data[new_node]
    
    self.__print('\n[E] %d' % self.__kf(result))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    
    
    # return the result
    return result

  def delete_max (self):
    self.__print('\ndelete_max()')
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    
    result = None

    # Deap is empty
    if self.__min_heap.is_empty() == True:
      return result
    
    # There is only one node in deap
    if self.__max_heap.is_empty() == True:
      result = self.__min_heap.data.pop()[1]
      return result
      
    # Take the root of max heap
    result = self.__max_heap.data[1][1]
    
    # Pop the last node of (min + max heap) and put it in the root of min heap
    length_min = len(self.__min_heap.data)
    length_max = len(self.__max_heap.data)
    assert(length_min >= length_max)
    if length_min == length_max:
      # Pop node from max heap
      node = self.__max_heap.data.pop()[1]
      length_max -= 1
    else:
      # Pop node from min heap
      node = self.__min_heap.data.pop()[1]
      length_min -= 1

    # Max heap is empty now     
    if self.__max_heap.is_empty() == True:
      return result

    self.__print('\n[2] node %d' % self.__kf(node))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))

    self.__max_heap.data[1] = (self.__kf(node), node)
    
    # Tidy up min heap from root
    new_node = self.__max_heap.tidy_up(1)
    
    self.__print('\n[2] new_node %d' % new_node)
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))

    # Compare to correspondence and swap if necessary
    correspond = new_node
    
    if self.__kf(self.__max_heap.data[new_node]) < self.__kf(self.__min_heap.data[correspond]):
      self.__max_heap.data[new_node], self.__min_heap.data[correspond] = self.__min_heap.data[correspond], self.__max_heap.data[new_node]
    
    self.__print('\n[E] %d' % self.__kf(result))
    self.__print('\n%s' % str(self.__min_heap.data))
    self.__print('\n%s' % str(self.__max_heap.data))
    
    
    # return the result
    return result

  def __print (self, information):
    pass
    #print information,

class MinMaxHeap (Heap):
  """
  MinMaxHeap Class

    Usage:

      mmh = MinMaxHeap()                          # Construct a MinMaxHeap
      
      mmh.insert(value[, object])                 # Insert a node with value
       
      value, object = mmh.delete_min()            # Return the (value, object) pair of minimum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
       
      value, object = mmh.delete_max()            # Return the (value, object) pair of maximum value.
                                                  #   object is None if not available
                                                  #   (None, None) is returned if the heap is empty           
  """
  def __init__ (self, key=(lambda d:d)):
    super(MinMaxHeap, self).__init__(rule=None)
    #self.data = self
    self.__kf = lambda n: key(self.data[n][0])

  def insert (self, value, object_=None):
    self.__print('\ninsert(%s, %s)' % (str(value), str(object_)))
    #super(MinMaxHeap, self).insert(value, object_)
    self.data.append((value, object_))
    node = len(self.data) - 1
    swap_node = None

    self.__print('\n[B]: %s' % (str(map(lambda x: self.__kf(x), range(1, len(self.data))))))

    if self.__is_in_min_level(node) == True:
      if (node >= 2) and (self.__kf(node) > self.__kf(node/2)):
        swap_node = node / 2
      elif (node >=4) and (self.__kf(node) < self.__kf(node/4)):
        swap_node = node / 4
    else:
      if (node >= 2) and (self.__kf(node) < self.__kf(node/2)):
        swap_node = node / 2
      elif (node >=4) and (self.__kf(node) > self.__kf(node/4)):
        swap_node = node / 4

    #self.__print('\n[2]: %s' % (str(map(lambda x: self.__kf(x), range(1, len(self.data))))))

    if swap_node != None:      
      self.data[node], self.data[swap_node] = self.data[swap_node], self.data[node]
      self.__print('\n[4]: %s' % (str(map(lambda x: self.__kf(x), range(1, len(self.data))))))
      self.__tidy_up_upward(swap_node) 

    self.__print('\n[E]: %s' % (str(map(lambda x: self.__kf(x), range(1, len(self.data))))))


  def delete_min (self):
    self.__print('\ndelete_min()')
    #super(MinMaxHeap, self).delete()
    if self.is_empty() == True:
      return (None, None)

    element = self.data[1]
    last = self.data.pop()
    if self.is_empty() == False:
      self.data[1] = last
      self.__tidy_up_downward(1)
    return element
          
  def delete_max (self):
    #pass
    self.__print('\ndelete_max()')
    if self.is_empty() == True:
      return (None, None)

    max_node = self.__max((1, 2, 3))
    
    element = self.data[max_node]
    
    # root is the maximum, means there is only one node in heap
    if max_node == 1:
      self.data.pop()
    else:
      last = self.data.pop()
      # the maximum node is the last node in heap
      if max_node >= len(self.data):
        pass
      else:
        self.data[max_node] = last
        self.__tidy_up_downward(max_node)
    
    return element
    

  def __min (self, nodes):
    return self.__min_max(nodes, (lambda x,y:x<=y), MinHeap)

  def __max (self, nodes):
    return self.__min_max(nodes, (lambda x,y:x>=y), MaxHeap)

  def __min_max (self, nodes, rule, heap_type):
    assert(len(nodes) > 0)
    length = len(self.data)
    L = []
    for n in nodes:
      if n < length:
        L.append((self.__kf(n), n))
    
    if len(L) == 0:
      return None
    elif len(L) == 1:
      return L[0][1]
    elif len(L) == 2:
      if rule(L[0][0], L[1][0]) == True:
        return L[0][1]
      else:
        return L[1][1]
    else:
      # Need to compare more than 2 elements. Use MinHeap.
      heap = heap_type()
      for key, node in L:
        heap.insert(key, node)
      return heap.delete()[1]

  def __tidy_up_upward (self, node):
    self.__print('\ntidy_up_upward(%d)' % node)
    if node >= 4:
      # Is node in min or max level?
      if self.__is_in_min_level(node) == True:
        rule = lambda c,p:self.__kf(c)>=self.__kf(p)
      else:
        rule = lambda c,p:self.__kf(c)<=self.__kf(p)
      
      while (node >= 4) and (rule(node, (node / 4)) == False):
        self.data[node], self.data[node / 4] = self.data[node / 4], self.data[node]
        node /= 4 

  def __tidy_up_downward (self, node):
    self.__print('\ninsert_empty_root()')
    length = len(self.data)
    assert(node < length)
    
    if self.__is_in_min_level(node) == True:
      rule = lambda x,y: self.__kf(x) <= self.__kf(y)
      compare = self.__min
    else:
      rule = lambda x,y: self.__kf(x) >= self.__kf(y)
      compare = self.__max
      

    # Do nothing if there is no child
    if node * 2 >= length:
      return

    temp_node = compare((node*2, node*2+1, node*4, node*4+1, node*4+2, node*4+3))
    assert(temp_node != None)
    
    if rule(node, temp_node) == True:
      return

    # Either left or right child is the minimum implies there is no grandchild
    # Swap data in temp_node and node and then done. 
    if temp_node <= (node*2+1):
      self.data[node], self.data[temp_node] = self.data[temp_node], self.data[node]
      return
    
    # temp_node is one of grandchildren
    # Swap data in temp_node and node
    self.data[node], self.data[temp_node] = self.data[temp_node], self.data[node]
    
    # if new temp_node data is greater than its parent
    # Swap data in temp_node and its parent
    if rule(temp_node, temp_node/2) == False:
      self.data[temp_node/2], self.data[temp_node] = self.data[temp_node], self.data[temp_node/2]

    # Go on tidying up temp_node (a grandchild of node)
    self.__tidy_up_downward(temp_node)

    

  def __is_in_min_level (self, node):
    import math
    return (int(math.log(node, 2))) % 2 == 0

  def __print (self, information):
    #print str(information),
    pass

class ThreadedBinaryTree (object):
  """

  """
  def __init__ (self, tree={}):
#     super(ThreadedBinaryTree, self).__init__({'data': '',
#                                               'left': self,
#                                               'left thread': True,
#                                               'right': self,
#                                               'right thread': False})
    self.data = {'data': '',
                 'left': self,
                 'left thread': True,
                 'right': self,
                 'right thread': False}
    keys = tree.keys()
    keys.sort()
    if keys == ['data', 'left', 'left thread', 'right', 'right thread']:
      self.data['data'] = tree['data']
      self.data['left'] = tree['left']
      self.data['left thread'] = tree['left thread']
      self.data['right'] = tree['right']
      self.data['right thread'] = tree['right thread']

  def insert_left (self, child_data, parent=None):
    if parent == None:
      parent = self.data

    child = {'data': child_data,
             'left': parent['left'],
             'left thread': parent['left thread'],
             'right': parent,
             'right thread': True}
    parent['left'] = child
    parent['left thread'] = False

    if child['left thread'] == False:
      node = child['left']
      while node['right'] != parent:
        node = node['right']
      node['right'] = child

    return child

  def insert_right (self, child_data, parent):
    if parent == self.data:
      return self.data
    else:
      child = {'data': child_data,
               'left': parent,
               'left thread': True,
               'right': parent['right'],
               'right thread': parent['right thread']}
      parent['right'] = child
      parent['right thread'] = False
      if child['right thread'] == False:
        node = self.__inorder_successor(child)
        node['left'] = child

      return child

  def traverse_inorder (self, delimiter=''):
    return self.__traverse(self.__inorder_successor, delimiter)

  def traverse_preorder (self, delimiter=''):
    return self.__traverse(self.__preorder_successor, delimiter)
    
  def traverse_postorder (self, delimiter=''):
    return self.__postorder_traverse(self.data['left'], delimiter)
    
  def __traverse (self, successor_method, delimiter):
    result = ''
    node = successor_method(self.data)
    while node != self.data:
      result = delimiter.join([result, str(node['data'])])
      node = successor_method(node)
    return result

  def inorder_successor (self, node):
    return self.__inorder_successor(node)

  def __inorder_successor (self, node):
    if node['right thread'] == True:
      return node['right']
    else:
      result = node['right']
      while result['left thread'] == False:
        result = result['left']
      return result

  def __preorder_successor (self, node):
    if node['left thread'] == False:
      return node['left']
    elif node['right thread'] == False:
      return node['right']
    else:
      result = node['right']
      while result['right thread'] == True:
        result = result['right']
      return result['right']

  def __postorder_successor (self, node):
    """
    Not efficient!
    """

  def __postorder_traverse (self, node, delimiter):
    result = ''
    if node['left thread'] == False:
      result = ''.join([result, self.__postorder_traverse(node['left'], delimiter)])
    if node['right thread'] == False:
      result = ''.join([result, self.__postorder_traverse(node['right'], delimiter)])
    result = delimiter.join([result, str(node['data'])])
    return result

class BinaryTreeDict (object):
  """

  """
  def __init__ (self, tree={}):
    #super(BinaryTreeDict, self).__init__({'data': '', 'left': None, 'right': None})
    self.data = {'data': '', 'left': None, 'right': None}
    keys = tree.keys()
    keys.sort()
    if keys == ['data', 'left', 'right']:
      self.data['data'] = tree['data']
      self.data['left'] = tree['left']
      self.data['right'] = tree['right']

  def insert_left_child (self, data, parent, right=False):
    child = {}
    child.update(data)
    if right == False:
      child.update({'left': parent['left'], 'right': None})
    else:
      child.update({'left': None, 'right': parent['left']})
    parent['left'] = child
    return child

  def insert_right_child (self, data, parent, left=False):
    child = {}
    child.update(data)
    if left == False:
      child.update({'left': None, 'right': parent['right']})
    else:
      child.update({'left': parent['right'], 'right': None})
    parent['right'] = child
    return child

  def traverse_inorder (self, delimiter=''):
    return self.__traverse_inorder_recursive(self.data, delimiter)

  def traverse_preorder (self, delimiter=''):
    return self.__traverse_preorder_recursive(self.data, delimiter)

  def traverse_postorder (self, delimiter=''):
    return self.__traverse_postorder_recursive(self.data, delimiter)

  def __traverse_inorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([self.__traverse_inorder_recursive(node['left'], delimiter),
                      str(node['data']),
                      self.__traverse_inorder_recursive(node['right'], delimiter)])

  def __traverse_preorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([str(node['data']),
                      self.__traverse_preorder_recursive(node['left'], delimiter),
                      self.__traverse_preorder_recursive(node['right'], delimiter)])

  def __traverse_postorder_recursive (self, node, delimiter):
    if node == None:
      return delimiter
    else:
      return delimiter.join([self.__traverse_postorder_recursive(node['left'], delimiter),
                      self.__traverse_postorder_recursive(node['right'], delimiter),
                      str(node['data'])])

class BinaryTreeArray (object):
  """
  Binary tree represented by array (Python list)
  """
  def __init__ (self, tree=[]):
    #super(BinaryTreeArray, self).__init__([None])
    self.data = [None]
    self.data.extend(tree)
    self.__null = None

  def insert_left (self, data, parent_index, put_child_to_right=False):
    if self.__has_left_child(parent_index) == True:
      if put_child_to_right == True:
        self.__move_tree(parent_index*2, parent_index*4+1)
      else:
        self.__move_tree(parent_index*2, parent_index*4)
    
    self.__set_data(parent_index*2, data)

  def insert_right (self, data, parent_index, put_child_to_left=False):
    if self.__has_right_child(parent_index) == True:
      if put_child_to_left == True:
        self.__move_tree(parent_index*2+1, parent_index*4+2)
      else:
        self.__move_tree(parent_index*2, parent_index*4+3)
    
    self.__set_data(parent_index*2+1, data)

  def traverse_inorder (self, index=1, delimiter=''):
    if len(self.data) <= index or self.data[index] == self.__null:
      return delimiter
      
    return delimiter.join([self.traverse_inorder(index*2, delimiter),
                    str(self.data[index]),
                    self.traverse_inorder(index*2+1, delimiter)])

  def traverse_preorder (self, index=1, delimiter=''):
    if len(self.data) <= index or self.data[index] == self.__null:
      return delimiter
      
    return delimiter.join([str(self.data[index]),
                    self.traverse_preorder(index*2, delimiter),
                    self.traverse_preorder(index*2+1, delimiter)])

  def traverse_postorder (self, index=1, delimiter=''):
    if len(self.data) <= index or self.data[index] == self.__null:
      return delimiter
      
    return delimiter.join([self.traverse_postorder(index*2, delimiter),
                    self.traverse_postorder(index*2+1, delimiter),
                    str(self.data[index])])

  def __set_data (self, index, data):
    if len(self.data) <= index:
      map(lambda x:self.data.append(self.__null), range(len(self.data), index+1))
    self.data[index] = data

  def __move_tree (self, old_root_index, new_root_index):
    if self.__has_left_child(old_root_index) == True:
      self.__move_tree(old_root_index*2, new_root_index*2)
    if self.__has_right_child(old_root_index) == True:
      self.__move_tree(old_root_index*2+1, new_root_index*2+1)
    
    self.__set_data(new_root_index, self.data[old_root_index])
    self.__set_data(old_root_index, self.__null)

  def __left_child (self, index):
    try:
      return self.data[index*2]
    except IndexError:
      return self.__null

  def __right_child (self, index):
    try:
      return self.data[index*2+1]
    except IndexError:
      return self.__null

  def __has_left_child (self, index):
    return self.__left_child(index) != self.__null

  def __has_right_child (self, index):
    return self.__right_child(index) != self.__null

class LoserTree (object):
  class __Node (object):
    def __init__ (self):
      self.data = {'L': None, 'w': None}
      self.parent = None
  
  def __init__ (self, k, key_function=(lambda x:x), order_function=(lambda p,c:p<=c)):
    assert(type(k) == type(1))
    assert(k >= 2)

    self.__k = k

    self.__kf = key_function
    self.__of = order_function

    # Construct tree
    self.__leaves = map(lambda x:self.__Node(), range(0, k))
    temp_queue = [] + self.__leaves
    while len(temp_queue) > 1:
      parent = self.__Node()
      temp_queue.pop(0).parent = parent
      temp_queue.pop(0).parent = parent
      temp_queue.append(parent)
    self.__root = parent

  def put (self, index, data):
    assert(index < self.__k)
    
    self.__print('\nput(%d, %s)' % (index, str(self.__kf(data))))

    child = self.__leaves[index]
    if data == None:
      child.data = {'L': None, 'w': None}
      lost = None
      child = child.parent
      parent = child
      while parent != None:
        if parent.data['w'][0] == index:
          parent.data['w'] = parent.data['L']
          parent.data['L'] = None
        elif parent.data['L'][0] == index:
          parent.data['L'] = None
        parent = parent.parent
    else:
      child.data['w'] = (index, data)
      lost = None

    
    self.__print('\n')
    self.__print(map(lambda l: str(self.__kf(l.data)), self.__leaves))
    
    while child.parent != None:
      parent = child.parent

      self.__print('\nBefore: child data:')
      try:
        self.__print('{W: (%d, %s)}' % (child.data['w'][0], str(self.__kf(child.data['w'][1]))))
      except TypeError:
        self.__print('{W: %s}' % (str(child.data['w'])))
      self.__print('\nBefore: parent data:')
      try:
        self.__print('{L: (%d, %s),' % (parent.data['L'][0], str(self.__kf(parent.data['L'][1])))),
      except TypeError:
        self.__print('{L: %s,' % (str(parent.data['L'])))
      try:
        self.__print('W: (%d, %s)}' % (parent.data['w'][0], str(self.__kf(parent.data['w'][1]))))
      except TypeError:
        self.__print('W: %s}' % (str(parent.data['w'])))
      self.__print('lost: %s' % (str(lost)))

      if (parent.data['L'] != None) and ((parent.data['L'] == child.data['w']) or 
                                         (parent.data['L'] == child.data['L']) or
                                         (parent.data['L'][0] == lost)):
        parent.data['L'] = child.data['w']
      elif (parent.data['w'] != None) and ((parent.data['w'] == child.data['w']) or 
                                           (parent.data['w'] == child.data['L']) or 
                                           (parent.data['w'][0] == lost)):
        parent.data['w'] = child.data['w']
      elif parent.data['w'] == None:
        parent.data['w'] = child.data['w']
      else:
        parent.data['L'] = child.data['w']
      
      if parent.data['L'] != None:
        if self.__of(self.__kf(parent.data['w'][1]), self.__kf(parent.data['L'][1])) == False:
          parent.data['w'], parent.data['L'] = parent.data['L'], parent.data['w']
          lost = parent.data['L'][0]
      

      self.__print('\nAfter: parent data:')
      try:
        self.__print('{L: (%d, %s),' % (parent.data['L'][0], str(self.__kf(parent.data['L'][1]))))
      except TypeError:
        self.__print('{L: %s,' % (str(parent.data['L'])))
      try:
        self.__print('W: (%d, %s)}' % (parent.data['w'][0], str(self.__kf(parent.data['w'][1]))))
      except TypeError:
        self.__print('{W: %s,' % (str(parent.data['w'])))
      self.__print('lost: %s' % (str(lost)))

      child = parent


  def get (self):
    assert(self.__root.data != None)
    self.__print('\nRoot data:')
    try:
      self.__print('{L: (%d, %s),' % (self.__root.data['L'][0], str(self.__kf(self.__root.data['L'][1]))))
    except TypeError:
      self.__print('{L: %s,' % (str(self.__root.data['L'])))
    try:
      self.__print('W: (%d, %s)}' % (self.__root.data['w'][0], str(self.__kf(self.__root.data['w'][1]))))
    except TypeError:
      self.__print('{W: %s,' % (str(self.__root.data['w'])))
    result = self.__root.data['w']
    
    if result != None:
      self.put(result[0], None)
    else:
      result = (None, None)

    return result

  def __print (self, info):
#     print info,
    pass

if __name__ == '__main__':
  n10 = {'data': 52, 'left': None, 'right': None}
  n9 = {'data': 55, 'left': n10, 'right': None}
  n8 = {'data': 45, 'left': None, 'right': None}
  n7 = {'data': 70, 'left': None, 'right': None}
  n6 = {'data': 50, 'left': n8, 'right': n9}
  n5 = {'data': 30, 'left': None, 'right': None}
  n4 = {'data': 10, 'left': None, 'right': None}
  n3 = {'data': 60, 'left': n6, 'right': n7}
  n2 = {'data': 20, 'left': n4, 'right': n5}
  n1 = {'data': 40, 'left': n2, 'right': n3}

  td = BinaryTreeDict(n1)
  #print td.traverse_preorder()
  
  ta = BinaryTreeArray()
  ta.insert_right(40, 0)
  ta.insert_left(20, 1)
  ta.insert_right(60, 1)
  ta.insert_left(10, 2)
  ta.insert_right(30, 2)
  ta.insert_left(50, 3)
  ta.insert_right(70, 3)
  ta.insert_left(45, 6)
  ta.insert_right(55, 6)
  ta.insert_left(52, 13)
  print 'BinaryTreeArray()'
  print 'Inorder:',
  print ta.traverse_inorder() == td.traverse_inorder(),
  print ' Preorder:',
  print ta.traverse_preorder() == td.traverse_preorder(),
  print ' Postorder:',
  print ta.traverse_postorder() == td.traverse_postorder()
  
  print 'Test of BinaryTree'
  bt = BinaryTree()
  n1 = bt.insert_left(40)
  n2 = bt.insert_left(20, n1)
  n3 = bt.insert_right(60, n1)
  n4 = bt.insert_left(10, n2)
  n5 = bt.insert_right(30, n2)
  n6 = bt.insert_left(50, n3)
  n7 = bt.insert_right(70, n3)
  n8 = bt.insert_left(45, n6)
  n9 = bt.insert_right(55, n6)
  n10 = bt.insert_left(52, n9)
  print 'Inorder:',
  print bt.traverse_inorder() == td.traverse_inorder(),
  print ' Preorder:',
  print bt.traverse_preorder() == td.traverse_preorder(),
  print ' Postorder:',
  print bt.traverse_postorder() == td.traverse_postorder()

  
  

  root = {}
  tn1  = {}
  tn2  = {}
  tn3  = {}
  tn4  = {}
  tn5  = {}
  tn6  = {}
  tn7  = {}
  tn8  = {}
  tn9  = {}
  tn10 = {}
  tn10.update({'data': 52, 'left': tn6,  'left thread': True,  'right': tn9,  'right thread': True})
  tn9.update({'data': 55, 'left': tn10, 'left thread': False, 'right': tn3,  'right thread': True})
  tn8.update({'data': 45, 'left': tn1,  'left thread': True,  'right': tn6,  'right thread': True})
  tn7.update({'data': 70, 'left': tn3,  'left thread': True,  'right': root, 'right thread': True})
  tn6.update({'data': 50, 'left': tn8,  'left thread': False, 'right': tn9,  'right thread': False})
  tn5.update({'data': 30, 'left': tn2,  'left thread': True,  'right': tn1,  'right thread': True})
  tn4.update({'data': 10, 'left': root, 'left thread': True,  'right': tn2,  'right thread': True})
  tn3.update({'data': 60, 'left': tn6,  'left thread': False, 'right': tn7,  'right thread': False})
  tn2.update({'data': 20, 'left': tn4,  'left thread': False, 'right': tn5,  'right thread': False})
  tn1.update({'data': 40, 'left': tn2,  'left thread': False, 'right': tn3,  'right thread': False})
  root.update({'data': '', 'left': tn1,  'left thread': False, 'right': root, 'right thread': False})
  tt = ThreadedBinaryTree(root)
  print 'ThreadedBinaryTree()'
  print 'Inorder:',
  print tt.traverse_inorder() == td.traverse_inorder(),
  print ' Preorder:',
  print tt.traverse_preorder() == td.traverse_preorder(),
  print ' Postorder:',
  print tt.traverse_postorder() == td.traverse_postorder()

  ttt = ThreadedBinaryTree()
  ttn1 = ttt.insert_left(40)
  ttn2 = ttt.insert_left(20, parent=ttn1)
  ttn3 = ttt.insert_right(60, parent=ttn1)
  ttn4 = ttt.insert_left(10, parent=ttn2)
  ttn5 = ttt.insert_right(30, parent=ttn2)
  ttn6 = ttt.insert_left(50, parent=ttn3)
  ttn7 = ttt.insert_right(70, parent=ttn3)
  ttn8 = ttt.insert_left(45, parent=ttn6)
  ttn9 = ttt.insert_right(55, parent=ttn6)
  ttn10 = ttt.insert_left(52, parent=ttn9)

  print 'Test of MaxHeap'
  #h = MaxHeap([20, 10, 15, 8, 3, 2, 7, 1])
  h = MaxHeap()
  h.insert(15)
  h.insert(8)
  h.insert(3)
  h.insert(7)
  h.insert(20)
  h.insert(10)
  h.insert(2)
  h.insert(1)
  #print h
  print h.data == [None, (20, None), (15, None), (10, None), (7, None), (8, None), (3, None), (2, None), (1, None)],
  print h.delete() == (20, None),
  #print h.data == [None, (15, None), (8, None), (10, None), (7, None), (1, None), (3, None), (2, None)]
  print h.delete() == (15, None),
  print h.data == [None, (10, None), (8, None), (3, None), (7, None), (1, None), (2, None)],
  print h.delete() == (10, None),
  #print h.data == [None, (8, None), (7, None), (2, None), (3, None), (1, None)]
  print h.delete() == (8, None),
  #print h.data == [None, (7, None), (1, None), (2, None), (3, None)]
  print h.delete() == (7, None)
  #print h.data == [None, (3, None), (1, None), (2, None)]
  print h.delete() == (3, None),
  print h.data == [None, (2, None), (1, None)],
  print h.delete() == (2, None),
  print h.data == [None, (1, None)],
  print h.delete() == (1, None),
  #print h
  print h.delete() == (None, None)
  #print h

  print 'Test of MinHeap'
  h = MinHeap()
  h.insert(15)
  h.insert(8)
  h.insert(3)
  h.insert(7)
  h.insert(20)
  h.insert(10)
  h.insert(2)
  h.insert(1)
  #print h
  print h.data == [None, (1, None), (2, None), (3, None), (7, None), (20, None), (10, None), (8, None), (15, None)],
  print h.delete() == (1, None),
  #print h.data == [None, (15, None), None), (8, None), (10, None), (7, None), (1, None), (3, None), (2, None), (None)]
  print h.delete() == (2, None),
  print h.data == [None, (3, None), (7, None), (8, None), (15, None), (20, None), (10, None)],
  print h.delete() == (3, None),
  #print h.data == [None, (8, None), (7, None), (2, None), (3, None), (1, None)]
  print h.delete() == (7, None),
  #print h.data == [None, (7, None), (1, None), (2, None), (3, None)]
  print h.delete() == (8, None)
  #print h.data == [None, (10, None), (15, None), (20, None)]
  print h.delete() == (10, None),
  print h.data == [None, (15, None), (20, None)],
  print h.delete() == (15, None),
  #print h.data == [None, (20, None)]
  print h.delete() == (20, None),
  #print h
  print h.delete() == (None, None)
  #print h

  print 'Test of LoserTree'
  k = 10
  lt = LoserTree(k)
  lt.put(1, 1)
  lt.put(3, 3)
  lt.put(5, 9)
  lt.put(7, 2)
  lt.put(2, 7)
  lt.put(4, 8)
  lt.put(8, 4)
  lt.put(9, 0)
  lt.put(6, 5)
  lt.put(0, 6)
  
  print map(lambda x: lt.get()[1], range(0, k)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  print lt.get() == (None, None)
  #print lt.get()
  #print lt.get()
  #print lt.get()


  print 'Test of MinMaxHeap'
  l = [45, 50, 70, 40, 30, 12, 30, 20, 9, 10, 15, 7]
  mmh = MinMaxHeap()
  for v in l:
    mmh.insert(v)
  print map(lambda x:mmh.delete_min()[0], range(0, len(l)+2)) == [7, 9, 10, 12, 15, 20, 30, 30, 40, 45, 50, 70, None, None], 
  for v in l:
    mmh.insert(v)
  print map(lambda x:mmh.delete_max()[0], range(0, len(l)+2)) == [70, 50, 45, 40, 30, 30, 20, 15, 12, 10, 9, 7, None, None] 


  print 'Test of Deap'
  l = [45, 50, 70, 40, 30, 12, 30, 20, 9, 10, 15, 7]
  d = Deap()
  for v in l:
    d.insert(v)
  print map(lambda x:d.delete_min(), range(0, len(l)+2)) == [7, 9, 10, 12, 15, 20, 30, 30, 40, 45, 50, 70, None, None], 
#   for v in l:
#     d.insert(v)
#   print map(lambda x:d.delete_max()[0], range(0, len(l)+2)) == [70, 50, 45, 40, 30, 30, 20, 15, 12, 10, 9, 7, None, None] 
  for v in l:
    d.insert(v)
  print map(lambda x:d.delete_max(), range(0, len(l)+2)) == [70, 50, 45, 40, 30, 30, 20, 15, 12, 10, 9, 7, None, None] 

  print 'Test of Leftist'
  lt = Leftist()
  lt.insert(13)
#   print lt.root.get_data()
  lt1 = Leftist()
  lt1.insert(11)
  lt1.combine(lt)
#   print lt1.root.get_data()
#   print lt1.root.get_left_child().get_data()
#   print lt1.root.get_right_child()
  lt = Leftist()
  lt.insert(7)
  lt.combine(lt1)
  lt1 = Leftist()
  lt1.insert(2)
  lt1.combine(lt)
  lt = Leftist()
  lt.insert(80)
  lt.insert(50)
  lt.combine(lt1)
#   print lt.traverse_inorder() == '.13..11..7..2..80..50.',
#   print lt.traverse_preorder() == '2.7.11.13.....50.80...',
#   print lt.traverse_postorder() == '..13..11..7...80..50.2'
  lt1 = Leftist()
  lt1.insert(12)
  lt1.insert(20)
  lt1.insert(18)
  lt2 = Leftist()
  lt2.insert(9)
  lt2.combine(lt1)
  lt1 = Leftist()
  lt1.insert(5)
  lt1.combine(lt2)
  lt2 = Leftist()
  lt2.insert(10)
  lt2.insert(15)
  lt3 = Leftist()
  lt3.insert(8)
  lt3.combine(lt2)
  lt1.combine(lt3)
#   print lt1.traverse_inorder() == '.20..12..18..9..5..15..10..8.',
#   print lt1.traverse_preorder() == '5.9.12.20...18....8.10.15....',
#   print lt1.traverse_postorder() == '..20...18.12..9...15..10..8.5'
  lt.combine(lt1)
  print lt.traverse_inorder()   == '15108805052012189213117',
  print lt.traverse_preorder()  == '25810155080912201871113',
  print lt.traverse_postorder() == '15108050820181295131172'
  
  print 'Test of AvlTree'
  avl_tree = AvlTree(lambda x:x[0:3])
  avl_tree.insert('March')
  avl_tree.insert('May')
  avl_tree.insert('November')
  avl_tree.insert('August')
  avl_tree.insert('April')
  avl_tree.insert('January')
  avl_tree.insert('December')
  avl_tree.insert('July')
  avl_tree.insert('Febuary')
  avl_tree.insert('June')
  avl_tree.insert('October')
  avl_tree.insert('September')
  print avl_tree.traverse_inorder('') == 'AprilAugustDecemberFebuaryJanuaryJulyJuneMarchMayNovemberOctoberSeptember',
  print avl_tree.traverse_preorder() == 'JanuaryDecemberAugustAprilFebuaryMarchJulyJuneNovemberMayOctoberSeptember',
  print avl_tree.traverse_postorder() == 'AprilAugustFebuaryDecemberJuneJulyMaySeptemberOctoberNovemberMarchJanuary',
  key = 'Sep'
  print avl_tree.search(key)[0], avl_tree.search(key)[1] == 'September'


  
  
  
  
