import re

class LStatement:

  def __init__(self, args):
    self.args = args

  def execute(self):
    pass

variables = {}

def getValue(input):
  if input in list(variables.keys()):
    return variables[input]
  if isinstance(input, list):
    return input
  if isinstance(input, LStatement):
    return input.execute()
  if input[0] == '"':
    return input[1:len(input)-1].replace("\\s", " ")
  if input == "true":
    return True
  if input == "false":
    return False
  return float(input)

class LAssignVariable(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    variables[self.args[0]] = getValue(self.args[1])

class LFunction(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return self

class LReturn(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0])

class LExecute(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    func = getValue(self.args[0])
    for statement in func.args:
      if isinstance(statement, LReturn):
        return statement.execute()
      statement.execute()

class LAddition(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    sum = 0
    for arg in self.args:
      sum += getValue(arg)
    return sum

class LSubtraction(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    subtracted = getValue(self.args[0])
    for arg in self.args[1:]:
      subtracted -= getValue(arg)
    return subtracted

class LMultiplication(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    multiplied = 1
    for arg in self.args:
      multiplied *= getValue(arg)
    return multiplied

class LDivision(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    divided = getValue(self.args[0])
    for arg in self.args[1:]:
      divided /= getValue(arg)
    return divided

class LArray(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    array = []
    for arg in self.args:
      array.append(getValue(arg))
    return array

class LIndex(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0])[int(getValue(self.args[1]))]

class LLength(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return len(getValue(self.args[0]))

class LAppend(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    newArray = getValue(self.args[0])
    newArray.append(getValue(self.args[1]))
    return newArray

class LDelete(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    newArray = getValue(self.args[0])
    del newArray[int(getValue(self.args[1]))]
    return newArray

class LGreaterThan(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0]) > getValue(self.args[1])

class LLessThan(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0]) < getValue(self.args[1])

class LEquals(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0]) == getValue(self.args[1])

class LAnd(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0]) and getValue(self.args[1])

class LOr(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return getValue(self.args[0]) or getValue(self.args[1])

class LNot(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return not getValue(self.args[0])

class LIf(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    if getValue(self.args[0]):
      self.args[1].execute()

class LIfElse(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    if getValue(self.args[0]):
      self.args[1].execute()
    else:
      self.args[2].execute()

class LWhileLoop(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    while getValue(self.args[0]):
      self.args[1].execute()

class LToNumber(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return float(getValue(self.args[0]))

class LToString(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return str(getValue(self.args[0]))

class LConcatenate(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    s = ""
    for arg in self.args:
      s += getValue(arg)
    return s

class LPrint(LStatement):

  def __init__(self, args):
    super().__init__(args)

  def execute(self):
    print(getValue(self.args[0]), end="")


class LPrintLine(LStatement):

  def __init__(self, args):
    super().__init__(args)

  def execute(self):
    print(getValue(self.args[0]))

class LPrompt(LStatement):
  def __init__(self, args):
    super().__init__(args)
  def execute(self):
    return input(getValue(self.args[0]))

def parse(text):
  statementList = []
  currentItem = ""
  i = 0
  while i < len(text):
    if text[i] == "(":
      counter = 0
      ss = ""
      for j in range(i, len(text)):
        if text[j] == "(":
          counter += 1
        elif text[j] == ")":
          counter -= 1

        if counter == 0:
          ss = text[i + 1:j]
          i = j
          break

      currentItem = parse(ss)
      if i == len(text) - 1:
        statementList.append(currentItem)
    elif text[i] == " " or text[i] == ")" or i == len(text) - 1:
      if (not isinstance(currentItem, list)) and i == len(text) - 1:
        currentItem += text[i]
      statementList.append(currentItem)
      currentItem = ""
    else:
      currentItem += text[i]
    i += 1
  return statementList


def parseStatement(statementList):
  name = statementList[0]
  args = []
  for i in range(1, len(statementList)):
    if isinstance(statementList[i], list):
      args.append(parseStatement(statementList[i]))
    else:
      args.append(statementList[i])
  match name:
    case "print":
      return LPrint(args)
    case "println":
      return LPrintLine(args)
    case "prompt":
      return LPrompt(args)
    case "+":
      return LAddition(args)
    case "*":
      return LMultiplication(args)
    case "-":
      return LSubtraction(args)
    case "/":
      return LDivision(args)
    case "assign":
      return LAssignVariable(args)
    case "func":
      return LFunction(args)
    case "return":
      return LReturn(args)
    case "exec":
      return LExecute(args)
    case "array":
      return LArray(args)
    case "index":
      return LIndex(args)
    case "append":
      return LAppend(args)
    case "delete":
      return LDelete(args)
    case "len":
      return LLength(args)
    case ">":
      return LGreaterThan(args)
    case "<":
      return LLessThan(args)
    case "=":
      return LEquals(args)
    case "and":
      return LAnd(args)
    case "or":
      return LOr(args)
    case "not":
      return LNot(args)
    case "if":
      return LIf(args)
    case "if-else":
      return LIfElse(args)
    case "while":
      return LWhileLoop(args)
    case "to-num":
      return LToNumber(args)
    case "to-str":
      return LToString(args)
    case "concat":
      return LConcatenate(args)

filePath = input("file path: ")
text = None
with open(filePath, "r") as file:
  text = file.read()

text = re.sub("\s+", " ", text)
statementList = parse(text)
statements = []
for item in statementList:
  statements.append(parseStatement(item))
for statement in statements:
  statement.execute()
