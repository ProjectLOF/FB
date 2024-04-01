import streamlit as st
from PIL import Image

st.title("MVP Webpage")

st.header("Thank you for visiting us and sharing your :blue[Feedback]!!! :sunglasses:")
from streamlit_star_rating import st_star_rating




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
   st_star_rating(label = "Please rate you experience", maxValue = 5, defaultValue = 3, key = "rating", emoticons = True )

