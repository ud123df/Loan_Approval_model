import streamlit as st
import pandas as pd 
import numpy as np 
import joblib
import altair as alt

# Load model and data
approval = joblib.load('loan_approval.joblib')
data = pd.read_csv("loan_data.csv")

# Title
st.set_page_config(
  page_title = "Loan Approval Dashboard",
  layout = "wide"
)
st.title("Loan Approval Dashboard")


# Options
employment_options = {
    'Salaried': 0,
    'Self-Employed': 1, 
    'Student': 2, 
    'Unemployed': 3
}
employment_type_reverse = {v: k for k, v in employment_options.items()}
data['employment_type_label'] = data['Employment_Type'].map(employment_type_reverse)
loan_purpose = {
    'Debt_Consolidation': 1,
    'Business': 0,
    'Education': 2,
    'Home_Improvement': 3,
    'Other': 5,
    'Medical': 4
}
loan_purpose_reverse = {v: k for k, v in loan_purpose.items()}
data['loan_purpose_label'] = data['Loan_Purpose'].map(loan_purpose_reverse)
# CSS styling
st.markdown("""
<style>
/* Button styling */
div.stButton > button:first-child {
    background-color:#0099FF !important;
    color:white !important;
    padding:12px 30px !important;
    border:none !important;
    border-radius:10px !important;
    box-shadow:0px 0px 10px rgba(0,153,255,0.6);
    font-size:18px;
}
div.stButton > button:first-child:hover {
    transform:scale(1.26) !Important;        
    background-color:white !important;
    color:#0099FF !important;
    border:2px solid #0099FF !important;
    box-shadow:2px 3px 15px !Important;        
}


</style>
""", unsafe_allow_html=True)

# Sidebar menu
page = st.sidebar.selectbox('Menu', ["Model", "Charts"]) 



if page == "Model":
    # Input variables
    st.markdown("<div class='inputs'>", unsafe_allow_html=True)
    Age = st.number_input("Enter the Age", 0)
    Employment_Type_label = st.selectbox("Employment Type", list(employment_options.keys()))
    Employment_Type = employment_options[Employment_Type_label]
    Annual_Income = st.number_input("Annual Income", 0)
    Credit_Score = st.number_input("Credit Score", 0)
    Loan_Amount = st.number_input("Loan Amount", 0)
    Loan_Term_Months = st.number_input("Loan Term Months", 0)
    Loan_Purposes = st.selectbox("Loan Purpose", list(loan_purpose.keys()))
    Loan_Purpose = loan_purpose[Loan_Purposes]
    Debt_to_Income_Ratio = st.number_input("Debt to Income Ratio", 0)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='checkbox'>", unsafe_allow_html=True)
    if st.button("Check"):
        input_data = np.array([[Age, Employment_Type, Annual_Income, Credit_Score,
                                Loan_Amount, Loan_Term_Months, Loan_Purpose, Debt_to_Income_Ratio]])
        prediction = approval.predict(input_data)[0]
        if prediction == 1:
            st.success("Approved")
        else:
            st.error("Not Approved")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Charts
    st.subheader("Loan Data Visuals")
    tab1, tab2= st.tabs(["Insome Trends & Credit Score", "Loan Insights &Loan_Amount"])
    # col1, col2 = st.columns(2)
    with tab1:
      col1, col2 = st.columns(2)

      #chart 1

      with col1:
        st.write('### Annual Income by Age')
        chart1 = alt.Chart(data).mark_line(color="#33C706", strokeWidth=2).encode(
            x = 'Age',
            y = 'Annual_Income'
        ).properties(
            width = 'container',
            height = 350
        ).interactive()
        # interactive_chart = line.interactive()
        # chart = chart1.interactive()

        st.altair_chart(chart1, use_container_width=True)
          #chart 2
      with col2:
        st.write('### Credit Score Spread')
        scatter = alt.Chart(data).mark_circle(size = 40, opacity = 0.4).encode(
            x = 'Age', 
            y = 'Credit_Score',
            color=alt.Color('Credit_Score',legend = alt.Legend(orient='right'), scale = alt.Scale(scheme ='blues')),
            tooltip=['Age', 'Credit_Score']
        ).properties(height = 350).interactive()
        st.altair_chart(scatter, use_container_width = True)
    # tab3, tab4 = st.tabs(["Loan Insights", "Loan_Amount"])  
    # col3, col4 = st.columns(2)
    #chart 3
      barh = alt.Chart(data).mark_bar().encode(
         y = alt.Y('loan_purpose_label:N', sort = '-x'),
         x= 'Loan_Amount:Q',
          color = 'loan_purpose_label:N'
      ).properties(
         title = "Loan Purose Distribution"
      ).interactive()
      st.altair_chart(barh, use_container_width = True)  


      #tab 2    


    with tab2:
      #chart 4
      col3, col4 = st.columns(2)
      with col3:
        st.write('### Loan amount / credit score')
        bar = alt.Chart(data).mark_bar(opacity = 0.6).encode(
            x = 'Credit_Score', 
            y = 'Loan_Amount',
            color = alt.Color('Credit_Score', scale=alt.Scale(scheme = 'redblue')),
            tooltip=['Credit_Score', 'Loan_Amount']
        ).properties(height = 350).interactive()
        st.altair_chart(bar, use_container_width = True)
    #chart 5
      with col4:
        st.write('### Annual_Income by Loan_Amount')
        bar = alt.Chart(data).mark_point(opacity = 0.6).encode(
            x = 'Loan_Amount',
            y = 'Annual_Income',
            color = alt.Color('Loan_Amount', scale=alt.Scale(scheme='bluegreen')),
            tooltip = ['Annual_Income', 'Loan_Amount']
        ).properties(height = 350, width = 450).interactive()
        st.altair_chart(bar, use_container_width = True)

    #chart 6
    
      pie = alt.Chart(data).mark_arc(innerRadius=60).encode(
         theta = "employment_type_label",
         color = "Annual_Income"
      ).interactive()
      st.altair_chart(pie, use_container_width = True)