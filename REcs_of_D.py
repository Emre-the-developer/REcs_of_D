import pandas as pd
import streamlit as st
#importing expected columns and checking
file_path = "REcs_of_D_trydata.csv"
data = pd.read_csv(file_path)

expected_columns = ['Title', 'Genre', 'Synopsis', 'Type', 'Studio', 'Rating', 'Scoredby', 'Episodes', 'Source', 'Aired', 'Image_url']
missing_columns = [col for col in expected_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns in the csv file: {missing_columns}")
    st.stop()

st.set_page_config(page_title="Movie Recommender", layout="wide")
#homepage making
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
    .header-container {
        background-color: #CC5500;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-container div {
        color: #FFFFFF;
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
    .movie-container {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
    }
    .movie-details {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .movie-image {
        flex: 1;
        max-width: 200px;
    }
    .movie-info {
        flex: 2;
    }
    .tags-container {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .tag {
        background-color: #CC5500;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .similar-movies {
        margin-top: 20px;
    }
    .similar-movies img {
        margin-right: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []
#showing home page
def show_home_page(user_name):
    st.markdown(f"""
        <div class="header-container">
            <div>{user_name}</div>
            <div>Mylist</div>
            <div>Sign Out</div>
        </div>
        <div class="search-container">
            <input type="text" class="search-input" placeholder="Search">
        </div>
    """, unsafe_allow_html=True)
    # imporing columns
    for index, row in data.iterrows():
        st.markdown(f"""
            <div class="movie-container">
                <div class="movie-title">{row['Title']}</div>
                <div class="movie-details">
                    <div class="movie-image">
                        <img src="{row['Image_url']}" alt="Movie Image" width="200">
                    </div>
                    <div class="movie-info">
                        <div>{row['Rating']} stars</div>
                        <div>Genres: {row['Genre']}</div>
                        <div>Synopsis: {row['Synopsis']}</div>
                        <div>Type: {row['Type']}</div>
                        <div>Studio: {row['Studio']}</div>
                        <div>Scored by: {row['Scoredby']}</div>
                        <div>Episodes: {row['Episodes']}</div>
                        <div>Source: {row['Source']}</div>
                        <div>Aired: {row['Aired']}</div>
                        <div>Movie Maintenance: <a href="{row['Image_url']}">flag this movie</a></div>
                    </div>
                
                
                
            
        """, unsafe_allow_html=True)
    #rating system
        rating = st.selectbox(f'Rate {row["Title"]}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        if st.button(f'Save Rating and Mark as Watched {row["Title"]}', key=f'save-{index}'):
            st.session_state.watched_movies.append({
                'title': row['Title'],
                'rating': rating
            })
            st.success('Rating saved and movie marked as watched!')

    st.subheader('Watched Movies')
    for movie in st.session_state.watched_movies:
        st.write(f"{movie['title']} - {movie['rating']} stars")

if "page" not in st.session_state:
    st.session_state.page = "Sign In"
#sign in and sign up
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
