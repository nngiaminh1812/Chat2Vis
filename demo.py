import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import pandas as pd
from chatbox import send_prompt, establish_api

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv('API_KEY')
print(API_KEY)
st.write(establish_api(API_KEY))
print("API Key inserted successfully!")

# Define the AI prompts for different datasets
description_prompts = {
    "netflix_titles.csv": """
        Use a dataframe called df from netflix_titles.csv with the following columns:
             'show_id','type','title','director','cast','country','date_added','release_year','rating','duration','listed_in','description'.
        The type of each column is as follows:
        - show_id: str
        - type: str
        - title: str
        - director: str
        - cast: str
        - country: str
        - date_added: str, contains values like 'August 4, 2017' for example
        - release_year: int
        - rating: str
        - duration: str
        - listed_in: str
        - description: str   
        Use df[''] to access the columns.     
        Strip leading/trailing whitespace from date_added column
        Label the x and y axes appropriately.
        Add a title. Set the fig suptitle as empty.
        Script should be ended with plt.show(). No need to return several ways to plot the same data.
        Returned script with no ''' at head and tail.
        'Axes' object has no attribute 'set_suptitle'.
        'Axes' object has no attribute 'set_figsuptitle'.
        No need to add code for 'Axes' more.
        Rotate the x-axis labels if needed.
        Using Python version 3.11.0, create a script using dataframe df to graph the following:
        """
        ,
    "StudentsPerformance.csv": """
        Use a dataframe called df from StudentsPerformance.csv with the following columns:
        "gender","race/ethnicity","parental level of education","lunch","test preparation course","math score","reading score","writing score"
        The type of each column is as follows:
        - gender: str, contains two unique values including "male", and "female"
        - race/ethnicity: str, contains five unique values including "group A", "group B", "group C", "group D", and "group E"
        - 'parental level of education': str, contains six unique values including "some high school", "high school", "some college", "associate's degree", "bachelor's degree", and "master's degree"
        - lunch: str, contains two unique values including "standard", and "free/reduced"
        - 'test preparation course': str, contains two unique values including "none", and "completed"
        - 'math score': int, contains values between 0 and 100
        - 'reading score': int, contains values between 0 and 100
        - 'writing score': int, contains values between 0 and 100
        Use df[''] to access the columns. 
        Label the x and y axes appropriately.
        Add a title. Set the fig suptitle as empty.
        Script should be ended with plt.show(). No need to return several ways to plot the same data.
        Returned script with no ''' at head and tail.
        'Axes' object has no attribute 'set_suptitle'.
        'Axes' object has no attribute 'set_figsuptitle'.
        No need to add code for 'Axes' more.
        Rotate the x-axis labels if needed.
        Using Python version 3.11.0, create a script using dataframe df to graph the following:
        """
}

code_prompts = {
    "netflix_titles.csv": """
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
df_movies = pd.read_csv('netflix_titles.csv')
df = df_movies.copy()
"""
,
    "StudentsPerformance.csv": """
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
df_students = pd.read_csv('StudentsPerformance.csv')
df = df_students.copy()
"""

}

# Function to interact with the Gemini API and generate a script to viz data
def show_chat2vis_ai(dataset):
    st.title("Give it to me")
    st.write("I am a data visualization expert, give me a question about visualizing data!")
    
    prompt = st.chat_input("Enter a prompt here")

    if prompt:
        full_prompt = [description_prompts[dataset] + prompt]
        response = send_prompt(full_prompt, code_prompts[dataset])
        
        if "Sorry" in response or "not a valid script" in response:
            st.write(response)
        else:
            try:
                response = response.replace("plt.show()", "")
                st.write(f"User Prompt: {prompt}")
                st.write("Visualization:")
                script = code_prompts[dataset] + response + "\nst.pyplot(fig)"
                print(f"Executed Script: \n{script}")
                exec(script)
                
                st.write("Script executed successfully. Check the visualization above.")
            except Exception as e:
                st.write(f"Error executing script: {e}")

def main():
    st.title("Welcome to Our Research Paper")
    st.write("This is a demo of our research.")
    
    dataset = st.selectbox("Choose a dataset", ["netflix_titles.csv", "StudentsPerformance.csv"])
    
    if dataset:
        show_chat2vis_ai(dataset)

if __name__ == "__main__":
    main()