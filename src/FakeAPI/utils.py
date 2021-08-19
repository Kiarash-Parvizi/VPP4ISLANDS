from random import uniform 
import pandas as pd


def read_dg_data():
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
    data = data_dict['data']
    for item in data:
        if item['Node_id'] == node_id:
            item['type'] = _type
            res_data.append(item)

def read_nodes_structure():
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