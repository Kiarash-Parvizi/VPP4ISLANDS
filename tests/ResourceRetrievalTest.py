from src.vppNode.VppBoxNode import VppBoxNode

vb = VppBoxNode(node_id=15)
vb.get_resource_data()
vb.get_flexible_load(12)
vb.get_fixed_load(12)
print(vb.flexible_load)
print(vb.fixed_load)
VppBoxNode.print_resource(vb.es_resources)
VppBoxNode.print_resource(vb.wf_resources)
VppBoxNode.print_resource(vb.pv_resources)
VppBoxNode.print_resource(vb.dg_resources)
VppBoxNode.print_resource(vb.fl_resources)