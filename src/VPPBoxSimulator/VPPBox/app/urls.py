from django.urls import path
from .views import get_load_data, get_line_data, get_uncertainty_data, get_dg_data, \
    get_es_data, get_fl_data, get_pv_data, get_wf_data

urlpatterns = [
    path('line-data/', get_line_data),
    path('load-data/<int:time>', get_load_data),
    path('uncertainty-params/<int:time>', get_uncertainty_data),
    path('DG/', get_dg_data),
    path('ES/', get_es_data),
    path('FL/', get_fl_data),
    path('PV/', get_pv_data),
    path('WF/', get_wf_data),
]