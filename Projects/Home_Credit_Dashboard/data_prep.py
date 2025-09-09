import pandas as pd
import streamlit as st
import numpy as np


def load_data(file_path="application_train.csv"):
    ###Preprocessing
    ###Load data
    df = pd.read_csv(file_path)
    ###Convert Ages
    df['AGE_YEARS']=(-df['DAYS_BIRTH'])/365.25
    ###Employment Tenure
    df['EMPLOYMENT_YEARS']=(-df['DAYS_EMPLOYED'])/365.25
    df.loc[df['EMPLOYMENT_YEARS']>100,'EMPLOYMENT_YEARS']=np.nan
    ###Create ratios
    df['DTI']=df['AMT_ANNUITY']/df['AMT_INCOME_TOTAL']
    df['LOAN_TO_INCOME']=df['AMT_CREDIT']/df['AMT_INCOME_TOTAL']
    df['ANNUITY_TO_CREDIT']=df['AMT_ANNUITY']/df['AMT_CREDIT']
    ###Handle missing values
    missing_percent=df.isnull().mean()*100
    df=df.loc[:,missing_percent<=60]
    for col in df.columns:
        if df[col].dtype in ['float64','int64']:
            df[col].fillna(df[col].median(),inplace=True)
        else:
            df[col].fillna(df[col].mode()[0],inplace=True)
    ###income brackets
    df['INCOME_BRACKET']=pd.qcut(df['AMT_INCOME_TOTAL'],q=[0,0.25,0.75,1.0],labels=['low','mid','high'])
    ####Sidebar radio with 5 pages
    page = st.sidebar.radio('Navigation', ['Overview & Data Quality', 'Target & Risk Segmentation',
                                      'Demographics & Household Profile', 'Financial Health & Affordability',
                                      'Correlations, Drivers & Interactive Slice-and-Dice'])
     # Global filters: Gender, Education, Family Status, Housing Type, Age range, Income bracket
    gender_filter = st.sidebar.multiselect('Gender', options=df['CODE_GENDER'].unique(), default=df['CODE_GENDER'].unique())
    filtered_df = df[df['CODE_GENDER'].isin(gender_filter)]
    # Add filters for education, family status, etc.
    min_age=18
    max_age=65
    filtered_df = filtered_df[(filtered_df['AGE_YEARS'] >= min_age) & (filtered_df['AGE_YEARS'] <= max_age)]
    return df