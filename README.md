**FL Translation & Analysis Toolkit**

**Overview**

This repository is dedicated to exploring and analysing the Forgotten Languages (FL) languages and content. It provides tools for translating FL languages, analysing linguistic patterns, and training machine learning models to improve translation quality. The toolkit now includes a database of FL content that can be searched and analysed using Streamlit and Python.
  
**Contents**

- **NEW** StreamlitApp: A Streamlit app for searching and viewing articles from the FL database. This app provides a user-friendly interface to query the database by keyword and date range, with the ability to search through different fields like Title, Author, Tags, and Full Text. (https://forgotten-languages-search.streamlit.app/)
- `FLSpreadsheetCreator.py`: Script for creating and updating translation spreadsheets.
- `FLTranslator.py`: Script for translating new text using the spreadsheet as a language dictionary.
- `FLTranslationML.py`: Machine learning script for training an AI model to translate an FL language to English.
  > currently training on Aylid
- `progress.md`: File containing recent model outputs, development notes, and a progress summary.
- `search_tool.py`: Python script for querying the FL database with various search criteria (e.g., title, author, tags, full text).

**FL Database** 

The FL database contains articles, metadata (author, tags, publication date), and full texts of FL content. The database is continuously updated and serves as the core resource for training machine learning models and performing in-depth analysis of FL languages. **Database Fields:**
- title: Title of the article
- author: Author of the article
- date_posted: Date the article was posted
- tags: Tags associated with the article
- english_text: isolated english portions of the article
- full_text: The full text of the article
  
**Future Plans**

- **Training an LLM on the FL Database:** A significant upcoming feature is the training of a Large Language Model (LLM) on the FL database for analysis. This model will be used to extract insights, analyse patterns, and possibly generate new translations.
- **Improving Translation Quality:** We will continue transitioning from word-level pairs to sentence-level data and incorporating seq2seq models with attention mechanisms to improve translation accuracy and contextual understanding.
- **Pattern Analysis Tools:** Adding more tools to facilitate pattern analysis and machine learning exploration of FL content, including word frequency analysis, sentence structures, and grammatical patterns.
- **Collaborative Features:** Developing features to expand and share translation progress, including collaborative workflows and data sharing.
- **Interactive Tutorials:** Creating notebooks and guides to provide interactive tutorials and demonstrations of the translation models and database search features.

