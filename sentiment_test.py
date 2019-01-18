from nltk.corpus import opinion_lexicon
from nltk.stem import PorterStemmer
import re, sys


#tokenise the feedback by removing stopwords, changing all to lowercase and stemming
#returns a list of words
def tokenise_file(file):

    with open(file, 'r') as f:
        data = f.read()

    stopwords_file = open('stopwords.txt', 'r').readlines()
    stopwords = [x.strip() for x in stopwords_file]

    ps = PorterStemmer()

    tokens = re.split('[^a-zA-Z0-9]', data)
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

    print(list_pos)
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

    print(list_neg)
    return count_neg


#reads filename and comapares counts of positive and negative words. If equal, will be classified as neutral
def main():
    file_name = sys.argv[1]
    review = tokenise_file(file_name)
    pos = compare_positive(review)
    neg = compare_negative(review)


    if pos > neg:
        print("this review is positive")
    elif neg > pos:
        print("this review is negative")
    else:
        print("this review is neutral")


if __name__ == "__main__":
    main()