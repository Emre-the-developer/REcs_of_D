import streamlit as st

st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    .main {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stTextInput input {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stButton button {
        background-color: #FF9900;
        color: #000000;
        width: 100%;
    }
    .top-picks-container {
        background-color: #CC5500;
        padding: 10px;
        border-radius: 5px;
    }
    .top-pick {
        background-color: #333333;
        color: #FFFFFF;
        margin: 5px;
        padding: 10px;
        border-radius: 5px;
    }
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .search-input {
        width: 50%;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to show the home page
def show_home_page(user_name):
    st.markdown(f"""
        <div style="background-color: #CC5500; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
            <div>{user_name}</div>
            <div>Mylist</div>
            <div>Sign Out</div>
        </div>
        <div class="search-container">
            <input type="text" class="search-input" placeholder="Search">
        </div>
        <h2 style="color: #FFFFFF;">Top Picks</h2>
        <div class="top-picks-container">
            <div class="top-pick">
                <div>Anime Name</div>
                <div>TV/Movie 26 Episodes</div>
                <div style="background-color: #FF0000; height: 150px; width: 100px;"></div>
                <div>Score: 7.0</div>
                <div>Genre: Western</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Sign In"

def show_sign_in():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        st.session_state.page = "Home"
        st.session_state.user_name = email
        st.success(f"Welcome, {email}!")
    if st.button("Create Account"):
        st.session_state.page = "Sign Up"

def show_sign_up():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    terms = st.checkbox("I accept the Terms of Service and Privacy Policy")
    if st.button("Create Account"):
        if terms:
            st.session_state.page = "Home"
            st.session_state.user_name = username
            st.success(f"Account created for {username}!")
        else:
            st.error("You must accept the terms to create an account.")
    if st.button("Sign In"):
        st.session_state.page = "Sign In"

if st.session_state.page == "Sign In":
    show_sign_in()
elif st.session_state.page == "Sign Up":
    show_sign_up()
else:
    show_home_page(st.session_state.get("user_name", "User"))

