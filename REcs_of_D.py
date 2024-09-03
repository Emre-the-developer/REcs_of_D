import time
import pandas as pd
import streamlit as st
import sqlite3

# Connect to SQLite database
con = sqlite3.connect("Recs_of_D.db")
cur = con.cursor()

# Import and check the CSV file
data = pd.read_csv(r"C:/Users/emref/Desktop/C13digihome/REcs_of_D/REcs_of_D_trydata3.csv")
data_sorted = data.sort_values(by='Scoredby', ascending=False)

# Check for expected columns
expected_columns = ['Title', 'Genre', 'Synopsis', 'Type', 'Studio', 'Rating', 'Scoredby', 'Episodes', 'Source', 'Aired', 'Image_url']
missing_columns = [col for col in expected_columns if col not in data_sorted.columns]
if missing_columns:
    st.error(f"Missing columns in the CSV file: {missing_columns}")
    st.stop()

# Ensure 'Title' column has no None values
data_sorted['Title'] = data_sorted['Title'].fillna('Unknown Title')

# Set Streamlit configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize session state variables
if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []
if "tags" not in st.session_state:
    st.session_state.tags = {row['Title']: "" for _, row in data_sorted.iterrows()}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "Sign In"
if "show_watched_list" not in st.session_state:
    st.session_state.show_watched_list = False

# Function to sign out
def sign_out():
    st.session_state.current_user = None
    st.session_state.page = "Sign In"

# Function to toggle watched list display
def toggle_watched_list():
    st.session_state.show_watched_list = not st.session_state.show_watched_list

# Function to create the movie table if it doesn't exist
def create_animetable():
    cur.execute('CREATE TABLE IF NOT EXISTS movietable(username TEXT, title TEXT, rating INTEGER, state INTEGER, episodes_watched INTEGER)')
    con.commit()

# Function to add anime data to the table
def add_animedata(username, title, rating, state, episodes_watched):
    if username is None or title is None or rating is None or state is None or episodes_watched is None:
        st.error("Error: One of the arguments is None")
        return
    try:
        cur.execute('INSERT INTO movietable(username, title, rating, state, episodes_watched) VALUES (?, ?, ?, ?, ?)', (username, title, rating, state, episodes_watched))
        con.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to retrieve user list from the database
def show_user_list(username):
    cur.execute('SELECT * FROM movietable WHERE username =?', (username,))
    data = cur.fetchall()
    return data

# Function to check if a title is already registered for a user
def registered_title_check(username, title):
    cur.execute('SELECT * FROM movietable WHERE username =? AND title =?', (username, title))
    data = cur.fetchall()
    return data

# Function to render movie images with different sizes
def render_movie_image(image_url, size="small"):
    width = 200 if size == "large" else 100
    return f'<img src="{image_url}" alt="Movie Image" width="{width}">'

