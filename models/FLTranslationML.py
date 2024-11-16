#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# === Note ===
# This model is trained specifically on the Aylid language. The model may not
# perform well for other languages without retraining on appropriate datasets.
# Use this model as an example or starting point for training similar models
# for other languages.

#####################################
# IMPORTS
#####################################
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional, Dropout, TimeDistributed
from tensorflow.keras.regularizers import l2
import tensorflow as tf
import pickle

#####################################
# DATA LOADING AND PREPROCESSING
#####################################
# Load Excel file containing English-FL word pairs
df = pd.read_excel('your_file.xlsx')
english_texts = df['English'].fillna('').tolist()
fl_texts = df['FL'].fillna('').tolist()

# Create tokenizers for converting words to numbers
eng_tokenizer = Tokenizer(char_level=False, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
fl_tokenizer = Tokenizer(char_level=False, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')

eng_tokenizer.fit_on_texts(english_texts)
fl_tokenizer.fit_on_texts(fl_texts)

# Convert words to sequences and pad them
X = eng_tokenizer.texts_to_sequences(english_texts)
y = fl_tokenizer.texts_to_sequences(fl_texts)

max_length = 5  # Maximum word length to consider
X_pad = pad_sequences(X, maxlen=max_length, padding='post')
y_pad = pad_sequences(y, maxlen=max_length, padding='post')

# Prepare final training data
vocab_size_fl = len(fl_tokenizer.word_index) + 1
vocab_size_eng = len(eng_tokenizer.word_index) + 1
y_one_hot = tf.keras.utils.to_categorical(y_pad, num_classes=vocab_size_fl)

#####################################
# MODEL ARCHITECTURE
#####################################
# Neural network with regularization to prevent overfitting
model = Sequential([
    Embedding(vocab_size_eng, 256, embeddings_regularizer=l2(0.01)),
    Bidirectional(LSTM(256, return_sequences=True, kernel_regularizer=l2(0.01))),
    Dropout(0.3),
    TimeDistributed(Dense(512, activation='relu', kernel_regularizer=l2(0.01))),
    Dropout(0.3),
    TimeDistributed(Dense(vocab_size_fl, activation='softmax'))
])

# Optimizer settings
optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.001,
    clipnorm=1.0
)

model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#####################################
# TRANSLATION FUNCTION
#####################################
def translate_text(text, eng_tokenizer, fl_tokenizer, model, max_length):
    # First check if word exists in training data
    eng_word = text.lower()
    if eng_word in df['English'].str.lower().values:
        actual_translation = df[df['English'].str.lower() == eng_word]['FL'].iloc[0]
        return actual_translation, 1.0
    
    # If not in training data, use model prediction
    sequence = eng_tokenizer.texts_to_sequences([eng_word])
    padded = pad_sequences(sequence, maxlen=max_length, padding='post')
    
    pred = model.predict(padded, verbose=0)
    pred_flat = pred[0].flatten()
    
    # Get top 3 predictions with their confidences
    top_k_indices = np.argsort(pred_flat)[-3:][::-1]
    top_k_confidences = pred_flat[top_k_indices]
    
    reverse_word_map = dict(map(reversed, fl_tokenizer.word_index.items()))
    
    # Check confidence difference between top predictions
    if len(top_k_confidences) >= 2:
        confidence_diff = top_k_confidences[0] - top_k_confidences[1]
        
        # If top prediction is significantly more confident
        if confidence_diff > 0.2:
            word_idx = top_k_indices[0] % vocab_size_fl
            result = reverse_word_map.get(word_idx, '')
            return result, top_k_confidences[0]
    
    # If no clear winner, use top prediction but with lower confidence
    word_idx = top_k_indices[0] % vocab_size_fl
    result = reverse_word_map.get(word_idx, '')
    return result, top_k_confidences[0] * 0.8  # Reduce confidence when uncertain

#####################################
# TRAINING CALLBACK
#####################################
class DetailedCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 10 == 0:
            print(f'\nEpoch {epoch + 1}/100')
            print(f'Training - accuracy: {logs["accuracy"]:.4f} - loss: {logs["loss"]:.4f}')
            print(f'Validation - accuracy: {logs["val_accuracy"]:.4f} - loss: {logs["val_loss"]:.4f}')
            
            test_words = ["system", "in", "computer", "and"]
            for word in test_words:
                sequence = eng_tokenizer.texts_to_sequences([word.lower()])
                padded = pad_sequences(sequence, maxlen=max_length, padding='post')
                pred = model.predict(padded, verbose=0)[0]
                pred_flat = pred.flatten()
                
                print(f"\nTest '{word}':")
                actual = df[df['English'] == word]['FL'].values[0] if word in df['English'].values else "unknown"
                print(f"Should be: '{actual}'")
                
                # Show top 3 predictions with confidences
                top_k_indices = np.argsort(pred_flat)[-3:][::-1]
                reverse_word_map = dict(map(reversed, fl_tokenizer.word_index.items()))
                print("Top 3 predictions:")
                for idx in top_k_indices:
                    word_idx = idx % vocab_size_fl
                    pred_word = reverse_word_map.get(word_idx, '')
                    conf = pred_flat[idx]
                    print(f"  {pred_word}: {conf:.4f}")

#####################################
# MODEL TRAINING
#####################################
history = model.fit(
    X_pad,
    y_one_hot,
    batch_size=32,
    epochs=100,
    validation_split=0.2,
    verbose=0,
    callbacks=[
        DetailedCallback(),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
    ]
)

#####################################
# FINAL TESTING
#####################################
test_words = ["light", "intelligence", "and", "in", "computer", "system"]
print("\nFinal Testing translations:")
print("-------------------------")
for word in test_words:
    predicted, confidence = translate_text(word, eng_tokenizer, fl_tokenizer, model, max_length)
    actual = df[df['English'] == word]['FL'].values[0] if word in df['English'].values else "unknown"
    print(f"\nEnglish: {word}")
    print(f"Predicted FL: {predicted}")
    print(f"Actual FL: {actual}")
    print(f"Confidence: {confidence:.4f}")
    if actual != "unknown":
        print(f"Match: {predicted == actual}")

#####################################
# STATISTICS AND EXAMPLES
#####################################
print(f"\nVocabulary sizes:")
print(f"English: {len(eng_tokenizer.word_index)} words")
print(f"FL: {len(fl_tokenizer.word_index)} words")

print("\nExample word pairs:")
for i in range(5):
    print(f"English: {english_texts[i]} -> FL: {fl_texts[i]}")

#####################################
# SAVE MODEL AND TOKENIZERS
#####################################
# Save the trained model
model.save('fl_translator_model.h5')

# Save the tokenizers
with open('eng_tokenizer.pickle', 'wb') as handle:
    pickle.dump(eng_tokenizer, handle)
    
with open('fl_tokenizer.pickle', 'wb') as handle:
    pickle.dump(fl_tokenizer, handle)

