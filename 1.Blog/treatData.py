#!/usr/local/bin/python3

import re
import os
import pandas as pd

def process_enem_data(enem2018_df, input_format='csv', **options):
    enem2018_df.fillna(0, inplace=True)
    enem2018_df.drop_duplicates('NU_INSCRICAO')
    enem2018_df = enem2018_df.rename(columns={ 'NU_INSCRICAO': 'registration'
                                             , 'CO_MUNICIPIO_RESIDENCIA': 'city_residence_code'
                                             , 'NO_MUNICIPIO_RESIDENCIA': 'city_residence'
                                             , 'CO_UF_RESIDENCIA': 'state_residence_code'
                                             , 'SG_UF_RESIDENCIA': 'state_residence'
                                             , 'NU_IDADE': 'age'
                                             , 'TP_SEXO': 'gender'
                                             , 'TP_ESTADO_CIVIL': 'matiral_status'
                                             , 'TP_COR_RACA': 'color_race'
                                             , 'TP_NACIONALIDADE': 'nationality'
                                             , 'TP_ST_CONCLUSAO': 'high_school_status'
                                             , 'TP_ANO_CONCLUIU': 'high_school_year_conclusion'
                                             , 'TP_ESCOLA': 'school_type'
                                             , 'IN_BAIXA_VISAO': 'def_low_vision'
                                             , 'IN_CEGUEIRA': 'def_blind'
                                             , 'IN_SURDEZ': 'def_deaf'
                                             , 'IN_DEFICIENCIA_AUDITIVA': 'def_low_hearing'
                                             , 'IN_SURDO_CEGUEIRA': 'def_blind_deaf'
                                             , 'IN_DEFICIENCIA_FISICA': 'def_physical'
                                             , 'IN_DEFICIENCIA_MENTAL': 'def_mental'
                                             , 'IN_DEFICIT_ATENCAO': 'def_attention'
                                             , 'IN_DISLEXIA': 'def_dyslexia'
                                             , 'IN_DISCALCULIA': 'def_dyscalculia'
                                             , 'IN_AUTISMO': 'def_autism'
                                             , 'IN_VISAO_MONOCULAR': 'def_monocular_vision'
                                             , 'IN_OUTRA_DEF': 'def_other'
                                             , 'IN_NOME_SOCIAL': 'social_name'
                                             , 'CO_MUNICIPIO_PROVA': 'city_test_code'
                                             , 'NO_MUNICIPIO_PROVA': 'city_test'
                                             , 'CO_UF_PROVA': 'state_test_code'
                                             , 'SG_UF_PROVA': 'state_test'
                                             , 'TP_PRESENCA_CN': 'presence_natural_science'
                                             , 'TP_PRESENCA_CH': 'presence_human_science'
                                             , 'TP_PRESENCA_LC': 'presence_languages'
                                             , 'TP_PRESENCA_MT': 'presence_math'
                                             , 'NU_NOTA_CN': 'grade_natural_science'
                                             , 'NU_NOTA_CH': 'grade_human_science'
                                             , 'NU_NOTA_LC': 'grade_languages'
                                             , 'NU_NOTA_MT': 'grade_math'
                                             , 'TP_STATUS_REDACAO': 'essay_status'
                                             , 'NU_NOTA_REDACAO': 'grade_essay'
                                             })
    return enem2018_df

def process_cities_data(brazil_df, input_format='csv', **options):
    brazil_df.fillna(0, inplace=True)
    brazil_df.drop_duplicates(['CITY', 'STATE'], keep='first')
    brazil_df = brazil_df.filter([ 'CITY', 'STATE', 'CAPITAL', 'IDHM Ranking 2010', 'IDHM'
                                 , 'IDHM_Renda', 'IDHM_Longevidade', 'IDHM_Educacao', 'LONG'
                                 , 'LAT', 'ALT'
                                 ])
    brazil_df = brazil_df.rename(columns={ 'CITY': 'city'
                                         , 'STATE': 'state'
                                         , 'CAPITAL': 'capital'
                                         , 'IDHM Ranking 2010': 'hdi_ranking'
                                         , 'IDHM': 'hdi'
                                         , 'IDHM_Renda': 'hdi_gni'
                                         , 'IDHM_Longevidade': 'hdi_life'
                                         , 'IDHM_Educacao': 'hdi_education'
                                         , 'LONG': 'longitude'
                                         , 'LAT': 'latitude'
                                         , 'ALT': 'altitude'
                                         })
    return brazil_df

def treatEnem():
    enem_2018_path = os.getcwd() + '/data/enem2018/enem_2018.csv'
    enem2018_df = pd.read_csv(enem_2018_path, delimiter=";")
    enem2018_df.fillna(0, inplace=True)

    print('Original Enem Dataset: ', enem2018_df.shape)
#     print(enem2018_df.head())
    
    enem = process_enem_data(enem2018_df)
    print('Treated Enem Dataset: ', enem.shape)
#     print(enem.head())

    enem.to_csv(os.getcwd() + '/data/analysis/enem_analysis.csv', sep=';', index = False)

    print('ENEM process has been finalized')
    
def treatCities():
    brazil_cities_path = os.getcwd() + '/data/brazil_cities.csv'
    brazil_df = pd.read_csv(brazil_cities_path, delimiter=";")
    brazil_df.fillna(0, inplace=True)

    print('Original Cities Dataset: ', brazil_df.shape)
#     print(brazil_df.head())

    brazil = process_cities_data(brazil_df)
    print('Treated Cities Dataset: ', brazil.shape)
#     print(brazil.head())

    brazil.to_csv(os.getcwd() + '/data/analysis/cities_analysis.csv', sep=';', index = False)

    print('Process of Brazilian cities has been finalized')

if __name__ == "__main__":
    treatEnem()
    treatCities()