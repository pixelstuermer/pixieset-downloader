import argparse
import json
import re

import requests
from hurry.filesize import size


def init_arguments_parser():
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument('base_url', type=str, help='base URL')
    arguments_parser.add_argument('collection_id', type=int, help='collection ID')
    arguments_parser.add_argument('collection_key', type=str, help='collection key')
    arguments_parser.add_argument('gallery_name', type=str, help='gallery name')
    arguments_parser.add_argument('cookie', type=str, help='valid HTTP session cookie')
    arguments_parser.add_argument('-f', '--filename', type=str, help='file name scheme')
    arguments_parser.add_argument('-s', '--separator', type=str, help='file name counter separator', default='_')
    arguments_parser.add_argument('-r', '--regex', type=str, help='original file name regex filter', default='.*')
    return arguments_parser.parse_args()


def perform_page_data_request(arguments, page):
    parameters = {'cid': arguments.collection_id,
                  'cuk': arguments.collection_key,
                  'gs': arguments.gallery_name,
                  'page': page}
    headers = {'x-requested-with': 'XMLHttpRequest',
               'user-agent': 'none'}
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
    return re.match('(?i).*\\.(gif|jpe?g|tiff?|png|webp|bmp)', image_name)


def matches(file_name_filter, file_name):
    return re.match(file_name_filter, file_name)


def get_default_image_name(image_name):
    return image_name.rsplit('/', 1)[-1]


def get_custom_image_name(image_name, separator, counter, file_suffix):
    return image_name + separator + str(counter) + '.' + file_suffix


def get_file_suffix(file_name):
    return file_name.rsplit('.', 1)[-1]


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
    page = 1
    images_counter = 0
    image_size_counter = 0
    while has_next_page:
        page_data_response = perform_page_data_request(arguments, page)
        page_data = json.loads(page_data_response.json()['content'])

        for image_data in page_data:
            for key in image_data:
                name_filter = arguments.regex
                value = get_normalized_url(str(image_data[key]))
                if is_url(value) and is_image_name(value) and matches(name_filter, value):
                    if arguments.filename is not None:
                        separator = arguments.separator
                        file_suffix = get_file_suffix(value)
                        image_name = get_custom_image_name(arguments.filename, separator, images_counter, file_suffix)
                    else:
                        image_name = get_default_image_name(value)
                    image_response = perform_image_request(value)
                    image_size = save_image_to_file(image_name, image_response.content)
                    print('File: ' + str(images_counter) + ', Name: ' + image_name + ', Size: ' + size(image_size))
                    images_counter += 1
                    image_size_counter += image_size

        has_next_page = not is_last_page(page_data_response)
        page += 1

    print('Downloaded ' + str(images_counter) + ' files with about ' + size(image_size_counter))


main()
