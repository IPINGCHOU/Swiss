import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set the title of the app
st.title("My Streamlit App")

# Add a header
st.header("Welcome to my app")

# Add some text
st.write("This is a simple Streamlit app.")

# Add an input box
user_input: str = st.text_input("Enter some text")

# Display the input text
st.write("You entered:", user_input)

# Add a button
if st.button("Click me"):
    st.write("Button clicked!")

# Add a slider
slider_value = st.slider("Select a value", 0, 100)
st.write("Slider value:", slider_value)

# Log the user input and slider value
logging.debug(f"User input: {user_input}")
logging.debug(f"Slider value: {slider_value}")