#### Main page

# libraries and modules:
import streamlit as st

# function for setup page:
def main_setup_page():
    st.set_page_config(
        page_title = "Movie Finder",
        page_icon = '🎬',
        layout = "wide",
        initial_sidebar_state = "expanded"
    )

# calling function:
main_setup_page()

# function for main image:
def main_img_page():
    st.image('main_logo_2.jpg',
             width=500)

# calling function:
main_img_page()

# function for main page:
def main_page():
    st.title('🎬 Movie Finder')
    st.sidebar.title('Application powered by ⤵️')
    
    sb1, sb2 = st.sidebar.columns(2)
    with sb1:
        st.sidebar.image('python_logo.png',
                        width = 60)
        st.sidebar.image('pandas_logo.png',
                        width = 60)
    with sb2:
        st.sidebar.image('plotly_logo.jpg',
                        width = 60)
        st.sidebar.image('streamlit_logo.png',
                        width = 60)
        st.sidebar.image('imdb_logo.png',
                        width = 60)
        st.sidebar.text(' ')
        st.sidebar.title("""
                        🎬 Movie Finder\n
                        Developed by\n
                        Miloš Popović\n
                        2024
                        """)
        st.sidebar.title("🖥️ | 🖱️ | ⌨️ | 🐍 | 🐼 | 📊")
    st.write(
    """

    Welcome to Movie Finder, your ultimate destination for discovering and exploring a vast world of movies.
    This web application is designed to be your go to tool for finding the perfect movies to indulge in, all powered by the extensive and reliable database from IMDB.
    The application is designed to help users efficiently explore movies through the incorporation of advanced filtering options within the application itself.
    These options include searching for movies based on genres, release dates, crew information and various other criteria.
    
    # ❔ Why Movies Finder

    🌐 Up to date Database:
    Application harness the power of IMDB, the most trusted source for entertainment information.
    The database is constantly updated to ensure you have access to the latest and most accurate information of video movies.

    ☰ Advanced Filtering:
    Say goodbye to endless scrolling and hello to precision searching!
    Movie Finder offers advanced filtering options that allow you to tailor your search based on different criteria.
    Whether you're in the mood for a thrilling drama, a laugh-out-loud comedy, the filters make it easy to find exactly what you're looking for.

    📊 Analytics:
    In addition, on a second page, you'll find an analysis section exploring various analytics for movies based on a release date (year) filter.
    The detailed analysis will provide interesting information, such as the top 10 movies or the most prevalent genre...
    
    # 💻 How It Works
    🔎 Search and Filter:\n
    Navigate to the 'Movies' page and adjust parameters such as release date, run time, rating scale, director, and more.
    Alternatively, users can explore the 'Analytics' page for more profound insights based on a Release data (year)
    by clicking on desired year.
        
    """)

    st.write(' ')
    st.write('# ✉️ Contact')
    st.write(' ')
    st.info(
    """
    For any inquiries or additional information, please feel free to reach out to us via email.

    Email: popovic_milos_89@yahoo.com

    Thank you for reaching out! """)

# calling main function:
main_page()