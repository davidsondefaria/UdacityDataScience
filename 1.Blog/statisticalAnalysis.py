import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def meanTestFiltered(test):
    """
        Calculates only the average of the test of the students who take the test.
        Parameters:
            test: dataframe with presence and grade columns.
        Returns:
            dictionary with average, min and max grades.
    """
    import re
    grades = []
    presence = 0
    for i, r in test.iterrows():
        if r[list(filter(lambda col: re.search("(presence|status)", col), test.columns))[0]] >= 1.0:
            grades.append(r[list(filter(lambda col: re.search("grade", col), test.columns))[0]])
            presence+=1
    return({ 'presence': presence
           , 'mean': sum(grades)/len(grades)
           , 'min': min(grades)
           , 'max': max(grades)
           })
        

def avgGrade(enem, onlyPresent=True):
    """
        Returns average grade of each test.
        Parameters:
            enem (pandas dataframe): ENEM dataframe that contains all grades.
            onlyPresent (boolean): TRUE if you only want the grades of the students who took the test. FALSE if you want all the grades.
        Returns:
            dictionary with test content and their respective averages, min e max grades.
    """
    if onlyPresent:
        return { 'natural_science': { 'presence': enem['presence_natural_science'].sum()
                                     ,'mean': enem.replace(0, np.NaN)['grade_natural_science'].mean()
                                     ,'min': enem.replace(0, np.NaN)['grade_natural_science'].min()
                                     ,'max': enem.replace(0, np.NaN)['grade_natural_science'].max()
                                    }
                ,'human_science': { 'presence': enem['presence_human_science'].sum()
                                   ,'mean': enem.replace(0, np.NaN)['grade_human_science'].mean()
                                   ,'min': enem.replace(0, np.NaN)['grade_human_science'].min()
                                   ,'max': enem.replace(0, np.NaN)['grade_human_science'].max()
                                  }
                ,'languages': { 'presence': enem['presence_languages'].sum()
                               , 'mean': enem.replace(0, np.NaN)['grade_languages'].mean()
                               ,'min': enem.replace(0, np.NaN)['grade_languages'].min()
                               ,'max': enem.replace(0, np.NaN)['grade_languages'].max()
                              }
                ,'math': { 'presence': enem['presence_math'].sum()
                          ,'mean': enem.replace(0, np.NaN)['grade_math'].mean()
                          ,'min': enem.replace(0, np.NaN)['grade_math'].min()
                          ,'max': enem.replace(0, np.NaN)['grade_math'].max()
                         }
                ,'essay': { 'presence': enem.replace(0, np.NaN)['essay_status'].count()
                           ,'mean': enem.replace(0, np.NaN)['grade_essay'].mean()
                           ,'min': enem.replace(0, np.NaN)['grade_essay'].min()
                           ,'max': enem.replace(0, np.NaN)['grade_essay'].max()
                          }
               }
    else:
        return { 'natural_science': { 'mean': enem['grade_natural_science'].mean()
                                     ,'min': enem['grade_natural_science'].min()
                                     ,'max': enem['grade_natural_science'].max()
                                    }
                ,'human_science': { 'mean': enem['grade_human_science'].mean()
                                   ,'min': enem['grade_human_science'].min()
                                   ,'max': enem['grade_human_science'].max()
                                  }
                ,'languages': { 'mean': enem['grade_languages'].mean()
                               ,'min': enem['grade_languages'].min()
                               ,'max': enem['grade_languages'].max()
                              }
                ,'math': { 'mean': enem['grade_math'].mean()
                          ,'min': enem['grade_math'].min()
                          ,'max': enem['grade_math'].max()
                         }
                ,'essay': { 'mean': enem['grade_essay'].mean()
                           ,'min': enem['grade_essay'].min()
                           ,'max': enem['grade_essay'].max()
                          }
               }
        
