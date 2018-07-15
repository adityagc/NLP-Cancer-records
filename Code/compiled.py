# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:41:06 2018

@author: kdabhadk
"""

model = 'NB_model.pkl'
vect= 'vectorizer.pkl'
inputfile='train.csv'

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split

def predict(inputfile,model,vect):

    train = pd.read_csv(inputfile)
    
    formaldx=[]
    for word in train['TEXT_PATH_FORMAL_DX'].astype(str):
        if [train['TEXT_PATH_FORMAL_DX'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            formaldx.append(text)
    
    comments = []
    for word in train['TEXT_PATH_COMMENTS'].astype(str):
        if [train['TEXT_PATH_COMMENTS'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            comments.append(text)
            
    patho = []
    for word in train['TEXT_PATH_GROSS_PATHOLOGY'].astype(str):
        if [train['TEXT_PATH_GROSS_PATHOLOGY'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            patho.append(text)
            
    fulltext = []
    for word in train['TEXT_PATH_FULL_TEXT'].astype(str):
        if [train['TEXT_PATH_FULL_TEXT'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            fulltext.append(text)
            
    clinicalhist = []
    for word in train['TEXT_PATH_CLINICAL_HISTORY'].astype(str):
        if [train['TEXT_PATH_CLINICAL_HISTORY'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            clinicalhist.append(text)
            
    microdesc = []
    for word in train['TEXT_PATH_MICROSCOPIC_DESC'].astype(str):
        if [train['TEXT_PATH_MICROSCOPIC_DESC'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            microdesc.append(text)
            
    natspec = []
    for word in train['TEXT_PATH_NATURE_OF_SPECIMENS'].astype(str):
        if [train['TEXT_PATH_NATURE_OF_SPECIMENS'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            natspec.append(text)
            
    addenda = []
    for word in train['TEXT_PATH_SUPP_REPORTS_ADDENDA'].astype(str):
        if [train['TEXT_PATH_SUPP_REPORTS_ADDENDA'].notnull()]:
            text = word.replace('\\X0D\\\\X0A\\',' ')
            text = text.replace('\r\n',' ')
            text = text.replace('\r \n',' ')
            addenda.append(text)
            
    patientid = []
    for word in train['PATIENT_DISPLAY_ID'].astype(str):
        if [train['PATIENT_DISPLAY_ID'].notnull()]:
            text = word.replace('PAT-',' ')
            patientid.append(text)
            
    #####################
    train['TEXT_PATH_FORMAL_DX'] = formaldx
    train['TEXT_PATH_COMMENTS'] = comments
    train['TEXT_PATH_GROSS_PATHOLOGY'] = patho
    train['TEXT_PATH_FULL_TEXT'] = fulltext
    train['TEXT_PATH_CLINICAL_HISTORY'] = clinicalhist
    train['TEXT_PATH_MICROSCOPIC_DESC'] = microdesc
    train['TEXT_PATH_NATURE_OF_SPECIMENS'] = natspec
    train['TEXT_PATH_SUPP_REPORTS_ADDENDA'] = addenda
    
    train['PATIENT_DISPLAY_ID'] = patientid
    #train.to_csv('train_cleaned_text.csv')
    
    ####################
    concat = train['TEXT_PATH_CLINICAL_HISTORY'].astype(str) + " " + train['TEXT_PATH_COMMENTS'].astype(str) + " " + train['TEXT_PATH_FORMAL_DX'].astype(str)+ " " + train['TEXT_PATH_FULL_TEXT'].astype(str)+ " " + train['TEXT_PATH_GROSS_PATHOLOGY'].astype(str)+ " " + train['TEXT_PATH_MICROSCOPIC_DESC'].astype(str)+ " " + train['TEXT_PATH_NATURE_OF_SPECIMENS'].astype(str)+ " " + train['TEXT_PATH_STAGING_PARAMS'].astype(str)+ " " + train['TEXT_PATH_SUPP_REPORTS_ADDENDA'].astype(str)
    new = pd.DataFrame()
    new['SITE'] = train['SITE']
    new['PATIENT_DISPLAY_ID']= train['PATIENT_DISPLAY_ID']
    new['Text'] = concat
    
    ####################
    clfrNB = joblib.load(model)
    vect = joblib.load(vect)
    
    output = []
    X_train= new['Text']
    X_test_vectorized = vect.transform(X_train)
    predicted = clfrNB.predict(X_test_vectorized)
    
    output = pd.DataFrame()
    output=train
    output['SITE'] = predicted
   
    
    return output.to_csv('results.csv'),dict(zip(output.PATIENT_DISPLAY_ID,output.SITE))

