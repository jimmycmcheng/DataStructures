#! usr/bin/python
from util import *

def insert_sort (data, order=lambda x,y: x<y, (left, right)=(0, None)):
  if right == None:
    right = len(data)
  
  assert(0 <= left <= right < len(data))
  
  for i in range(left+1, right+1):
    index = __insert_sort_search_right(data[i], data[left:i], order) + left
    data[index:i+1] = [data[i]] + data[index:i]

  return data

def __insert_sort_search_right (value, sorted_list, order):
  i = 0
  while i < len(sorted_list) and order(sorted_list[i], value) == True:
    i += 1
  return i
      

def qsort (data, order=lambda x,y: x<=y, (left, right)=(0, None)):
  #print 'qsort'
  #print data, key, left, right, order
  if right == None:
    right = len(data)
  
  if left >= right:
    return
  #assert(left <= right)
  
  pivot = data[left]
  i = left
  j = right + 1
  while True:
    i += 1
    while i < right and order(data[i], pivot) == True:
      i += 1
    j -= 1
    while j > left and order(pivot, data[j]) == True:
      j -= 1
    if i < j:
      data[i], data[j] = data[j], data[i]
    elif i >= j:
      break

  #print i, j
  data[left], data[j] = data[j], data[left]
  qsort(data, order, (left, j-1))
  qsort(data, order, (j+1, right))

  return data

def qsortm (data, order=lambda x,y: x<=y, (left, right)=(0, None)):
  if right == None:
    right = len(data)
  #print 'qsort'
  #print data, key, left, right, order
  if left >= right:
    return data
  
  middle = (left + right) / 2
  if order(data[left], data[right]):
    if order(data[middle], data[left]):
      pass
    elif order(data[right], data[middle]):
      data[left], data[right] = data[right], data[left]
    else:
      data[middle], data[left] = data[left], data[middle]
  else: # data[left] > data[right]:
    if order(data[left], data[middle]):
      pass
    elif order(data[middle], data[right]):
      data[left], data[right] = data[right], data[left]
    else:
      data[middle], data[left] = data[left], data[middle]

  pivot = data[left]
  i = left
  j = right + 1
  while True:
    i += 1
    while i < right and order(data[i], pivot) == True:
      i += 1
    j -= 1
    while j > left and order(pivot, data[j]) == True:
      j -= 1
    if i < j:
      data[i], data[j] = data[j], data[i]
    elif i >= j:
      break

  #print i, j
  data[left], data[j] = data[j], data[left]
  qsortm(data, order, (left, j-1))
  qsortm(data, order, (j+1, right))

  return data

def __adjust_heap (list_, parent, order):
  length = len(list_)
  assert(parent < length)

  left_child = (parent + 1) * 2 - 1
  right_child = (parent + 1) * 2
#   print '[%d] %s' % (parent, str(list_[parent])),
#   print '[%d]' % (left_child),
#   try:
#     print '%s' % (str(list_[left_child])),
#   except IndexError:
#     pass
#   print '[%d]' % (right_child),
#   try:  
#     print '%s' % (str(list_[right_child])),
#   except IndexError:
#     pass
#   print ''

  if left_child < length:

    adjust = None
    if (left_child < length) and (order(list_[parent], list_[left_child]) == True):
      if (right_child < length) and (order(list_[left_child], list_[right_child]) == True):
        adjust = right_child
      else:
        adjust = left_child
    elif (right_child < length) and (order(list_[parent], list_[right_child]) == True):
      adjust = right_child
    
    if adjust != None:
      list_[parent], list_[adjust] = list_[adjust], list_[parent]
      __adjust_heap(list_, adjust, order)
  
  #print list_
  return list_

def __heap_sort_external_heap (data, order=(lambda x,y: x<=y), (left, right)=(0, None)):
  from bintree import Heap
  
  if right == None:
    right = len(data) - 1
  
  assert(left <= right < len(data))
  
  if right - left + 1 > 1:
  
    h = Heap(lambda c,p:order(p, c))
    for d in data[left:(right + 1)]:
      h.insert(d)
  
    d = h.delete()[0]
    i = left
    while d != None:
      data[i] = d
      d = h.delete()[0]
      i += 1

  return data    

