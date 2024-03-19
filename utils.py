import logging
import sys
import re

def deduplicate_dicts(dict_list, key):
    seen = set()
    unique_dicts = []
    for d in dict_list:
        val = d.get(key)
        if val not in seen:
            seen.add(val)
            unique_dicts.append(d)
    return unique_dicts

def logger_init():
    logging.basicConfig(filename='arxivdigest.log', level=logging.INFO)
    logger = logging.getLogger('arxivdigest')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def tokenize(text):
    text = re.sub(r'\W+', ' ', text).lower()
    return set(text.split())

def find_most_similar_paper_jaccard(paper_list, paper):
    paper_set = tokenize(paper)

    max_similarity = 0
    most_similar_paper = None

    for current_paper in paper_list:
        current_paper_set = tokenize(current_paper['title'])
        similarity = jaccard_similarity(paper_set, current_paper_set)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_paper = current_paper

    return most_similar_paper