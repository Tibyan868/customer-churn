import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title='customer churn prediction',
    page_icon='',
    layout='centered'
)

st.title("customer churn prediction")
st.markdown("enter data to know whether the customer churn or not")
@st.cache_resource
def load_model():
    try:
        return pickle.load(open('model.pkl','rb'))
    except:
        return None
model=load_model()
if model is None:
    st.warning("not find the model")
with st.form('churn_form'):
    st.subheader("basic information")
    col1,col2=st.columns(2)
    with col1:
        gender=st.selectbox("(gender)",['Male','Female'])
        senior_citizen=st.selectbox("(senior citizen)",[0,1])
        partner=st.selectbox("(partner)",['yes','no'])
        depents=st.selectbox("(dependents)",['yes','no'])
        tenure=st.slider("(tenure)",min_value=0,max_value=72,value=12)
    with col2:
        contract = st.selectbox("(Contract)", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("(Paperless Billing)", ["Yes", "No"])
        payment_method = st.selectbox("(Payment Method)", [
            "Electronic check", "Mailed check", 
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly_charges = st.number_input("monthly payment($)", min_value=0.0, max_value=200.0, value=50.0)
        total_charges = st.number_input("total apyment($)", min_value=0.0, max_value=10000.0, value=500.0)

 
    submit_button = st.form_submit_button(label="🔍 prediction")

if submit_button:
    if model is None:
        st.error("error wile downloading..")
    else:
        input_data = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [senior_citizen],
            'Partner': [partner],
            'Dependents': [depents],
            'tenure': [tenure],
            'Contract': [contract],
            'PaperlessBilling': [paperless_billing],
            'PaymentMethod': [payment_method],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        })
        
        
        try:
            
            prediction = model.predict(input_data.values
            )
            prediction_proba = model.predict_proba(input_data)
            
            st.divider()
            st.subheader("prediction result")
            
            if prediction[0] == 1 or prediction[0] == 'Yes':
                st.error(f"⚠️ warrning customer will get out (Churn)**")
                st.write(f" {prediction_proba[0][1]*100:.2f}%`")
            else:
                st.success(f"✅ loyal cutomer will stay (Not Churn)**")
                st.write(f" {prediction_proba[0][0]*100:.2f}%`")
                
        except Exception as e:
            st.error(f"error occure")