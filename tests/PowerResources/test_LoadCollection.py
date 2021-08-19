from ..VPP.test_15bus import * 

def test_LoadCollection():
    
    print(f"....TEST test_LoadCollection is started...")

    for node_id, node in vppNode.junctionMp.getItems():
        
        # check if the node is VppBoxNode
        if isinstance(node, VppBoxNode):
            
            # if that node has a fixed_loads
            if node.load_collection:
                
                print(f"OK: Right node_id {node_id}")

                if not node.trade_compatible:

                    for fixload_key, fixload in node.load_collection.fixed_loads.getItems():
                        
                        # testing the get methods
                        
                        # P_S_L
                        ac_val = node.load_collection.get("P_S_L")
                        pred_val = fixload.get("P_L")

                        assert ac_val == pred_val, f"LoadCollection.get(P_S_L) is not matched with FixedLoad.get(P_L)"
                        
                        print(f"OK: Right get(P_S_L)")


                        # Q_S_L
                        ac_val = node.load_collection.get("Q_S_L")
                        pred_val = fixload.get("Q_L")

                        assert ac_val == pred_val, f"LoadCollection.get(Q_S_L) is not matched with FixedLoad.get(Q_L)"
                        
                        print(f"OK: Right get(Q_S_L)")
                

                if not node.load_collection.flex_loads.is_empty():

                    for flex_key, flexload in node.load_collection.flex_loads.getItems():

                        # INC_S
                        ac_val = flexload.get("INC")
                        pred_val = node.load_collection.get("INC_S")

                        assert ac_val == pred_val, f"LoadCollection.get(INC_S) is not matched with FixedLoad.get(INC)"
                        
                        print(f"OK: Right get(INC_S)")


                        # alpha_S_flex
                        ac_val = flexload.get("alpha_flex")
                        pred_val = node.load_collection.get("alpha_S_flex")

                        assert ac_val == pred_val, f"LoadCollection.get(alpha_S_flex) is not matched with FixedLoad.get(alpha_flex)"
                        
                        print(f"OK: Right get(alpha_S_flex)")


                        # LR_S_pickup
                        ac_val = flexload.get("LR_pickup")
                        pred_val = node.load_collection.get("LR_S_pickup")

                        assert ac_val == pred_val, f"LoadCollection.get(LR_S_pickup) is not matched with FixedLoad.get(LR_pickup)"
                        
                        print(f"OK: Right get(LR_S_pickup)")


                        # LR_S_drop
                        ac_val = flexload.get("LR_drop")
                        pred_val = node.load_collection.get("LR_S_drop")

                        assert ac_val == pred_val, f"LoadCollection.get(LR_S_drop) is not matched with FixedLoad.get(LR_drop)"
                        
                        print(f"OK: Right get(LR_S_drop)")


if __name__ == "__main__":
    test_LoadCollection()