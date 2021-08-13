import argparse

import requests


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


def is_last_page(response):
    return response.json()['isLastPage']


def main():
    arguments = init_arguments_parser()
    has_next_page = True
    page = 0
    while has_next_page:
        response = perform_page_data_request(arguments, page)
        has_next_page = not is_last_page(response)
        page += 1


main()
