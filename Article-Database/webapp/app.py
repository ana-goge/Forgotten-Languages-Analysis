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
st.write("Use this tool to search for articles based on different criteria. Select a search type and enter the relevant keyword.")

# Search options (removed Full Text and English Text options)
search_type = st.selectbox("Search by:", ["Keyword", "Date Range"])

if search_type == "Date Range":
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if start_date and end_date:
        if start_date > end_date:
            st.write("Error: Start date must be before end date.")
        else:
            # Convert dates to strings in the format YYYY-MM-DD
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")
            
            with st.spinner("Searching..."):
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
elif search_type == "Keyword":
    keyword = st.text_input("Enter a general keyword to search in selected fields:", placeholder="Enter keyword here")

    # Allow the user to choose which fields to search
    fields_to_search = st.radio(
        "Select fields to search:",
        options=["All fields (Title, Author, Tags, Full Text)", "Title", "Author", "Tags", "Full Text"],
        index=0  # Default is 'All fields'
    )

    if keyword.strip():
        with st.spinner("Searching..."):
            with sqlite3.connect(DB_FILE) as conn:
                try:
                    # Dynamically build the query based on selected fields
                    query = """
                        SELECT title, author, date_posted, tags, url, full_text
                        FROM posts
                        WHERE """
                    
                    conditions = []
                    params = []

                    # If searching for all fields
                    if fields_to_search == "All fields (Title, Author, Tags, Full Text)":
                        conditions += [
                            "title LIKE ?",
                            "author LIKE ?",
                            "tags LIKE ?"
                        ]
                        params += [f"%{keyword}%"] * 3

                        # Handle full_text separately to avoid issues with SQL syntax
                        conditions.append("full_text LIKE ?")
                        params.append(f"%{keyword}%")

                    # If searching in a specific field (title, author, tags, full_text)
                    else:
                        if fields_to_search == "Full Text":
                            conditions.append("full_text LIKE ?")
                            params.append(f"%{keyword}%")
                        else:
                            conditions.append(f"{fields_to_search.lower()} LIKE ?")
                            params.append(f"%{keyword}%")

                    # Combine all conditions with "OR"
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
