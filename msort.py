#! usr/bin/python
from shift import *

def merge_recursive (list_1, list_2=[], key_function=(lambda x: x), order=(lambda x,y: x <= y)):
  mlist = list_1 + list_2
  length = len(mlist)
  
  if length <= 1:
    return mlist

  mlist[0:(length/2)] = merge_recursive(mlist[0:(length/2)], key_function=key_function, order=order)
  mlist[(length/2):] = merge_recursive(mlist[(length/2):], key_function=key_function, order=order)
  mlist = sorted_merge(mlist[0:(length/2)], mlist[(length/2):], key_function=key_function, order=order)
  return mlist

def merge_iterative (list_1, list_2=[], key_function=(lambda x: x), order=(lambda x,y: x <= y)):
  mlist = list_1 + list_2
  block_length = 1
  
  while block_length < len(mlist):
    __merge_pass(mlist, block_length, key_function, order)
    block_length *= 2

  return mlist

def __merge_pass (list_, block_length, key_function, order):
  i = 0;
  while (i + 2) * block_length < len(list_):
    list_[i*block_length:(i+2)*block_length] = sorted_merge(list_[i*block_length:(i+1)*block_length], list_[(i+1)*block_length:(i+2)*block_length], key_function, order)
    i += 2
  if (i + 1) * block_length < len(list_):
    list_[i*block_length:] = sorted_merge(list_[i*block_length:(i+1)*block_length], list_[(i+1)*block_length:], key_function, order)


def sorted_merge (slist_1, slist_2=[], key_function=(lambda x: x), order=(lambda x,y: x <= y)):
  mlist = []
  
  index_1 = 0
  length_1 = len(slist_1)
  index_2 = 0
  length_2 = len(slist_2)
  
  while index_1 < length_1 and index_2 < length_2:
    if order(key_function(slist_1[index_1]), key_function(slist_2[index_2])):
      mlist.append(slist_1[index_1])
      index_1 += 1
    else:
      mlist.append(slist_2[index_2])
      index_2 += 1
  
  if index_1 >= length_1:
    mlist.extend(slist_2[index_2:])
  else:
    mlist.extend(slist_1[index_1:])
  
  return mlist

def msort_shift (slist_1, slist_2, key_function=(lambda x: x), order=(lambda x,y: x <= y)):
  mlist = slist_1 + slist_2
  i = 0
  end_1 = len(slist_1) - 1
  j = end_1 + 1
  length_2 = len(mlist)
  while True:
    q = 0
    #while j + q < length_2 and mlist[j + q] <= mlist[i]:
    while j + q < length_2 and order(key_function(mlist[j + q]), key_function(mlist[i])) == True:
      q += 1
    if q > 0:
      circular_shift(mlist, q, (i, j+q-1))
    i += q + 1
    end_1 += q
    j += q
    if i > end_1 or j >= length_2:
      break

  return mlist

if __name__ == '__main__':
  print sorted_merge([0, 4], [1, 3, 5, 7, 9]
                     ) == msort_shift([0, 4], [1, 3, 5, 7, 9]),
  print sorted_merge([4, 0], [9, 7, 5, 3, 1], order=(lambda x,y: x >= y)
                     ) == msort_shift([4, 0], [9, 7, 5, 3, 1], order=(lambda x,y: x >= y)),
  
  print merge_iterative([4, 0], [1, 9, 5, 7, 3]
                        ) == msort_shift([0, 4], [1, 3, 5, 7, 9]),
  print merge_iterative([4, 0], [1, 9, 5, 7, 3], order=(lambda x,y: x >= y)
                        ) == msort_shift([4, 0], [9, 7, 5, 3, 1], order=(lambda x,y: x >= y)),
  print merge_iterative([4, 0, 1, 9, 5, 7, 3]
                        ) == msort_shift([0, 4], [1, 3, 5, 7, 9]),
  print merge_iterative([4, 0, 5, 1, 9, 7, 3], order=(lambda x,y: x >= y)
                        ) == msort_shift([4, 0], [9, 7, 5, 3, 1], order=(lambda x,y: x >= y)),
 
  print merge_recursive([4, 0, 5, 1, 9, 7, 3], order=(lambda x,y: x >= y)
                        ) == msort_shift([4, 0], [9, 7, 5, 3, 1], order=(lambda x,y: x >= y)),
  print merge_recursive([4, 0], [1, 9, 5, 7, 3]
                        ) == msort_shift([0, 4], [1, 3, 5, 7, 9]),


