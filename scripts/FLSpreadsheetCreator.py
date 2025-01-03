#!/usr/bin/env python
# coding: utf-8

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

    # Create a DataFrame with word pairs
    new_data = {
        'English': english_words,
        'FL': fl_words
    }
    new_df = pd.DataFrame(new_data)

    # If the output file exists, load it
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        # Concatenate the existing DataFrame with the new one
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    # Remove exact duplicates first
    combined_df = combined_df.drop_duplicates()

    # Create dictionaries to store all translations
    eng_to_fl_dict = {}
    fl_to_eng_dict = {}

    # Build the translation dictionaries
    for _, row in combined_df.iterrows():
        eng = row['English']
        fl = row['FL']
        
        if eng not in eng_to_fl_dict:
            eng_to_fl_dict[eng] = set()
        eng_to_fl_dict[eng].add(fl)
        
        if fl not in fl_to_eng_dict:
            fl_to_eng_dict[fl] = set()
        fl_to_eng_dict[fl].add(eng)

    # Create the final DataFrame with alternates
    final_data = []
    for eng, fl_set in eng_to_fl_dict.items():
        fl_list = sorted(list(fl_set))
        primary_fl = fl_list[0]
        alt_fl = ', '.join(fl_list[1:]) if len(fl_list) > 1 else ''
        
        # Get English alternatives for the primary FL
        eng_alts = sorted(list(fl_to_eng_dict[primary_fl] - {eng}))
        eng_alt_str = ', '.join(eng_alts) if eng_alts else ''
        
        final_data.append({
            'English': eng,
            'FL': primary_fl,
            'FL_Alt': alt_fl,
            'English_Alt': eng_alt_str
        })

    # Create final DataFrame and sort by English
    result_df = pd.DataFrame(final_data).sort_values('English').reset_index(drop=True)

    # Save the file
    result_df.to_excel(output_file, index=False)
    
    # Print conflicts if they exist
    conflicts = result_df[(result_df['FL_Alt'] != '') | (result_df['English_Alt'] != '')]
    if not conflicts.empty:
        print("\nWords with multiple translations found:")
        print(conflicts[['English', 'FL', 'FL_Alt', 'English_Alt']])
    
    print(f"\nSpreadsheet updated and saved to {output_file}")

def view_translation_file(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        print("\nCurrent contents of the translation file:")
        print(df.to_string())
        print(f"\nTotal entries: {len(df)}")
    else:
        print(f"File not found: {file_path}")

# Example usage
english_text = "The computer model called World3, developed for the LTG study, simulated numerous interactions within and among the key subsystems of the global economy: population, industrial capital, pollution, agricultural systems, and non renewable resources. For its time, World3 was necessarily coarse, for example modelling the total global population rather than separate regions or nations."
fl_text = "Fad ikaik tød neritt NodeSpacesGC, ingamitt ti fad FL soddry, eråekitt inin enafa geru beni ader fad etat påes nayn fad desomed neding: edieåijk, foreru gere, deligekijk, yriona eli, beni gen eder liadenen. Ti enuli esom, NodeSpacesGC ter enera meb, ti isen eraelonende fad rosen desomed edieåijk inedie ak ogeri tare tingik anot."
output_file = 'AYLID.xlsx'

update_translation_spreadsheet(english_text, fl_text, output_file)

# In[ ]:




