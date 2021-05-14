from src.vppNode.VppBoxNode import VppBoxNode


vpp = VppBoxNode(4, 12, 12)

print("TESTING RESOURCE LOADING FROM API")
vpp.load_resources_from_api()

vpp.print_resource(vpp.es_resources)
vpp.print_resource(vpp.dg_resources)

print("TESTING P_L and Q_L")
print(vpp.fixed_load.get("P_L", t=4))
print(vpp.fixed_load.get("P_L", t=1))
print(vpp.fixed_load.get("Q_L", t=7))
