#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 16:21:17 2022

@author: changsu
"""
import pandas as pd
import shap
import numpy as np
import matplotlib.pyplot as plt
import pickle
from io import BytesIO
import base64


def predict_tool(file_dir, p_info):
    '''
    file_dir:   dir of files used in following process
    p_info:     pd dataframe of patient info
    
    '''

    # load model
    with open(file_dir+'/'+'model.pkl' , 'rb') as f:
        model = pickle.load(f)

    target_data = p_info
    ids = target_data['ids']
    X_data = target_data.drop(columns=['ids'])
    y_pred = model.predict_proba(X_data)[:, 1]
    y_pred_norm = 100 * (np.clip(y_pred, 0, 0.7) - 0) / (0.7 - 0)

    y_pred_df = pd.DataFrame(columns=['StudyId', 'Caries_Lesions_risk'])
    y_pred_df['StudyId'] = target_data['ids'].values
    #y_pred_df.insert(1, "Severe_PD_risk", y_pred_norm, True)
    y_pred_df['Caries_Lesions_risk'] = y_pred_norm

    labs = X_data.copy()
    labs.rename(columns = {'Oral_Health_Index':'Oral Health Instructions','Bitewing_Series':'Bitewing Series',
                            'Tobacco_Counsel':'# Tobacco Counsel','Completed_Tx': '# Completed Treatments',
                            'Recall_Exams':'# Recall Exams', 'Nutritional_Counsel':'# Nutritional Counsel',
                            'Class_II_Restorations':'Class II Restorations',
                            'Other_Composite_restorations':'Composite Restorations',
                            'Fixed_Pros_Natural_Teeth':'Fixed Prosthesis (Natural Teeth)', 
                            'Fixed_Pros_Implant_or_Other':'Fixed Prosthesis (Implant)',
                            'Periodontal_Tx':'Periodontal Treatments','RyanWhite_Insurance':'RyanWhiteInsurance', 
                            'Basic_Complexity': 'Basic Complexity','Complex_Complexity':'Complex Complexity'}, inplace=True)
    labs = list(labs.columns)
    # individual prediction interpretation
    for idx in range(len(target_data)):
        p_id = target_data.loc[idx, 'ids']
        #print(idx, p_id)
        explainer = shap.TreeExplainer(model)
        shap_values_val = explainer.shap_values(X_data)
        plt.switch_backend('Agg')
        shap.force_plot(0,
                shap_values_val[idx, :],
                X_data.iloc[idx, :],
                feature_names = labs,
                contribution_threshold=0.15,
                matplotlib=True, show=False, figsize=(20,4))
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        shap_plot = base64.b64encode(image_png)
        shap_plot = shap_plot.decode('utf-8')
        #plt.savefig(save_dir + '/evidence_%s.pdf' % p_id, bbox_inches='tight')
        plt.close()
        shap_df = pd.DataFrame(shap_values_val, columns=X_data.columns)
        #shap_df.to_csv(save_dir + '/evidence_%s.csv' % p_id, index=False)
    #y_pred_df.to_csv(save_dir + '/predicted_risk.csv')
    return shap_df, y_pred_norm, shap_plot, X_data
