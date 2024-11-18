import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules import db
import sqlite3
import streamlit as st


DATABASE_PATH = "./databases/mental_health.db"


def read_data():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM mental_health where user_name='"+st.session_state.get("current_user", None)+"' ORDER BY date DESC", conn)
    return df


def get_average_scores(conn):
    df2 = pd.read_sql_query(
        "SELECT AVG(feeling) as avg_feeling, AVG(serenity) as avg_serenity, AVG(sleep) as avg_sleep, AVG(productivity) as avg_productivity, AVG(enjoyment) as avg_enjoyment FROM mental_health where user_name='"+st.session_state.get("current_user", None)+"' ", conn)
    return df2.values[0]


def get_average_scores_dataframe(average_scores):
    df3 = pd.DataFrame({
        "category": ["feeling", "serenity", "sleep", "productivity", "enjoyment"],
        "average": average_scores
    })
    return df3


def show_dataframe():
    st.write("## Mental Health Data")
    df = read_data()
    st.dataframe(df)


def delete_data():
    if st.button("Delete all data"):
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("delete from mental_health where  user_name='"+st.session_state.get("current_user", None)+"' ")
        st.write("All data has been deleted from the database.")


def show_visualization():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = read_data()

        # Generate the visualizations
        fig1 = px.line(df, x="date", y="average", line_shape="spline", color_discrete_sequence=["red"])
        fig1.update_layout(xaxis_tickformat='%Y-%m-%d',
                           title="Average Mental Health Score Over Time")

        fig2 = px.line(df, x="date", y=["feeling", "serenity", "sleep", "productivity", "enjoyment"],
                       line_shape="spline")
        fig2.update_layout(xaxis_tickformat='%Y-%m-%d',
                           title="Mental Health Scores Over Time")

        # Get and plot the average scores
        average_scores = get_average_scores(conn)
        df3 = get_average_scores_dataframe(average_scores)

        fig3 = px.bar_polar(df3, r="average", theta="category", template="plotly_dark")
        fig3.update_traces(opacity=0.7)
        fig3.update_layout(title="Average Mental Health Scores by Category")

    # Show the visualizations on the page
    show_dataframe()
    delete_data()
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)