def __heap_sort_internal_heap (data, order=(lambda x,y: x<=y), (left, right)=(0, None)):
  if right == None:
    right = len(data) - 1

  length = len(data)
  assert(right < length)
  
  length = right - left + 1

  if length < 2:
    return data

  list_ = data[left:(right+1)]

  #print list_

  i = (length - 1)  / 2
  while i >= 0:
    __adjust_heap(list_, i, order)
    i -= 1

  #print list_

  i = length - 1
  while i > 0:
    list_[0], list_[i] = list_[i], list_[0]
    list_[0:i] = __adjust_heap(list_[0:i], 0, order)
    i -= 1

  data[left:right+1] = list_

  return data

def heap_sort (data, order=(lambda x,y: x<=y), (left, right)=(0, None)):
  return __heap_sort_external_heap(data, order, (left, right))

def radix_sort (data, rule=((lambda x: x), (lambda x,y: x<=y)), (left, right)=(0, None)):
  assert(type(rule).__name__ == type(()).__name__)

  if type(rule[0]).__name__ != type(()).__name__:
    rule = [rule]
  else:
    rule = list(rule)
    rule.reverse()

  if right == None:
    right = len(data) - 1
  
  assert(0 <= left < right < len(data))

  handle_data = data[left:(right+1)]

  for key_function, order_function in rule:
    list_ = []
    for d in handle_data:
      key = key_function(d)
      try:
        list_[key].append(d)
      except IndexError:
        list_.extend(map(lambda x: [], range(len(list_), (key + 1))))
        list_[key].append(d)
    # Test order_function. If the specified ordering is non-increasing, list_ has to be reversed.
    if order_function(0, 1) == False:
      list_.reverse()

    handle_data[0:] = reduce(lambda x,y: x+y, list_)

  data[left:(right+1)] = handle_data
  return data

def count_sort (data, order=lambda x,y: x<y, (left, right)=(0, None)):
  if right == None:
    right = len(data)
  
  length = right - left + 1
  if length > 1:
    counts = zeros(length)
    for i in range(left, right):
      for j in range(i+1, right+1):
        if order(data[i], data[j]) == True:
          counts[j - left] += 1
        else:
          counts[i - left] += 1
    
    # Sort
    i = left
    while i <= right:
      j = counts[i - left] + left
      if i != j:
        data[i], data[j] = data[j], data[i]
        counts[i - left], counts[j - left] = counts[j - left], counts[i - left]
      else:
        i += 1

  return data

def exchange_sort (data, order=lambda x,y: x<y, (left, right)=(0, None)):
  if right == None:
    right = len(data)
  
  length = right - left + 1
  if length > 1:
    temp_data = data[left:(right+1)]
    
    for i in range(0, (length-1)):
      exchange = False
      for j in range(0, (length-i-1)):
        if order(temp_data[j], temp_data[j+1]) == False:
          temp_data[j], temp_data[j+1] = temp_data[j+1], temp_data[j]
          exchange = True
          
      if exchange == False:
        #print 'Done. Break'
        break
    
    data[left:(right+1)] = temp_data

  return data

def shaker_sort (data, order=lambda x,y: x<y, (left, right)=(0, None)):
  if right == None:
    right = len(data)
  
  length = right - left + 1
  if length > 1:
    temp_data = data[left:(right+1)]

    #print temp_data
    
    i = 0
    while i < (length - 1):
      min_ = i
      exchange = False
      for j in range(i, (length-i-1)):
        if order(temp_data[j], temp_data[j+1]) == False:
          temp_data[j], temp_data[j+1] = temp_data[j+1], temp_data[j]
          exchange = True
        if order(temp_data[min_], temp_data[j]) == False:
          min_ = j
          
      if exchange == False:
        #print 'Done. Break'
        break
      
      temp_data[min_], temp_data[i] = temp_data[i], temp_data[min_]
      i += 1

      #print temp_data
      #print min_
      #input('')
      #import os
      #os.system('PAUSE')
          
    
    data[left:(right+1)] = temp_data

  return data


