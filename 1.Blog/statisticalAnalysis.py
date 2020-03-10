import re
import os
import pandas as pd

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
        return { 'natural_science': meanTestFiltered(enem[['presence_natural_science', 'grade_natural_science']])
                ,'human_science': meanTestFiltered(enem[['presence_human_science', 'grade_human_science']])
                ,'languages': meanTestFiltered(enem[['presence_languages', 'grade_languages']])
                ,'math': meanTestFiltered(enem[['presence_math', 'grade_math']])
                ,'essay': meanTestFiltered(enem[['essay_status', 'grade_essay']])
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
        
# {'mean_grade_natural_science': []
# ,'mean_grade_human_science': []
# ,'mean_grade_languages': []
# ,'mean_grade_math': []
# ,'mean_grade_essay': []}
