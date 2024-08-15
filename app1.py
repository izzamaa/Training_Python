import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title= "Demo Dashboard",
    page_icon= "💸",
    layout="wide"
    )

st.title("📈 Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("---")

# Sidebar section
st.sidebar.title("Dashboard Filters and Features")

# List of Features
st.sidebar.header("Features")
st.sidebar.write("""
- **Overview**: Provides a summary of key loan metrics.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
""")

loan = pd.read_pickle('data_input/loan_clean')

with st.container(border=True):

    # First row of two columns
    col1, col2 = st.columns(2)

    # Metrics for the first row
    col1.metric("Total Loans", f"{loan.shape[0]:,}", help="total number of loans")
    col1.metric("Total Loan Amount", f"${loan['loan_amount'].sum():,.0f}", help="sum of all loan amounts")

    col2.metric("Average Interest Rate", f"{loan['interest_rate'].mean():.0f}%", help="percentage of the loan amount that the borrower has to pay")
    col2.metric("Average Loan Amount", f"${loan['loan_amount'].mean():,.0f}", help="average interest rate across all loans")

st.markdown("---")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs([
        'Loans Issued Over Time',
        'Loan Amount Over Time',
        'Issue Date Analysis'
    ])

    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count().sort_index()
        line_count = px.line(
            loan_date_count,
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
	        },
            template='seaborn',
            markers = True
        ).update_layout(showlegend=False)
        st.plotly_chart(line_count)

    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum().sort_index()
        line_sum = px.line(
            loan_date_sum,
            labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
	        },
            template='seaborn',
            markers = True
        ).update_layout(showlegend=False)
        st.plotly_chart(line_sum)
    
    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        bar_count = px.bar(
            loan_day_count,
            title='Distribution of Loans by Day of the Week',
            labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
	        },
            template='seaborn',
            category_orders= {
            'issue_weekday' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            } 
        ).update_layout(showlegend=False)
        st.plotly_chart(bar_count)

st.markdown("---")

st.header("Loan Performance")

with st.expander("", expanded=True):

    column1, column2 = st.columns(2)

    with column1:
        pie = px.pie(
            loan,
            title='Distribution of Loans by Condition',
            names = 'loan_condition',
            hole = 0.5,
            template = 'seaborn'
            ).update_traces(textinfo='percent + value')
        st.plotly_chart(pie)

    with column2:
        grade = loan['grade'].value_counts().sort_index()
        bar = px.bar(
            grade,
            title='Distribution of Loans by Grade',
            labels={
            'grade':'Grade',
            'value':'Number of Loans'
	        },
            template='seaborn'
            ).update_layout(showlegend=False)
        st.plotly_chart(bar)

# st.markdown("---")

# st.header('Financial Analysis')

# loan_conditions = loan['loan_condition'].unique()

# selected_condition = st.selectbox(
#     "Select Loan Condition",
#     options=loan_conditions,
#     index=0 
# )

# condition = loan[loan['loan_condition'] == selected_condition]

# loan_amount_hist = px.histogram(
#     condition,
#     x='loan_amount',
#     nbins=30,  
#     color='term',
#     title='Loan Amount Distribution by Condition',
#     template='seaborn',
#     labels={
#         'loan_amount': 'Loan Amount',
#         'term': 'Loan Term'
#     }
# )

# loan_amount_box = px.box(
#     condition,
#     x='purpose',
#     y='loan_amount',
#     color='term',
#     title='Loan Amount Distribution by Purpose',
#     template='seaborn',
#     labels={
#         'loan_amount': 'Loan Amount',
#         'term': 'Loan Term',
#         'purpose': 'Loan Purpose'
#     }
# )

# with st.container(border=True):

#     tab1, tab2 = st.tabs([
#         'Loan Amount Distribution',
#         'Loan Amount Distribution by Purpose',
#     ])

#     with tab1:
#         st.plotly_chart(loan_amount_hist)

#     with tab2:
#         st.plotly_chart(loan_amount_box)