import argparse
import json
import re

import requests
from hurry.filesize import size


def init_arguments_parser():
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument('base_url', type=str, help='Base URL')
    arguments_parser.add_argument('collection_id', type=int, help='Collection ID')
    arguments_parser.add_argument('collection_key', type=str, help='Collection key')
    arguments_parser.add_argument('gallery_name', type=str, help='Gallery name')
    arguments_parser.add_argument('cookie', type=str, help='Valid HTTP session cookie')
    return arguments_parser.parse_args()


def perform_page_data_request(arguments, page):
    parameters = {'cid': arguments.collection_id,
                  'cuk': arguments.collection_key,
                  'gs': arguments.gallery_name,
                  'page': page}
    headers = {'x-requested-with': 'XMLHttpRequest'}
    cookies = {'PHPSESSID': arguments.cookie}
    return requests.get(arguments.base_url, params=parameters, headers=headers, cookies=cookies)


def perform_image_request(image_url):
    return requests.get(image_url)


def is_last_page(page_data_response):
    return page_data_response.json()['isLastPage']


def get_normalized_url(url):
    if url.startswith('//'):
        return url.replace('//', 'https://')
    else:
        return url


def is_url(url):
    return re.match('https?://.*', url)


def is_image_name(image_name):
    return re.match('.*\\.(gif|jpe?g|tiff?|png|webp|bmp)', image_name)


def get_default_image_name(image_name):
    return image_name.rsplit('/', 1)[-1]


def save_image_to_file(image_name, image_data):
    image_file = open(image_name, 'wb')
    image_file.write(image_data)
    image_file.seek(0, 2)
    image_file_size = image_file.tell()
    image_file.close()
    return image_file_size


def main():
    arguments = init_arguments_parser()
    has_next_page = True
    page = 0
    images_counter = 0
    image_size_counter = 0
    while has_next_page:
        page_data_response = perform_page_data_request(arguments, page)
        page_data = json.loads(page_data_response.json()['content'])

        for image_data in page_data:
            for key in image_data:
                normalized_key = get_normalized_url(str(image_data[key]))
                if (is_url(normalized_key)) and (is_image_name(normalized_key)):
                    image_response = perform_image_request(normalized_key)
                    image_name = get_default_image_name(normalized_key)
                    image_size = save_image_to_file(image_name, image_response.content)
                    images_counter += 1
                    image_size_counter += image_size
                    print('File: ' + str(images_counter) + ', Name: ' + image_name + ', Size: ' + size(image_size))

        has_next_page = not is_last_page(page_data_response)
        page += 1

    print('Downloaded ' + str(images_counter) + ' files with about ' + size(image_size_counter))


main()
