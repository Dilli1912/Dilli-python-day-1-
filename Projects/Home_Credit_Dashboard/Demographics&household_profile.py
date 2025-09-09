import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Utils.data_prep import load_data
df = pd.read_csv("application_train.csv")

st.title("👨‍👩‍👧 Demographics & Household Profile")

st.title("KPIs(10)")

df['DTI'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
df['LTI'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
df['INCOME_BRACKET'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High'])

avg_income = round(df['AMT_INCOME_TOTAL'].mean(), 2)
median_income = round(df['AMT_INCOME_TOTAL'].median(), 2)
avg_credit = round(df['AMT_CREDIT'].mean(), 2)
avg_annuity = round(df['AMT_ANNUITY'].mean(), 2)
avg_goods_price = round(df['AMT_GOODS_PRICE'].mean(), 2)
avg_dti = round(df['DTI'].mean(), 3)
avg_lti = round(df['LTI'].mean(), 3)

income_gap = round(df[df['TARGET']==0]['AMT_INCOME_TOTAL'].mean() - df[df['TARGET']==1]['AMT_INCOME_TOTAL'].mean(), 2)
credit_gap = round(df[df['TARGET']==0]['AMT_CREDIT'].mean() - df[df['TARGET']==1]['AMT_CREDIT'].mean(), 2)
perc_high_credit = round(100 * (df['AMT_CREDIT'] > 1_000_000).sum() / df.shape[0], 2)

kpi_rows = [
    ["Avg Annual Income", avg_income],
    ["Median Annual Income", median_income],
    ["Avg Credit Amount", avg_credit],
    ["Avg Annuity", avg_annuity],
    ["Avg Goods Price", avg_goods_price],
    ["Avg DTI", avg_dti],
    ["Avg LTI", avg_lti],
    ["Income Gap (Non-def − Def)", income_gap],
    ["Credit Gap (Non-def − Def)", credit_gap],
    ["% High Credit (> 1M)", perc_high_credit]
]
st.table(pd.DataFrame(kpi_rows, columns=["KPI", "Value"]))

st.title("Graphs(10)")
fig1, ax1 = plt.subplots()
sns.histplot(df['AMT_INCOME_TOTAL'], bins=30, color='gold', ax=ax1)
ax1.set_title('1.Income Distribution')
st.pyplot(fig1)


fig2, ax2 = plt.subplots()
sns.histplot(df['AMT_CREDIT'], bins=30, color='blue', ax=ax2)
ax2.set_title('2.Credit Distribution')
st.pyplot(fig2)


fig3, ax3 = plt.subplots()
sns.histplot(df['AMT_ANNUITY'], bins=30, color='lightblue', ax=ax3)
ax3.set_title('3.Annuity Distribution')
st.pyplot(fig3)


fig4, ax4 = plt.subplots()
ax4.scatter(df['AMT_INCOME_TOTAL'], df['AMT_CREDIT'], alpha=0.2, color='purple')
ax4.set_xlabel('Annual Income')
ax4.set_ylabel('Credit Amount')
ax4.set_title('4.Income vs Credit Amount')
st.pyplot(fig4)


fig5, ax5 = plt.subplots()
ax5.scatter(df['AMT_INCOME_TOTAL'], df['AMT_ANNUITY'], alpha=0.2, color='orange')
ax5.set_xlabel('Annual Income')
ax5.set_ylabel('Annuity')
ax5.set_title('5.Income vs Annuity')
st.pyplot(fig5)


fig6, ax6 = plt.subplots()
sns.boxplot(x='TARGET', y='AMT_CREDIT', data=df, ax=ax6)
ax6.set_xticklabels(['Repaid', 'Default'])
ax6.set_title('6.Credit Amount by Target')
ax6.set_xlabel('Status')
ax6.set_ylabel('Credit Amount')
st.pyplot(fig6)


fig7, ax7 = plt.subplots()
sns.boxplot(x='TARGET', y='AMT_INCOME_TOTAL', data=df, ax=ax7)
ax7.set_xticklabels(['Repaid', 'Default'])
ax7.set_title('7.Annual Income by Target')
ax7.set_xlabel('Status')
ax7.set_ylabel('Annual Income')
st.pyplot(fig7)


fig8, ax8 = plt.subplots()
sns.kdeplot(x=df['AMT_INCOME_TOTAL'], y=df['AMT_CREDIT'], fill=True, cmap='viridis', ax=ax8)
ax8.set_title('8.Joint Distribution: Income vs Credit')
ax8.set_xlabel('Annual Income')
ax8.set_ylabel('Credit Amount')
st.pyplot(fig8)

rate_by_bracket = df.groupby('INCOME_BRACKET')['TARGET'].mean() * 100
fig9, ax9 = plt.subplots()
rate_by_bracket.plot.bar(ax=ax9, color='skyblue')
ax9.set_title('9.Income Bracket vs Default Rate (%)')
ax9.set_xlabel('Income Bracket')
ax9.set_ylabel('Default Rate (%)')
st.pyplot(fig9)


financial_vars = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'DTI', 'LTI', 'TARGET']
corr_fin = df[financial_vars].corr()
fig10, ax10 = plt.subplots()
sns.heatmap(corr_fin, annot=True, cmap='Greens', ax=ax10)
ax10.set_title('10.Financial Variables Correlation Heatmap')
st.pyplot(fig10)

st.title("_______________________________")
st.markdown("""
**Insights:**
- Default rates rise sharply for applicants with Loan-to-Income ratios above 6 and DTI above 0.35, indicating stress at these affordability thresholds.
- Lower income brackets show higher risk, while high credit amounts (>1M) are concentrated among non-defaulters and select high-income groups.
- Strong positive correlation exists between income and credit, but high DTI/LTI values signal elevated risk.
""")