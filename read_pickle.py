import pickle

with open('data/saves/nieuwbef.clab', 'rb') as f:
    data = pickle.load(f)

print(data)