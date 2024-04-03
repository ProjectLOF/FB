import streamlit as st
from PIL import Image
from streamlit_star_rating import st_star_rating
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import plotly.express as px 
from datetime import datetime



st.title("POC Webpage")


tab_poc_voting, tab_poc_viz = st.tabs(["POC Voting", "POC Viz"])



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
         collection = db["poc_stage"]
         data = pd.DataFrame(list(collection.find({})))
         st.write(data)    
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
   fig = px.histogram(df, x="best_dish", labels={'best_dish':'Recommended Dish'}, title="Most Recommended Dishes")
   fig.update_layout(yaxis_title="Number of Customers")
   st.plotly_chart(fig)

   fig2 = px.line(df, x=df.index, y='overall_rating', labels={'index':'Customers'}, title="Overall Customer Rating")
   fig2.update_layout(yaxis_title="Customer Rating")
   st.plotly_chart(fig2)



