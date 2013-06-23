#! usr/bin/python

def reverse (a_list, (from_, to)=(0, None)):
  if to == None:
    to = len(a_list) - 1

  assert(0 <= from_ <= to < len(a_list))
  
  while from_ < to:
    a_list[from_], a_list[to] = a_list[to], a_list[from_]
    from_ += 1
    to -= 1

def circular_shift (a_list, shift_number, (left,right)=(0,None)):
  assert(shift_number >= 0)
  if right == None:
    right = len(a_list) - 1
  assert(0 <= left <= right < len(a_list))
  
  length = right - left + 1
  shift_number %= length
  if shift_number > 0:
    reverse(a_list, (left, left+length-1))
    reverse(a_list, (left, left+shift_number-1))
    reverse(a_list, (left+shift_number, left+length-1))

if __name__ == '__main__':
  l = [0, 1, 2, 3]

  print l
  circular_shift(l, 1, (1, 3))
  print l

