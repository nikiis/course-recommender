import json, argparse, re
from pprint import pprint
from nltk.corpus import opinion_lexicon
from nltk.stem import PorterStemmer
from collections import defaultdict


#tokenise the feedback by removing stopwords, changing all to lowercase and stemming
#returns a list of words
def tokenise(feedback):

    stopwords_file = open('stopwords.txt', 'r').readlines()
    stopwords = [x.strip() for x in stopwords_file]

    ps = PorterStemmer()

    tokens = re.split('[^a-zA-Z0-9]', feedback)
    lowercase = [word.lower() for word in tokens if word.isalnum()]
    engstop = set(stopwords)
    filter_stopword = [word for word in lowercase if word not in engstop]
    stemmingword = [ps.stem(word) for word in filter_stopword]

    #print(stemmingword)
    return stemmingword


#Using nltk opinion lexicon, compare words in feedback to positive words and count occurence
#returns total count of positive words found
def compare_positive(review):
    positive_words = opinion_lexicon.positive()
    count_pos = 0
    list_pos = []

    for word in positive_words:
        for w in review:
            if word == w:
                list_pos.append(word)
                count_pos += 1
    # print(count_pos)
    return count_pos

#Using nltk opinion lexicon, compare words in feedback to negative words and count occurence
#returns total count of negative words found
def compare_negative(review):
    negative_words = opinion_lexicon.negative()
    count_neg = 0
    list_neg = []

    for word in negative_words:
        for w in review:
            if word == w:
                list_neg.append(word)
                count_neg += 1
    # print(list_neg)
    return count_neg


def semantic_analysis(data):
    pos_dict = {}
    neg_dict = {}

    for c in data['courses']:
        pos = 0
        neg = 0
        print(c['courseName'])
        for feedback in c['feedback']:
            tokenised_comment = tokenise(feedback)
            pos += compare_positive(tokenised_comment)
            neg += compare_negative(tokenised_comment)
        pos_dict[c['courseName']] = pos
        neg_dict[c['courseName']] = neg

    print(pos_dict)
    print(neg_dict)

    for cname in pos_dict:
        total = float(pos_dict.get(cname) + neg_dict.get(cname))
        if pos_dict.get(cname) > neg_dict.get(cname):
            percentage = (pos_dict.get(cname) / total) * 100.00
            print("{} : is positive by {:.2f} %".format(cname,percentage))
        elif neg_dict.get(cname) > pos_dict.get(cname):
            percentage = (neg_dict.get(cname) / total) * 100.00
            print("{} : is negative by {:.2f} %".format(cname, percentage))
        else:
            print("this is neutral")


def main(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    semantic_analysis(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='enter filename')
    parser.add_argument('filename', type=str, help='json filename')
    args = parser.parse_args()
    main(args.filename)