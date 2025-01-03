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
st.write("Use this tool to search for articles based on various fields. Enter a keyword and select the fields you wish to search in, and optionally filter by date range.")

# General Keyword Search Option with Toggle for Fields
search_type = "General Keyword"  # Only keep the general keyword option

# Keyword input and field selection
keyword = st.text_input("Enter a general keyword to search in selected fields:", placeholder="Enter keyword here")
fields_to_search = st.radio(
    "Select fields to search:",
    options=["All fields (Title, Author, Tags, Full Text)", "Title", "Author", "Tags", "Full Text"],
    index=0  # Default is 'All fields'
)

# Date Range search
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Processing the search query
if keyword.strip() or (start_date and end_date):  # Ensure either keyword or date range is provided
    with st.spinner("Searching..."):
        with sqlite3.connect(DB_FILE) as conn:
            try:
                query = """
                    SELECT title, author, date_posted, tags, url, full_text
                    FROM posts
                    WHERE """
                
                params = []
                conditions = []

                # Add keyword search conditions
                if keyword.strip():
                    if fields_to_search == "All fields (Title, Author, Tags, Full Text)":
                        conditions += [
                            "title LIKE ?",
                            "author LIKE ?",
                            "tags LIKE ?",
                            "full_text LIKE ?"
                        ]
                        params += [f"%{keyword}%"] * 4
                    else:
                        conditions.append(f"{fields_to_search.lower()} LIKE ?")
                        params.append(f"%{keyword}%")
                
                # Add date range conditions
                if start_date and end_date:
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    end_date_str = end_date.strftime("%Y-%m-%d")
                    conditions.append("date_posted_formatted BETWEEN ? AND ?")
                    params += [start_date_str, end_date_str]

                # Build the query based on the selected conditions
                query += " AND ".join(conditions)

                # Execute the query
                df = pd.read_sql_query(query, conn, params=params)

                if df.empty:
                    st.write(f"No results found for the search criteria.")
                else:
                    st.write(df)
            except Exception as e:
                st.write(f"Error: {e}")  # Display the error for further debugging
else:
    st.write("Please enter a valid keyword or select a date range.")

st.write("Powered by Streamlit")
