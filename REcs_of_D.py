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
        <div class="movie-container">
            <div class="movie-title">Castle in the Sky</div>
            <div class="movie-details">
                <div class="movie-image">
                    <img src="https://i.imgur.com/abcd1234.png" alt="Movie Image" width="200">
                </div>
                <div class="movie-info">
                    <div>4.10 stars</div>
                    <div>Genres: Action, Adventure, Animation, Fantasy, Romance, Family</div>
                    <div>Languages: Japanese</div>
                    <div>Director: Hayao Miyazaki</div>
                    <div>Cast: Keiko Yokozawa, Mayumi Tanaka, Minori Terada, Kotoe Hatsui, Fujio Tokita, more...</div>
                    <div>DVD Release Date: April 15, 2003</div>
                    <div>Movie Maintenance: flag this movie</div>
                </div>
            </div>
            <div class="tags-container">
                <div class="tag">steampunk</div>
                <div class="tag">imagination</div>
                <div class="tag">anime</div>
                <div class="tag">Studio Ghibli</div>
                <div class="tag">Hayao Miyazaki</div>
                <div class="tag">adventure</div>
                <div class="tag">great soundtrack</div>
                <div class="tag">robots</div>
                <div class="tag">fantasy world</div>
                <div class="tag">aviation</div>
            </div>
            <div class="similar-movies">
                <h3>Similar Movies</h3>
                <div>
                    <img src="https://i.imgur.com/abcd1234.png" alt="Porco Rosso" width="100">
                    <img src="https://i.imgur.com/abcd1234.png" alt="Spirited Away" width="100">
                    <img src="https://i.imgur.com/abcd1234.png" alt="Nausicaä of the Valley" width="100">
                    <img src="https://i.imgur.com/abcd1234.png" alt="Princess Mononoke" width="100">
                    <img src="https://i.imgur.com/abcd1234.png" alt="My Neighbor Totoro" width="100">
                    <img src="https://i.imgur.com/abcd1234.png" alt="Kiki's Delivery Service" width="100">
                </div>
            </div>
            <div>
                <label for="rating">Rate this movie:</label>
                <select id="rating">
                    <option value="1">1 Star</option>
                    <option value="2">2 Stars</option>
                    <option value="3">3 Stars</option>
                    <option value="4">4 Stars</option>
                    <option value="5">5 Stars</option>
                </select>
                <button onclick="rateMovie()">Rate</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Rating and saving to watched list
    rating = st.selectbox('Rate this movie:', [1, 2, 3, 4, 5])
    if st.button('Save Rating and Mark as Watched'):
        st.session_state.watched_movies.append({
            'title': 'Castle in the Sky',
            'rating': rating
        })
        st.success('Rating saved and movie marked as watched!')

    # Display watched movies
    st.subheader('Watched Movies')
    for movie in st.session_state.watched_movies:
        st.write(f"{movie['title']} - {movie['rating']} stars")

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
