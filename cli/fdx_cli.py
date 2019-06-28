from fdx_color_extractor import FdxColorExtractor
import sys
import click
import os
import json
sys.path.append('../core')


@click.command()
@click.option('--swatch', '-s', default=False, help='True, True indicates images are swatch images')
@click.option('--image', '-i', help='path of the image')
@click.option('--dir', '-d', help='path of the directory')
@click.option('--out', '-o', default=None, help='Name of the output file')
def compute(swatch, image, dir, out):
	""" Command Line Interface for color extractor wraps on top of the core app.


		Parameters
		----------
		swatch: boolean
			True indicates the image is swatch image and vice versa
		image: str
			Path to the image
		dir: str
			Path to the directory
		out: str
			Path to the output file to which output would be printed
	"""
	if out:
		print_to = open(out.encode('utf-8'), 'w')
	else:
		print_to = sys.stdout
	if image:
		compute_results(image, swatch, print_to)
	elif dir:
		compute_results(dir, swatch, print_to)


def compute_results(path, swatch, print_to):
	"""
		gets the rgb, hsl values and hasl tags for all images using extract method of FdxColorExtractor and prints the image_path
		and the above values as a json record

		Parameters
		----------
		path : str
			The path to the directory or the path of an image

		swatch : boolean
			True indicates image is a swatch image and vice versa

		print_to : File/sys.stdout
			The file to which ouput needs to be printed to
	"""
	file_urls = get_images(path)
	for file_url in file_urls:
		# gets the fdxcolorextractor object containing color palette
		color_palette = FdxColorExtractor(file_url, swatch).extract()

		# gets the dictionary part of the object
		color_palette_dict = color_palette.__dict__

		# dumps to json asking the encoder to take dict form of every object
		color_palette_jsondump = json.dumps(color_palette_dict, default=lambda o: o.__dict__)

		print(color_palette_jsondump, file=print_to)


def get_images(path):
	"""
		Gets paths of all images in a given directory or a list containing one image if the given path is that of an image

		Parameters
		----------
		path : The path to the directory

		Returns
		-------
		images : list of all images
	"""
	exts = ['.png', '.jpg', '.jpeg']
	images = []
	if os.path.isfile(path):
		file_name, file_ext = os.path.splitext(path)
		if file_ext in exts:
			return [path]
	else:
		files = get_files(path)
		for file in files:
			file_name, file_ext = os.path.splitext(file)
			if file_ext in exts:
				images.append(file)
		return images


def get_files(path):
	"""
		Gets paths of all files in a given directory

		Parameters
		----------
		path : The path to the directory

		Returns
		-------
		files : list of all files
	"""
	files = []
	for dirpath, _, filenames in os.walk(path):
		for filename in [f for f in filenames]:
			files.append(os.path.join(dirpath, filename))
	return files


if __name__ == "__main__":
	compute()
