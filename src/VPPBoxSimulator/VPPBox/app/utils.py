from os import EX_CANTCREAT
from random import uniform 
import pandas as pd

def create_random_loads(number_of_nodes):
    data = []
    for i in range(number_of_nodes):
        data.append(
            {
                'node_id': i,
                'load': uniform(20.5, 40.5)
            }
        )

    return {
        'data': data
    }

def create_line_data():
    data = [
        {
            'node_a': 1,
            'node_b': 2,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 2,
            'node_b': 3,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 2,
            'node_b': 6,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 2,
            'node_b': 9,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 3,
            'node_b': 4,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 3,
            'node_b': 11,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 4,
            'node_b': 5,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 4,
            'node_b': 14,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 4,
            'node_b': 15,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 6,
            'node_b': 7,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 6,
            'node_b': 8,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 9,
            'node_b': 10,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 11,
            'node_b': 12,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
        {
            'node_a': 12,
            'node_b': 13,
            'r': uniform(0, 3),
            'x': uniform(0, 2),
            'i_max': uniform(100, 300),
            'i_max_pu': uniform(1, 3)
        },
    ]

    return {
        'data': data
    }

def read_uncertainty_params(time):
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
            'DG': item[2],
            'DA_PRICE': item[3],
            'RT_PRICE': item[4],
            'TIME': time
        },
        'status': 200
    }

def read_load_data(time):
    df = pd.read_csv('data/loads.csv')

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

    print(data)

    return {
        'data': data,
        'status': 200
    }

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