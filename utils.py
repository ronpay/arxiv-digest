def deduplicate_dicts(dict_list, key):
    seen = set()
    unique_dicts = []
    for d in dict_list:
        val = d.get(key)
        if val not in seen:
            seen.add(val)
            unique_dicts.append(d)
    return unique_dicts