#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import Image
import os
import sys
import yaml


def save_jpeg(image, path):
	image.save(path, quality=94, optimize=True, progressive=True)


def generate_large(original, output_base, max_size):
	output_path = "{}.jpg".format(output_base)
	generated = original.copy()
	generated.thumbnail((max_size, max_size), Image.LANCZOS, None)
	save_jpeg(generated, output_path)


def generate_thumbnail(original, output_base, variant):

	output_path = "{}-{}.jpg".format(output_base, variant)
	max_size = 0, 0
	if variant[0] == "w":
		max_size = int(variant[1:]), 9999
	else:
		max_size = 9999, int(variant[1:])
	generated = original.copy()
	generated.thumbnail(max_size, Image.LANCZOS, None)
	save_jpeg(generated, output_path)


photos_file = open('photo_generation.yml', 'r', encoding='utf-8')
photos = yaml.safe_load(photos_file)

for item in photos:
	original = Image.open("res/{}.jpg".format(item["path"]))
	if item.get("mirror", False):
		original = original.transpose(Image.FLIP_LEFT_RIGHT)
	if len(sys.argv) < 2:
		sys.exit('error: output path argument is not specified')
	output_base_path = os.path.join(sys.argv[1], item["path"])
	os.makedirs(os.path.dirname(output_base_path), exist_ok=True)

	print("Generating {}...".format(item["path"]))
	default_size = item.get("default_size", 794)
	generate_large(original, output_base_path, default_size)

	for variant in item.get("output", ['h152']):
		print(" - {}...". format(variant))
		generate_thumbnail(original ,output_base_path, variant)
