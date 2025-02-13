import pickle

with open('data/saves/salut.clab', 'rb') as f:
    data = pickle.load(f)

print(data)