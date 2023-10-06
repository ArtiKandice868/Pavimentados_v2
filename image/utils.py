import cv2 
import tensorflow as tf

def transform_images(images, size):
	"""
	Transform the images for the Yolo model
	"""
	images = tf.image.resize(images, (size, size))
	images = images/255.0
	return images