import streamlit as st
from PIL import Image
from streamlit_star_rating import st_star_rating
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import plotly.express as px 



st.title("POC Webpage")


tab_options, tab_poc_voting, tab_poc_viz = st.tabs(["Options", "POC Voting", "POC Viz"])



def update_db(dish_recommendation,stars):

      uri = "mongodb+srv://{}:{}@projectlofcluster.kxjkvqf.mongodb.net/?retryWrites=true&w=majority&appName=ProjectLOFCluster".format(st.secrets["db_username"],st.secrets["db_password"] )
      # Create a new client and connect to the server
      client = MongoClient(uri, server_api=ServerApi('1'))
      # Send a ping to confirm a successful connection
      try:
         client.admin.command('ping')
         st.write("Pinged your deployment. You successfully connected to MongoDB!")
         db = client["feedback_v0"]
         collection = db["poc_stage"]
         document = {"table_number": "12", "best_dish": dish_recommendation , "overall_rating":stars}
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

   with st.form("Feedback", clear_on_submit=True):
      dish_recommendation = st.selectbox("Recommend a friend", ["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"])
      stars = st_star_rating("Please rate you experience", maxValue=5, defaultValue=3, key="rating_form")
      submit = st.form_submit_button("Feedback_submit")
      if submit:
         update_db(dish_recommendation,stars)
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



with tab_options:


   with st.container():
      st.write("*Option 1*")

      # You can call any Streamlit command, including custom components:
      st.selectbox("Best Dish", ["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"])

   with st.container():
      st.write("*Option 2*")

      st.radio("What was the best dish you had today?", ["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"])  


   with st.container():
      st.write("*Option 3*")

      # You can call any Streamlit command, including custom components:
      st.select_slider(
      'What was the best dish you had today?',
      options=["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"], label_visibility="visible")


   with st.container():
      st.write("*Option 4*")
      st.write("What was the best dish you had today?")

      col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
      col1.button("None", use_container_width = True)
      col2.button("Mutton Biryani", use_container_width = True)
      col3.button("Chicken Vindalo", use_container_width = True)
      col4.button("Fried Rice", use_container_width = True)


   with st.container():
      st.write("*Option 5*")

      st.multiselect("What dish would you recommend to your friends?", ["None","Mutton Biryani", "Chicken Vindalo", "Fried Rice"])


   with st.container():
      st.write("*Option 6*")
      stars = st_star_rating("Please rate you experience", maxValue=5, defaultValue=3, key="rating")



   with st.container():
      st.write("*Option 7*")
      emoji = st_star_rating(label = "Please rate you experience", maxValue = 5, defaultValue = 3, key = "emoji rating", emoticons = True )



