import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Utils.data_prep import load_data


df = pd.read_csv("application_train.csv")
st.title("💰 Financial Health & Affordability")

st.title("KPIs(10)")

total = df.shape[0]
male = (df['CODE_GENDER'] == 'M').sum()
female = (df['CODE_GENDER'] == 'F').sum()
perc_male = round(100 * male / total, 2)
perc_female = round(100 * female / total, 2)

df['AGE_YEARS']=-df['DAYS_BIRTH']/365.25
df['EMPLOYMENT_YEARS']=-df['DAYS_EMPLOYED']/365.25
avg_age_default = round(df[df['TARGET'] == 1]['AGE_YEARS'].mean(), 2)
avg_age_nondefault = round(df[df['TARGET'] == 0]['AGE_YEARS'].mean(), 2)

perc_with_children = round(100 * (df['CNT_CHILDREN'] > 0).sum() / total, 2)
avg_family_size = round(df['CNT_FAM_MEMBERS'].mean(), 2)

family_status_counts = df['NAME_FAMILY_STATUS'].value_counts(normalize=True) * 100
perc_married = round(family_status_counts.get('Married', 0), 2)
perc_single = round(family_status_counts.get('Single / not married', 0), 2)

higher_ed_list = ['Academic degree', 'Higher education']
perc_high_ed = round(100 * df['NAME_EDUCATION_TYPE'].isin(higher_ed_list).sum() / total, 2)

perc_living_with_parents = round(100 * (df['NAME_HOUSING_TYPE'] == 'With parents').sum() / total, 2)

perc_working = round(100 * (df['OCCUPATION_TYPE'].notnull()).sum() / total, 2)
avg_employment_years = round(df['EMPLOYMENT_YEARS'].mean(), 2)

kpi_data = [
    ["% Male", perc_male],
    ["% Female", perc_female],
    ["Avg Age — Defaulters", avg_age_default],
    ["Avg Age — Non-Defaulters", avg_age_nondefault],
    ["% With Children", perc_with_children],
    ["Avg Family Size", avg_family_size],
    ["% Married", perc_married],
    ["% Single", perc_single],
    ["% Higher Education", perc_high_ed],
    ["% Living With Parents", perc_living_with_parents],
    ["% Currently Working", perc_working],
    ["Avg Employment Years", avg_employment_years]
]
st.table(pd.DataFrame(kpi_data, columns=["KPI", "Value"]))

st.title("Graphs(10)")

fig1, ax1 = plt.subplots()
sns.histplot(df['AGE_YEARS'], bins=30, color='skyblue', ax=ax1)
ax1.set_title('1.Age Distribution (All)')
ax1.set_xlabel('Age (Years)')
st.pyplot(fig1)


fig2, ax2 = plt.subplots()
sns.histplot(df[df['TARGET']==0]['AGE_YEARS'], color='green', label='Repaid', kde=True, bins=30, ax=ax2)
sns.histplot(df[df['TARGET']==1]['AGE_YEARS'], color='red', label='Default', kde=True, bins=30, ax=ax2)
ax2.set_title('2.Age Distribution by Target')
ax2.set_xlabel('Age (Years)')
ax2.legend()
st.pyplot(fig2)


fig3, ax3 = plt.subplots()
df['CODE_GENDER'].value_counts().plot.bar(color=['blue','pink'], ax=ax3)
ax3.set_title('3.Gender Distribution')
ax3.set_xlabel('Gender')
ax3.set_ylabel('Count')
st.pyplot(fig3)


fig4, ax4 = plt.subplots()
df['NAME_FAMILY_STATUS'].value_counts().plot.bar(ax=ax4)
ax4.set_title('4.Family Status Distribution')
ax4.set_xlabel('Family Status')
st.pyplot(fig4)


fig5, ax5 = plt.subplots()
df['NAME_EDUCATION_TYPE'].value_counts().plot.bar(ax=ax5)
ax5.set_title('5.Education Distribution')
ax5.set_xlabel('Education Type')
st.pyplot(fig5)


fig6, ax6 = plt.subplots()
df['OCCUPATION_TYPE'].value_counts().head(10).plot.bar(ax=ax6)
ax6.set_title('6.Top 10 Occupations')
ax6.set_xlabel('Occupation')
st.pyplot(fig6)


fig7, ax7 = plt.subplots()
df['NAME_HOUSING_TYPE'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax7)
ax7.set_title('7.Housing Type Distribution')
ax7.set_ylabel('')
st.pyplot(fig7)


fig8, ax8 = plt.subplots()
sns.countplot(x='CNT_CHILDREN', data=df, ax=ax8, palette='coolwarm')
ax8.set_title('8.Children Count Distribution')
ax8.set_xlabel('Number of Children')
st.pyplot(fig8)


fig9, ax9 = plt.subplots()
sns.boxplot(x='TARGET', y='AGE_YEARS', data=df, ax=ax9)
ax9.set_xticklabels(['Repaid', 'Default'])
ax9.set_title('9.Age vs Target')
ax9.set_xlabel('Status')
ax9.set_ylabel('Age (Years)')
st.pyplot(fig9)


corr_df = df[['AGE_YEARS', 'CNT_CHILDREN', 'CNT_FAM_MEMBERS', 'TARGET']].corr()
fig10, ax10 = plt.subplots()
sns.heatmap(corr_df, annot=True, cmap='YlGnBu', ax=ax10)
ax10.set_title('10.Correlation Heatmap')
st.pyplot(fig10)

st.title("___________________________")
st.markdown("""
**Insights:**
- Younger applicants and those with smaller families or no children appear to have higher default rates, potentially reflecting less financial stability in early career or single life stages.
- Older applicants and those with larger families tend to show lower default rates, possibly due to accumulated wealth, employment stability, and stronger support networks.
- The presence of children and increased family size may act as partial risk mitigators, as these groups often have deeper household resources and may prioritize loan repayment for family wellbeing.
""")