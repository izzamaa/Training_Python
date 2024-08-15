import streamlit as st
import pandas as pd
import plotly.express as px

loan = pd.read_pickle('data_input/loan_clean')

st.set_page_config(
    page_title= "Demo Dashboard",
    page_icon= "💸",
    layout="wide"
    )

st.title("📈 Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("---")

st.header('Financial Analysis')

loan_conditions = loan['loan_condition'].unique()

selected_condition = st.selectbox(
    "Select Loan Condition",
    options=loan_conditions,
    index=0 
)

condition = loan[loan['loan_condition'] == selected_condition]

loan_amount_hist = px.histogram(
    condition,
    x='loan_amount',
    nbins=30,  
    color='term',
    title='Loan Amount Distribution by Condition',
    template='seaborn',
    labels={
        'loan_amount': 'Loan Amount',
        'term': 'Loan Term'
    }
)

loan_amount_box = px.box(
    condition,
    x='purpose',
    y='loan_amount',
    color='term',
    title='Loan Amount Distribution by Purpose',
    template='seaborn',
    labels={
        'loan_amount': 'Loan Amount',
        'term': 'Loan Term',
        'purpose': 'Loan Purpose'
    }
)

with st.container(border=True):

    tab1, tab2 = st.tabs([
        'Loan Amount Distribution',
        'Loan Amount Distribution by Purpose',
    ])

    with tab1:
        st.plotly_chart(loan_amount_hist)

    with tab2:
        st.plotly_chart(loan_amount_box)