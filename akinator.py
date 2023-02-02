def chooseLabel(df, labels):
  mins = [min(df[l].value_counts()) for l in labels]
  return labels[mins.index(max(mins))]

def genBinaryTree(df, labels):
  if len(df) == 1:
    return df['Name'].tolist()[0]
  if len(labels) == 1:
    return df["Name"].tolist()
  if len(df) == 0 or len(labels) == 0:
    return None

  label = chooseLabel(df, labels)
  newLabels = [l for l in labels if l!= label]

  return {
    "label": label,
    -1: genBinaryTree(df[df[label] != 1], newLabels),
    1: genBinaryTree(df[df[label] != -1], newLabels),
  }

class Akinator:
  df = None
  tree = {}
  executions = {}
  lastId = 0

  def __init__(self, dataFrame):
    self.df = dataFrame

  def genId(self):
    id = self.lastId
    self.lastId += 1
    return id
    
  def createExecution(self):
    id = self.genId()
    self.executions[id] = [self.tree]
    return id

  def genTreeFromDf(self):
    self.tree = self.genTree(self.df, self.df.columns.tolist()[2:])
    
  def genTree(self, df, labels):
    if len(df) == 1:
      return df['Name'].tolist()[0]
    if len(labels) == 1:
      return df["Name"].tolist()
    if len(df) == 0 or len(labels) == 0:
      return None

    label = chooseLabel(df, labels)
    newLabels = [l for l in labels if l!= label]

    return {
      "label": label,
      -1: genBinaryTree(df[df[label] != 1], newLabels),
      1: genBinaryTree(df[df[label] != -1], newLabels),
    }
  
  def addCharacter(character):
    # A implementar
    pass
  
  def getQuestion(self, id):
    return self.executions[id][-1]['label']

  def execute(self, id, inp):
    if self.executions[id] == []:
      return None
    tree = self.executions[id].pop()

    def evaluate(inp):
      if type(tree[inp]) == str or type(tree[inp]) == list:
        return tree[inp]
      else: 
        self.executions[id].append(tree[inp])
        return None

    if inp != 0:
       return evaluate(inp)        
    else:
      result = evaluate(-1)
      if result!= None:
        return result
      return evaluate(1)