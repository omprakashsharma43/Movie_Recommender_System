import streamlit as st
import pickle
import pandas as pd
import requests
import datetime

st.set_page_config(layout="wide")

# # # Background Image :-----------------------------------------------------------------------

import base64
# Function to load and encode local image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Path to your image
img_path = "photo.jpg"
img_base64 = get_base64_of_bin_file(img_path)

# CSS with overlay for opacity control
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: 
        linear-gradient(rgba(10,10,10,0.75), rgba(10,10,10,0.75)),  /* overlay */
        url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# # # Open Pickle File :-------------------------------------------------------------------------
movies_dict=pickle.load(open("movie_dict.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))

movies = pd.DataFrame(movies_dict)


# # # Fetch Poster Function :--------------------------------------------------------------------- 

def fetch_poster(movie_id):  #8265bd1679663a7ea12ac168da84d2e8
    try:
        response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=4990f10b4b23f1616f0f2df3bbcf56e8&language=en-US".format(movie_id))
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        
    except:
        return "https://via.placeholder.com/500x750?text=No+Internet"



# # # Movie Recommendation Function :------------------------------------------------------------- 

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0] # In similarity , Dataframe of Vectors[Distances] = Dataframe of Array
    distances = similarity[movie_index] # Individual array -> Vector[Distances]
 
    movies_list = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[0:6] # when sorting index position loose then use enumirate
    
    recommended_movies_title = []
    recommended_movies_director = []
    recommended_movies_rdate = []
    recommended_movies_id = []

    recommended_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies_id.append(movie_id)
        recommended_movies_title.append(movies.iloc[i[0]].title)
        recommended_movies_director.append(movies.iloc[i[0]].director[0])

        # Release Date
        date = str(movies.iloc[i[0]].release_date)
        original_date_str = date
        date_object = datetime.datetime.strptime(original_date_str, "%Y-%m-%d")
        formatted_date_str = date_object.strftime("%d-%b-%Y")

        recommended_movies_rdate.append(formatted_date_str)

        # Fetch poster from API
        recommended_poster.append(fetch_poster(movie_id))  
    return recommended_movies_id, recommended_movies_title,recommended_movies_director,recommended_movies_rdate , recommended_poster    



# # # Streamlit Content :----------------------------------------------------------------------------- 

# Title
# st.title("------------------------- Movie Recommender System ! -------------------------")

st.markdown("<h1 style='text-align: center;'>Movie Recommender System !</h1>", unsafe_allow_html=True)
st.text("_________________________________________________________________________________________________________________________________________________________________________")


# Checkbox
selected_movie_name = st.selectbox(
    "Select Movies of your choice... ",
    movies["title"].values
    )


# Button
if st.button("Recommend"):
    st.text("_________________________________________________________________________________________________________________________________________________________________________")

    id, movie_names, director_names, release_dates , posters= recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1 :
        st.image(posters[0])
        st.markdown("###### Movie Title :")
        st.markdown(f"##### {movie_names[0]}") 

        st.markdown("###### Director Name :")
        st.markdown(f"##### {director_names[0]}") 
        
        st.markdown("###### Release Date :")
        st.markdown(f"##### {release_dates[0]}") 

        st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[0]}")

    with col2 :
        st.image(posters[1])
        st.markdown("###### Movie Title :")
        st.markdown(f"##### {movie_names[1]}") 

        st.markdown("###### Director Name :")
        st.markdown(f"##### {director_names[1]}") 
        
        st.markdown("###### Release Date :")
        st.markdown(f"##### {release_dates[1]}") 

        st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[1]}")

         

    with col3 :
        st.image(posters[2])
        st.markdown("###### Movie Title :")
        st.markdown(f"##### {movie_names[2]}") 

        st.markdown("###### Director Name :")
        st.markdown(f"##### {director_names[2]}") 
        
        st.markdown("###### Release Date :")
        st.markdown(f"##### {release_dates[2]}") 
        
        st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[2]}")


    with col4 :
        st.image(posters[3])
        st.markdown("###### Movie Title :")
        st.markdown(f"##### {movie_names[3]}") 

        st.markdown("###### Director Name :")
        st.markdown(f"##### {director_names[3]}") 
        
        st.markdown("###### Release Date :")
        st.markdown(f"##### {release_dates[3]}") 

        st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[3]}")

        

    with col5 :
       st.image(posters[4])                
       st.markdown("###### Movie Title :")
       st.markdown(f"##### {movie_names[4]}") 

       st.markdown("###### Director  :")
       st.markdown(f"##### {director_names[4]}") 
        
       st.markdown("###### Release Date :")
       st.markdown(f"##### {release_dates[4]}") 
        
       st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[4]}")


    
    with col6 :
       st.image(posters[5])                
       st.markdown("###### Movie Title :")
       st.markdown(f"##### {movie_names[5]}") 

       st.markdown("###### Director Name :")
       st.markdown(f"##### {director_names[5]}") 
        
       st.markdown("###### Release Date :")
       st.markdown(f"##### {release_dates[5]}") 

       st.link_button("Go to Movie ", f"https://www.themoviedb.org/movie/{id[5]}")

         
