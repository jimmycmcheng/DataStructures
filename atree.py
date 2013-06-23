#! usr/bin/python

from bintree import *

class AlphabetTree (BinaryTreeDict):
  """

  """
  def __init__ (self, tree={}):
    super(AlphabetTree, self).__init__(tree)
    self.update({'end': False, 'data': ''})

  def print_report (self):
    self.__traverse(self, '')

  def __traverse (self, node, previous_string):
    if node['end'] == True:
      print '%s, %d' % (previous_string + node['data'], node['count']),
      print node['occurence']

    if node['left'] != None:
      self.__traverse(node['left'], previous_string + node['data'])

    if node['right'] != None:
      self.__traverse(node['right'], previous_string)


  def handle_word (self, word, occurence):
    result, node, word = self.search(word, self)

    # The word is existed in tree
    if result == False:
      node = self.add_word(word, node)

    node['count'] = node['count'] + 1
    node['occurence'].append(occurence)
    node['end'] = True

  def add_word (self, word, parent):
    data = {'data': word[0], 'count': 0, 'occurence': [], 'end': False}
    result, node = self.__search_character(word[0], parent['left'])
    if node == None:
      node = self.insert_left_child(data, parent, right=True)
    else:
      result, node = self.__search_character(word[0], parent['left'])
      node = self.insert_right_child(data, node)

    if len(word) == 1:
      return node
    else:
      return self.add_word(word[1:], node)

  def search (self, word, parent):
    if len(word) == 0:
      return False, None, None

    result, node = self.__search_character(word[0], parent['left'])
    if result == False:
      return False, parent, word

    if len(word) == 1:
      return result, node, word
    
    return self.search(word[1:], node)

  def __search_character(self, character, node):
    if node == None or node['data'] > character:
      return False, None

    while True:
      if node['data'] == character:
        return True, node
      elif node['right'] == None or node['right']['data'] > character:
          return False, node
      else:
          node = node['right']

    

if __name__ == '__main__':

  article = [  'Following Los Angeles 113103 loss to the Milwaukee Bucks on Thursday night the Lakers revealed the injury He left the arena using one crutch but appeared to be walking without pain'
             , 'Bryant led the Lakers with 30 points leaving him four points behind Wilt Chamberlain for fourth place on the NBAs career list Bryant played 36 12 minutes and didnt show any signs of difficulty during the game'
             , 'Inflamed on me Ill be all right Bryant told Yahoo Sports'
             , 'Bryant struggled from the field going 6 of 17 but made 18 of 20 free throws'
             , 'The Lakers are eighth in the Western Conference a halfgame ahead of Utah for the final playoff spot']

  at = AlphabetTree()
  for line in range(0, len(article)):
    map(lambda x: at.handle_word(x, occurence=line+1), article[line].lower().split(' '))

  at.print_report()
