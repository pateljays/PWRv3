from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import *
from main.predict_tool.prediction_tool import predict_tool
from django_pandas.io import read_frame
from django.conf import settings
import os, json

from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import shap
import numpy as np
import matplotlib.pyplot as plt
import pickle

f_data_dict = {'ids':'Patient ID'}

labels_dict = {
    'Oral_Health_Index'             :'Oral Health Index',
    'Bitewing_Series'                :'Bitewing Series',
    'Tobacco_Counsel'               :'# Tobacco Counsel',
    'Completed_Tx'                   :'# Completed Treatments',
    'Recall_Exams'                   :'# Recall Exams',
    'Nutritional_Counsel'            :'# Nutritional Counsel',
    'Class_II_Restorations'          :'Class II Restorations',
    'Other_Composite_restorations'   :'Composite Restorations',
    'Fixed_Pros_Natural_Teeth'       :'Fixed Prosthesis (Natural Teeth)',
    'Fixed_Pros_Implant_or_Other'    :'Fixed Prosthesis (Implant)',
    'Periodontal_Tx'                 :'Periodontal Treatments',
    'RyanWhite_Insurance'            :'Ryan‑White Insurance',
    'RyanWhite_Insurance'            :'Ryan‑White Insurance',
    'Basic_Complexity'               :'Basic Complexity',
    'Complex_Complexity'             :'Complex Complexity'
}

# Create your views here.
@csrf_exempt
def main_index(request):
    if request.method == 'GET':
        f_plot = {'pf_cate':[], 
                'pf_val':[], 
                'rf_cate':[],
                'rf_val':[], 
                'f_data_dict':{}}
        params = {'result_display_status':'init', 
                'p_id':'', 
                'y_pred_norm':'',
                'bullet_data':json.dumps(''),
                'f_plot':f_plot, 
                'shap_plot':''}
        return render(request, 'main/index.html', {'params':params})
    elif request.method == 'POST':
        #get user input
        try:
            p_id = int(request.POST.get('PID'))
        except:
            params = {'result_display_status':'p_id_not_right'}
            return render(request, 'main/index.html', {'params':params})
        
        #check if patient exist
        if PatientInfo.objects.filter(ids=p_id).exists():
            '''
            prepare patient information
            '''
            p_rec = read_frame(PatientInfo.objects.filter(ids=p_id))
            p_rec = p_rec.fillna(value=np.nan)
            file_dir = os.path.join(settings.BASE_DIR, 'main/predict_tool/')
            shap_df, y_pred_norm, shap_plot, data_imputed = predict_tool(file_dir, p_rec)
            shap_df.rename(index=labels_dict, inplace=True)
            #round risk score
            y_pred_norm = round(y_pred_norm[0],2)
            #prepare bullet data
            bullet_data = [{"title":"Score",
                            "subtitle":"in total", 
                            "ranges":[10,20,30,40,50,60,70,80,90,100], 
                            "measures":[y_pred_norm], 
                            "markers":[y_pred_norm]}]
            #prepare protective factors plot
            pf_data = shap_df.T
            pf_data = shap_df.T.loc[shap_df.T[0] < 0].sort_values(by=0)
            pf_cate = list(pf_data.index)[:10]
            pf_val   = [-v for v in pf_data.iloc[:10, 0]]

            # map to human labels here
            pf_cate = [ labels_dict.get(f, f) for f in pf_cate ]

            # same for the risk factors
            rf_data = shap_df.T.loc[shap_df.T[0] > 0].sort_values(by=0, ascending=False)
            rf_cate = list(rf_data.index)[:10]
            rf_val   = list(rf_data.iloc[:10, 0])
            rf_cate  = [ labels_dict.get(f, f) for f in rf_cate ]
            #prepare a y label attachement ==>> label (number)
            y_label_atta = data_imputed.to_dict('records')[0]

            #put data together
            f_plot = {
                'pf_cate'    : pf_cate,
                'pf_val'     : pf_val,
                'rf_cate'    : rf_cate,
                'rf_val'     : rf_val,
                'f_data_dict': labels_dict,  # if you need the mapping in your template, too
                'y_label_atta': data_imputed.to_dict('records')[0]
            }
            
            see=y_label_atta
            params = {'result_display_status':'show_result', 
                    'p_id':p_id, 
                    'y_pred_norm':y_pred_norm,
                    'bullet_data':json.dumps(str(bullet_data).replace("'",'"')),
                    'f_plot':f_plot, 
                    'see':see, 
                    'shap_plot':shap_plot}
            return render(request, 'main/index.html', {'params':params})
        else:
            params = {'result_display_status':'no_result'}
            return render(request, 'main/index.html', {'params':params})


###### ajax functions #######

def get_pid(request):
    try:
        p_id = int(request.GET.get('term', ''))
    except:
        data = 'fail_1'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    
    p_info = PatientInfo.objects.filter(ids__startswith=p_id).values_list('ids', flat=True)
    p_info=list(set(p_info))[:10]
    p_info.sort()
    results = []
    for pid in p_info:
        p_json = {}
        p_json['value'] = pid
        results.append(p_json)
    if len(results)==0:
        results=[{'value':'Patient NOT in Database'}]
    
    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)















