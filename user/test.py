import os

cwd = os.path.dirname(os.path.abspath(__file__))
print(cwd)
print(os.path.abspath(os.path.join(cwd, os.pardir)))
