import os
import sqlite3
import streamlit as st
import pandas as pd
import gzip
import shutil

# Decompress the database file
DB_COMPRESSED = "./Article-Database/webapp/newdb.db.gz"  
DB_FILE = "newdb.db"

if not os.path.exists(DB_FILE): 
    with gzip.open(DB_COMPRESSED, 'rb') as f_in:
        with open(DB_FILE, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

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
    if title.strip():  # Ensure input is not empty or just whitespace
        results = query_database(
            """
            SELECT title, author, date_posted, tags 
            FROM posts 
            WHERE title LIKE ?
            """,
            (f"%{title}%",)
        )
        if not results.empty:
            st.write(results)
        else:
            st.write(f"No results found for the title or keyword '{title}'.")
    else:
        st.write("Please enter a valid title or keyword.")

elif search_type == "Author":
    author = st.text_input("Enter an author's name:")
    st.write(f"Debug: User entered author '{author}'")  # Print the input for debugging
    if author.strip():  # Ensure input is not empty or just whitespace
        results = query_database(
            """
            SELECT title, author, date_posted, tags 
            FROM posts 
            WHERE author = ?
            """,
            (author,)  # Ensure this matches the input correctly
        )
        if not results.empty:
            st.write(results)
        else:
            st.write(f"No results found for the author '{author}'.")
    else:
        st.write("Please enter a valid author's name.")

elif search_type == "Tags":
    tag = st.text_input("Enter a tag:")
    if tag.strip():  # Ensure input is not empty or just whitespace
        results = query_database(
            """
            SELECT title, author, date_posted, tags 
            FROM posts 
            WHERE tags LIKE ?
            """,
            (f"%{tag}%",)
        )
        if not results.empty:
            st.write(results)
        else:
            st.write(f"No results found for the tag '{tag}'.")
    else:
        st.write("Please enter a valid tag.")

elif search_type == "Date Range":
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if start_date and end_date:
        if start_date > end_date:
            st.write("Error: Start date must be before end date.")
        else:
            # Convert dates to strings in the format YYYY-MM-DD
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            
            results = query_database(
                """
                SELECT title, author, date_posted, tags 
                FROM posts 
                WHERE date_posted BETWEEN ? AND ?
                """,
                (start_date_str, end_date_str)
            )
            if not results.empty:
                st.write(results)
            else:
                st.write(f"No results found between {start_date_str} and {end_date_str}.")
    else:
        st.write("Please select both start and end dates.")

st.write("Powered by Streamlit")
