from src.vppNode.VppBoxNode import VppBoxNode
from src import vppNode
from src.vppNode.VppNode import VppNode
from src.vppNode.VppBoxNode import VppBoxNode
import pandas as pd

class NodeResults:
    def __init__(self, node: VppNode) -> None:
        self.node = node
        self.dir_sp_p_da_buy = 'output/buy.xlsx'
        self.dir_sp_p_da_sell = 'output/sell.xlsx'
        self.dir_u_dg = 'output/u_dg.csv'
        self.dir_v_dg_su = 'output/v_dg_su.csv'
        self.dir_v_dg_sd = 'output/v_dg_sd.csv'

    def to_excel(self):
        sb_box: VppBoxNode = self.node.get_junction(1)

        df_buy = pd.DataFrame(sb_box.sp_p_da_buy.values(), index=[0])
        df_sell = pd.DataFrame(sb_box.sp_p_da_sell.values(), index=[0])
        # df_u = pd.DataFrame(sb_box.,index=[0])
        
        # dgs = {}

        # for key, box_node in self.node.junctionMp.getItems():
        #     if not box_node.dg_resources.is_empty():
        #         dgs[key] = box_node.dg_resources.mp.values()
        # print(dgs)
        
        df_buy.to_excel(self.dir_sp_p_da_buy)
        df_sell.to_excel(self.dir_sp_p_da_sell)
