from flask import (Blueprint, render_template, request, send_file, Response, redirect, jsonify)
from ..models import sculpture_model
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

# Define the route structure for this page
bp = Blueprint('routes/home', __name__, url_prefix='/')

cnn = None
graph = None


def load_model():
    """
    Load the model and graph when we start the app
    
    :return: None
    """
    global cnn, graph
    cnn = sculpture_model.create_model()
    graph = tf.get_default_graph()


# A simple page that says hello
@bp.route('/', methods=["GET"])
def home():
    return render_template('home.html', title='home')


# Page for uploading images
@bp.route('/upload', methods=["POST"])
def upload_image():
    if 'sculpt_file' not in request.files:
        print("No File")
        return '', 204

    # Make sure its a valid image
    try:
        img = sculpture_model.load_image(request.files['sculpt_file'].stream)
    except IOError:
        print("IO Error")
        return '', 204

    preds = sculpture_model.predict_image(cnn, graph, img)
    plot_img = create_plot(preds)

    return jsonify(plot_img=plot_img)


def create_plot(preds):
    """
    Create a viz of the predictions

    :param preds: Predictions for each class

    :return: _____
    """
    y_pos = np.arange(len(preds.keys()))
    probs = [preds[style] for style in preds]

    fig, ax = plt.subplots()
    ax.barh(y_pos, probs, align='center', color="#ff6f69")

    #for i, v in enumerate(probs):
    #    ax.text(v + 3, i + .25, str(v), color="#ff6f69", fontweight='bold')

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


