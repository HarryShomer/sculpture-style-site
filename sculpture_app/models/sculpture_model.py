"""
Code to predict a single image
"""
from keras import models
from keras import layers
from keras.applications import Xception
from keras import regularizers
from keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os
from PIL import Image
from io import BytesIO
import base64

# Stop from crashing -> Must be b4 pyplot
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Looks the nicest
plt.style.use('ggplot')

# Global cnn and graph - only load once
cnn = None
graph = None


def load_model():
    """
    Load the model and graph when we start the app
    
    :return: None
    """
    global cnn, graph
    cnn = create_model()
    graph = tf.get_default_graph()


def create_plot(preds):
    """
    Create a viz of the predictions

    :param preds: Predictions for each class

    :return: base64 of plot
    """
    y_pos = np.arange(len(preds.keys()))
    probs = [preds[style] for style in preds]

    fig, ax = plt.subplots()
    ax.barh(y_pos, probs, align='center', color="#ff6f69")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(preds.keys()))
    ax.invert_yaxis()  # labels read top-to-bottom

    ax.set_xlabel('% of Being Style')
    # ax.set_ylabel("Art Style")
    ax.set_title('Probabilities of Belonging to each Style')

    plt.tight_layout(h_pad=4, w_pad=2)

    buf = BytesIO()
    plt.savefig(buf, format='png')    
    plt.close()            
    myimage = buf.getvalue() 
    buf.close()

    return base64.b64encode(myimage)


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
    sculpt_cnn = models.Model(inputs=base_model.input, outputs=predictions)
    sculpt_cnn.load_weights(os.path.join(os.path.dirname(os.path.realpath(__file__)), "xception_finetune_12_reg_75_block4.h5"))
    print("-> The CNN has been fully loaded")

    return sculpt_cnn


def predict_image(img):
    """
    Predict & print the class probabilities for some image
    
    :param img: image array
    
    :return probabilities for each style
    """
    global graph, cnn

    pred_classes = {}
    classes = ["BAROQUE", "EARLY RENAISSANCE", "HIGH RENAISSANCE", "IMPRESSIONISM", "MANNERISM",
               "MEDIEVAL", "MINIMALISM", "NEOCLASSICISM",  "REALISM", "ROCOCO",
               "ROMANTICISM", "SURREALISM"
               ]

    # Needed as flask run multiple threads
    with graph.as_default():
        preds = cnn.predict(img)

    for index in range(0, 12):
        pred_classes[classes[index]] = round(preds[0][index]*100, 2)

    return pred_classes

