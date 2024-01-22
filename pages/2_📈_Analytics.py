#### Third page => analytics

# libraries and modules:
import streamlit as st, pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# setup page:
def setup_page():
    st.set_page_config(
        page_title='Movie Finder:Analytics',
        page_icon='📈',
        layout='wide',
        initial_sidebar_state='expanded'
        )

# calling function:
setup_page()

# function for setup of images:
def images_setup():
    st.image('analytics.png',
             width = 450)

# calling function:
images_setup()

# function for page and sidebar:
def main_page():
   st.title(' ')
   st.title("📈 Analytics of Movies")

# calling function:
main_page()

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
   
   cols_to_cat = ['Run time category',
                  'Rating category',
                  'Votes category',
                  'Genre 1',
                  'Genre 2',
                  'Genre 3']
   
   for col in cols_to_cat:
       df[col] = df[col].astype(dtype='category')

   colz = ['Actor', 'Actress', 'Writer', 'Producer', 'Editor', 'Composer', 'Cinematographer']
   
   df = df.drop(columns=colz)

   df['Votes category'] = (
      df['Votes category'].replace({'> 500,000 and row <= 1,000,000' : '> 500,000 and <= 1,000,000'}))

   return df

# calling dataframe function:
dfm = load_data()

# sidebar:
st.sidebar.header('☰ Filters')
st.sidebar.text(' ')
year = st.sidebar.selectbox("Please select **Release date**:",
                            pd.unique(dfm['Release date'].sort_values(ascending = False)))
dfm = dfm[dfm["Release date"] == year]

# function for charts:
def chart_prep(d, c):
    data = list(d[c].value_counts(normalize = True).values)
    data = list(map(lambda x: round(x, 2), data))
    category = list(d[c].value_counts(normalize = True).index)
    return [data, category]

# charts 1:
def charts1():
    st.title(' ')
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
            label = 'Total **NUMBER** of movies 🔽:',
            value = len(dfm))
    k2.metric(
            label = 'Average **RATING** value 🔽:',
            value = round(dfm['Rating'].mean(), 1))
    k3.metric(
            label = 'Highest **VOTE** number 🔽:',
            value = dfm['Num of votes'].max())
    k4.metric(   
            label = 'Most present **GENRE** category 🔽:',
            value = (
                dfm[dfm['Genre 1'] != 'Unknown'].groupby(by = 'Genre 1')['Movie title'].count().idxmax()))
    
    # chart columns:
    col1, col2 = st.columns(2)

    # chart 1 => barchart:
    d = chart_prep(dfm, 'Rating category')[0]
    cat = chart_prep(dfm, 'Rating category')[1]
    texted = [f'{round(x * 100, 2)}%' for x in d]

    colors = {
        'Bad': 'firebrick',
        'Ok': 'tomato',
        'Good': 'gray',
        'Very good': 'dodgerblue'}

    bar_ratings = (
        px.bar(x = cat,
            y = d,
            text = texted,
            color = cat,
            color_discrete_map=colors, 
            labels = {'x': 'Ratings', 'y': '%'}))

    bar_ratings.update_layout(
        xaxis={'categoryorder':'array',
                'categoryarray':['Bad','Ok','Good','Very good']},
        legend_title = None)

    bar_ratings.update_traces(
        hovertemplate = None,
        hoverinfo = "skip")
    
    with col1:
        st.header('Ratings category:')
        st.plotly_chart(bar_ratings,
                        theme =  'streamlit',
                        use_container_width = True)
        
    # chart 2 => buble chart:
    ix = list(dfm['Genre 1'].value_counts().sort_values(ascending = False)[0:3].index)[::-1]
    vl = list(dfm['Genre 1'].value_counts().sort_values(ascending = False)[0:3].values)[::-1]

    bubble = go.Figure(data=[go.Scatter(
        x=ix,
        y=vl,
        mode='markers',
        marker=dict(
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',
                    'rgb(44, 160, 101)'],
            opacity=[0.4, 0.6, 1.0],
            size=[30, 60, 100]))])

    bubble.update_traces(
        hovertemplate="Count: %{y}<br>",
        text=vl,
        name='')

    bubble.update_layout(
        yaxis_title="Count")
    
    with col2:
        st.header('Top 3 Genres:')
        st.plotly_chart(bubble,
                        theme = 'streamlit',
                        use_container_width = True)
             
