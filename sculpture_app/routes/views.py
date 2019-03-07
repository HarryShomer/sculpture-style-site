from flask import (Blueprint, render_template, request, jsonify)
from ..models import sculpture_model

# Define the route structure for this page
bp = Blueprint('views', __name__, url_prefix='/')


# Standard home page
@bp.route('/', methods=["GET"])
def home():
    return render_template('home.html', title='home')

# About me & work
@bp.route('/about', methods=["GET"])
def about():
    return render_template('about.html', title='about')


# Methodology of cnn
@bp.route('/methods', methods=["GET"])
def methods():
    return render_template('methodology.html', title='methodology')


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

    preds = sculpture_model.predict_image(img)
    plot_img = sculpture_model.create_plot(preds)

    # Style with max probability
    #max_style = max(preds, key=preds.get)

    return jsonify(plot_img=plot_img.decode('utf-8'))

