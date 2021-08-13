import argparse


def init_arguments():
    arguments_parser = argparse.ArgumentParser()
    arguments_parser.add_argument('cid', type=int, help='Collection ID')
    arguments_parser.add_argument('cuk', type=str, help='Collection URL key')
    arguments_parser.add_argument('gs', type=str, help='Gallery name')
    return arguments_parser.parse_args()


init_arguments()
