import sqlite3
import streamlit as st


def init_db():
    conn = sqlite3.connect('databases/mental_health.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mental_health (date TEXT, feeling TEXT, serenity TEXT, sleep TEXT,
                     productivity TEXT, enjoyment TEXT, average TEXT,user_name TEXT NOT NULL)''')
    conn.commit()
    return conn

def save_assessment(date, feeling, serenity, sleep, productivity, enjoyment, average):
    conn = sqlite3.connect('databases/mental_health.db')
    with conn:
        conn.execute("INSERT INTO mental_health (date, feeling, serenity, sleep, productivity, enjoyment, average,user_name) VALUES (?, ?, ?, ?, ?, ?, ?,?)", (date, feeling, serenity, sleep, productivity, enjoyment, average,st.session_state.get("current_user", None)))


def fetch_data(conn):
    data = conn.execute("SELECT * FROM mental_health where user_name=?",(st.session_state.get("current_user", None))).fetchall()
    return data
