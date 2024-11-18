import streamlit as st
import pandas as pd
from groq import Groq
import openai
from modules import db
import tabulate
import sqlite3

DATABASE_PATH = "./databases/mental_health.db"

# Authenticate with the OpenAI API

def show_guidance():
    st.write("## Mental Health Guidances")

    # Retrieve the data from the database
    conn = db.init_db()
    df = pd.read_sql_query("SELECT * FROM mental_health where user_name='"+st.session_state.get("current_user", None)+"' ORDER BY date DESC", conn)

    # Generate the prompt string
    dataframe_string = tabulate.tabulate(df.head(), headers='keys', tablefmt='pipe', showindex=False)
    prompt = f"I have been tracking my mental health over the last 5 days, and I'd like some insights and tips based on my data. Here is my data:\n"+dataframe_string+"\nCan you provide personalized advice based on this data to help improve my well-being? Specifically, I'd appreciate tips to enhance my serenity, sleep quality, productivity, and overall enjoyment"

    # Add a button to generate guidance
    if st.button("Generate guidance"):
        
        client = Groq(
            api_key="",
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        # Display the response to the user
        guidance = chat_completion.choices[0].message.content
        st.write(guidance)
