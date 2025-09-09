import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Utils.data_prep import load_data

df = pd.read_csv("application_train.csv")
st.title("🎯 Target & Risk Segmentation")

df['AGE_YEARS'] = (-df['DAYS_BIRTH']) / 365.25
df['EMPLOYMENT_YEARS'] = (-df['DAYS_EMPLOYED']) / 365.25
df.loc[df['EMPLOYMENT_YEARS'] > 100, 'EMPLOYMENT_YEARS'] = np.nan
st.title("KPIs(10)")
gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df['CODE_GENDER'].dropna().unique()))
education = st.sidebar.selectbox("Education", ["All"] + sorted(df['NAME_EDUCATION_TYPE'].dropna().unique()))
family_status = st.sidebar.selectbox("Family Status", ["All"] + sorted(df['NAME_FAMILY_STATUS'].dropna().unique()))
housing_type = st.sidebar.selectbox("Housing Type", ["All"] + sorted(df['NAME_HOUSING_TYPE'].dropna().unique()))


filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df['CODE_GENDER'] == gender]
if education != "All":
    filtered_df = filtered_df[filtered_df['NAME_EDUCATION_TYPE'] == education]
if family_status != "All":
    filtered_df = filtered_df[filtered_df['NAME_FAMILY_STATUS'] == family_status]
if housing_type != "All":
    filtered_df = filtered_df[filtered_df['NAME_HOUSING_TYPE'] == housing_type]

st.title("Target & Risk Segmentation")


defaults = filtered_df['TARGET'].sum()
default_rate = filtered_df['TARGET'].mean() * 100
default_gender = filtered_df.groupby('CODE_GENDER')['TARGET'].mean() * 100
default_education = filtered_df.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean() * 100
default_family = filtered_df.groupby('NAME_FAMILY_STATUS')['TARGET'].mean() * 100
avg_income_def = filtered_df[filtered_df['TARGET'] == 1]['AMT_INCOME_TOTAL'].mean()
avg_credit_def = filtered_df[filtered_df['TARGET'] == 1]['AMT_CREDIT'].mean()
avg_annuity_def = filtered_df[filtered_df['TARGET'] == 1]['AMT_ANNUITY'].mean()
avg_employment_def = filtered_df[filtered_df['TARGET'] == 1]['EMPLOYMENT_YEARS'].mean()
default_housing = filtered_df.groupby('NAME_HOUSING_TYPE')['TARGET'].mean() * 100

kpi_data = {
    "Total Defaults": defaults,
    "Default Rate (%)": round(default_rate,2),
    "Default Rate by Gender (%)": default_gender.round(2).to_dict(),
    "Default Rate by Education (%)": default_education.round(2).to_dict(),
    "Default Rate by Family Status (%)": default_family.round(2).to_dict(),
    "Avg Income – Defaulters": round(avg_income_def,2),
    "Avg Credit – Defaulters": round(avg_credit_def,2),
    "Avg Annuity – Defaulters": round(avg_annuity_def,2),
    "Avg Employment (Years) – Defaulters": round(avg_employment_def,2),
    "Default Rate by Housing Type (%)": default_housing.round(2).to_dict()
}
kpi_df = pd.DataFrame(kpi_data.items(), columns=['KPI', 'Value'])
st.table(kpi_df)

st.title("Graphs(10)")

fig1, ax1 = plt.subplots()
filtered_df['TARGET'].value_counts().sort_index().plot.bar(ax=ax1, color=['green', 'red'])
ax1.set_xticklabels(['Repaid', 'Default'], rotation=0)
ax1.set_title('Counts: Default vs Repaid')
ax1.set_xlabel('Status')
ax1.set_ylabel('Count')
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
default_gender.plot.bar(ax=ax2, color=['skyblue', 'orange'])  # adjust colors as needed
ax2.set_title('Default Rate by Gender (%)')
ax2.set_xlabel('Gender')
ax2.set_ylabel('Default Rate (%)')
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
default_education.plot.bar(ax=ax3, color='blue')
ax3.set_title('Default Rate by Education (%)')
ax3.set_xlabel('Education')
ax3.set_ylabel('Default Rate (%)')
st.pyplot(fig3)

fig4, ax4 = plt.subplots()
default_family.plot.bar(ax=ax4, color='pink')
ax4.set_title('Default Rate by Family Status (%)')
ax4.set_xlabel('Family Status')
ax4.set_ylabel('Default Rate (%)')
st.pyplot(fig4)

fig5, ax5 = plt.subplots()
default_housing.plot.bar(ax=ax5, color='gold')
ax5.set_title('Default Rate by Housing Type (%)')
ax5.set_xlabel('Housing Type')
ax5.set_ylabel('Default Rate (%)')
st.pyplot(fig5)

fig6, ax6 = plt.subplots()
sns.boxplot(x='TARGET', y='AMT_INCOME_TOTAL', data=filtered_df, ax=ax6)
ax6.set_xticklabels(['Repaid', 'Default'])
ax6.set_title('Income by Target')
ax6.set_xlabel('Status')
ax6.set_ylabel('Annual Income')
st.pyplot(fig6)


fig7, ax7 = plt.subplots()
sns.boxplot(x='TARGET', y='AMT_CREDIT', data=filtered_df, ax=ax7)
ax7.set_xticklabels(['Repaid', 'Default'])
ax7.set_title('Credit by Target')
ax7.set_xlabel('Status')
ax7.set_ylabel('Credit Amount')
st.pyplot(fig7)


fig8, ax8 = plt.subplots()
sns.violinplot(x='TARGET', y='AGE_YEARS', data=filtered_df, ax=ax8, inner='box')
ax8.set_xticklabels(['Repaid', 'Default'])
ax8.set_title('Age vs Target')
ax8.set_xlabel('Status')
ax8.set_ylabel('Age (Years)')
st.pyplot(fig8)


fig9, ax9 = plt.subplots()
for t, color in zip([0, 1], ['green', 'red']):
    label = 'Repaid' if t == 0 else 'Default'
    sns.histplot(filtered_df[filtered_df['TARGET'] == t]['EMPLOYMENT_YEARS'], label=label, ax=ax9, alpha=0.6, color=color)
ax9.set_title('Employment Years by Target')
ax9.set_xlabel('Employment Years')
ax9.set_ylabel('Count')
ax9.legend()
st.pyplot(fig9)


df_contract = filtered_df.groupby(['NAME_CONTRACT_TYPE', 'TARGET']).size().unstack().fillna(0)
fig10, ax10 = plt.subplots()
df_contract.plot(kind='bar', stacked=True, ax=ax10, color=['blue', 'red'])
ax10.set_title('NAME_CONTRACT_TYPE vs Target')
ax10.set_xlabel('Contract Type')
ax10.set_ylabel('Applicants')
ax10.legend(['Repaid', 'Default'])
st.pyplot(fig10)

st.title("____________________________")
st.markdown("""
**Insights:**
- The highest default rates are observed among single applicants and those with lower education levels, suggesting that marital status and education may play an important role in credit risk.
- Applicants living in municipal housing and those with high loan-to-income ratios tend to default more frequently, possibly due to greater financial vulnerability and less household stability.
- In contrast, married applicants with higher incomes and stable employment show the lowest default rates, indicating that economic security and family support are protective factors.
- These patterns suggest focused strategies for risk management: prioritize additional checks for applicants who are single, have low income, or exhibit high debt-to-income ratios.
""")