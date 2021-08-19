from ..VPP.test_15bus import * 
from src.FakeAPI.utils import read_es_data


def test_ES():

    print(f"....TEST test_ES is started...")

    data = read_es_data()['data']

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a ES
            if node.es_resources.getItems():
                
                # checking the node_id
                res_from_file = None
                found = False
                for dt in data:
                    if dt['Node_id'] == node_id:
                        found = True
                        res_from_file = dt
                        break
                if not found:
                    assert "Wrong ES node_id"
                
                print(f"OK: Right node_id {node_id}")
            
                for resource_key, resource in node.es_resources.getItems():
                    
                    # testing the get methods

                    # P_ChES_max                
                    pred_val = resource.get('P_ChES_max')
                    ac_val = res_from_file['P_charge']
                    assert pred_val == ac_val, \
                                f"P_ChEs_max is not matched with get(P_ChES_max) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_ChES_max)")


                    # P_DchES_max    
                    pred_val = resource.get('P_DchES_max')
                    ac_val = res_from_file['P_discharge']
                    assert pred_val == ac_val, \
                                f"P_DchES_max is not matched with get(P_DchES_max) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_DchES_max)")


                    # eta_ChES
                    pred_val = resource.get('eta_ChES')
                    ac_val = res_from_file['Efficiency'] / 100.
                    assert pred_val == ac_val, \
                                f"eta_ChES is not matched with get(eta_ChES) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(eta_ChES)")


                    # eta_DchES
                    pred_val = resource.get('eta_DchES')
                    ac_val = res_from_file['Efficiency'] / 100.
                    assert pred_val == ac_val, \
                                f"eta_DchES is not matched with get(eta_DchES) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(eta_DchES)")


                    # SOE_ES_min
                    pred_val = resource.get('SOE_ES_min')
                    ac_val = res_from_file['SOE_min'] * res_from_file['Energy Capacity'] / 100.
                    assert pred_val == ac_val, \
                                f"SOE_ES_min is not matched with get(SOE_ES_min) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(SOE_ES_min)")


                    # SOE_ES_max
                    pred_val = resource.get('SOE_ES_max')
                    ac_val = res_from_file['SOE_max'] * res_from_file['Energy Capacity'] / 100.
                    assert pred_val == ac_val, \
                                f"SOE_ES_max is not matched with get(SOE_ES_max) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(SOE_ES_max)")

                    # SOE_ES_init
                    pred_val = resource.get('SOE_ES_init')
                    ac_val = res_from_file['SOE_initial'] * res_from_file['Energy Capacity'] / 100.
                    assert pred_val == ac_val, \
                                f"SOE_ES_init is not matched with get(SOE_ES_init) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(SOE_ES_init)")


                    # Energy_Capacity
                    pred_val = resource.get('Energy_Capacity')
                    ac_val = res_from_file['Energy Capacity']
                    assert pred_val == ac_val, \
                                f"Energy_Capacity is not matched with get(Energy_Capacity) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(Energy_Capacity)")


if __name__ == "__main__":
    test_ES()