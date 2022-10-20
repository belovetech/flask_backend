import json

x = json.loads("False".lower())
y = json.loads("True".lower())
print(x, type(x))
print(y, type(y))
print(json.loads("false"))
