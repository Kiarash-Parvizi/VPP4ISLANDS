from ..VPP.test_15bus import * 
from src.Forecaster.utils import read_node_fixed_load


def test_FixedLoad():

    print(f"....TEST test_FixedLoad is started...")

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode) and (not node.trade_compatible):
            
            # if that node has a fixed_loads
            if node.load_collection.fixed_loads.getItems():
                

                print(f"OK: Right node_id {node_id}")
                
                for fixload_key, fixload in node.load_collection.fixed_loads.getItems():
                    
                    # testing the get method

                    # P_L
                    for time in range(1, fixload.NT + 1):

                        pred_val = fixload.get('P_L')[time]
                        ac_val  =  1000 * read_node_fixed_load(node.node_id, time)['data']['load'] / fixload.sbase
                        assert pred_val == ac_val, \
                            f"uncertainty_params is not matched with get(P_L) at time of {time} => " + \
                                f"{pred_val} != {ac_val}"

                    print("OK: Right get(P_L)")


                    # Q_L
                    for time in range(1, fixload.NT + 1):
                        pred_val = fixload.get('Q_L')[time]
                        ac_val  = 1000 * read_node_fixed_load(node.node_id, time)['data']['load'] * fixload.pf / fixload.sbase
                        assert pred_val == ac_val, \
                            f"uncertainty_params is not matched with get(Q_L) at time of {time} => " + \
                                f"{pred_val} != {ac_val}"

                    print("OK: Right get(Q_L)")


if __name__ == "__main__":
    test_FixedLoad()