# Forgotten Languages Article Database

## Overview
This project contains a searchable SQLite database of articles scraped from the Forgotten Languages blog. The database is designed for exploration and research purposes, with support for keyword-based searches
by title, author, tags, and date range.

## Contents
- **`newdb.db`**: The compressed SQLite database containing the scraped articles. 
- **`search_tool.py`**: A Python script to query the database for posts by title, author, tags, or date range.
- **`requirements.txt`**: A file listing the Python dependencies required for the search tool.

## Usage Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/forgotten_languages.git
   cd forgotten_languages/Article Database
2. **Decompress the Database**
  `gzip -d newdb.db.gz`
3. **Install Dependencies**
   `pip install -r requirements.txt`
4. **Run the Search Tool**
   `python search_tool.py`
5. **Search Examples** 
     - Search by title: Enter a keyword like `"terraforming"`
     - Search by author: Find articles by specific authors like `"Direne"`
     - Search by tags: Explore articles tagged with `"Defense"`
     - Search by date range: Query articles published between specific dates (e.g., `2024-12-01` to `2025-01-01`).

**Note:** This repository does not include the scraper to avoid overwhelming the original blog hosts. It only includes the scraped database and tools for analysis.
