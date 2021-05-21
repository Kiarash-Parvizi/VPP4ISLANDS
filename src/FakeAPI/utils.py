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
            'DA_PRICE': item[2],
            'RT_PRICE': item[3],
            'TIME': time
        },
        'status': 200
    }

def read_fixed_load_data(time):
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

def read_flexibe_load_data(time):
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

def read_node_flexible_load(node_id: int, time: int) -> dict:
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