from src.vppNode.VppBoxNode import VppBoxNode

if __name__ == '__main__':
    vb = VppBoxNode()
    vb.update_resources()
    VppBoxNode.print_resource(vb.es_resources)
    VppBoxNode.print_resource(vb.wf_resources)
    VppBoxNode.print_resource(vb.pv_resources)
    VppBoxNode.print_resource(vb.dg_resources)
    VppBoxNode.print_resource(vb.fl_resources)