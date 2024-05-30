
#0-offensive 1-Hate 2-Neither

import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def create_and_train_model(X, y):
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    sequences = tokenizer.texts_to_sequences(X)
    X_padded = pad_sequences(sequences)

    
    X_train, X_test, y_train, y_test = train_test_split(X_padded, y_encoded, test_size=0.2, random_state=42)

    
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=100, input_length=X_padded.shape[1]))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(LSTM(units=50))
    model.add(Dense(units=64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=len(np.unique(y_encoded)), activation='softmax'))  

    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

    
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy}")

    model.save('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/content_moderation_model.h5')
    print("Model saved.")

    
    with open('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/tokenizer.pkl', 'wb') as file:
        pickle.dump(tokenizer, file)

    with open('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/ label_encoder.pkl', 'wb') as file:
        pickle.dump(label_encoder, file)

    print("Tokenizer and LabelEncoder saved.")

    print(accuracy)

    return model, tokenizer, label_encoder

def predict_with_model(model, tokenizer, label_encoder, input_text):
    input_sequence = tokenizer.texts_to_sequences([input_text])
    padded_sequence = pad_sequences(input_sequence, maxlen=model.input_shape[1])

   
    predicted_probabilities = model.predict(padded_sequence)
    predicted_class = np.argmax(predicted_probabilities)
    predicted_label = label_encoder.inverse_transform([predicted_class])[0]
    confidence = predicted_probabilities[0][predicted_class]

    if confidence <= 0.6:
        predicted_label=2
    


    
    print("\nInput Text:")
    print(f"- {input_text}")

    print("\nPredicted Probabilities:")
    print(predicted_probabilities)

    print("\nPredicted Class:")
    print(predicted_label)
    return predicted_label

def load_saved_model():
    
    loaded_model = load_model('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/content_moderation_model.h5')

    
    with open('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/tokenizer.pkl', 'rb') as file:
        loaded_tokenizer = pickle.load(file)

    with open('C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/label_encoder.pkl', 'rb') as file:
        loaded_label_encoder = pickle.load(file)

    print("Model, Tokenizer, and LabelEncoder loaded.")
    return loaded_model, loaded_tokenizer, loaded_label_encoder


data=pd.read_csv('D:/labeled_data.csv')
#print(data)
#X = ['hi', 'idiot', 'u are black']
#y = [2, 0, 1]
X=data['tweet']
y=data['class']
#print('X',X)
#print(y)
def input_model(content):
    #print(content)
    prediction=[]
    train_model=False
    if train_model:
        trained_model, tokenizer, label_encoder = create_and_train_model(X, y)
    else:
        trained_model, tokenizer, label_encoder = load_saved_model()

    result_string = content.replace('"', '').replace("'", '')

    soup = BeautifulSoup(content, 'html.parser')
    p_tag = soup.find_all('p')
    #print("p_tag",p_tag)
    for i in p_tag:
        print(i)
        cleaned_text = i.get_text(separator=' ', strip=True) if i else ''
        #print(cleaned_text)
        a=predict_with_model(trained_model, tokenizer, label_encoder, cleaned_text)
        prediction.append(a)
        print("Predictions",prediction)
    
    return prediction
 
print(input_model('<p><img alt="" src="/media/uploads/2023/12/04/test2-94.jpg" style="height:200px; width:150px" /></p><p>You are nothing but a waste of space in this bloody world...women belong in the kitchen you slut idiot i hate u so much you black people dont belong here women are a peice of shit who belong in th bloody kitchen hell dammit shit bloody losers</p>'))









