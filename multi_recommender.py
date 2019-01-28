import pandas
import json
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

stopWords = set(stopwords.words('english'))

def preprocess_series(series):
    pp_text = []

    def preprocess(text):
        text = re.sub(r'([^\s\w]|_)+', '', text)

        preprocessed = []

        text = word_tokenize(text)
        for word in text:
            word = word.lower()
            if word not in stopWords:
                preprocessed.append(word)

        return preprocessed

    for desc in series:
        desc = preprocess(desc)
        pp_text.append(' '.join(desc))

    new_series = pandas.Series(pp_text)

    return new_series


def level_allowed(int):
    levels = {2: ['08'], 3: ['09', '10'], 4: ['10', '11'], 5: ['11'] }
    return levels[int]


def TFIDF():

    # returns full similarity matrix

    df['CourseSummary'] = df['CourseSummary'] + df['CourseDescription']
    df['CourseSummary'] = preprocess_series(df['CourseSummary'])

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform((df['CourseSummary']))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def get_recommendations(list):
    sim_scores = list
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:]
    course_indices = [i[0] for i in sim_scores]
    return df.iloc[course_indices]


def obj_info(index):

    record = df.iloc[index]

    return record["Code"], record['Name'], record['Area'], record['Average']


def match_prerequisites(list):

    id_list = []
    for l in list:
        id = df.iloc[indices_name[l]]['Code']
        id_list.append(id)

    return id_list


def normalize_enjoyment(dictionary):

    s = sum(dictionary.values())

    new_vals = {}
    for k, v in dictionary.items():
        new_vals[k] = 1+ v/s

    return new_vals


if __name__=="__main__":

    with open('data.json', 'r') as f:
        data = json.load(f)
    df = pandas.DataFrame(data['courses'])

    # user input
    previous_courses = {"INFR10070": 5, "INFR10067": 1, "INFR09028": 5}
    year_of_study = 4
    interests = ["Networks"]



    cosine_sim = TFIDF()
    courses = df['Name']
    indices = pandas.Series(df.index, index=df['Code'])
    indices_name = pandas.Series(df.index, index=df['Name'])

    array = []

    print("Course + Rating")

    for course_code, enjoyment in previous_courses.items():
        idx = indices[course_code]
        raw_scores = cosine_sim[idx]
        modified = []
        mean_raw = sum(raw_scores)/float(len(raw_scores))

        print("\t", df.iloc[indices[course_code]]['Name'], enjoyment)

        for i, score in enumerate(raw_scores):


            record = df.iloc[i]

            if record['Code'] in previous_courses or record['Level'] not in level_allowed(year_of_study):
                new_score = 0
            elif len(record['Prerequisites'])>0 and \
                    any([p for p in match_prerequisites(record['Prerequisites']) if p not in previous_courses]):
                new_score = 0
            else:
                new_score = (enjoyment * score) + (0.001 * float(record['Average']))
                if record['Area'] in interests:
                    new_score += (0.7 * mean_raw)

            modified.append(new_score)
        array.append(modified)

    array = np.array(array)
    new_reccomend = ([sum([row[i] for row in array]) for i in range(0,len(array[0]))])
    tuple_list = [(i, score) for i, score in enumerate(new_reccomend) if score != 0]

    reccoms = get_recommendations(tuple_list)[:5]

    print('\n\nRecommendations')

    for i, r in enumerate(reccoms['Code']):
        x, a, b, c = obj_info(indices[r])
        print("\t",i+1, "\t", a)
