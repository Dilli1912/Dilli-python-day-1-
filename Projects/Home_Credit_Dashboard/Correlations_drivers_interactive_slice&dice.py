import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Utils.data_prep import load_data
df = pd.read_csv("application_train.csv")

st.title("🪢 Correlations,Drivers & Interactive Slice and Dice")

st.title("KPIs(10)")


df['AGE_YEARS'] = -df['DAYS_BIRTH'] / 365.25
df['EMPLOYMENT_YEARS'] = -df['DAYS_EMPLOYED'] / 365.25
df['DTI'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
df['LTI'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']


gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df['CODE_GENDER'].dropna().unique()))
education = st.sidebar.selectbox("Education", ["All"] + sorted(df['NAME_EDUCATION_TYPE'].dropna().unique()))
filtered_df = df.copy()
if gender != "All":
    filtered_df = filtered_df[filtered_df['CODE_GENDER'] == gender]
if education != "All":
    filtered_df = filtered_df[filtered_df['NAME_EDUCATION_TYPE'] == education]


corrs = filtered_df.corr(numeric_only=True)
target_corr = corrs['TARGET'].drop('TARGET', errors='ignore')
top_5_pos = target_corr.sort_values(ascending=False).head(5).round(3)
top_5_neg = target_corr.sort_values().head(5).round(3)

income_corrs = corrs['AMT_INCOME_TOTAL'].drop('AMT_INCOME_TOTAL', errors='ignore')
credit_corrs = corrs['AMT_CREDIT'].drop('AMT_CREDIT', errors='ignore')
most_corr_income = income_corrs.abs().idxmax()
most_corr_credit = credit_corrs.abs().idxmax()

variance_explained = np.sum(np.abs(target_corr.sort_values(ascending=False)[:5]))
num_high_corr = (np.abs(target_corr) > 0.5).sum()

kpi_rows = [
    ["Top 5 +Corr with TARGET", ', '.join(f"{f}: {v}" for f, v in top_5_pos.items())],
    ["Top 5 −Corr with TARGET", ', '.join(f"{f}: {v}" for f, v in top_5_neg.items())],
    ["Most correlated with Income", most_corr_income],
    ["Most correlated with Credit", most_corr_credit],
    ["Corr(Income, Credit)", round(corrs.loc['AMT_INCOME_TOTAL', 'AMT_CREDIT'], 3)],
    ["Corr(Age, TARGET)", round(corrs.loc['AGE_YEARS', 'TARGET'], 3)],
    ["Corr(Employment Years, TARGET)", round(corrs.loc['EMPLOYMENT_YEARS', 'TARGET'], 3)],
    ["Corr(Family Size, TARGET)", round(corrs.loc['CNT_FAM_MEMBERS', 'TARGET'], 3)],
    ["Variance Explained by Top 5 Features", variance_explained.round(3)],
    ["Features with |corr| > 0.5", int(num_high_corr)]
]
st.table(pd.DataFrame(kpi_rows, columns=["KPI", "Value"]))

st.title("Graphs(10)")

num_cols_for_heatmap = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'CNT_CHILDREN', 'CNT_FAM_MEMBERS', 'TARGET']
corr_selected = filtered_df[num_cols_for_heatmap].corr()
fig1, ax1 = plt.subplots()
sns.heatmap(corr_selected, annot=True, cmap='magma', ax=ax1)
ax1.set_title('1.Correlation Heatmap: Selected Numeric Features')
st.pyplot(fig1)


target_corr_abs = np.abs(target_corr).sort_values(ascending=False)
fig2, ax2 = plt.subplots()
target_corr_abs[:10].plot.bar(ax=ax2)
ax2.set_title('2.Top |Correlation| of Features vs TARGET')
ax2.set_xlabel('Feature')
ax2.set_ylabel('|Correlation|')
st.pyplot(fig2)


fig3, ax3 = plt.subplots()
sns.scatterplot(x='AGE_YEARS', y='AMT_CREDIT', hue='TARGET', data=filtered_df, alpha=0.6, ax=ax3)
ax3.set_title('3.Age vs Credit (Hue=TARGET)')
ax3.set_xlabel('Age (Years)')
ax3.set_ylabel('Credit Amount')
st.pyplot(fig3)


fig4, ax4 = plt.subplots()
sns.scatterplot(x='AGE_YEARS', y='AMT_INCOME_TOTAL', hue='TARGET', data=filtered_df, alpha=0.6, ax=ax4)
ax4.set_title('4.Age vs Income (Hue=TARGET)')
ax4.set_xlabel('Age (Years)')
ax4.set_ylabel('Annual Income')
st.pyplot(fig4)


fig5, ax5 = plt.subplots()
sns.stripplot(x='TARGET', y='EMPLOYMENT_YEARS', data=filtered_df, jitter=True, ax=ax5)
ax5.set_title('5.Employment Years vs TARGET')
ax5.set_xticklabels(['Repaid', 'Default'])
ax5.set_xlabel('Status')
ax5.set_ylabel('Employment Years')
st.pyplot(fig5)


fig6, ax6 = plt.subplots()
sns.boxplot(x='NAME_EDUCATION_TYPE', y='AMT_CREDIT', data=filtered_df, ax=ax6)
ax6.set_title('6.Credit Amount by Education')
ax6.set_xlabel('Education Type')
ax6.set_ylabel('Credit Amount')
plt.xticks(rotation=90)
st.pyplot(fig6)


fig7, ax7 = plt.subplots()
sns.boxplot(x='NAME_FAMILY_STATUS', y='AMT_INCOME_TOTAL', data=filtered_df, ax=ax7)
ax7.set_title('7.Income by Family Status')
ax7.set_xlabel('Family Status')
ax7.set_ylabel('Annual Income')
plt.xticks(rotation=45)
st.pyplot(fig7)


pairplot_cols = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'TARGET']
pp_fig = sns.pairplot(filtered_df[pairplot_cols], hue='TARGET', diag_kind='kde', plot_kws={'alpha':0.5})
st.pyplot(pp_fig.fig)


rate_by_gender = filtered_df.groupby('CODE_GENDER')['TARGET'].mean() * 100
fig9, ax9 = plt.subplots()
rate_by_gender.plot.bar(ax=ax9, color='skyblue')
ax9.set_title('9.Default Rate by Gender (Filtered)')
ax9.set_xlabel('Gender')
ax9.set_ylabel('Default Rate (%)')
st.pyplot(fig9)


rate_by_edu = filtered_df.groupby('NAME_EDUCATION_TYPE')['TARGET'].mean() * 100
fig10, ax10 = plt.subplots()
rate_by_edu.plot.bar(ax=ax10, color='teal')
ax10.set_title('10.Default Rate by Education (Filtered)')
ax10.set_xlabel('Education Type')
ax10.set_ylabel('Default Rate (%)')
plt.xticks(rotation=0)
st.pyplot(fig10)

st.title("_____________________________")

st.markdown("""
**Insights & Policy Recommendations:**
- Features like employment stability, income, and annuity show notable correlations with default risk, supporting the use of caps on LTI and minimum income thresholds.
- Young, single, lower-income applicants with unstable employment are high-risk segments.
- Use strong drivers from the correlation analysis to refine policy: e.g., require minimum employment years, limit LTI to <6, and mandate higher income for high credit applicants.
""")