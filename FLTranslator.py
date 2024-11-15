#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This script will: 
# Load your existing Excel spreadsheet as a dictionary.
# Read an input text file (in either English or FL).
# Replace words based on the existing dictionary.
# Output the translated text.

import pandas as pd
import re

def translate_text(input_text, dictionary_file, direction='english_to_fl'):
    # Load the translation dictionary
    df = pd.read_excel(dictionary_file)

    # Create a dictionary from the DataFrame
    if direction == 'english_to_fl':
        translation_dict = pd.Series(df['FL'].values, index=df['English']).to_dict()
    elif direction == 'fl_to_english':
        translation_dict = pd.Series(df['English'].values, index=df['FL']).to_dict()
    else:
        raise ValueError("Invalid direction. Use 'english_to_fl' or 'fl_to_english'.")

    # Remove punctuation and make everything lowercase
    input_text = re.sub(r'[^\w\s]', '', input_text).lower()

    # Split the text into words
    words = input_text.split()

    # Translate words
    translated_words = [translation_dict.get(word, word) for word in words]

    # Join translated words back into a string
    translated_text = ' '.join(translated_words)

    return translated_text

# Example usage
dictionary_file = 'AYLID.xlsx'
english_text = "The computer model simulated numerous interactions within the global economy."
translated_text = translate_text(english_text, dictionary_file, direction='english_to_fl')
print("Translated text:", translated_text)


# In[ ]:



