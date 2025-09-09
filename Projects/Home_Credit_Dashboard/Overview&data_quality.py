import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Utils.data_prep import load_data

df = pd.read_csv("application_train.csv")
st.title("📊 Overview & Data Quality")
missing_perc=df.isnull().mean()*100

df['AGE_YEARS'] = (-df['DAYS_BIRTH']) / 365.25
df['EMPLOYMENT_YEARS'] = (-df['DAYS_EMPLOYED']) / 365.25
df.loc[df['EMPLOYMENT_YEARS'] > 100, 'EMPLOYMENT_YEARS'] = np.nan

st.title("KPIs(10)")


kpi_data = {
    "Total Applicants": df['SK_ID_CURR'].nunique(),
    "Default Rate (%)": round(df['TARGET'].mean() * 100, 2),
    "Repaid Rate (%)": round((1 - df['TARGET'].mean()) * 100, 2),
    "Total Features": df.shape[1],
    "Avg Missing per Feature (%)": round(df.isnull().mean().mean() * 100, 2),
    "Number Numerical Features": df.select_dtypes(include=[np.number]).shape[1],
    "Number Categorical Features": df.select_dtypes(include=['object']).shape[1],
    "Median Age (Years)": round(df['AGE_YEARS'].median(), 2),
    "Median Annual Income": round(df['AMT_INCOME_TOTAL'].median(), 2),
    "Average Credit Amount": round(df['AMT_CREDIT'].mean(), 2)
}
kpi_df = pd.DataFrame(kpi_data.items(), columns=['KPI', 'Value'])
st.table(kpi_df)


cols_to_drop = df.isnull().mean()[df.isnull().mean() > 0.60].index.tolist()
st.write(f"Columns to consider dropping (missing > 60%): {cols_to_drop}")

st.title("Graphs(10)")


fig1, ax1 = plt.subplots()
df['TARGET'].value_counts().plot.pie(autopct='%1.1f%%', colors=['green', 'red'], ax=ax1)
ax1.set_title('1.Target Distribution')
ax1.set_ylabel('')
st.pyplot(fig1)


fig2, ax2 = plt.subplots()
missing_perc.sort_values(ascending=False).head(20).plot.bar(color='blue', ax=ax2)
ax2.set_title('2.Top 20 Features by Missing %')
ax2.set_ylabel('% Missing')
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
sns.histplot(df['AGE_YEARS'], bins=30, kde=True, color='skyblue', ax=ax3)
ax3.set_title('3.Age Distribution (Years)')
st.pyplot(fig3)

fig4, ax4 = plt.subplots()
sns.histplot(df['AMT_INCOME_TOTAL'], bins=30, kde=True, color='gold', ax=ax4)
ax4.set_title('4.Annual Income Distribution')
st.pyplot(fig4)


fig5, ax5 = plt.subplots()
sns.histplot(df['AMT_CREDIT'], bins=30, kde=True, color='orange', ax=ax5)
ax5.set_title('5.Credit Amount Distribution')
st.pyplot(fig5)

fig6, ax6 = plt.subplots()
sns.boxplot(x=df['AMT_INCOME_TOTAL'], color='gold', ax=ax6)
ax6.set_title('6.Income Boxplot')
ax6.set_ylabel('Frequency')
st.pyplot(fig6)


fig7, ax7 = plt.subplots()
sns.boxplot(x=df['AMT_CREDIT'], color='grey', ax=ax7)
ax7.set_title('7.Credit Amount Boxplot')
ax7.set_ylabel('Frequency')
st.pyplot(fig7)

fig8, ax8 = plt.subplots()
sns.countplot(x='CODE_GENDER', data=df, palette='pastel', ax=ax8)
ax8.set_title('8.Gender Distribution')
st.pyplot(fig8)

fig9, ax9 = plt.subplots()
sns.countplot(y='NAME_FAMILY_STATUS', data=df, palette='viridis', order=df['NAME_FAMILY_STATUS'].value_counts().index, ax=ax9)
ax9.set_title('9.Family Status Counts')
st.pyplot(fig9)

fig10, ax10 = plt.subplots()
sns.countplot(y='NAME_EDUCATION_TYPE', data=df, palette='mako', order=df['NAME_EDUCATION_TYPE'].value_counts().index, ax=ax10)
ax10.set_title('10.Education Level Counts')
st.pyplot(fig10)

st.title("____________________________")
st.markdown("""
**Insights:**
- The age distribution is slightly right-skewed, indicating most applicants are middle-aged; younger applicants tend to have a higher default rate.
- Household profiles show many applicants are married and those with children, but a notable portion live with parents or alone―single applicants and smaller households show elevated risk.
- Education level is generally high among applicants, yet default risk persists even in higher-educated groups, and some occupation categories have much fewer records, which could signal missingness or inconsistent data entry.
""")