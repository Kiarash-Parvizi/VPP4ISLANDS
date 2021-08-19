from ..VPP.test_15bus import * 
from src.FakeAPI.utils import read_wf_data
from src.Forecaster.utils import read_uncertainty_params



def test_WF():

    print(f"....TEST test_WF is started...")


    data = read_wf_data()['data']

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a WF
            if node.wf_resources.getItems():
                
                # checking the node_id
                res_from_file = None
                found = False
                for dt in data:
                    if dt['Node_id'] == node_id:
                        found = True
                        res_from_file = dt
                        break
                if not found:
                    assert "Wrong WF node_id"

                print(f"OK: Right node_id {node_id}")
                
                for wf_key, wf in node.wf_resources.getItems():
                    
                    # testing the get method
                    p_wind = wf.get('P_Wind')
                    for w in range(1, wf.NW + 1):
                        for time in range(1, wf.NT + 1):
                            pred_val = p_wind[w][time]
                            ac_val  =  read_uncertainty_params(time)['data']['WF'] * wf.p_max / wf.sbase
                            assert pred_val == ac_val, \
                                f"uncertainty_params is not matched with get(P_Wind) at time of {time} => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_Wind)")


if __name__ == "__main__":
    test_WF()