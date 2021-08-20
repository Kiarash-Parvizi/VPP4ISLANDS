from random import uniform 
import pandas as pd


def read_uncertainty_params(time: int) -> dict:
    """read data/uncertainty_parameters.csv file and return corresponding dict
    format of the file based on the given time.

    Args:
        time (int from 1 to 24): time

    Returns:
        dict: {
            'data': {
                'WF': WF value of that time,
                'PV': PV value of that time,
                'DA_PRICE': DA_PRICE value of that time,
                'RT_PRICE': RT_PRICE value of that time,
                'TIME': time
            },
            'status': 200 for ok
        }
    """
    df = pd.read_csv('data/uncertainty_parameters.csv')
    try:
        item = df["t" + str(time)]
    except:
        return {
            'data': {},
            'status': 404
        }
    return {
        'data' : {
            'WF': item[0],
            'PV': item[1],
            'DA_PRICE': item[2],
            'RT_PRICE': item[3],
            'TIME': time
        },
        'status': 200
    }

def read_fixed_load_data(time: int) -> dict:
    """reads data/fixed_loads.csv file and returns the corresponding dict format
    of that file based on the given time.

    Args:
        time (int from 1 to 24): time

    Returns:
        dict: {
            'data': [
                {
                    'node_id': node id of that fixed load
                    'load': fixed load value of that node at the time of 'time'
                }
            ]
            'status': 200 for ok
        }
    """
    df = pd.read_csv('data/fixed_loads.csv')

    try:
        item = df['t' + str(time)]
        node_ids = df['Node No.']
    except:
        return {
            'data': [],
            'status': 404
        }
    
    data = [{
        'node_id': int(node_ids[i]),
        'load': float(item[i])
    } for i in range(len(df))]


    return {
        'data': data,
        'status': 200
    }

def read_flexibe_load_data(time: int) -> dict:
    """reads data/flexible_loads.csv file and returns the corresponding dict format
    of that file based on the given time.

    Args:
        time (int from 1 to 24): time

    Returns:
        dict: {
            'data': [
                {
                    'node_id': node id of that flexible load
                    'load': flexible load value of that node at the time of 'time'
                }
            ]
            'status': 200 for ok
        }
    """
    df = pd.read_csv('data/flexible_loads.csv')

    try:
        item = df['t' + str(time)]
        node_ids = df['Node No.']
    except:
        return {
            'data': [],
            'status': 404
        }
    
    data = [{
        'node_id': int(node_ids[i]),
        'load': float(item[i])
    } for i in range(len(df))]


    return {
        'data': data,
        'status': 200
    }

def read_node_flexible_load(node_id: int, time: int) -> dict:
    """reads data/flexible_loads.csv file and returns the corresponding dict format
    of that file based on the given time and node_id.

    Args:
        time (int from 1 to 24): time

    Returns:
        dict: {
            'data': flexible load value
            'status': 200 for ok
        }
    """
    data = read_flexibe_load_data(time)['data']
    
    new_data = None
    
    for dt in data:
        if dt['node_id'] == node_id:
            new_data = dt
    
    if new_data == None:
        return {
            'data': {},
            'status': 404
        }
    
    return {
        'data': new_data,
        'status': 200
    }

def read_node_fixed_load(node_id: int, time: int) -> dict:
    """reads data/fixed_loads.csv file and returns the corresponding dict format
    of that file based on the given time and node_id.

    Args:
        time (int from 1 to 24): time

    Returns:
        dict: {
            'data': fixed load value
            'status': 200 for ok
        }
    """
    data = read_fixed_load_data(time)['data']
    
    new_data = None
    
    for dt in data:
        if dt['node_id'] == node_id:
            new_data = dt
    
    if new_data == None:
        return {
            'data': {},
            'status': 404
        }
    
    return {
        'data': new_data,
        'status': 200
    }