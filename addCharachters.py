from fastapi import HTTPException

class Character:
  labels: list[str] = ['Died','Dead','Male','Blonde','Fight','Wall','Child','Murder','Wild','King','Love','Honor']
  values: list[int] = []
  name: str = None

  def __init__ (self, name: str):
    self.name = name
  
  def addValues(self, values: list[int]):
    if len(values) != len(self.labels):
      raise HTTPException(status_code=400, detail='O número de argumentos dados não condiz com a quantidade de campos, use 0 para simbolizar não sei')
    self.values = values
  
  def returnLabels(self):
    return self.labels
  
  def buildCsvLine(self, key):
    arr = [str(x) for x in [key, self.name, *self.values]]
    return ','.join(arr) + "\n"


class AddCharachters:
  dataBase = 'base.csv'
  character: Character = None
  nextKey: int = None
  
  def addCharacter(self, char: Character):
    self.character = char
    return self.character

  def commitChanges(self):
    if not self.nextKey:
      with open(self.dataBase, 'r') as file:
        last_line = file.readlines()[-1]
        self.nextKey = int(last_line.split(',')[0])
        self.nextKey += 1
    
    with open(self.dataBase, 'a') as file:
      file.write(self.character.buildCsvLine(self.nextKey))
      self.nextKey += 1

    return True
