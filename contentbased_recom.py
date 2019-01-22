import json, argparse, pprint
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval
import pandas as pd
import numpy as np



def similarity(data,mycourse):

    dict_descriptions = {}
    indice_dict = {}

    for i, c in enumerate(data['courses']):
        dict_descriptions[c['courseName']] = c['summary'] + c['area']
        indice_dict[i] = c['courseName']

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(dict_descriptions)

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    for i in indice_dict:
        if indice_dict.get(i) == mycourse:
            print( cosine_sim[i])
    #print(indice_dict)


def main(filename, course):
    with open(filename, 'r') as f:
        data = json.load(f)

    mycourse = " "
    titles = []

    for c in data['courses']:
        titles.append(c['courseName'])
        if c['courseName'] == course:
            mycourse = c['courseName']
            #data['courses'].remove(c)
    similarity(data,mycourse)
    #pprint.pprint(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='enter filename')
    parser.add_argument('filename', type=str, help='json filename')
    parser.add_argument('current_course', type=str, help = 'course currently taken by user')
    args = parser.parse_args()
    main(args.filename, args.current_course)