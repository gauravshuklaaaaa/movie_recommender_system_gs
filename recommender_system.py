import streamlit as st 
import pickle
import pandas as pd 
import requests

def fetch_movie_details(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4466b0524f90535ea380af84dd4b09ee'.format(movie_id))
    data=response.json()
    # print(data)
    poster="https://image.tmdb.org/t/p/original/"+data['poster_path']
    title=data.get('title')
    overview=data.get('overview')
    rating=data.get('vote_average')
    release_date=data.get('release_date')

    
    
    return poster,title,overview,rating,release_date





def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x: x[1])[1:7]
    recommend_movies=[]
    recommended_movies_posters=[]
    recommended_details=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].id
        poster, title, overview, rating, release_date = fetch_movie_details(movie_id)
        recommended_details.append((poster, title, overview, rating, release_date))
      

        # recommend_movies.append(movies.iloc[i[0]].title)
        #   # fetch poster from API 
        # recommended_movies_posters.append(fetch_poster(movie_id))
    # return recommend_movies,recommended_movies_posters
    return recommended_details
 


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open ('similarity.pkl','rb'))
# for ui 
st.markdown("<h1 style='text-align:center;color:#FF5733;'>🎬 Movies Recommender System</h1>", unsafe_allow_html=True)
st.write("Find similar movies based on your favourite ones! Just type in a movie name and get recommendations.")

# selected_movie_name = st.selectbox(
#     "Kaun si movie ka recommendation lena chahenge aap ?",
#     movies['title'].values
# )
st.markdown("""
    <style>
    .search-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .search-box input {
        padding: 10px 15px;
        width: 300px;
        border-radius: 10px;
        border: 1px solid #FF5733;
        font-size: 16px;
    }
    .search-btn button {
        background-color: #FF5733 !important;
        color: white !important;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 16px;
        cursor: pointer;
    }
    .search-btn button:hover {
        background-color: #e74c3c !important;
    [data-testid="stAppViewContainer"] {
    background-color: #121212;
    color: white;
    }
    h1 {
        color: #FF5733;
        text-align: center;
    }
        }
            
    </style>
""", unsafe_allow_html=True)
col1, col2 = st.columns([4,1])
with col1:
    movie_search = st.text_input("", placeholder="🔍 Type a movie name...", key="search_box")
with col2:
    st.write("")
    st.write("")
    search_clicked = st.button("Search 🎬", key="search_btn")
if search_clicked:
    matched_movies=movies[movies['title'].str.contains(movie_search, case=False, na=False)]
    if not matched_movies.empty:
        st.session_state['matched_movies']=matched_movies['title'].values.tolist()
    else:
        st.session_state['matched_movies']=[]
        st.warning("Movie not found. Please check the spelling or try another movie.")

if 'matched_movies' in st.session_state and st.session_state['matched_movies']:
    selected_movie = st.selectbox("App kaunsi movie select karna chahte hai ?", st.session_state['matched_movies'])
    
    if st.button("Recommend", key='recommend_search'):
        recommendations = recommend(selected_movie)
        if recommendations:
                st.subheader("Top Recommendations 🎥")
                st.markdown("---")

                
                cols=st.columns(3)


                for idx,( poster, title, overview, rating, release_date) in enumerate(recommendations):
                    # st.markdown("<div style='background-color:#1e1e1e; padding:15px; border-radius:15px; margin-bottom:15px;'>", unsafe_allow_html=True)
                    # colA, colB = st.columns([1,2])
                    # with colA:
                    with cols[idx%3]:
                        st.image(poster, use_container_width=True)
                    
                        st.markdown(f'<b>{title}</b><br><i>📅{release_date}</i>',unsafe_allow_html=True)
                        
                        short_overview=overview if len(overview)<=150 else overview[:150]+"..."
                        st.write(short_overview)
                        num_stars=int(round(rating/2))
                        stars="⭐"*num_stars
                        st.markdown(f"{stars} ({rating}/10)")


                    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #888888; margin-top: 30px; font-size: 14px;'>
Crafted with ❤️ by Gaurav Shukla
</div>
""", unsafe_allow_html=True)


    # else:
    #     st.write("Movie not found. Please check the spelling or try another movie.")
