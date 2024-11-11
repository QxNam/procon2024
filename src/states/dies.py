import numpy as np

loaded_data = np.load('pattents.npz')

def choose(id:int=1):
    return loaded_data['arr_{}'.format(id)]

if __name__ == '__main__':
    print(choose(4))