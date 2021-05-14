import requests
from src.Forecaster.UncertaintyParams import UncertaintyParams

class Forecaster:
    """ Connects to ForecasterAPI and gets params.
    """
    def __init__(self, node_id: int = None) -> None:
        self.pf = 0.6197
        self.node_id = node_id
        self.forecaster_connector = ForecasterAPI(self.node_id)
    
    def get_wind(self, w: int, t: int):
        return self.forecaster_connector.get_wind(w=w, t=t)
    
    def get_pv(self, w: int, t: int):
        return self.forecaster_connector.get_pv(w=w, t=t)
    
    def get_pl(self, t: int):
        return self.forecaster_connector.get_fixed_load(t=t)
    
    def get_ql(self, t: int):
        return self.forecaster_connector.get_fixed_load(t=t) * self.pf

    def get_da(self, t: int):
        return self.forecaster_connector.get_da(t)

class ForecasterAPI:

    def __init__(self, node_id: int) -> None:
        self.endpoint = "http://localhost:8001"
        self.node_id = node_id

    def __get_uncertainty_params(self, w: int, t: int):
        res = requests.get(self.endpoint + "/uncertainty-params/" + str(t)).json()
        uncertainty_params = UncertaintyParams.get_instance_by_json(res['data'])
        if res['status'] != 404:
            return {
                'pv': uncertainty_params.pv_pu,
                'wind': uncertainty_params.wf_pu,
                'da': uncertainty_params.da_price,
                'rt': uncertainty_params.rt_price
            }
        
        raise(IndexError(f"No results for time={t}"))

    def get_fixed_load(self, t: int):
        res = res = requests.get(self.endpoint + "/node-fixed-load/" + str(
            self.node_id) + f"?time={t}").json()
        data = res['data']
        if res['status'] != 404:
            return data['load']
        
        raise(IndexError(f"No results for time={t}"))
    
    def get_flexible_load(self, w: int, t: int):
        res = res = requests.get(self.endpoint + "/node-flexible-load/" + str(
            self.node_id) + f"?time={t}").json()
        data = res['data']
        if res['status'] != 404:
            return data['load']
        
        raise(IndexError(f"No results for time={t}"))
    
    def get_wind(self, w: int, t: int):
        return self.__get_uncertainty_params(w=w, t=t)['wind']
    
    def get_pv(self, w: int, t: int):
        return self.__get_uncertainty_params(w=w, t=t)['pv']
    
    def get_da(self, t: int):
        return self.__get_uncertainty_params(w=-1, t=t)['da']