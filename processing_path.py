import codecs
import csv
import json
import os
from os import listdir
import sys
import re
import operator
import random
import time
import spacy

nlp = spacy.load('en_core_web_sm')


def open_csv_file_comma(csv_file_path):
    with open(csv_file_path, 'r', encoding='ISO-8859-1') as infile:
        data_reader = csv.reader(infile, delimiter=',', quotechar='"')
        data_list_object = list(data_reader)
    return data_list_object


def string_cleaning(string):
    # add padding to other punctuation
    string = re.sub(r'"', '', string)
    string = re.sub(r'(_+)', '_', string)
    string = re.sub(r'(\.+)', '.', string)
    string = re.sub(r',', ' , ', string)
    string = re.sub(r'\\X0D\\\\X0A\\', '\n\r', string)
    string = re.sub(r'(\d)(\s|)(x)(\s|)(\d)', r'\1 \3 \5', string)
    string = re.sub(r"\s{2,}", " ", string)

    return string


def section_labeling(all_headers, inscope_headers, inscope_index, row, x1):

    # global new_file_list
    new_file_list = []
    #noun_phase_chunk = []

    for indx in inscope_index:

        focus = row[indx]

        if all_headers[indx] == 'PATIENT_DISPLAY_ID':
            new_file_list.append("Patient_ID :")
            new_file_list.append(focus)
            pt_id = focus
        elif all_headers[indx] == 'SITE':
            new_file_list.append("SITE_ID :")
            new_file_list.append(focus)
            site_id = focus
        else:
            item = all_headers[indx]
            if 'TEXT_PATH_' in item:
                item = re.sub(r'TEXT_PATH_', '', item)
            else:
                pass

            sect_id = ("%s :" % (item))
            new_file_list.append(sect_id)
            focus_new = string_cleaning(focus)
            doc = nlp(focus_new)
            for sent in doc.sents:
                new_file_list.append(sent.text)
                #doc2 = nlp(sent.text)
                #for chunk in doc2.noun_chunks:
                    #noun_phase_chunk.append(chunk.text)

    # file_id = (site_id + "_" + pt_id + "_" + str(x1))
    #new_file_list
    # noun_phase_chunk

    return new_file_list


def use_model_predict_site(patient_sectioned):
    sites_id = patient_sectioned[1]
    return sites_id


def get_cancer_site(for_processing, fi):

    nlp = spacy.load('en_core_web_sm')

    rows_data = open_csv_file_comma(for_processing)

    all_headers = rows_data[0]
    inscope_headers = ['SITE', 'PATIENT_DISPLAY_ID', 'TEXT_PATH_CLINICAL_HISTORY', 'TEXT_PATH_COMMENTS', 'TEXT_PATH_FORMAL_DX', 'TEXT_PATH_FULL_TEXT', 'TEXT_PATH_GROSS_PATHOLOGY', 'TEXT_PATH_MICROSCOPIC_DESC', 'TEXT_PATH_NATURE_OF_SPECIMENS', 'TEXT_PATH_STAGING_PARAMS', 'TEXT_PATH_SUPP_REPORTS_ADDENDA']
    inscope_index = []
    for head in inscope_headers:
        indexy = all_headers.index(head)
        inscope_index.append(indexy)

    sectioned_lists = []

    x1 = 1
    while x1 < len(rows_data):

        row = rows_data[x1]
        new_list = section_labeling(all_headers, inscope_headers, inscope_index, row, x1)
        sectioned_lists.append(new_list)
        x1 = x1 + 1

        out_site_dict = dict()

    x2 = 0
    while x2 < len(sectioned_lists):

        patient_sectioned = sectioned_lists[x2]
        patient_identifier = patient_sectioned[3]
        if patient_identifier in out_site_dict.keys():
            new_patient_id = (patient_identifier + '_' + 'r1')
            site_final = use_model_predict_site(patient_sectioned)
            out_site_dict[new_patient_id] = site_final
        else:
            site_final = use_model_predict_site(patient_sectioned)
            out_site_dict[patient_identifier] = site_final

        x2 = x2 + 1

        json_out = ({"batch_id": fi, "result": out_site_dict})

    return json_out
