from src.Forecaster.Forecaster import Forecaster

# test for Forecaster

forecaster = Forecaster(3)

assert forecaster.get_pv(1, 5) == 0
assert forecaster.get_pv(1, 15) == 0.399085600261257
assert forecaster.get_pv(1, 13) == 0.571428408163312


assert forecaster.get_wind(1, 5) == 0.731974142217802

assert forecaster.get_pl(1, 4) == 58.67647059

assert forecaster.get_ql(1, 4) == (forecaster.get_pl(1, 4) * 0.6197)

print(forecaster.get_da(15))