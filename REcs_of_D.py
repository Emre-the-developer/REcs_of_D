import time
import pandas as pd
import streamlit as st
import sqlite3

from Database1 import *
from Recommendation import anime_Recs
# Connect to SQLite database
con = sqlite3.connect("Recs_of_D.db")
cur = con.cursor()


# Import and check the CSV file
data = pd.read_csv("C:/Users/emref/Desktop/C13digihome/REcs_of_D/REcs_of_D_trydata3.csv")
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

st.markdown("""
    <style>
        /* Global background and text color */
        body {
            background-color: black;
            color: white;
        }

        /* Streamlit main container background color */
        .main {
            background-color: black;
        }

        /* Adjusting text and other elements for dark theme */
        .stButton button {
            background-color: #FF9900;
            color: white;
        }

        /* Search bar and buttons */
        .search-container {
            position: relative;
            width: 50%;
            margin-bottom: 20px;
            color: white;
        }
        
        .search-icon {
            color: #FF9900;
            font-size: 20px;
        }

        #search_input {
            background-color: #333;
            color: white;
            border: 2px solid #FF9900;
        }

        /* Header styling */
        .header-container {
            background-color: #333;
        }

        .dropbtn {
            background-color: #333;
            color: #FF9900;
        }

        .dropdown-content a {
            background-color: #444;
            color: white;
        }

        .dropdown-content a:hover {
            background-color: #FF9900;
            color: black;
        }

        /* Buttons for Watched List and general button styling */
        .my-list-button {
            background-color: #FF9900;
            color: white;
        }

        .my-list-button:hover {
            background-color: #FF6600;
        }

        /* Movie container styling */
        .movie-container {
            background-color: #333;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            color: white;
        }

        .movie-image {
            border-radius: 5px;
            width: 150px;
            height: auto;
        }

        .movie-info {
            padding-left: 20px;
        }
    </style>
""", unsafe_allow_html=True)


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

    # Display the user options and "My List" button
    col1, col2 = st.columns([3, 1])  # Adjust the columns for better alignment

    with col1:
        st.markdown(f"""
            <div class="user-options">
                <div class="dropdown">
                    <button class="dropbtn">{user_name}</button>
                    <div class="dropdown-content">
                        <a href="#" onclick="sign_out();">Sign Out</a>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("My List", key="my_list_button"):
            toggle_watched_list()
    
    if st.session_state.show_watched_list:
        st.subheader('Watched Movies')
        sorted_movies = sorted(show_user_list(user_name), key=lambda x: -x[2])
        for movie in sorted_movies:
            st.write(f"{movie[1]} - {movie[2]} stars, {movie[4]} episodes watched")
            if st.button(f'Remove {movie[1]} from Watched List', key=f'remove-{movie[1]}'):
                delete_animedata(user_name, movie[1])  # Remove from database
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
                padding: 10px 20px 10px 40px;
                font-size: 18px;
                border: 2px solid #FF9900;
                border-radius: 5px;
                outline: none;
            }
        </style>
    """, unsafe_allow_html=True)

    Recs = show_Rec_user_list(user_name)
    Recs_df = pd.DataFrame([{"Title": rec[1], "recvalue": rec[2]} for rec in Recs])
    Recs_df.sort_values(by='recvalue', ascending=False)
    # Merge the sorted Recs with data_sorted based on 'Title'
    data_sorted['Episodes'] = data_sorted['Episodes'].fillna(1).astype(int)
    merged_data = pd.merge(Recs_df, data_sorted, on='Title', how='inner')

    search_query = st.text_input("", key="search_input", label_visibility="collapsed").lower()
    filtered_data = merged_data[merged_data['Title'].str.lower().str.contains(search_query)]

    # Pagination setup
    page_size = 12
    total_pages = len(filtered_data) // page_size + 1
    st.write("Change Page")
    current_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)

    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size
    paginated_data = filtered_data[start_index:end_index]

    for index, row in paginated_data.iterrows():
        title = row['Title']
        is_watched = any(movie['title'] == title for movie in st.session_state.watched_movies)

        if is_watched:
            if st.button(f'Remove {title} from Watched List', key=f'remove-{index}'):
                delete_animedata(user_name, title)
                st.session_state.watched_movies = [movie for movie in st.session_state.watched_movies if movie['title'] != title]
                st.success(f'{title} removed from watched list!')
            continue

        st.markdown(f"""
            <div class="movie-container">
                <img src="{row['Image_url']}" class="movie-image">
                <div class="movie-info">
                    <h3>{title}</h3>
                    <p>Rating: {row['Rating']}</p>
                    <p>Scored by: {row['Scoredby']}</p>
                    <p>Type: {row['Type']}</p>
                    <p>Episodes: {row['Episodes']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        rating = st.selectbox(f'Rate {title}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        states = ["Continuing", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
        statebox = st.selectbox(f"State of {title}", states, key=f'state_{index}')
        state_index = states.index(statebox)
        episode_count = st.selectbox(f'Episodes Watched for {title}:', range(0, int(row["Episodes"]) + 1), key=f'episodes_{index}')
        
        if st.button(f'Add {title} to Watched List', key=f'add-{index}'):
            if registered_title_check(user_name, title):
                st.error(f'{title} is already in your watched list!')
            else:
                add_animedata(user_name, title, rating, state_index, episode_count)
                st.session_state.watched_movies.append({'title': title, 'rating': rating, 'state': state_index, 'episodes_watched': episode_count})
                create_Reclist()
                new_Recs = anime_Recs(title,user_name)
                print("new Recs print: ",new_Recs)
                for rec_title, rec_value in new_Recs:
                    print("username: ", user_name,rec_title,rec_value)
                    add_Recdata(user_name,rec_title,rec_value)
                st.success(f'{title} added to watched list!')
                jkl = show_Rec_user_list(user_name)
                print(jkl)
        st.markdown("### Filter by State:")
    states_labels = ["Continuing", "Completed", "On-Hold", "Dropped", "Plan to Watch"]
    state_movies = {}

    for state in states_labels:
        if st.button(state):
            # Retrieve movies for the selected state
            state_movies[state] = show_user_list_by_state(user_name, states_labels.index(state))

    # Function to retrieve user list by state
    def show_user_list_by_state(username, state_index):
        cur.execute('SELECT * FROM movietable WHERE username =? AND state =?', (username, state_index))
        data = cur.fetchall()
        return data

    # Display the filtered movies if a state button was clicked
    for state, movies in state_movies.items():
        if movies:
            st.subheader(f"{state} Movies")
            for movie in movies:
                st.write(f"{movie[1]} - {movie[2]} stars, {movie[4]} episodes watched")
                if st.button(f'Remove {movie[1]} from Watched List', key=f'remove-{movie[1]}'):
                    delete_animedata(user_name, movie[1])
                    st.session_state.watched_movies = [m for m in st.session_state.watched_movies if m['title'] != movie[1]]
                    st.success(f'{movie[1]} removed from watched list!')


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

# Main program
if _name_ == "_main_":
    handle_navigation()
    # Example usage of drop_table_if_code_matches function
    #drop_table_if_code_matches("movietable", "your_secret_code_here")
    con.close()  # Close database connection at the end