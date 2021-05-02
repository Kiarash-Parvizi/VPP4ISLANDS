from .VppNode import VppNode

# interaction point between one VppNode and other components
class VppInterface:
    def __init__(self, vppNode: VppNode) -> None:
        # set other modules later
        self.vppNode = vppNode

    def get_optimizer_input_data():
        return {
            'null'
        }

    # change the graph and other possible related components based on setpoints
    def distribute_optimizerOutput(dat):
        pass
