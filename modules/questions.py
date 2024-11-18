import streamlit as st
from modules import db
from datetime import datetime
import plotly.graph_objects as go

def ask_questions():
    st.write("## Mental Health Check-In")
    # Define the questions
    questions = [
        "How are you feeling today? (0 = Terrible, 10 = Great)",
        "How would you rate your level of serenity today? (0 = Poorly, 10 = Very well)",
        "How well did you sleep last night? (0 = Poorly, 10 = Very well)",
        "How productive were you today? (0 = Not at all, 10 = Extremely productive)",
        "How much did you enjoy your day today? (0 = Not at all, 10 = Very much)"
    ]

    # Define an empty list to store answers
    answers = []

    # Ask the questions and get the answers
    for question in questions:
        answer = st.slider(question, 0, 10)
        answers.append(answer)

    # Calculate the average of the answers
    average = sum(answers) / len(answers)

    st.markdown('##')
    # Display the average on the page
    st.write(f"Your average mental health score today is {average:.1f}")

    # Add the gauge chart to show where the average score lies on a scale of 0 to 10
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=average,
        mode="gauge+number",
    title={'text': "Mental Health Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'steps': [
                {'range': [0, 2], 'color': "red"},
                {'range': [2, 4], 'color': "orange"},
                {'range': [4, 6], 'color': "yellow"},
                {'range': [6, 8], 'color': "lightgreen"},
                {'range': [8, 10], 'color': "green"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': average}}))

    st.plotly_chart(fig, use_container_width=True, height=50)

    # Get the current date and time
    now = datetime.now()

    # Format the date as a string in the format "YYYY-MM-DD"
    date_string = now.strftime('%Y-%m-%d')

    # Add the entry to the database
    if st.button('Submit to your daily MindLens tracker'):
        #db.create_table()  # Create the table if it doesn't exist
        db.save_assessment(date=date_string, feeling=answers[0], serenity=answers[1], sleep=answers[2],
                     productivity=answers[3], enjoyment=answers[4], average=average)
        st.write("Your mental health check-in has been submitted!")

    return answers