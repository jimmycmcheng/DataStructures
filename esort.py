#! usr/bin/python


def k_way_merge (out, in_, key_function=(lambda x: x), order_function=(lambda x,y: x<=y)):
  from bintree import LoserTree
  
  assert((type(in_) == type([]) or type(())) and (len(in_) > 0))
  assert(type(in_[-1]) == type(lambda x:x))
  assert(type(out) == type(lambda x:x))
  
  k = len(in_)
  lt = LoserTree(k, key_function, order_function)
  for i in range(0, k):
    data = in_[i]()
    if data != None:
      lt.put(i, data)
  
  i, data = lt.get()
  while i != None:
    out(data)
    data = in_[i]()
    if data != None:
      lt.put(i, data)
    i, data = lt.get()

def __test_read_function (ll, i):
  if (len(ll[i])) > 0:
    return ll[i].pop(0)
  else:
    return None



if __name__ == '__main__':
  print 'Test k_way_merge'
  ll = [[1, 5, 8, 10, 57, 100], [3, 4, 9, 13], [0, 2, 9, 11, 15, 20, 37, 97]]
  length = len(reduce(lambda x,y: x+y, ll))
  out = []
  
  k_way_merge(out=(lambda d: out.append(d)), 
              in_=map(lambda i: lambda: __test_read_function(ll, i), range(0, len(ll))))
  print out == [0, 1, 2, 3, 4, 5, 8, 9, 9, 10, 11, 13, 15, 20, 37, 57, 97, 100],
  print len(out) == length
