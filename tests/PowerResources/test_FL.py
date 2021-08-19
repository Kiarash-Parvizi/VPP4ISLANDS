from ..VPP.test_15bus import * 
from src.FakeAPI.utils import read_fl_data



def test_FL():


    print(f"....TEST test_FL is started...")


    data = read_fl_data()['data']

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a FL
            if node.load_collection.flex_loads.getItems():
                
                # checking the node_id
                res_from_file = None
                found = False
                for dt in data:
                    if dt['Node_id'] == node_id:
                        found = True
                        res_from_file = dt
                        break
                if not found:
                    assert "Wrong FL node_id"
                
                print(f"OK: Right node_id {node_id}")
            
                for resource_key, resource in node.load_collection.flex_loads.getItems():
                    
                    # testing the get methods

                    # INC                
                    pred_val = resource.get('INC')
                    ac_val = res_from_file['INC']
                    assert pred_val == ac_val, \
                                f"P_ChEs_max is not matched with get(INC) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(INC)")

                    # alpha_flex                
                    pred_val = resource.get('alpha_flex')
                    ac_val = res_from_file['Alfa'] / 100.
                    assert pred_val == ac_val, \
                                f"alpha_flex is not matched with get(alpha_flex) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(alpha_flex)")

                    
                    # LR_pickup                
                    pred_val = resource.get('LR_pickup')
                    ac_val = res_from_file['LR_pickup']
                    assert pred_val == ac_val, \
                                f"LR_pickup is not matched with get(LR_pickup) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(LR_pickup)")


                    # LR_drop                
                    pred_val = resource.get('LR_drop')
                    ac_val = res_from_file['LR_drop']
                    assert pred_val == ac_val, \
                                f"LR_drop is not matched with get(LR_drop) => " + \
                                    f"{pred_val} != {ac_val}"

                    print("OK: Right get(LR_drop)")


if __name__ == "__main__":
    test_FL()