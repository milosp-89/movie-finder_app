#### Second page => movies

# libraries and modules:
import streamlit as st, pandas as pd

# setup page:
def setup_page():
    st.set_page_config(
        page_title='Movie Finder:Movies',
        page_icon='🎥',
        layout='wide',
        initial_sidebar_state='expanded'
        )
    
# calling function:
setup_page()

# function for setup of images:
def images_setup():
   im1, im2, im3, im4, im5 = st.columns(5)
   with im1:
      st.image('oldboy.jpg', width = 100)
   with im2:
      st.image('gf.jpg', width = 100)
   with im3:
      st.image('spr.jpg', width = 100)
   with im4:
      st.image('jagten.jpg', width = 100)
   with im5:
      st.image('glad.jpg', width = 100)

# calling function:
images_setup()

# function for page and sidebar:
def page_sidebar():
   st.title(' ')
   st.title("🎥 Movies dataframe")
   st.sidebar.title('☰')
   st.sidebar.header('Advanced filters to use ⤵️')

# calling function:
page_sidebar()

# function for dataframe:
@st.cache_data
def load_data():
   files = ['movies_part1.csv',
            'movies_part2.csv',
            'movies_part3.csv',
            'movies_part4.csv',
            'movies_part5.csv']
   concatenated_df = pd.DataFrame()
   for f in files:
      df = pd.read_csv(f,
                      sep=';',
                      low_memory=False,
                      index_col=False)
      concatenated_df = pd.concat([concatenated_df, df])
      df = concatenated_df
   
   df = df[df['Year'] != 'Unknown']
   df['Year'] = df['Year'].astype(dtype='int64')
   df['Rating'] = (
        df['Rating'].replace(',', '.', regex = True).
            astype(dtype = 'float64'))
   
   df.columns = ['Movie title', 'Release date', 'Run time(min)', 'Run time(hh:mm)', 'Run time category',
                  'Rating', 'Rating category', 'Num of votes', 'Votes category', 'Genres', 'Genre 1',
                  'Genre 2', 'Genre 3', 'Actor', 'Actress', 'Writer', 'Director', 'Producer', 'Editor', 'Composer',
                  'Cinematographer', 'Hyperlink']
   
   df['Votes category'] = (
      df['Votes category'].replace({'> 500,000 and row <= 1,000,000' : '> 500,000 and <= 1,000,000'}))

   df = df[['Movie title', 'Hyperlink', 'Release date', 'Run time(min)', 'Run time(hh:mm)', 'Run time category',
            'Rating', 'Rating category', 'Num of votes', 'Votes category', 'Genres', 'Genre 1',
            'Genre 2', 'Genre 3', 'Actor', 'Actress', 'Writer', 'Director', 'Producer', 'Editor', 'Composer',
            'Cinematographer']]
    
   return df

# calling function:
df = load_data()

############
#### filters:

# function for slider:
def slider(data, title, column):
   try:
       object = (
          st.sidebar.slider(f'{title}:',
                           data[column].min(),
                           data[column].max(),
                           (data[column].min(), data[column].max())))
       
       if object:
          mask = (
             data[column] >= object[0]) & (data[column] <= object[1])
          filtered_df = data[mask]
          data = filtered_df
          return data
           
   except:
       st.warning('Entered value not present in a dataframe! Please delete the value and try again', icon="⚠️")
       st.stop()
       
# function for single select:
def single_select(data, title, column):
   object = (
      st.sidebar.selectbox(f'{title}:',
                        list(data[column].sort_values(ascending=False).unique()), index=None)
            )
   
   if object is not None:
      mask = data[column] == object
      filtered_df = data[mask]
      data = filtered_df
   return data

# function for search/find:
def search(data, title, column):
   object = (
      st.sidebar.text_input(f'{title}:'))
   if object is not None:
         mask = data[column].apply(lambda x: object.lower() in str(x).lower())
         filtered_df = data[mask]
         data = filtered_df
   return data
 
#### filters:

# genres search/type filter:
df = search(df,
            'Search by Genres',
            'Genres')

# genre1 single select filter:
df = single_select(df,
                   'Select Genre 1',
                   'Genre 1')

# genre2 single select filter:
df = single_select(df,
                   'Select Genre 2',
                   'Genre 2')

# genre3 single select filter:
df = single_select(df,
                   'Select Genre 3',
                   'Genre 3')

st.sidebar.text(' ')

# release date slider filter:
df = slider(df,
            'Adjust Release date (Year) range',
            'Release date')

# release data single select filter:
df = single_select(df,
                   'Select Release date (Year)',
                   'Release date')

st.sidebar.text(' ')

# director search/type filter:
df = search(df,
            'Search by Director',
            'Director')

st.sidebar.text(' ')

# rating slider filter:
df = slider(df,
            'Adjust Rating range',
            'Rating')

# rating single select filter:
df = single_select(df,
                   'Select Rating category',
                   'Rating category')

st.sidebar.text(' ')

# number of votes slider filter:
df = slider(df,
            'Adjust Number of votes range',
            'Num of votes')

# votes category select filter:
df = single_select(df,
                   'Select Votes category',
                   'Votes category')

# filters for number of votes as start / end:
try:
    votes_search_start = st.sidebar.text_input("Enter starting Vote value:",
                                               df['Num of votes'].min())
    
    votes_search_end = st.sidebar.text_input("Enter ending Vote value:",
                                             df['Num of votes'].max())
    
    if votes_search_start and votes_search_end:
        start_value = int(votes_search_start)
        end_value = int(votes_search_end)
        df = df[(df['Num of votes'] >= start_value) & (df['Num of votes'] <= end_value)]
except:
    st.warning('Entered value not present in a dataframe! Please delete the value and try again', icon="⚠️")
    st.stop()
    
st.sidebar.text(' ')

# run time category single select filter:
df = single_select(df,
                   'Select Run time category',
                   'Run time category')

# function to modify df:
def mod_df():
   st.dataframe(
      df.head(1000),
      column_config = {
         'Hyperlink':st.column_config.LinkColumn('Hyperlink'),
      },
      hide_index = True,
      width = 1540,
      height = 500,
   )

# calling function:
mod_df()

# function for export data:
def convert_df():
    return df.to_csv(sep = ',',
                    index = False,
                    decimal = ',')

# function for download button:
def btn_download():
   st.download_button(
      label = 'Download Movies data in .csv',
      data = convert_df(),
      file_name = 'movies.csv',
      mime = 'text/csv',
   )

# calling function:
btn_download()
