#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import re
import os

def update_translation_spreadsheet(english_text, fl_text, output_file):
    # Remove punctuation and make everything lowercase
    english_text = re.sub(r'[^\w\s]', '', english_text).lower()
    fl_text = re.sub(r'[^\w\s]', '', fl_text).lower()

    # Split the text into individual words
    english_words = english_text.split()
    fl_words = fl_text.split()

    # Ensure both texts have the same number of words
    if len(english_words) != len(fl_words):
        raise ValueError("The English and FL texts do not have the same number of words.")

    # Create a DataFrame with new word pairs
    new_data = {'English': english_words, 'FL': fl_words}
    new_df = pd.DataFrame(new_data)

    # If the output file exists, load it
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)

        # Concatenate the existing DataFrame with the new one
        combined_df = pd.concat([existing_df, new_df])

    else:
        combined_df = new_df

    # Remove duplicate pairs and reset index
    combined_df = combined_df.drop_duplicates().reset_index(drop=True)

    # Check for "overbooked" words (English words with multiple FL translations)
    overbooked = combined_df.groupby('English')['FL'].nunique()
    overbooked = overbooked[overbooked > 1]

    if not overbooked.empty:
        print("Overbooking detected for the following words (having multiple translations):")
        for english_word in overbooked.index:
            translations = combined_df[combined_df['English'] == english_word]['FL'].unique()
            print(f"'{english_word}': {translations}")

    # Save the updated DataFrame to an Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Spreadsheet updated and saved to {output_file}")

# Example usage
english_text = "The computer model called World3, developed for the LTG study, simulated numerous interactions within and among the key subsystems of the global economy: population, industrial capital, pollution, agricultural systems, and non renewable resources. For its time, World3 was necessarily coarse, for example modelling the total global population rather than separate regions or nations."
fl_text = "Fad ikaik tød neritt NodeSpacesGC, ingamitt ti fad FL soddry, eråekitt inin enafa geru beni ader fad etat påes nayn fad desomed neding: edieåijk, foreru gere, deligekijk, yriona eli, beni gen eder liadenen. Ti enuli esom, NodeSpacesGC ter enera meb, ti isen eraelonende fad rosen desomed edieåijk inedie ak ogeri tare tingik anot."
output_file = 'AYLID.xlsx'

update_translation_spreadsheet(english_text, fl_text, output_file)


# In[ ]:




