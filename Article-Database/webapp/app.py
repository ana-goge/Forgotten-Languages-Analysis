import sqlite3
import streamlit as st
import pandas as pd

# Connect to the SQLite database
DB_FILE = "newdb.db"

def query_database(query, params=()):
    """Execute a query and return results as a DataFrame."""
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql_query(query, conn, params)

# Streamlit app layout
st.title("Forgotten Languages Database Search Tool")

# Search options
search_type = st.selectbox("Search by:", ["Title", "Author", "Tags", "Date Range"])

if search_type == "Title":
    title = st.text_input("Enter a title or keyword:")
    if title:
        results = query_database(
            "SELECT title, author, date_posted, tags FROM posts WHERE title LIKE ?",
            (f"%{title}%",)
        )
        st.write(results)

elif search_type == "Author":
    author = st.text_input("Enter an author's name:")
    if author:
        results = query_database(
            "SELECT title, author, date_posted, tags FROM posts WHERE author LIKE ?",
            (f"%{author}%",)
        )
        st.write(results)

elif search_type == "Tags":
    tag = st.text_input("Enter a tag:")
    if tag:
        results = query_database(
            "SELECT title, author, date_posted, tags FROM posts WHERE tags LIKE ?",
            (f"%{tag}%",)
        )
        st.write(results)

elif search_type == "Date Range":
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if start_date and end_date:
        results = query_database(
            "SELECT title, author, date_posted, tags FROM posts WHERE date_posted BETWEEN ? AND ?",
            (start_date, end_date)
        )
        st.write(results)

st.write("Powered by Streamlit")
