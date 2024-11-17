import numpy as np

def create_die(n:int, type='I') -> np.ndarray:
    '''
    Create a die with (n x n) cells

    Args:
        n (int): Number of cells in the die
        type (str): Type of the die (I, II, III)

    Returns:
        list: A list of strings representing the die cells, where each cell is represented by a string of '0's and '1's
    '''
    die = np.ones((n, n), dtype=np.int8)
    if type == 'II':
        die[1::2] = 0
    elif type == 'III':
        die[:,1::2] = 0
    return die

def create() -> dict:
    '''
    Create a dictionary containing the cell data and save it as a JSON file
    
    Returns:
        dict_cell: A dictionary containing the cell data
    '''
    dies = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    res = []
    for d in dies:
        for type in ['I', 'II', 'III']:
            res.append(create_die(d, type))
    
    return res

data = create()[2:]

output_file_path = "pattents.npz"
np.savez(output_file_path, *data)
print('✅ Save successfully!')

# Tải dữ liệu từ file .npz
loaded_data = np.load('pattents.npz')
print('Lenght: ', len(loaded_data))
print('die 4: \n', loaded_data['arr_4'])
