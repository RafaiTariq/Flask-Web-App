import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


from PIL import Image, ImageOps



# Declare a flask app
app = Flask(__name__)


# You can use pretrained model from Keras
# Check https://keras.io/applications/
from keras.applications.mobilenet_v2 import MobileNetV2
model = MobileNetV2(weights='imagenet')

print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'models/your_model.h5'

# Load your own trained model
# model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')


def model_predict(img, model):
    img = img.resize((224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='tf')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

# @app.route('/recognizer/')
# def about():
#     return render_template('recognizer.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)

        # Process your result for human
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        result = str(pred_class[0][0][1])               # Convert to string
        result = result.replace('_', ' ').capitalize()
        
        # Serialize the result, you can add additional fields
        return jsonify(result=result, probability=pred_proba)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()




def rgb_to_hex(rgb):
	return '%02x%02x%02x' % rgb


def give_most_hex(file_path, code):
	my_image = Image.open(file_path).convert('RGB')
	size = my_image.size
	if size[0] >= 400 or size[1] >= 400:
		my_image = ImageOps.scale(image=my_image, factor=0.2)
	elif size[0] >= 600 or size[1] >= 600:
		my_image = ImageOps.scale(image=my_image, factor=0.4)
	elif size[0] >= 800 or size[1] >= 800:
		my_image = ImageOps.scale(image=my_image, factor=0.5)
	elif size[0] >= 1200 or size[1] >= 1200:
		my_image = ImageOps.scale(image=my_image, factor=0.6)
	my_image = ImageOps.posterize(my_image, 2)
	image_array = np.array(my_image)

	# create a dictionary of unique colors with each color's count set to 0
	# increment count by 1 if it exists in the dictionary
	unique_colors = {} # (r, g, b): count
	for column in image_array:
		for rgb in column:
			t_rgb = tuple(rgb)
			if t_rgb not in unique_colors:
				unique_colors[t_rgb] = 0
			if t_rgb in unique_colors:
				unique_colors[t_rgb] += 1

	# get a list of top ten occurrences/counts of colors
	# from unique colors dictionary
	sorted_unique_colors = sorted(
		unique_colors.items(), key=lambda x: x[1],
	reverse=True)
	converted_dict = dict(sorted_unique_colors)
	# print(converted_dict)

	# get only 10 highest values
	values = list(converted_dict.keys())
	# print(values)
	top_10 = values[0:10]
	# print(top_10)

	# code to convert rgb to hex
	if code == 'hex':
		hex_list = []
		for key in top_10:
			hex = rgb_to_hex(key)
			hex_list.append(hex)
		return hex_list
	else:
		return top_10


# app = Flask(__name__)

# @app.route('/about/', methods=['GET', 'POST'])
# def about():
#     if request.method == 'POST':
# 		f = request.files['file']
# 		colour_code = request.form['colour_code']
# 		colours = give_most_hex(f.stream, colour_code)
# 		return render_template('about.html',
# 							colors_list=colours,
# 							code=colour_code)
# 	return render_template('about.html')


@app.route('/about/', methods=['GET', 'POST'])
def recognize():
	if request.method == 'POST':
		f = request.files["file"]
		colour_code = request.form['colour_code']
		colours = give_most_hex(f.stream, colour_code)
		return render_template('about.html',
							colors_list=colours,
							code=colour_code)
	return render_template('about.html')


# if __name__ == '__main__':
# 	app.run(debug=True)
