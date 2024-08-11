import time
import pandas as pd
import streamlit as st
import sqlite3

# Connect to SQLite database
con = sqlite3.connect("Recs_of_D.db")
cur = con.cursor()

# Importing expected columns and checking
data = pd.read_csv(r"C:\Users\emref\Desktop\C13digihome\REcs_of_D\REcs_of_D_trydata3.csv")
data_sorted = data.sort_values(by='Scoredby', ascending=False)

expected_columns = ['Title', 'Genre', 'Synopsis', 'Type', 'Studio', 'Rating', 'Scoredby', 'Episodes', 'Source', 'Aired', 'Image_url']
missing_columns = [col for col in expected_columns if col not in data_sorted.columns]
if missing_columns:
    st.error(f"Missing columns in the CSV file: {missing_columns}")
    st.stop()

# Ensure 'Title' column has no None values
data_sorted['Title'] = data_sorted['Title'].fillna('Unknown Title')

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize session state variables
if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []
if "tags" not in st.session_state:
    st.session_state.tags = {row['Title']: "" for _, row in data_sorted.iterrows()}
if "show_watched_list" not in st.session_state:
    st.session_state.show_watched_list = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "Sign In"

# Function to toggle watched list display
def toggle_watched_list():
    st.session_state.show_watched_list = not st.session_state.show_watched_list

def create_animetable():
    cur.execute('CREATE TABLE IF NOT EXISTS movietable(username TEXT, title TEXT, rating INTEGER, state INTEGER, episodes_watched INTEGER)')
    con.commit()

def add_animedata(username, title, rating, state, episodes_watched):
    cur.execute('INSERT INTO movietable(username, title, rating, state, episodes_watched) VALUES (?, ?, ?, ?, ?)', (username, title, rating, state, episodes_watched))
    con.commit()

def show_user_list(username):
    cur.execute('SELECT * FROM movietable WHERE username =?', (username,))
    data = cur.fetchall()
    return data

def registered_title_check(username, title):
    cur.execute('SELECT * FROM movietable WHERE username =? AND title =?', (username, title))
    data = cur.fetchall()
    return data

# Function to render movie images with different sizes
def render_movie_image(image_url, size="small"):
    if size == "large":
        width = 200  # Larger image size
    else:
        width = 100  # Smaller image size
    return f'<img src="{image_url}" alt="Movie Image" width="{width}">'