def gradeHDIRelation( enem, cities, onlyPresent=True
                     ,lines=['hdi', 'hdi_gni', 'hdi_life', 'hdi_education']
                     ,columns=['grade_natural_science', 'grade_human_science', 'grade_languages', 'grade_math', 'grade_essay']
                    ):
    """
        Relates the average scores for each test to the cities' HDI, makes a graph and returns the dataset with the average scores for each city.
        Parameters:
            enem (pandas dataframe): ENEM dataframe that contains all grades.
            cities (pandas dataframe): Cities dataframe that contains all hdi.
            onlyPresent (boolean): TRUE if you only want the grades of the students who took the test. FALSE if you want all the grades.
            lines (list): list of all hdi that you want to plot. MAX length = 4.
            columns (list): list of all test content that you want to plot.
        Returns:
            Cities dataframe with average grades columns.
    """
    cities = cities[cities.columns[~cities.columns.isin(['capital'])]]
    if onlyPresent:
        mean_by_city = enem.replace(0, np.NaN).groupby(['city_residence','state_residence'], as_index=False).mean()
    else:
        mean_by_city = enem.groupby(['city_residence','state_residence'], as_index=False).mean()
    cities_avg = pd.merge(cities, mean_by_city, how='inner', left_on=['city','state'], right_on=['city_residence','state_residence'])
    df = cities_avg[~(cities_avg == 0).any(axis=1)]
    
    fig = plt.figure()
    for i in range(len(lines)):
        ax = fig.add_subplot(2, 2, i+1)
        df.sort_values(by=lines[i]).plot(kind='line', x=lines[i], y=columns, ax=ax, figsize=(20, 15))

    return cities_avg

def gradeSchoolRelation( enem, onlyPresent=True
                        ,lines=['Uninformed', 'Public school', 'Private school', 'Foreign school']
                        ,columns=['grade_natural_science', 'grade_human_science', 'grade_languages', 'grade_math', 'grade_essay']
                       ):
    """
        Lists the average grades by type of school, places them on a bar graph and returns the dataset with the average grades for each type.
        Parameters:
            enem (pandas dataframe): ENEM dataframe that contains all grades.
            onlyPresent (boolean): TRUE if you only want the grades of the students who took the test. FALSE if you want all the grades.
            lines (list): list of all school types that you want to plot.
            columns (list): list of all test content that you want to plot.
        Returns:
            Tuple:
                0: Dictionary with average difference beetwen school types.
                1: Dataframe with average grades by type of school.
    """
    
    if onlyPresent:
        mean_by_school = enem.replace(0, np.NaN).groupby(['school_type'], as_index=False).mean()
    else:
        mean_by_school = enem.groupby(['school_type'], as_index=False).mean()
    
    diff_public_private = {content+'_diff': mean_by_school.loc[mean_by_school['school_type'] == 3, content].values[0] \
                       - mean_by_school.loc[mean_by_school['school_type'] == 2, content].values[0] \
                       for content in mean_by_school.keys()[1:]}

    diff_public_foreign = {content+'_diff': mean_by_school.loc[mean_by_school['school_type'] == 4, content].values[0] \
                           - mean_by_school.loc[mean_by_school['school_type'] == 2, content].values[0] \
                           for content in mean_by_school.keys()[1:]}

    diff_private_foreign = {content+'_diff': mean_by_school.loc[mean_by_school['school_type'] == 4, content].values[0] \
                           - mean_by_school.loc[mean_by_school['school_type'] == 3, content].values[0] \
                           for content in mean_by_school.keys()[1:]}

    diff = { 'avg_diff_private_public': diff_public_private
           , 'avg_diff_foreign_public': diff_public_foreign
           , 'avg_diff_foreign_private': diff_private_foreign
           }

    df = mean_by_school
    for i in range(len(lines)):
        df.loc[(df['school_type'] == i+1),'school_type'] = lines[i]
    
    df.plot(kind='bar', x='school_type', y=columns, figsize=(10, 8), grid=True)
        
    return (diff, df)

