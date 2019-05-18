# -*- coding: utf-8 -*-
"""
Custom function that will be wrapped for be HTTP compliant
"""

from logging import getLogger

from flask import render_template

from datastructure.Response import Response
from utils.util import print_prediction_on_image, random_string

log = getLogger()


def upload_image_predict(html_file):
	"""
	Parse the HTML file
	:param html_file:
	:return:
	"""
	return render_template(html_file)


def predict_image(img_path, clf, PREDICTION_PATH):
	"""

	:param PREDICTION_PATH: global variable where image recognized are saved
	:param img_path: image that have to be predicted
	:param clf: classifier in charge to predict the image
	:return:
	"""
	response = Response()
	log.debug("predict_image | Predicting {}".format(img_path))
	prediction = clf.predict(img_path)
	log.debug("predict_image | Image analyzed!")
	# Manage success
	if prediction is not None and isinstance(prediction, list) and len(prediction) == 1:
		img_name = random_string() + ".png"
		log.debug("predict_image | Generated a random name: {}".format(img_path))
		log.debug("predict_image | Visualizing face recognition ...")
		print_prediction_on_image(img_path, prediction, PREDICTION_PATH, img_name)
		response.status = "OK"
		response.description = img_name
		response.data = prediction[0][0]

	# Manage error
	elif prediction is None:
		response.error = "CLASSIFIER_NOT_LOADED"
		response.description = "Classifier is None | Training mandatory"
		log.error("predict_image | Seems that the classifier is not loaded :/")

	elif isinstance(prediction, list):
		if len(prediction) == 0:
			response.error = "NO_FACE_FOUND"
			response.description = "Seems that in this images there is no face :/"
			log.error("predict_image | Seems that in this images there is no face :/")

		elif len(prediction) > 1:
			response.error = "TOO_MANY_FACES"
			response.description = "Seems that in this images there are too many faces :/"
			log.error("predict_image | Seems that in this images there are too many faces :/")

	elif prediction == -1:
		# TODO: Add custom algorithm that "try to understand" who haven't never recognized
		response.error = "FACE_NOT_RECOGNIZED"
		response.description = "Seems that this face is related to nobody that i've seen before ..."
		log.error("predict_image | Seems that this face is lated to nobody that i've seen before ...")

	return response.__dict__
