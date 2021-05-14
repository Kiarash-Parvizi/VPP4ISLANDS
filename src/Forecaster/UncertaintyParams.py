class UncertaintyParams:
    """ UncertaintyParams is a class which represents uncertainty parameters given by VPPBox
    Attributes:
    wf_pu       (float): P.U of WF
    pv_pu       (float): P.U of PV
    da_price    (float): DA Price
    rt_price    (float): RT Price
    time        (float)
    """

    def __init__(self, wf_pu: float, pv_pu: float, da_price: float, rt_price: float, time: float):
        self.wf_pu = wf_pu
        self.pv_pu = pv_pu
        self.da_price = da_price
        self.rt_price = rt_price
        self.time = time

    def __str__(self):
        return self.__class__.__name__ + ": { " + \
               "\n\tP.U of WF: " + str(self.wf_pu) + \
               "\n\tP.U of PV: " + str(self.pv_pu) + \
               "\n\tDA Price: " + str(self.da_price) + \
               "\n\tRT Price: " + str(self.rt_price) + \
               "\n\ttime    : " + str(self.time) + \
               "\n}"

    @staticmethod
    def get_instance_by_json(item: dict):
        wf_pu = item['WF']
        pv_pu = item['PV']
        da_price = item['DA_PRICE']
        rt_price = item['RT_PRICE']
        time = item['TIME']
        return UncertaintyParams(wf_pu=wf_pu, pv_pu=pv_pu, da_price=da_price, rt_price=rt_price, time=time)
