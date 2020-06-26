from collections import defaultdict


class GeneOntology(object):

    def __init__(self, onto_file):
        self.all_go = defaultdict(dict)

        self._parse_go(onto_file)
        self.mfo = self._get_go_annotations('mfo')
        self.bpo = self._get_go_annotations('bpo')
        self.cco = self._get_go_annotations('cco')

    def _parse_go(self, onto_file):
        # information to save for a GO term
        go_id = ''
        go_name = ''
        namespace = ''
        parents = set()
        alt_ids = set()

        term = False

        with open(onto_file) as read_in:
            for line in read_in:
                splitted_line = line.strip().split(':')
                if '[Term]' in line:  # new term begins
                    term = True
                    if not go_id == '':
                        if go_id in self.all_go.keys():
                            print(go_id)
                        self.all_go[go_id] = {'name': go_name, 'go': namespace, 'parents': parents}
                        for a in alt_ids:
                            self.all_go[a] = {'name': go_name, 'go': namespace, 'parents': parents}

                        # reset annotations
                        go_id = ''
                        go_name = ''
                        namespace = ''
                        parents = set()
                        alt_ids = set()
                elif term and 'id: GO:' in line and 'alt_id' not in line:
                    go_id = "GO:{}".format(splitted_line[2].strip())
                elif term and 'alt_id: GO' in line:
                    alt_id = "GO:{}".format(splitted_line[2].strip())
                    alt_ids.add(alt_id)
                elif term and 'name:' in line:
                    go_name = splitted_line[1].strip()
                elif term and 'namespace:' in line:
                    tmp_nampespace = splitted_line[1].strip()
                    if tmp_nampespace == 'biological_process':
                        namespace = 'bpo'
                    elif tmp_nampespace == 'molecular_function':
                        namespace = 'mfo'
                    elif tmp_nampespace == 'cellular_component':
                        namespace = 'cco'
                elif term and 'is_a:' in line:
                    splitted_term = splitted_line[2].split("!")
                    go_term = "GO:{}".format(splitted_term[0].strip())
                    parents.add(go_term)
                elif '[Typedef]' in line:
                    term = False

        self.all_go[go_id] = {'name': go_name, 'go': namespace, 'parents': parents}

        # include all parents (also grandparents,...)
        for go_term in self.all_go.keys():
            new_parents = self._set_parents(go_term)
            self.all_go[go_term]['parents'].update(new_parents)

        # exclude parents that are not part of the database  # TODO needed?
        # for go_term in self.all_go.keys():
        #     parents = set(self.all_go[go_term]['parents'])
        #     to_remove = set()
        #     for p in parents:
        #         if p not in self.all_go.keys():
        #             to_remove.add(p)
        #     for t in to_remove:
        #         parents.remove(t)
        #     self.all_go[go_term]['parents'] = parents

    def _set_parents(self, term):
        new_parents = set()

        parents = self.all_go[term]['parents']
        for p in parents:
            tmp_parents = self._set_parents(p)
            new_parents.update(tmp_parents)
        new_parents.update(parents)

        return new_parents

    def _get_go_annotations(self, onto):
        ontology = defaultdict(dict)

        for k in self.all_go.keys():
            if self.all_go[k]['go'] == onto:
                ontology[k] = self.all_go[k]

        return ontology

    def get_parent_terms(self, go_term):
        if go_term in self.all_go.keys():
            return self.all_go[go_term]['parents']
        else:
            return set()

    def get_all_terms(self, leaf_annotations):
        all_annotations = defaultdict(set)

        for k in leaf_annotations.keys():
            go_terms = leaf_annotations[k]
            for g in go_terms:
                parent_terms = self.get_parent_terms(g)
                all_annotations[k].add(g)
                all_annotations[k].update(parent_terms)

        return all_annotations

    def get_ontology(self, go_term):
        if go_term in self.all_go.keys():
            return self.all_go[go_term]['go']
        else:
            return ''

    def get_name(self, go_term):
        return self.all_go[go_term]['name']
