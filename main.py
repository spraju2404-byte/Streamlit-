import streamlit as st

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"], .st-emotion-cache-17l78vu {
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Specifically targeting the sidebar navigation links */
    [data-testid="stSidebarNavItems"] span {
        font-family: 'Roboto', sans-serif !important;
        font-size: 18px; /* Optional: adjust size */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# These paths are relative to where main.py is located
page_1 = st.Page("views/account.py", title="Account", icon="👤")
page_2 = st.Page("views/login.py", title="Login", icon="🔐")
page_3 = st.Page("views/coding.py", title="Coding", icon="💻")

pg = st.navigation([page_1, page_2, page_3])
pg.run()