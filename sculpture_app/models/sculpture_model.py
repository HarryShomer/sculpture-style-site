"""
Code to predict a single image
"""
from keras import models
from keras import layers
from keras.applications import Xception
from keras import regularizers
from keras.preprocessing import image
import numpy as np
import os


def load_image(file_stream):
    """
    Load the file to predict
    """
    img = image.load_img(file_stream, target_size=(299, 299))
    np_image = image.img_to_array(img)
    np_image = np.array(np_image).astype('float32')/255

    # Make to a rank 4 tesnor (1, 299, 299, 3) -> 1 is for the batch size
    np_image = np.expand_dims(np_image, axis=0)

    return np_image


def create_model():
    """
    Create our fine-tuned model & load the weights
    """
    base_model = Xception(include_top=False, weights=None)

    # Add Custom FC
    x = base_model.output
    x = layers.Dense(128,
                     activation='relu',
                     kernel_regularizer=regularizers.l2(0.0075))(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.5)(x)
    predictions = layers.Dense(12, activation='softmax')(x)

    # Turn into model & load the weights
    cnn = models.Model(inputs=base_model.input, outputs=predictions)
    cnn.load_weights(os.path.join(os.path.dirname(os.path.realpath(__file__)), "xception_finetune_12_reg_75_block4.h5"))
    print("-> The CNN has been fully loaded")

    return cnn


def predict_image(model, graph, img):
    """
    Predict & print the class probabilities for some image
    
    :param model: CNN
    :param graph: tf graph
    :param img: image array
    
    :return probabilities for each style
    """
    pred_classes = {}
    classes = ["BAROQUE", "EARLY RENAISSANCE", "HIGH RENAISSANCE", "IMPRESSIONISM", "MANNERISM",
               "MEDIEVAL", "MINIMALISM", "NEOCLASSICISM",  "REALISM", "ROCOCO",
               "ROMANTICISM", "SURREALISM"
               ]

    # Needed as flask run multiple threads
    with graph.as_default():
        preds = model.predict(img)

    for index in range(0, 12):
        pred_classes[classes[index]] = round(preds[0][index]*100, 2)

    return pred_classes

