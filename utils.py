import logging
import sys

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