# calling function 1:
charts1()

# charts 2:
def charts2():
    c1, c2 = st.columns(2)

    #chart 3 => scatter plot:
    scatter = px.scatter(dfm,
                        x="Rating",
                        y="Num of votes",
                        color="Num of votes")

    scatter.update_traces(
        hovertemplate = None,
        hoverinfo = "skip")

    with c1:
        st.header('Correlation between votes and ratings:')
        st.plotly_chart(scatter,
                        theme =  'streamlit',
                        use_container_width = True)
        
    # chart 4 => table:
    with c2:
        st.header('Top 3 shortest movies:')
        shortest = (
            dfm[(dfm['Rating'] > 7.0) 
            & (dfm['Num of votes'] > 10000)].sort_values(by='Run time(min)',
                                                        ascending=True)[['Movie title',
                                                                        'Run time(hh:mm)',
                                                                        'Rating',
                                                                        'Num of votes',
                                                                        'Hyperlink']][0:3]
        )
        st.dataframe(
            shortest,
            column_config={
                
                "Hyperlink": st.column_config.LinkColumn("Hyperlink"),
            },
            hide_index=True,
            width=700
        )

# calling function 2:
charts2()

# charts3:
def charts3():
    cc1, cc2 = st.columns(2)

    # chart 5 pie/donut chart:
    with cc1:
        xx = dfm[(dfm['Rating'] > 7.0) 
                & (dfm['Num of votes'] > 10000)]

        xx = xx[xx['Director'] != 'Unknown']['Director'].value_counts().sort_values(ascending=False)[0:3]

        data = list(xx.values)
        category = list(xx.index)
        colors = ['teal', 'dodgerblue', 'khaki']

        directors = go.Figure(data=[go.Pie(labels=category,
                                        values=data,
                                        title="Top 3 directors",
                                        hole=0.4,
                                        marker=dict(colors=colors))])

        directors.update_traces(
            hovertemplate=None,
            hoverinfo="skip")

        st.plotly_chart(directors,
                        theme='streamlit',
                        use_container_width=True)
        
    # chart 6 table top movies:
    with cc2:
        st.header('Top 10 movies:')
        top_mov = dfm[(dfm['Rating'] > 7.0) 
                     & (dfm['Num of votes'] > 15000)].sort_values(by = 'Rating', ascending = False)[0:10]

        mov = top_mov[['Movie title', 'Run time(hh:mm)', 'Rating', 'Num of votes', 'Genres', 'Hyperlink']]

        st.dataframe(
                    mov,
                    column_config={
                        
                        "Hyperlink": st.column_config.LinkColumn("Hyperlink"),
                    },
                    hide_index=True,
                    width=700
                )

# calling function:
charts3()

# charts4:
def charts4():
    c1, c2 = st.columns(2)

    # chart 7, histogram votes category:
    with c1:
         st.header('Votes category distribution:')
         hist_votes = px.histogram(dfm[dfm['Votes category'] != '<=5000'], y="Votes category",
                                   color_discrete_sequence=['lightcyan'],
                                   text_auto=True).update_yaxes({'categoryorder':'array',
                                                                'categoryarray':['> 5000 and <= 10,000',
                                                                '> 10,000 and <= 50,000',
                                                                '> 50,000 and <= 100,000',
                                                                '> 100,000 and <= 500,000',
                                                                '> 500,000 and <= 1,000,000',
                                                                '> 1,000,000']})
        
         hist_votes.update_traces(
            hovertemplate=None,
            hoverinfo="skip")
        
         hist_votes.update_layout(
            xaxis_title_text = 'Count of movies', 
            yaxis_title_text = 'Votes category')

         st.plotly_chart(hist_votes,
                        theme =  'streamlit',
                        use_container_width = True)
            
    # chart 8, tree map:
    with c2:
        treemap = px.treemap(dfm, 
                 path=['Run time category'],
                 color_discrete_map='viridis')

        treemap.update_traces(
            hovertemplate=None,
            hoverinfo="skip",
            textfont=dict(size=15))

        st.header('Run time category tree map:')
        st.plotly_chart(treemap,
                        theme='streamlit',
                        use_container_width=True)

# calling function:
charts4()
