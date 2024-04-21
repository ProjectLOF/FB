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



def test_db(dish_recommendation,customer_service, ambience_service, user_comment, order):
      documens = [{"table_number": "12", "datetime":str(datetime.now()),"recommendation": dish_recommendation, "cs_rating":customer_service, 
         "ambience_service": ambience_service, "user_comments": user_comment, "order": order}, {"table_number": "12", "datetime":str(datetime.now()),"recommendation": dish_recommendation[0], "cs_rating":customer_service, 
         "ambience_service": ambience_service, "user_comments": user_comment, "order": order}]



def update_db(dish_recommendation,customer_service, ambience_service, user_comment, order,dish_improvement,user_improvement,repeat_intension):

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
         "ambience_service": ambience_service, "user_comments": user_comment, 
         "order": order,"dish_to_improvement":dish_improvement,"improvements": user_improvement, "repeat_intension": repeat_intension}
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
         return orders
   except Exception as e:
      st.write(e)

def get_latest_orders():
   uri = "mongodb+srv://{}:{}@projectlofcluster.kxjkvqf.mongodb.net/?retryWrites=true&w=majority&appName=ProjectLOFCluster".format(st.secrets["db_username"],st.secrets["db_password"] )
   client = MongoClient(uri, server_api=ServerApi('1'))
   try:
         client.admin.command('ping')
         db = client["order_db_v0"]
         collection = db["demo_setup_v0"]
         db_response =list(collection.find().sort([('_id', -1)]).limit(1))
         orders = db_response[0]["order_list"]
         orders.append("None")
         return orders

   except Exception as e:
      st.write(e)
    
def get_latest_questions():
   uri = "mongodb+srv://{}:{}@projectlofcluster.kxjkvqf.mongodb.net/?retryWrites=true&w=majority&appName=ProjectLOFCluster".format(st.secrets["db_username"],st.secrets["db_password"] )
   client = MongoClient(uri, server_api=ServerApi('1'))
   try:
         client.admin.command('ping')
         db = client["order_db_v0"]
         collection = db["demo_questions_v0"]
         db_response =list(collection.find().sort([('_id', -1)]).limit(1))
         questions = db_response[0]["questions_list"]
         return questions

   except Exception as e:
      st.write(e)

st.header("Thank you for visiting us and sharing your :blue[Feedback]!!! :sunglasses:")

orders = get_latest_orders()
        
with st.container(border=True):    
   dish_improvement = st.multiselect("Dish to be Improved?", orders,default="None")
   user_improvement = "NA"
   if len(dish_improvement) > 0 and "None" not in dish_improvement :
            user_improvement = st.selectbox("What are the improvements?", ["Need more Spice","Need more Salt","Need Less Spice","Need less Salt", "Drop the dish"])
with st.form("Feedback", clear_on_submit=True): 
   repeat_intension = st.selectbox("Will you visit us again?", ["Yes", "Undecided", "Never"])
   dish_recommendation = st.multiselect("Recommend dish to a friend",orders,default="None",)
   customer_service = st_star_rating("Please Rate Our Customer Service", maxValue=5, defaultValue=3, key="cs_rating_form")
   ambience_service = st_star_rating("Please Rate Our Ambience ", maxValue=5, defaultValue=3, key="ambience_rating_form")
   user_comment = st.text_input("More Feedback?")
   submit = st.form_submit_button("Feedback_submit")
   if submit:
      update_db(dish_recommendation,customer_service, ambience_service, user_comment, 
                orders,dish_improvement,user_improvement,repeat_intension)
      st.write("Your feedback has been stored to improve your experience in the future")