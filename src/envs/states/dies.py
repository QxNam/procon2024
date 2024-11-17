import numpy as np

loaded_data = np.load('./pattents.npz')

def choose(id:int=1):
    return loaded_data['arr_{}'.format(id)]

def get_dies():
    return [choose(i) for i in range(24)]

if __name__ == '__main__':
    for i, die in enumerate(get_dies()):
        print(f"Die {i}: \n{die}")