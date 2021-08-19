from ..VPP.test_15bus import * 
from src.FakeAPI.utils import read_pv_data
from src.Forecaster.utils import read_uncertainty_params


def test_PV():


    print(f"....TEST test_PV is started...")


    data = read_pv_data()['data']

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a PV
            if node.pv_resources.getItems():
                
                # checking the node_id
                res_from_file = None
                found = False
                for dt in data:
                    if dt['Node_id'] == node_id:
                        found = True
                        res_from_file = dt
                        break
                if not found:
                    assert "Wrong PV node_id"
                
                print(f"OK: Right node_id {node_id}")
            
                for resource_key, resource in node.pv_resources.getItems():
                    
                    # testing the get method
                    p_pv = resource.get('P_PV')
                    for w in range(1, resource.NW + 1):
                        for time in range(1, resource.NT + 1):
                            pred_val = p_pv[w][time]
                            ac_val  =  read_uncertainty_params(time)['data']['PV'] * resource.p_max / resource.sbase
                            assert pred_val == ac_val, \
                                f"uncertainty_params is not matched with get(P_PV) at time of {time} => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_PV)")

if __name__ == "__main__":
    test_PV()