# Function to show the home page
def show_home_page(user_name):
    # Add custom CSS for the "My List" button
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #333;
                padding: 10px 20px;
                border-radius: 10px;
            }
            .logo-container {
                flex: 1;
            }
            .logo-link img {
                width: 50px;
            }
            .user-options {
                flex: 2;
                text-align: right;
            }
            .dropdown {
                display: inline-block;
                position: relative;
            }
            .dropbtn {
                background-color: #333;
                color: #FF9900;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                cursor: pointer;
                border-radius: 5px;
            }
            .dropdown-content {
                display: none;
                position: absolute;
                background-color: #f9f9f9;
                min-width: 160px;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                z-index: 1;
            }
            .dropdown:hover .dropdown-content {
                display: block;
            }
            .dropdown-content a {
                color: black;
                padding: 12px 16px;
                text-decoration: none;
                display: block;
            }
            .dropdown-content a:hover {
                background-color: #ddd;
            }
            .my-list-button {
                background-color: #FF9900;
                color: #FFFFFF;
                padding: 10px 40px;  /* Adjust padding for stretching */
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-size: 16px;
                margin-left: 10px;
                width: 100%;  /* Full width for stretching */
            }
            .my-list-button:hover {
                background-color: #FF6600;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="header-container">
            <div class="logo-container">
                <a href="#" onclick="location.reload();" class="logo-link">
                    <img src="https://your-logo-url.com/logo.png" alt="Logo">
                </a>
            </div>
            <div class="user-options">
                <div class="dropdown">
                    <button class="dropbtn">{user_name}</button>
                    <div class="dropdown-content">
                        <a href="#" onclick="sign_out();">Sign Out</a>
                    </div>
                </div>
                <button class="my-list-button" onclick="document.location.reload()">My List</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.show_watched_list:
        st.subheader('Watched Movies')
        sorted_movies = sorted(show_user_list(user_name), key=lambda x: -x[2])
        for movie in sorted_movies:
            st.write(f"{movie[1]} - {movie[2]} stars, {movie[4]} episodes watched")
            if st.button(f'Remove {movie[1]} from Watched List', key=f'remove-{movie[1]}'):
                st.session_state.watched_movies = [m for m in st.session_state.watched_movies if m['title'] != movie[1]]
                st.success(f'{movie[1]} removed from watched list!')
        return
    
    # Search bar implementation
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

    # Pagination setup
    page_size = 12
    total_pages = len(filtered_data) // page_size + 1
    st.write("Change Page")
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, format="%d", placeholder="Load more")
    start_index = (current_page - 1) * page_size
    end_index = min(start_index + page_size, len(filtered_data))

    for index in range(start_index, end_index):
        row = filtered_data.iloc[index]
        st.markdown(f"""
            <div class="movie-container">
                {render_movie_image(row['Image_url'], size="large")}
                <div class="movie-info">
                    <div class="movie-title">{row['Title']}</div>
                    <div>{row['Rating']} stars</div>
                    <div>Genres: {row['Genre']}</div>
                    <div>Synopsis: {row['Synopsis']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        create_animetable()  # Ensure table exists before inserting data
        rating = st.selectbox(f'Rate {row["Title"]}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        states = ["Continuing", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
        statebox = st.selectbox(f"State of {row['Title']}", states, key=f'state_{index}')
        state_index = states.index(statebox)
        episode_count = st.selectbox(f'Episodes Watched for {row["Title"]}:', range(0, int(row["Episodes"]) + 1), key=f'episodes_{index}')
        
        title_check = registered_title_check(user_name, row["Title"])
        if not title_check and st.button(f'Save Rating and State for {row["Title"]}', key=f'save-{index}'):
            add_animedata(user_name, row["Title"], rating, state_index, episode_count)
            st.success('Rating, state, and episodes watched saved!')

# User authentication functions
def create_usertable():
    cur.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, email TEXT, password TEXT)')
    con.commit()

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

# Function to show sign-in page
def show_sign_in():
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        create_usertable()
        result = login_user(username, password)
        if result:
            st.success(f"Welcome, {username}!")
            st.session_state.current_user = username
            st.session_state.page = "Home"
        else:
            st.error("Incorrect username or password")

# Function to show sign-up page
def show_sign_up():
    st.title("Sign Up")
    new_user = st.text_input("Username", key="new_user")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if new_password != confirm_password:
        st.error("Passwords do not match")
    elif st.button("Sign Up"):
        create_usertable()
        add_userdata(new_user, new_email, new_password)
        st.success("You have successfully created an account")
        st.info("Go to the Sign In page to log in")

# Function to handle page navigation
def handle_navigation():
    if st.session_state.page == "Sign In":
        show_sign_in()
    elif st.session_state.page == "Sign Up":
        show_sign_up()
    elif st.session_state.page == "Home" and st.session_state.current_user:
        show_home_page(st.session_state.current_user)
    else:
        st.session_state.page = "Sign In"
        show_sign_in()

def drop_table_if_code_matches(db_name, table_name, input_code, correct_code):
    # Check if the input code matches the correct code
    if input_code == correct_code:
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            # Drop the table
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()

            st.success(f"Table '{table_name}' has been dropped successfully.")

        except sqlite3.Error as e:
            st.error(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    else:
        st.error("Input code did not match. Table drop aborted.")

# Main program
if __name__ == "__main__":
    # Handle navigation
    handle_navigation()

    # Optional: Drop table based on input code
    input_code = st.text_input("Enter code to drop the table")
    correct_code = '1234'  # Set your correct code here
    if st.button("Drop Table"):
        drop_table_if_code_matches("Recs_of_D.db", "movietable", input_code, correct_code)

    # Close database connection at the end
    con.close()
