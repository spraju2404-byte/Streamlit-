import streamlit as st
import pandas as pd
import numpy as np
import io
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def set_bg_hack(main_bg):
    
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("{main_bg}");
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack('https://images3.alphacoders.com/133/1337141.png')
st.title("💻 Data Science & Machine Learning")

# 1. File Upload Section
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.success("CSV file loaded successfully!")
        
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.success("Excel file loaded successfully!")
        
        if not df.empty:
            st.subheader("Data Preview")
            col1, col2 = st.columns(2)
            with col1:
                st.write("First 5 Rows")
                st.dataframe(df.head(5)) 
            with col2:
                st.write("Last 5 Rows")
                st.dataframe(df.tail(5)) 

            # 2. Data Cleaning Section
            st.subheader("Missing Values Check")
            st.write(df.isnull().sum())

            # Fill missing values for specific Iris dataset columns if they exist
            if 'SepalLengthCm' in df.columns:
                df['SepalLengthCm'] = df['SepalLengthCm'].fillna(df['SepalLengthCm'].mean())
            if 'SepalWidthCm' in df.columns:
                df['SepalWidthCm'] = df['SepalWidthCm'].fillna(df['SepalWidthCm'].median())
            if 'PetalWidthCm' in df.columns:
                df['PetalWidthCm'] = df['PetalWidthCm'].fillna(df['PetalWidthCm'].median())
            if 'PetalLengthCm' in df.columns:
                df['PetalLengthCm'] = df['PetalLengthCm'].fillna(0)

            st.write("Cleaned Data Preview (First 10 Rows)")
            st.dataframe(df.head(10))

            # 3. Download as Pickle
            buffer = io.BytesIO()
            df.to_pickle(buffer)
            buffer.seek(0)
            st.download_button(
                label="Download Cleaned Data (Pickle)",
                data=buffer,
                file_name="converted_data.pkl",
                mime="application/octet-stream"
            )
            
            # 4. Model Training Section
            st.divider()
            st.header("🤖 Model Training")

            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'Id' in numeric_cols: numeric_cols.remove('Id')

            target_col = st.selectbox("Select Target Column (Species)", df.columns, index=len(df.columns)-1)
            feature_cols = st.multiselect("Select Features for Training", numeric_cols, default=numeric_cols)

            if st.button("Train Model"):
                if not feature_cols:
                    st.error("Please select at least one numeric feature.")
                else:
                    X = df[feature_cols]
                    y = df[target_col]
                    
                    # Split data
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
                    
                    # Train Random Forest
                    model = RandomForestClassifier(random_state=42)
                    model.fit(X_train, y_train)
                    
                    # Evaluation
                    y_pred = model.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)
                    
                    # Save to session state for the Prediction section
                    st.session_state['trained_model'] = model
                    st.session_state['feature_names'] = feature_cols
                    st.session_state['df_for_defaults'] = df # Store to calculate means later
                    
                    st.metric("Model Accuracy", f"{accuracy:.2%}")
                    st.success("Model trained successfully!")

            # 5. Prediction Section
            if 'trained_model' in st.session_state:
                st.divider()
                st.header("Prediction")
                st.write("Enter measurements to identify the species:")
                
                user_inputs = {}
                col_a, col_b = st.columns(2)
                
                for i, feat in enumerate(st.session_state['feature_names']):
                    target_col_ui = col_a if i % 2 == 0 else col_b
                    with target_col_ui:
                        default_val = float(st.session_state['df_for_defaults'][feat].mean())
                        user_inputs[feat] = st.number_input(
                            f"{feat}", 
                            value=round(default_val, 2),
                            step=0.1
                        )
                
                if st.button("Run Prediction"):
                    input_df = pd.DataFrame([user_inputs])
                    prediction = st.session_state['trained_model'].predict(input_df)
                    st.subheader("Result:")
                    st.success(f"The model identifies this as: **{prediction[0]}**")

        else:
            st.warning("The file is empty.")
            
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.divider()
if st.button("⬅️ Back to Account"):
    st.switch_page("views/account.py")