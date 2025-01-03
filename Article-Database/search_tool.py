import sqlite3

def search_posts_by_title(keyword):
    """Search posts in the database by title keyword."""
    with sqlite3.connect('newdb.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT title, author, date_posted, tags FROM posts WHERE title LIKE ?",
            (f"%{keyword}%",)
        )
        results = cursor.fetchall()
        return results

if __name__ == "__main__":
    print("Welcome to the Forgotten Languages Database Search Tool!")
    keyword = input("Enter a keyword to search for in post titles: ")
    results = search_posts_by_title(keyword)
    if results:
        print(f"\nFound {len(results)} result(s):\n")
        for row in results:
            print(f"Title: {row[0]}, Author: {row[1]}, Date: {row[2]}, Tags: {row[3]}")
    else:
        print("\nNo results found.")
