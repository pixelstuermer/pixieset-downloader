import argparse
import requests


def init_arguments_parser():
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument('url', type=str, help='Base URL')
    arguments_parser.add_argument('collection_id', type=int, help='Collection ID')
    arguments_parser.add_argument('collection_key', type=str, help='Collection key')
    arguments_parser.add_argument('gallery', type=str, help='Gallery name')
    arguments_parser.add_argument('cookie', type=str, help='Valid HTTP session cookie')
    return arguments_parser.parse_args()


def perform_request(arguments):
    parameters = {'cid': arguments.collection_id, 'cuk': arguments.collection_key, 'gs': arguments.gallery, 'page': 0}
    headers = {'x-requested-with': 'XMLHttpRequest'}
    cookies = {'PHPSESSID': arguments.cookie}
    return requests.get(arguments.url, params=parameters, headers=headers, cookies=cookies)


def main():
    arguments = init_arguments_parser()
    response = perform_request(arguments)


main()
