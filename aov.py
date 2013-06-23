#! usr/bin/python

from graph import Digraph

class AovNetwork (Digraph):
  def __init__ (self):
    super(AovNetwork, self).__init__()
    self.__candidates = []
    self.__activities = {}
  
  def add_activity (self, activity, predecessors):
    v = self.__get_activity(activity)
    v_data = v.get_data()
    
    # If has no predecessor
    if predecessors == None or len(predecessors) == 0:
      v_data.update({'predecessor number': 0})
      #self.__candidates.append(v)

    # Has one or more predecessors
    else:
      v_data.update({'predecessor number': len(predecessors)})
      for pred in predecessors:
        v_pred = self.__get_activity(pred)
        self.add_edge(v_pred, v)

  def generate_topological_order (self):
    if self.__check_feasibility() == False:
      self.__print('Not feasible!')
      return None
    
    self.__initialize()
    
    # Put activities having no predecessor into the candidate list
    for act in filter(lambda x: x.get_data()['predecessor check count'] == 0, self.vertice):
      self.__put_candidate(act)

    result = []
    while len(self.__candidates) > 0:
      v = self.__get_candidate()
      v_data = v.get_data()
      result.append(v_data['name'])
      for suc in v.get_adjacent():
        suc_data = suc.get_data()
        suc_data['predecessor check count'] -= 1
        if suc_data['predecessor check count'] == 0:
          self.__put_candidate(suc)
        elif suc_data['predecessor check count'] < 0:
          self.__print_error('Something wrong with activity %s' % (suc_data['name']))
          exit
    return result

  def __get_candidate (self):
    return self.__candidates.pop(0)

  def __put_candidate (self, candidate):
    self.__candidates.append(candidate)
    #self.__candidates.insert(0, candidate)

  def __initialize (self):
    for act in self.vertice:
      act_data = act.get_data()
      act_data.update({'predecessor check count': act_data['predecessor number']})

  def __get_activity (self, activity):
    try:
      return self.__activities[activity]
    except KeyError:
      v = self.add_vertex({'name': activity})
      self.__activities.update({activity: v})
      return v

  def __print (self, info):
    print info

  def __print_error (self, info):
    print info
    
  def __check_feasibility (self):
    return True


if __name__ == '__main__':
  aov = AovNetwork()
  aov.add_activity('C1', None)
  aov.add_activity('C2', None)
  aov.add_activity('C4', None)
  aov.add_activity('C3', ['C1', 'C2'])
  aov.add_activity('C5', ['C4'])
  aov.add_activity('C6', ['C5'])
  aov.add_activity('C7', ['C3', 'C6'])
  aov.add_activity('C8', ['C3'])
  aov.add_activity('C9', ['C7', 'C8'])
  aov.add_activity('C10', ['C7'])
  aov.add_activity('C11', ['C10'])
  aov.add_activity('C12', ['C7'])
  aov.add_activity('C13', ['C7'])
  aov.add_activity('C14', ['C13'])
  aov.add_activity('C15', ['C6'])

  print aov.vertice
  """
  [{'data': {'predecessor number': 0, 'name': 'C1'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C3'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7d90>), ({'data': {'predecessor number': 1, 'name': 'C8'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e90>)]}, <graph.GraphEdge object at 0x1053b7e10>)]}, <graph.GraphEdge object at 0x1053b7c90>)]}, 
   {'data': {'predecessor number': 0, 'name': 'C2'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C3'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7d90>), ({'data': {'predecessor number': 1, 'name': 'C8'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e90>)]}, <graph.GraphEdge object at 0x1053b7e10>)]}, <graph.GraphEdge object at 0x1053b7cd0>)]}, 
   {'data': {'predecessor number': 0, 'name': 'C4'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C5'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C6'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7dd0>), ({'data': {'predecessor number': 1, 'name': 'C15'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053c1050>)]}, <graph.GraphEdge object at 0x1053b7d50>)]}, <graph.GraphEdge object at 0x1053b7d10>)]}, 
   {'data': {'predecessor number': 2, 'name': 'C3'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7d90>), ({'data': {'predecessor number': 1, 'name': 'C8'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e90>)]}, <graph.GraphEdge object at 0x1053b7e10>)]}, 
   {'data': {'predecessor number': 1, 'name': 'C5'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C6'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7dd0>), ({'data': {'predecessor number': 1, 'name': 'C15'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053c1050>)]}, <graph.GraphEdge object at 0x1053b7d50>)]}, 
   {'data': {'predecessor number': 1, 'name': 'C6'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, <graph.GraphEdge object at 0x1053b7dd0>), ({'data': {'predecessor number': 1, 'name': 'C15'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053c1050>)]}, 
   {'data': {'predecessor number': 2, 'name': 'C7'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e50>), ({'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, <graph.GraphEdge object at 0x1053b7ed0>), ({'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f50>), ({'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, <graph.GraphEdge object at 0x1053b7f90>)]}, 
   {'data': {'predecessor number': 1, 'name': 'C8'}, 'adjacent': [({'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7e90>)]}, 
   {'data': {'predecessor number': 2, 'name': 'C9'}, 'adjacent': []}, 
   {'data': {'predecessor number': 1, 'name': 'C10'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7f10>)]}, 
   {'data': {'predecessor number': 1, 'name': 'C11'}, 'adjacent': []}, 
   {'data': {'predecessor number': 1, 'name': 'C12'}, 'adjacent': []}, 
   {'data': {'predecessor number': 1, 'name': 'C13'}, 'adjacent': [({'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, <graph.GraphEdge object at 0x1053b7fd0>)]}, 
   {'data': {'predecessor number': 1, 'name': 'C14'}, 'adjacent': []}, 
   {'data': {'predecessor number': 1, 'name': 'C15'}, 'adjacent': []}]
  """
  print aov.generate_topological_order()
  print aov.generate_topological_order() == ['C1', 'C2', 'C4', 'C3', 'C5', 'C8', 'C6', 'C7', 'C15', 'C9', 'C10', 'C12', 'C13', 'C11', 'C14']

