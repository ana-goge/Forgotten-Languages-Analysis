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

# Streamlit app layout
st.title("Forgotten Languages Database Search Tool")

# Search options (removed Full Text and English Text options)
search_type = st.selectbox("Search by:", ["General Keyword", "Title", "Author", "Tags", "Date Range"])

if search_type == "Title":
    title = st.text_input("Enter a title or keyword:")
    st.write(f"Debug: User entered title '{title}'")  # Debugging input

    if title.strip():
        # Test the query in isolation
        with sqlite3.connect(DB_FILE) as conn:
            try:
                query = """
                    SELECT title, author, date_posted, tags, url 
                    FROM posts 
                    WHERE title LIKE ?
                """
                df = pd.read_sql_query(query, conn, params=(f"%{title}%",))
                if df.empty:
                    st.write(f"No results found for the title or keyword '{title}'.")
                else:
                    st.write(df)
            except Exception as e:
                st.write(f"Error: {e}")  # Display the error for further debugging
    else:
        st.write("Please enter a valid title or keyword.")

elif search_type == "Author":
    author = st.text_input("Enter an author's name:")
    st.write(f"Debug: User entered author '{author}'")  # Debugging input

    if author.strip():
        # Test the query in isolation
        with sqlite3.connect(DB_FILE) as conn:
            try:
                query = """
                    SELECT title, author, date_posted, tags, url 
                    FROM posts 
                    WHERE author = ?
                """
                df = pd.read_sql_query(query, conn, params=(author,))
                if df.empty:
                    st.write(f"No results found for author '{author}'.")
                else:
                    st.write(df)
            except Exception as e:
                st.write(f"Error: {e}")  # Display the error for further debugging
    else:
        st.write("Please enter a valid author's name.")

elif search_type == "Tags":
    tag = st.text_input("Enter a tag:")
    st.write(f"Debug: User entered tag '{tag}'")  # Debugging input

    if tag.strip():
        # Test the query in isolation
        with sqlite3.connect(DB_FILE) as conn:
            try:
                query = """
                    SELECT title, author, date_posted, tags, url 
                    FROM posts 
                    WHERE tags LIKE ?
                """
                df = pd.read_sql_query(query, conn, params=(f"%{tag}%",))
                if df.empty:
                    st.write(f"No results found for the tag '{tag}'.")
                else:
                    st.write(df)
            except Exception as e:
                st.write(f"Error: {e}")  # Display the error for further debugging
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
            
            with sqlite3.connect(DB_FILE) as conn:
                try:
                    query = """
                        SELECT title, author, date_posted, tags, url 
                        FROM posts 
                        WHERE date_posted_formatted BETWEEN ? AND ?
                    """
                    df = pd.read_sql_query(query, conn, params=(start_date_str, end_date_str))
                    if df.empty:
                        st.write(f"No results found between {start_date_str} and {end_date_str}.")
                    else:
                        st.write(df)
                except Exception as e:
                    st.write(f"Error: {e}")  # Display the error for further debugging
    else:
        st.write("Please select both start and end dates.")

# General Keyword Search Option with Toggle for Fields
elif search_type == "General Keyword":
    keyword = st.text_input("Enter a general keyword to search in selected fields:")
    st.write(f"Debug: User entered keyword '{keyword}'")  # Debugging input

    # Allow the user to choose which fields to search
    fields_to_search = st.multiselect(
        "Select fields to search:",
        ["title", "author", "tags", "full_text"],
        default=["title", "author", "tags", "full_text"]  # Default is all fields selected
    )

    if keyword.strip():
        with sqlite3.connect(DB_FILE) as conn:
            try:
                # Build the query dynamically based on selected fields
                query = """
                    SELECT title, author, date_posted, tags, url, full_text
                    FROM posts
                    WHERE """
                
                # Add the selected fields to the query
                conditions = []
                params = []
                for field in fields_to_search:
                    conditions.append(f"{field} LIKE ?")
                    params.append(f"%{keyword}%")
                
                # Join the conditions with "OR"
                query += " OR ".join(conditions)

                # Execute the query
                df = pd.read_sql_query(query, conn, params=params)

                if df.empty:
                    st.write(f"No results found for the keyword '{keyword}'.")
                else:
                    st.write(df)
            except Exception as e:
                st.write(f"Error: {e}")  # Display the error for further debugging
    else:
        st.write("Please enter a valid keyword.")

st.write("Powered by Streamlit")
