import pandas as pd


def read_dg_data():
    """reads data/DG_source.csv

    Returns:
        [dict]: {
            'data': [
                {
                    key value informations of the data/DG_source.csv file.
                }
            ]
            'status': 200
        }
    """
    df = pd.read_csv('data/DG_source.csv')
    
    cols = df.columns

    data = []

    for index, row in df.iterrows():
        _dic = {}
        for col in cols:
            if (col == "DG No.") or (col == "Node_id"):
                _dic[col] = int(row[col])
            else:
                _dic[col] = float(row[col])

        data.append(_dic)

    return {
        'data': data,
        'status': 200
    }

def read_es_data():
    """reads data/ES_source.csv

    Returns:
        [dict]: {
            'data': [
                {
                    key value informations of the data/ES_source.csv file.
                }
            ]
            'status': 200
        }
    """
    df = pd.read_csv('data/ES_source.csv')
    
    cols = df.columns

    data = []

    for index, row in df.iterrows():
        _dic = {}
        for col in cols:
            if (col == "ES No.") or (col == "Node_id"):
                _dic[col] = int(row[col])
            else:
                _dic[col] = float(row[col])

        data.append(_dic)
    
    return {
        'data': data,
        'status': 200
    }

def read_fl_data():
    """reads data/FL_source.csv

    Returns:
        [dict]: {
            'data': [
                {
                    key value informations of the data/FL_source.csv file.
                }
            ]
            'status': 200
        }
    """
    df = pd.read_csv('data/FL_source.csv')
    
    cols = df.columns

    data = []

    for index, row in df.iterrows():
        _dic = {}
        for col in cols:
            if (col == "FL No.") or (col == "Node_id"):
                _dic[col] = int(row[col])
            else:
                _dic[col] = float(row[col])

        data.append(_dic)
    
    return {
        'data': data,
        'status': 200
    }

def read_pv_data():
    """reads data/PV_source.csv

    Returns:
        [dict]: {
            'data': [
                {
                    key value informations of the data/PV_source.csv file.
                }
            ]
            'status': 200
        }
    """
    df = pd.read_csv('data/PV_source.csv')
    
    cols = df.columns

    data = []

    for index, row in df.iterrows():
        _dic = {}
        for col in cols:
            if (col == "PV No.") or (col == "Node_id"):
                _dic[col] = int(row[col])
            else:
                _dic[col] = float(row[col])

        data.append(_dic)
    
    return {
        'data': data,
        'status': 200
    }

def read_wf_data():
    """reads data/WF_source.csv

    Returns:
        [dict]: {
            'data': [
                {
                    key value informations of the data/WF_source.csv file.
                }
            ]
            'status': 200
        }
    """
    df = pd.read_csv('data/WF_source.csv')
    
    cols = df.columns

    data = []

    for index, row in df.iterrows():
        _dic = {}
        for col in cols:
            if (col == "WF No.") or (col == "Node_id"):
                _dic[col] = int(row[col])
            else:
                _dic[col] = float(row[col])

        data.append(_dic)
    
    return {
        'data': data,
        'status': 200
    }

def read_node_data(node_id: int) -> dict:
    """reads node's resources data based on given node id

    Args:
        node_id (int): node id

    Returns:
        dict: {
            'data' :[
                {
                    'node_id': for instance 5,
                    'type': for instance ES,
                    and ES parameters with keys of corresponding CSV files.
                },
                ...
            ],
            'status': 200
        }
    """
    data = []

    wf_dict: dict = read_wf_data()
    pv_dict: dict = read_pv_data()
    fl_dict: dict = read_fl_data()
    es_dict: dict = read_es_data()
    dg_dict: dict = read_dg_data()

    find_node_data(node_id, "WF", wf_dict, data)
    find_node_data(node_id, "PV", pv_dict, data)
    find_node_data(node_id, "FL", fl_dict, data)
    find_node_data(node_id, "ES", es_dict, data)
    find_node_data(node_id, "DG", dg_dict, data)

    return {
        'data': data,
        'status': 200
    }

def find_node_data(node_id: int, _type: str, data_dict: dict, res_data: list):
    """finds all the resource informations of the given node_id from the data_dict  
    and adds them to the res_data list with extra key called _type, which is equal
    to the _type varable

    Args:
        node_id (int): node id
        _type (str): name of the type, like DG, ES, PV, ...
        data_dict (dict): dictionary format of the data
        res_data (list): result list
    """
    data = data_dict['data']
    for item in data:
        if item['Node_id'] == node_id:
            item['type'] = _type
            res_data.append(item)

def read_nodes_structure():
    """reads the node_structure.csv file which represents the connections of the
    VppBoxNodes.

    Returns:
        [dict]: {
            'data': [
                {
                    nodes: Tuple of start and end node,
                    line: {
                        r:, x, i_max, i_max_pu
                    }
                }
            ]
        }
    """
    df = pd.read_csv('data/nodes_structure.csv')
    
    data = []

    for index, row in df.iterrows():
        data.append(
            {
                'nodes': (int(row['node_a']), int(row['node_b'])),
                'line': {'r': row['r'], 'x': row['x'], 'i_max': row['i_max'], 'i_max_pu': row['i_max_pu']}
            }
        )
    
    return {
        'data': data
    }