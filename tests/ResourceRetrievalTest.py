from src.vppNode.VppBoxNode import VppBoxNode

vb = VppBoxNode()
vb.update_resources()
VppBoxNode.print_resource(vb.es_resources)
VppBoxNode.print_resource(vb.wf_resources)
VppBoxNode.print_resource(vb.pv_resources)
VppBoxNode.print_resource(vb.dg_resources)
VppBoxNode.print_resource(vb.fl_resources)