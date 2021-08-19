from ..VPP.test_15bus import *
from src.FakeAPI.utils import read_nodes_structure
import math


def test_structure():
    
    print("...TEST test_structure is started...")

    data = read_nodes_structure()['data']
    
    for edge_key, edge in vppNode.edgeMp.getItems():
        line = edge.lineProps
        junction = edge.junctions

        for dt in data:
            if dt['nodes'] == junction:
                print(f"junction: {junction}")
                dt_line = dt['line']

                # test get methods

                # R
                ac_val = dt_line['r']
                pred_val = line.get("R")
                assert ac_val == pred_val, \
                    f"LineProb.get(R) is not equal to file value for {junction}"
                print("OK: get(R)")

                # X
                ac_val = dt_line['x']
                pred_val = line.get("X")
                assert ac_val == pred_val, \
                    f"LineProb.get(X) is not equal to file value for {junction}"
                print("OK: get(X)")

                # I_max
                ac_val = dt_line['i_max']
                pred_val = line.get("I_max")
                assert ac_val == pred_val, \
                    f"LineProb.get(I_max) is not equal to file value for {junction}"
                print("OK: get(I_max)")


                # Z
                ac_val = math.sqrt(dt_line['r'] ** 2 + dt_line['x'] ** 2)
                pred_val = line.get("Z")
                assert ac_val == pred_val, \
                    f"LineProb.get(Z) is not equal to file value for {junction}"
                print("OK: get(Z)")


if __name__ == "__main__":
    test_structure()