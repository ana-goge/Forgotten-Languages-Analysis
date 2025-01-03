import sqlite3
from datetime import datetime

def search_posts(query_type, query_value=None, start_date=None, end_date=None):
    """Search posts in the database based on the query type and value."""
    with sqlite3.connect('newdb.db') as conn:
        cursor = conn.cursor()
        
        if query_type == "title":
            cursor.execute(
                "SELECT title, author, date_posted, tags FROM posts WHERE title LIKE ?",
                (f"%{query_value}%",)
            )
        elif query_type == "author":
            cursor.execute(
                "SELECT title, author, date_posted, tags FROM posts WHERE author LIKE ?",
                (f"%{query_value}%",)
            )
        elif query_type == "tags":
            cursor.execute(
                "SELECT title, author, date_posted, tags FROM posts WHERE tags LIKE ?",
                (f"%{query_value}%",)
            )
        elif query_type == "date_range":
            cursor.execute(
                "SELECT title, author, date_posted, tags FROM posts WHERE date_posted BETWEEN ? AND ?",
                (start_date, end_date)
            )
        else:
            raise ValueError("Invalid query type. Must be 'title', 'author', 'tags', or 'date_range'.")

        results = cursor.fetchall()
        return results

if __name__ == "__main__":
    print("Welcome to the Enhanced Forgotten Languages Database Search Tool!")
    print("You can search by: title, author, tags, or date range.\n")

    query_type = input("Enter the type of search (title/author/tags/date_range): ").strip().lower()

    if query_type in ["title", "author", "tags"]:
        query_value = input(f"Enter a keyword to search by {query_type}: ").strip()
        results = search_posts(query_type, query_value=query_value)
    elif query_type == "date_range":
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
        
        # Validate dates
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            exit()

        results = search_posts(query_type, start_date=start_date, end_date=end_date)
    else:
        print("Invalid search type. Please choose from title, author, tags, or date_range.")
        exit()

    # Display results
    if results:
        print(f"\nFound {len(results)} result(s):\n")
        for row in results:
            print(f"Title: {row[0]}, Author: {row[1]}, Date: {row[2]}, Tags: {row[3]}")
    else:
        print("\nNo results found.")
