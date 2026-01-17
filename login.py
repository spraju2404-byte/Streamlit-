import streamlit as st

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

set_bg_hack('https://t4.ftcdn.net/jpg/09/25/09/11/360_F_925091131_VMdryn0adBBZbepg1WGzPyjI5faAaZjI.jpg')
# Check if the user finished the Account page first
if not st.session_state.get("account_complete", False):
    st.warning("⚠️ Please complete the Account page first!")
    st.stop()

st.title(f"🔐 Login for {st.session_state.user_name}")
st.write("Enter your credentials")

# Initialize the login verification state
if "login_verified" not in st.session_state:
    st.session_state.login_verified = False

# 1. Manual Entry Fields
with st.container(border=True):
    input_user = st.text_input("Username")
    input_pass = st.text_input("Password", type="password")
    
    # Validation Button
    if st.button("Log In", use_container_width=True):
        # Manually check the credentials
        if input_user == "admin" and input_pass == "123":
            st.session_state.login_verified = True
            st.success("Credentials verified! You may now proceed.")
        else:
            st.session_state.login_verified = False
            st.error("Invalid Username or Password. Please try again.")

st.divider()
st.info("Username: admin :: Password: 123 ")
# 2. The Navigation Button (Enabled ONLY after manual login)
if st.button(
    "Go to Coding Workspace ➡️", 
    disabled=not st.session_state.login_verified,
    use_container_width=True,
    type="primary" # Makes the button stand out when enabled
):
    st.switch_page("views/coding.py")