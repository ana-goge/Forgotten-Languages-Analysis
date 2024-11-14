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

        # Check for conflicts
        for _, row in new_df.iterrows():
            english_word = row['English']
            fl_word = row['FL']

            # Find any existing translations for the English word
            existing_translations = existing_df[existing_df['English'] == english_word]

            # If there are existing translations, check if they conflict
            if not existing_translations.empty:
                for _, existing_row in existing_translations.iterrows():
                    existing_fl_word = existing_row['FL']
                    if existing_fl_word != fl_word:
                        # Conflict found
                        print(f"Conflict detected: '{english_word}' is already translated as '{existing_fl_word}', but the new translation is '{fl_word}'.")
                        user_input = input("Do you want to proceed with the new translation? (yes/no): ")
                        if user_input.lower() != 'yes':
                            # Skip this conflicting pair
                            new_df = new_df[new_df['English'] != english_word]
                            break

        # Concatenate the existing DataFrame with the new one
        combined_df = pd.concat([existing_df, new_df])

    else:
        combined_df = new_df

    # Remove duplicate pairs and reset index
    combined_df = combined_df.drop_duplicates().reset_index(drop=True)

    # Save the updated DataFrame to an Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Spreadsheet updated and saved to {output_file}")

# Example usage
english_text = "The computer model called World3, developed for the LTG study, simulated numerous interactions within and among the key subsystems of the global economy: population, industrial capital, pollution, agricultural systems, and non renewable resources. For its time, World3 was necessarily coarse, for example modelling the total global population rather than separate regions or nations."
fl_text = "Fad ikaik tød neritt NodeSpacesGC, ingamitt ti fad FL soddry, eråekitt inin enafa geru beni ader fad etat påes nayn fad desomed neding: edieåijk, foreru gere, deligekijk, yriona eli, beni gen eder liadenen. Ti enuli esom, NodeSpacesGC ter enera meb, ti isen eraelonende fad rosen desomed edieåijk inedie ak ogeri tare tingik anot."
output_file = 'AYLID.xlsx'

create_translation_spreadsheet(english_text, fl_text, output_file)


# In[18]:


english_text = "The output power of modern day lasers ranges from milliwatts to megawatts (in cases where they deliver continuous output power), or even petawatts (10^15 W) for short pulse lasers. In military terms, lasers with continuous output powers greater than 20 kW are classified as High Energy Lasers (HEL). Output powers in the range of kilowatts or even megawatts allow the creation of laser beams with potential harmful intensity over distances of up to several hundred kilometres. These beams can be used to heat up targets, which then may lead to structural failure of the target object."
fl_text = "Fad yrisyr gwang nayn tiov ered ashe uvayn eno milliwatt kij edrylaeth neste selig rano keru angeskar fad yrisyr gwang, tingik addyrorod petawatt (10^15 W) ti ocha rupi ashe. Neste rof sike, ashe en fad yrisyr kese allerie ak 20 kW eshe dalitt teø ernåaddyr andorem ashe (HEL). Yrisyr kese neste fad nemat nayn gati tingik addyrorod edrylaeth dore fad ledseskeijk nayn aynona ase en asteø etere doleen rianyd efi nayn derels kij rylia eraeloitt few. Ense ase ømedø oraelaeth emoritt kij tedsele derels tæd, menudi aynilayn ifo ediga kij kine cynen nayn fad ereri se."
output_file = 'AYLID.xlsx'

update_translation_spreadsheet(english_text, fl_text, output_file)


# In[19]:


english_text = "However, in 1995, these weapons were officially banned under International Humanitarian Law. If the aim is to destroy hard targets rather than to blind the enemy, however, the laser requires an output power many orders of magnitude higher than that of blinding lasers." 
fl_text = "Efa, neste 1995, ense nafe iberhy nyl tioniluititt ek vel lellegw amade. Mehe fad ilogit neste kij ordesaeth prist tæd inedie ak kij medafo fad kotor, efa, fad aynona riga yron yrisyr gwang asie drylø nayn aethepå shitef ak sidinark nayn gededenende ashe."
output_file = 'AYLID.xlsx'

update_translation_spreadsheet(english_text, fl_text, output_file)


# In[20]:


english_text = "Another project currently under research and development is the Airborne Laser (ABL) program. Also aiming for ballistic missile defense, the intention of the project is to use a Boeing 747 airplane as a flying platform for a multimegawatt HEL. The estimated range of an ABL is between 200 and 600 kilometres. The ABL would circle around hostile missile bases and destroy launched missiles in their boost phase. The ABL will employ a chemical oxygen iodine laser (COIL) (wavelength three = 1.315 μm). The Tactical High Energy Laser (THEL) is intended for point defence. Its primary task would be defending a limited area against mortars and artillery rockets. The program has already resulted in the development of a field tested prototype. This prototype managed to destroy mortars and rockets in a test environment. The THEL is a ground based chemical laser (deuterium fluoride DF, wavelength three = 3.8 μm). The system consists of several portable, container sized units."
fl_text = "Kaeshaf iometh ingie ek vedem beni rineryn neste fad grone aynona (ABL) aynanu. Gweser imaende ti loga edser deyfse, fad gwesijk nayn fad iometh neste kij baarin eda Boeing 747 topod teø eda delsestende diene ti eda multimegawatt HEL. Fad otiitt nemat nayn yron ABL neste fania 200 beni 600 few. Fad ABL disk ringe eli aeshes edser derer beni ordesaeth ærwyritt reh neste ararth igating senud. Fad ABL alere eme eda keleri hera inet aynona (eneddrypå) (eømi λ = 1.315 µm). fad reg ernåaddyr andorem aynona (THEL) neste deneitt ti dyriter selor. Enuli hyre faaddry disk oraelaeth rerende eda ingeddyneritt derove iker arilen beni elle igered. Fad aynanu sheke desieh adeditt neste fad rineryn nayn eda kerels badseitt etin. Inne etin rumeitt kij ordesaeth arilen beni igered neste eda liagat nel. Fad THEL neste eda gwede elihallitt keleri aynona (bleser deser DF, eømi λ = 3.8 µm). Fad tese odyri nayn rylia rarie, temet diecedreitt thor."
output_file = 'AYLID.xlsx'

update_translation_spreadsheet(english_text, fl_text, output_file)


# In[ ]:




