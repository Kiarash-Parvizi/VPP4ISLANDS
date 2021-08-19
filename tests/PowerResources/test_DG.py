from ..VPP.test_15bus import * 
from src.FakeAPI.utils import read_dg_data


def test_DG():
    
    print(f"....TEST test_DG is started...")
    
    data = read_dg_data()['data']

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a DG
            if node.dg_resources.getItems():
                
                # checking the node_id
                res_from_file = None
                found = False
                for dt in data:
                    if dt['Node_id'] == node_id:
                        found = True
                        res_from_file = dt
                        break
                if not found:
                    assert "Wrong DG node_id"
                
                print(f"OK: Right node_id {node_id}")
            
                for resource_key, resource in node.dg_resources.getItems():
                    
                    # testing the get methods

                    # SUC_DG                
                    pred_val = resource.get('SUC_DG')
                    ac_val = res_from_file['SUC']
                    assert pred_val == ac_val, \
                                f"SUC_DG is not matched with get(SUC_DG) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(SUC_DG)")


                    # SDC_DG    
                    pred_val = resource.get('SDC_DG')
                    ac_val = res_from_file['SDC']
                    assert pred_val == ac_val, \
                                f"SDC_DG is not matched with get(SDC_DG) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(SDC_DG)")


                    # C_DG
                    pred_val = resource.get('C_DG')
                    ac_val = res_from_file['Cost']
                    assert pred_val == ac_val, \
                                f"C_DG is not matched with get(C_DG) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(C_DG)")


                    # P_DG_min
                    pred_val = resource.get('P_DG_min')
                    ac_val = res_from_file['P_min']
                    assert pred_val == ac_val, \
                                f"P_DG_min is not matched with get(P_DG_min) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_DG_min)")


                    # P_DG_max
                    pred_val = resource.get('P_DG_max')
                    ac_val = res_from_file['P_max']
                    assert pred_val == ac_val, \
                                f"P_DG_max is not matched with get(P_DG_max) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_DG_max)")


                    # Q_DG_min
                    pred_val = resource.get('Q_DG_min')
                    ac_val = res_from_file['Q_min']
                    assert pred_val == ac_val, \
                                f"Q_DG_min is not matched with get(Q_DG_min) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(Q_DG_min)")


                    # Q_DG_max
                    pred_val = resource.get('Q_DG_max')
                    ac_val = res_from_file['Q_max']
                    assert pred_val == ac_val, \
                                f"Q_DG_max is not matched with get(Q_DG_max) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(Q_DG_max)")


                    # RU_DG
                    pred_val = resource.get('RU_DG')
                    ac_val = res_from_file['Rup']
                    assert pred_val == ac_val, \
                                f"RU_DG is not matched with get(RU_DG) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(RU_DG)")


                    # RD_DG
                    pred_val = resource.get('RD_DG')
                    ac_val = res_from_file['Rdn']
                    assert pred_val == ac_val, \
                                f"RD_DG is not matched with get(RD_DG) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(RD_DG)")


                    # MUT
                    pred_val = resource.get('MUT')
                    ac_val = res_from_file['MUT']
                    assert pred_val == ac_val, \
                                f"MUT is not matched with get(MUT) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(MUT)")


                    # MDT
                    pred_val = resource.get('MDT')
                    ac_val = res_from_file['MDT']
                    assert pred_val == ac_val, \
                                f"MDT is not matched with get(MDT) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(MDT)")


if __name__ == "__main__":
    test_DG()