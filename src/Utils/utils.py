from src.vppNode.VppBoxNode import VppBoxNode
from src import vppNode
from src.vppNode.VppNode import VppNode
from src.vppNode.VppBoxNode import VppBoxNode
import pandas as pd

class NodeResults:
    """a class for creating output files based on final resutls of the optimizer.
    """
    def __init__(self, node: VppNode) -> None:
        self.node = node
        self.dir_sp_p_da_buy = 'output/buy.xlsx'
        self.dir_sp_p_da_sell = 'output/sell.xlsx'
        self.dir_u_dg = 'output/u_dg.xlsx'
        self.dir_v_dg_su = 'output/v_dg_su.xlsx'
        self.dir_v_dg_sd = 'output/v_dg_sd.xlsx'
        self.dir_opt_res = 'output/ofv.xlsx'

    def to_excel(self, **kwargs):
        """a method to create excel files based on output variables of VppBoxes
        (setpoints)
        Args:
            **kwargs: Arbitrary keyword arguments.
            buy (bool): True to create output/buy.xlsx
            sell (bool): True to create output/sell.xlsx
            u_dg (bool): True to create output/u_dg.xlsx
            v_dg_su (bool): True to create output/v_dg_su.xlsx
            v_dg_sd (bool): True to create output/v_dg_sd.xlsx
            opt (bool): True to create output/ofv.xlsx
        """
        sb_box: VppBoxNode = self.node.get_junction(1)

        df_buy = pd.DataFrame(sb_box.sp_p_da_buy.values(), index=[0])
        df_sell = pd.DataFrame(sb_box.sp_p_da_sell.values(), index=[0])
                
        u_dg_row = []
        u_dg_cols = []

        v_dg_su_row = []
        v_dg_su_cols = []

        v_dg_sd_row = []
        v_dg_sd_cols = []

        indecies = []

        for key, box_node in self.node.junctionMp.getItems():
            if not box_node.dg_resources.is_empty():
                for key1, value1 in box_node.dg_resources.getItems():
                    
                    w1_sp_u_dg = value1.sp_u_dg[1]
                    w1_sp_v_dg_su = value1.sp_v_dg_su[1]
                    w1_sp_v_dg_sd = value1.sp_v_dg_sd[1]
                    
                    u_dg_row.append(list(w1_sp_u_dg.values()))
                    u_dg_cols.append(list(w1_sp_u_dg.keys()))

                    v_dg_su_row.append(list(w1_sp_v_dg_su.values()))
                    v_dg_su_cols.append(list(w1_sp_v_dg_su.keys()))

                    v_dg_sd_row.append(list(w1_sp_v_dg_sd.values()))
                    v_dg_sd_cols.append(list(w1_sp_v_dg_sd.keys()))

                    indecies.append(f"{key},{key1}")

        df_u_dg = pd.DataFrame(u_dg_row, columns=u_dg_cols[0], index=indecies)
        df_v_dg_su = pd.DataFrame(v_dg_su_row, columns=v_dg_su_cols[0], index=indecies)
        df_v_dg_sd = pd.DataFrame(v_dg_sd_row, columns=v_dg_sd_cols[0], index=indecies)
        df_ofv = pd.DataFrame(self.node.OFV, columns=list(range(1, len(self.node.OFV)+1)), index=[0])

        if kwargs.pop('buy', False):
            df_buy.to_excel(self.dir_sp_p_da_buy)
        if kwargs.pop('sell', False):
            df_sell.to_excel(self.dir_sp_p_da_sell)
        if kwargs.pop('u_dg', False):
            df_u_dg.to_excel(self.dir_u_dg)
        if kwargs.pop('v_dg_su', False):
            df_v_dg_su.to_excel(self.dir_v_dg_su)
        if kwargs.pop('v_dg_sd', False):
            df_v_dg_sd.to_excel(self.dir_v_dg_sd)
        if kwargs.pop('opt', False):
            df_ofv.to_excel(self.dir_opt_res)