import streamlit as st


st.title("👤 Account Setup")

# Initialize session state for the name and validation
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "account_complete" not in st.session_state:
    st.session_state.account_complete = False

# Manual input for the name
name_input = st.text_input("Enter your full name to unlock the app:", value=st.session_state.user_name)

if st.button("Save Profile"):
    if name_input.strip():
        st.session_state.user_name = name_input
        st.session_state.account_complete = True
        st.success(f"Profile saved! Welcome, {name_input}.")
    else:
        st.session_state.account_complete = False
        st.error("Please enter a valid name.")

st.write("---")

# The button is disabled until account_complete is True
if st.button(
    "Proceed to Login Page ➡️", 
    disabled=not st.session_state.account_complete,
    use_container_width=True
):
    st.switch_page("views/login.py")


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

set_bg_hack('https://images.pexels.com/photos/3980364/pexels-photo-3980364.jpeg?cs=srgb&dl=pexels-harun-tan-2311991-3980364.jpg&fm=jpg')