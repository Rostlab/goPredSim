def read_config_file(file_in):
    config_data = dict()
    with open(file_in) as read_in:
        for line in read_in:
            splitted_line = line.strip().split(':')
            config_data[splitted_line[0]] = splitted_line[1].strip()

    return config_data


def read_go_annotations(file_in):
    go_annotations = defaultdict(set)

    with open(file_in) as read_in:
        for line in read_in:
            splitted_line = line.strip().split()
            identifier = splitted_line[0]
            go_terms = set(splitted_line[1].split(','))

            go_annotations[identifier] = go_terms

    return go_annotations