from textblob import TextBlob
import re, sys
import argparse


#reads filename and comapares counts of positive and negative words. If equal, will be classified as neutral
def main(filename):
    with open(filename, 'r') as f:
        data = TextBlob(f.read())

    lol = data.sentiment



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='enter filename')
    parser.add_argument('filename', type=str, help='json filename')
    args = parser.parse_args()
    main(args.filename)