# Showing home page
def show_home_page(user_name):
    # Temporary Welcome Message
    welcome_placeholder = st.empty()
    welcome_placeholder.markdown(f"<h2>Welcome {user_name}!</h2>", unsafe_allow_html=True)
    time.sleep(2)  # Show the message for 2 seconds
    welcome_placeholder.empty()  # Clear the welcome message

    st.markdown(f"""
        <div class="header-container">
            <div>{user_name}</div>
            <div><button onclick="document.location.reload()">My List</button></div>
            <div><button onclick="document.location.reload()">Sign Out</button></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Watched List", key="watched-list-toggle"):
        toggle_watched_list()
    
    if st.session_state.show_watched_list:
        st.subheader('Watched Movies')
        sorted_movies = sorted(show_user_list(user_name), key=lambda x: -x[2])
        for movie in sorted_movies:
            st.write(f"{movie[1]} - {movie[2]} stars, {movie[4]} episodes watched")
            if st.button(f'Remove {movie[1]} from Watched List', key=f'remove-{movie[1]}'):
                st.session_state.watched_movies = [m for m in st.session_state.watched_movies if m['title'] != movie[1]]
                st.success(f'{movie[1]} removed from watched list!')
        return
    
    # Remodeled search bar with icon and styling
    st.markdown("""
        <div class="search-container">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="search_input" placeholder="Search for a movie...">
        </div>
        <style>
            .search-container {
                position: relative;
                width: 50%;
                margin-bottom: 20px;
            }
            .search-icon {
                position: absolute;
                top: 50%;
                left: 10px;
                transform: translateY(-50%);
                color: #FF9900;
                font-size: 20px;
            }
            #search_input {
                width: 100%;
                padding: 10px 10px 10px 35px;
                border-radius: 20px;
                border: 2px solid #FF9900;
                background-color: #333333;
                color: #FFFFFF;
                font-size: 16px;
            }
            #search_input:focus {
                outline: none;
                border-color: #FF6600;
            }
        </style>
    """, unsafe_allow_html=True)

    search_query = st.text_input("", key="search_input", label_visibility="collapsed").lower()
    filtered_data = data_sorted[data_sorted['Title'].str.lower().str.contains(search_query)]

    # Page size is adjustable
    page_size = 12
    # Calculate the total number of pages
    total_pages = len(filtered_data) // page_size + 1
    # Get the current page number from user input
    st.write("Change Page")
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, format="%d", placeholder="Load more")
    # Calculate the start and end indices for the current page
    start_index = (current_page - 1) * page_size
    end_index = min(start_index + page_size, len(filtered_data))

    for index in range(start_index, end_index):
        row = filtered_data.iloc[index]
        st.markdown(f"""
            <div class="movie-container">
                {render_movie_image(row['Image_url'], size="large")}  <!-- Large image on home page -->
                <div class="movie-info">
                    <div class="movie-title">{row['Title']}</div>
                    <div>{row['Rating']} stars</div>
                    <div>Genres: {row['Genre']}</div>
                    <div>Synopsis: {row['Synopsis']}</div>
                    <div>Type: {row['Type']}</div>
                    <div>Studio: {row['Studio']}</div>
                    <div>Scored by: {row['Scoredby']}</div>
                    <div>Episodes: {row['Episodes']}</div>
                    <div>Source: {row['Source']}</div>
                    <div>Aired: {row['Aired']}</div>
                    <div class="edit-link" onClick="document.getElementById('edit-form-{index}').style.display = 'block';">Edit</div>
                </div>
                <div id="edit-form-{index}" style="display:none;">
                    <form>
                        <label for="tags">Tags:</label><br>
                        <input type="text" id="tags" name="tags" value="{st.session_state.tags[row['Title']]}"><br>
                        <input type="submit" value="Save">
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Rating and episodes system
        create_animetable()
        rating = st.selectbox(f'Rate {row["Title"]}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        states = ["Continuing", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
        statebox = st.selectbox(f"State of {row['Title']}", states, key=f'state_{index}')
        state_index = states.index(statebox)
        episode_count = st.selectbox(f'Episodes Watched for {row["Title"]}:', range(0, row["Episodes"] + 1), key=f'episodes_{index}')
        
        title_check = registered_title_check(user_name, row["Title"])
        if title_check:
            continue
        else:
            if st.button(f'Save Rating and State for {row["Title"]}', key=f'save-{index}'):
                add_animedata(user_name, row["Title"], rating, state_index, episode_count)
                st.success('Rating, state, and episodes watched saved!')

# User authentication functions
def create_usertable():
    cur.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, email TEXT, password TEXT)')
    
def add_userdata(username, email, password):
    cur.execute('INSERT INTO userstable(username, email, password) VALUES (?, ?, ?)', (username, email, password))
    con.commit()

def login_user(username, password):
    cur.execute('SELECT * FROM userstable WHERE username =? AND password =?', (username, password))
    data = cur.fetchall()
    return data

def view_all_users():
    cur.execute('SELECT * FROM userstable')
    data = cur.fetchall()
    return data

# Sign in and sign up
def show_sign_in():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign In")
    ID_input = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        create_usertable()
        result = login_user(ID_input, password)
        if result:
            st.session_state.page = "Home"
            st.session_state.current_user = result[0]
        else:
            st.error("Invalid username or password")
    if st.button("Create Account"):
        st.session_state.page = "Sign Up"

def show_sign_up():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    accept_terms = st.checkbox("I agree to the terms and conditions")

    if st.button("Create Account"):
        create_usertable()
        users = view_all_users()
        emails = [user[1] for user in users]
        usernames = [user[0] for user in users]

        if not accept_terms:
            st.error("You must accept the terms to create an account.")
        elif email in emails:
            st.error("Email already registered")
        elif username in usernames:
            st.error("Username already taken")
        else:
            add_userdata(username, email, password)
            st.session_state.page = "Home"
            st.session_state.current_user = username
            st.success(f"Account created for {username}!")
    if st.button("Sign In"):
        st.session_state.page = "Sign In"

# Page routing
if st.session_state.page == "Sign In":
    show_sign_in()
elif st.session_state.page == "Sign Up":
    show_sign_up()
else:
    show_home_page(st.session_state.current_user[0])

# Styling and layout
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
        color: #FFFFFF;
        border-radius: 10px;
    }
    .stButton button:hover {
        background-color: #CC7A00;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #FF9900;
        border-radius: 10px;
    }
    .movie-container {
        display: flex;
        align-items: flex-start;
        padding: 10px;
        border-bottom: 1px solid #CCCCCC;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .movie-image img {
        border-radius: 10px;
        margin-right: 20px;  /* Space between the image and the info */
    }
    .movie-info {
        flex: 1;
    }
    .edit-link {
        color: #FF9900;
        cursor: pointer;
        text-decoration: underline;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)
