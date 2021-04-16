from src.vppNode.VppBoxNode import VppBoxNode

if __name__ == '__main__':
    vb = VppBoxNode()
    print(vb.get_uncertainty_params(12))
