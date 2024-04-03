import streamlit as st
from PIL import Image
from streamlit_star_rating import st_star_rating
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import plotly.express as px 
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("POC Webpage")


tab_poc_voting, tab_poc_viz = st.tabs(["POC Voting", "POC Viz"])


def test_db(dish_recommendation,customer_service, ambience_service, user_comment, order):
      documens = [{"table_number": "12", "datetime":str(datetime.now()),"recommendation": dish_recommendation, "cs_rating":customer_service, 
         "ambience_service": ambience_service, "user_comments": user_comment, "order": order}, {"table_number": "12", "datetime":str(datetime.now()),"recommendation": dish_recommendation[0], "cs_rating":customer_service, 
         "ambience_service": ambience_service, "user_comments": user_comment, "order": order}]



def update_db(dish_recommendation,customer_service, ambience_service, user_comment, order):

      uri = "mongodb+srv://{}:{}@projectlofcluster.kxjkvqf.mongodb.net/?retryWrites=true&w=majority&appName=ProjectLOFCluster".format(st.secrets["db_username"],st.secrets["db_password"] )
      # Create a new client and connect to the server
      client = MongoClient(uri, server_api=ServerApi('1'))
      # Send a ping to confirm a successful connection
      try:
         client.admin.command('ping')
         #st.write("Pinged your deployment. You successfully connected to MongoDB!")
         db = client["feedback_v0"]
         collection = db["poc_v1"]
         document = {"table_number": "12", "datetime":str(datetime.now()),"recommendation": dish_recommendation, "cs_rating":customer_service, 
         "ambience_service": ambience_service, "user_comments": user_comment, "order": order}
         inserted_document = collection.insert_one(document)
         client.close()
      except Exception as e:
         st.write(e)


def get_all_data():
   uri = "mongodb+srv://{}:{}@projectlofcluster.kxjkvqf.mongodb.net/?retryWrites=true&w=majority&appName=ProjectLOFCluster".format(st.secrets["db_username"],st.secrets["db_password"] )
   client = MongoClient(uri, server_api=ServerApi('1'))
   try:
         client.admin.command('ping')
         st.write("Pinged your deployment. You successfully connected to MongoDB!")
         db = client["feedback_v0"]
         collection = db["poc_v1"]
         data = pd.DataFrame(list(collection.find({})))
         st.dataframe(data)    
         client.close()
         return data
   except Exception as e:
      st.write(e)



with tab_poc_voting :

   st.header("Thank you for visiting us and sharing your :blue[Feedback]!!! :sunglasses:")

   order = ["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"]

   with st.form("Feedback", clear_on_submit=True):
      with st.container(border=True):
         dish_recommendation = st.multiselect("Recommend a friend",order)
      with st.container(border=True):   
         customer_service = st_star_rating("Please Rate Our Customer Service", maxValue=5, defaultValue=3, key="cs_rating_form")
      with st.container(border=True):
         ambience_service = st_star_rating("Please Rate Our Ambience ", maxValue=5, defaultValue=3, key="ambience_rating_form")
      with st.container(border=True):
         user_comment = st.text_input("More Feedback?")

      
      submit = st.form_submit_button("Feedback_submit")
      if submit:
         update_db(dish_recommendation,customer_service, ambience_service, user_comment, order)

         st.write("Your feedback has been stored to improve your experience in the future")


with tab_poc_viz:
   df = get_all_data()
   # plotting the pie chart
   if df.empty:
      st.write("No data in DB")
   else:
      recommendation_series = df.recommendation.explode().fillna('[]').value_counts()
      
      with st.container(border=True):
         fig = px.histogram(recommendation_series, x=recommendation_series.index,y= "count", title="Most Recommended Dishes")
         fig.update_layout(yaxis_title="Number of Customers")
         st.plotly_chart(fig, use_container_width=True)

      with st.container(border=True):

         fig2 = px.line(df, x=df.datetime, y='cs_rating', labels={'datetime':'Time'}, title="Overall Customer Service Rating")
         fig2.update_layout(yaxis_title="Customer Service Rating")
         st.plotly_chart(fig2, use_container_width=True)

      with st.container(border=True):

         fig3 = px.line(df, x=df.datetime, y='ambience_service', labels={'datetime':'Time'}, title="Overall Ambience Rating")
         fig3.update_layout(yaxis_title="Ambience Rating")
         st.plotly_chart(fig3, use_container_width=True)
      
      with st.container(border=True):
         
         text = (df.user_comments.str.cat(sep=','))
         # Create and generate a word cloud image:
         wordcloud = WordCloud().generate(text)
         # Display the generated image:
         plt.imshow(wordcloud, interpolation='bilinear')

         st.pyplot()


      



