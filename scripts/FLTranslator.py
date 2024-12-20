#!/usr/bin/env python
# coding: utf-8

# In[2]:
import pandas as pd
import re
import os

def load_translation_dictionary(excel_file):
    """Load the Excel file and create bidirectional translation dictionaries"""
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Translation dictionary file not found: {excel_file}")
        
    df = pd.read_excel(excel_file)
    
    # Initialize dictionaries
    eng_to_fl = {}
    fl_to_eng = {}
    
    for _, row in df.iterrows():
        eng = row['English'].lower()
        fl = row['FL'].lower()
        
        # Add primary translations
        eng_to_fl[eng] = fl
        fl_to_eng[fl] = eng
        
        # Add alternative FL translations if they exist
        if pd.notna(row['FL_Alt']):
            for alt_fl in row['FL_Alt'].split(', '):
                fl_to_eng[alt_fl.lower()] = eng
        
        # Add alternative English translations if they exist
        if pd.notna(row['English_Alt']):
            for alt_eng in row['English_Alt'].split(', '):
                eng_to_fl[alt_eng.lower()] = fl
    
    return eng_to_fl, fl_to_eng

def translate_text(text, dictionary_file, direction='eng_to_fl', mark_unknown=True):
    """
    Translate text between English and FL
    
    Parameters:
    - text: Input text to translate
    - dictionary_file: Path to Excel file containing translations (required)
    - direction: 'eng_to_fl' or 'fl_to_eng'
    - mark_unknown: If True, marks unknown words with brackets; if False, leaves them unchanged
    """
    # Validate direction
    if direction not in ['eng_to_fl', 'fl_to_eng']:
        raise ValueError("Direction must be either 'eng_to_fl' or 'fl_to_eng'")
    
    # Load dictionaries
    eng_to_fl, fl_to_eng = load_translation_dictionary(dictionary_file)
    
    # Choose dictionary based on direction
    dictionary = eng_to_fl if direction == 'eng_to_fl' else fl_to_eng
    
    # Split text into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Prepare results
    translation = []
    unknown_words = []
    stats = {'known': 0, 'unknown': 0}
    
    # Process each word
    for word in words:
        if word in dictionary:
            translation.append(dictionary[word])
            stats['known'] += 1
        else:
            translation.append(f"[{word}?]" if mark_unknown else word)
            unknown_words.append(word)
            stats['unknown'] += 1
    
    # Prepare output
    result = {
        'original': text,
        'translated': ' '.join(translation),
        'unknown_words': unknown_words,
        'stats': stats,
        'coverage': (stats['known'] / len(words)) * 100 if words else 0
    }
    
    return result

def print_translation_result(result):
    """Pretty print the translation results"""
    print("\n=== Translation Results ===")
    print("\nOriginal text:")
    print(result['original'])
    print("\nTranslated text:")
    print(result['translated'])
    print("\nStatistics:")
    print(f"Words translated: {result['stats']['known']}")
    print(f"Unknown words: {result['stats']['unknown']}")
    print(f"Translation coverage: {result['coverage']:.1f}%")
    if result['unknown_words']:
        print("\nUnknown words:")
        print(", ".join(result['unknown_words']))

if __name__ == "__main__":
    # Get dictionary file path from user
    dictionary_file = input("Enter the path to your translation dictionary Excel file: ")
    
    # Example translations
    english_text = input("\nEnter text to translate: ")
    direction = input("Enter translation direction (eng_to_fl/fl_to_eng): ").lower()
    mark_unknown = input("Mark unknown words? (yes/no): ").lower() == 'yes'
    
    try:
        result = translate_text(english_text, 
                              dictionary_file=dictionary_file,
                              direction=direction,
                              mark_unknown=mark_unknown)
        print_translation_result(result)
    except Exception as e:
        print(f"\nError: {str(e)}")

# Example usage
dictionary_file = "path/to/your/dictionary.xlsx"
text = "The laser requires power"
result = translate_text(text, 
                       dictionary_file=dictionary_file,
                       direction='eng_to_fl',
                       mark_unknown=True)
print_translation_result(result)

# In[ ]:




