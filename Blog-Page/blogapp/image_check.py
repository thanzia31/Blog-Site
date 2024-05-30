
import os
from django.conf import settings
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import warnings
warnings.filterwarnings('ignore' )
from bs4 import BeautifulSoup
from io import BytesIO
import requests
from PIL import ImageFile,Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

img_size = (224, 224)
batch_size = 32

def create_model():
    dataset_dir = "D:/imagemod"

    train_datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    validation_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    

    train_generator = train_datagen.flow_from_directory(
        os.path.join(dataset_dir, 'train'),
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary'
    )

    validation_generator = validation_datagen.flow_from_directory(
        os.path.join(dataset_dir, 'val1'),
        target_size=img_size,
        batch_size=batch_size,
        class_mode='binary'
    )
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False

    model = Sequential([
         base_model,
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=10,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size
    )

    model.save("C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/image_moderation_model.h5")

    evaluation_result = model.evaluate(validation_generator)
    print("Validation Accuracy:", evaluation_result[1])
    return model

def input_model_image(content):

    
    train_model = False

    if train_model:
        model = create_model()
    else:
        model_path = "C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/image_moderation_model.h5"
        model = load_model(model_path)
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('img')

    predictions = []

    for img_tag in img_tags:
        img_url = img_tag['src']

        
        if img_url.startswith('/media/'):
            img_path = os.path.join(settings.MEDIA_ROOT, img_url[7:])  
            img = Image.open(img_path)
            img = img.convert('RGB')

            img = img.resize((224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            prediction = model.predict(img_array)
            predictions.append((img_url, prediction[0][0]))
        else:
            print(f"Skipping non-local image: {img_url}")

    return predictions


#input_model("C:/Users/i310thgeN/Downloads/download.jpeg")
#print(input_model_image("C:\Users\i310thgeN\Documents\webpage\djangoproject\blog\media\images\photo1_3_cQDWWEv.jpg"))
a=input_model_image('<p>Hi there how are you</p><p><img src="C:/Users/i310thgeN/Documents/webpage/djangoproject/blog/static/images/fashion.jpg"/></p>')
print(a)
for path,predict in a:
    if predict>0.5:
        print('Image not approved ')
    else:
        print('image approved')
        