if __name__ == '__main__':
  #l = [(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)]
  #l = [(10, 5), (7, 8), (8, 9), (9, 10), (8, 3)]
  #print l
  
  print 'qsort:',
  print qsortm([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
               lambda x,y: x[0]>=y[0], 
               (0, 11)
               ) == [(10, 5), (9, 10), (8, 9), (8, 3), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)]

  print 'insert_sort:',
  print insert_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                    lambda x,y: x[0]<=y[0], 
                    (0, 11)
                    ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print insert_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                    lambda x,y: x[0]>=y[0], 
                    (0, 11)
                    ) == [(10, 5), (9, 10), (8, 3), (8, 9), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)]
  
  print 'heap_sort:',
  print __heap_sort_internal_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                                  lambda x,y: x[0]<=y[0]
                                  ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print __heap_sort_internal_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)],
                                  lambda x,y: x[0]>=y[0]
                                  ) == [(10, 5), (9, 10), (8, 3), (8, 9), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)],
  print __heap_sort_internal_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                                  lambda x,y: x[0]>=y[0], (2,6)
                                  ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)]

  print __heap_sort_external_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)]
                                  ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print __heap_sort_external_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                                  lambda x,y: x[0]>=y[0]
                                  ) == [(10, 5), (9, 10), (8, 9), (8, 3), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)],
  print __heap_sort_external_heap([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                                  lambda x,y: x[0]>=y[0], (2,6)
                                  ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)]

  print heap_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], lambda x,y: x[0]>=y[0], (2,6)
                  ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)],

  print radix_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                   (((lambda x: x[0]), (lambda x,y: x>=y)),
                    ((lambda x: x[1]), (lambda x,y: x<=y))), 
                   (3, 11)) == [(6, 0), (1, 1), (2, 2), (10, 5), (9, 10), (8, 3), (8, 9), (7, 8), (5, 7), (4, 6), (3, 4), (3, 11)]

  print 'count_sort: ',
  print count_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                   lambda x,y: x[0]>=y[0], 
                   (0, 11)
                   ) == [(10, 5), (9, 10), (8, 3), (8, 9), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)],
  print count_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)],
                   lambda x,y: x[0]<=y[0], 
                   (0, 11)
                   ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print count_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                   lambda x,y: x[0]>=y[0], 
                   (2,6)
                   ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)]

  print 'exchange_sort:',
  print exchange_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                      lambda x,y: x[0]>=y[0], 
                      (0, 11)
                      ) == [(10, 5), (9, 10), (8, 3), (8, 9), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)],
  print exchange_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)],
                      lambda x,y: x[0]<=y[0], 
                      (0, 11)
                      ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print exchange_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                      lambda x,y: x[0]>=y[0], 
                      (2,6)
                      ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)]

  print 'shaker_sort:',
  print shaker_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                      lambda x,y: x[0]>=y[0], 
                      (0, 11)
                      ) == [(10, 5), (9, 10), (8, 9), (8, 3), (7, 8), (6, 0), (5, 7), (4, 6), (3, 4), (3, 11), (2, 2), (1, 1)],
  print shaker_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)],
                      lambda x,y: x[0]<=y[0], 
                      (0, 11)
                      ) == [(1, 1), (2, 2), (3, 4), (3, 11), (4, 6), (5, 7), (6, 0), (7, 8), (8, 3), (8, 9), (9, 10), (10, 5)],
  print shaker_sort([(6, 0),(1, 1),(2, 2),(8, 3),(3, 4),(10, 5),(4, 6),(5, 7),(7, 8),(8, 9),(9, 10), (3, 11)], 
                      lambda x,y: x[0]>=y[0], 
                      (2,6)
                      ) == [(6, 0), (1, 1), (10, 5), (8, 3), (4, 6), (3, 4), (2, 2), (5, 7), (7, 8), (8, 9), (9, 10), (3, 11)]
  
  
  
  
  
  
