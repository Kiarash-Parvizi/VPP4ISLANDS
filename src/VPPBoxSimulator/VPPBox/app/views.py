from django.shortcuts import render
from django.http.response import JsonResponse
from .utils import read_load_data, create_line_data, read_uncertainty_params, read_dg_data, \
    read_es_data, read_fl_data, read_pv_data, read_wf_data


def get_load_data(request, time):
    data = read_load_data(time)
    return JsonResponse(data)

def get_line_data(request):
    data = create_line_data()
    return JsonResponse(data)

def get_uncertainty_data(request, time):
    data  = read_uncertainty_params(time)
    return JsonResponse(data)

def get_dg_data(request):
    data = read_dg_data()
    return JsonResponse(data)

def get_es_data(request):
    data = read_es_data()
    return JsonResponse(data)

def get_fl_data(request):
    data = read_fl_data()
    return JsonResponse(data)

def get_pv_data(request):
    data = read_pv_data()
    return JsonResponse(data)

def get_wf_data(request):
    data = read_wf_data()
    return JsonResponse(data)