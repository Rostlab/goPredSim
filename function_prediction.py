from collections import defaultdict
from embedding_lookup import EmbeddingLookup
import numpy
import sys


class FunctionPrediction(object):

    def __init__(self, embedding_db, go_db, go, go_type):
        self.go = go

        if go_type == 'all':
            self.lookup_db = EmbeddingLookup(embedding_db)
            self.go_db = go_db
        elif go_type == 'mfo' or go_type == 'bpo' or go_type == 'cco':
            # only use proteins in the annotation set which actually have an annotation in this ontology
            self.go_db = defaultdict(set)
            embedding_db_reduced = dict()
            for k in embedding_db.keys():
                terms = go_db[k]
                go_terms = self.get_terms_by_go(terms)[go_type]
                if len(go_terms) > 0:
                    embedding_db_reduced[k] = embedding_db[k]
                    self.go_db[k] = go_terms
            self.lookup_db = EmbeddingLookup(embedding_db_reduced)
        else:
            sys.exit("{} is not a valid GO. Valid GOs are [all|mfo|bpo|cco]".format(go_type))

    def get_terms_by_go(self, terms):
        terms_by_go = {'mfo': set(), 'bpo': set(), 'cco': set()}

        for t in terms:
            onto = self.go.get_ontology(t)
            if onto != '':
                terms_by_go[onto].add(t)

        return terms_by_go

    def run_prediction_embedding_all(self, querys, distance, hits, criterion):

        predictions = defaultdict(defaultdict)
        hit_ids = defaultdict(defaultdict)

        if distance == 'euclidean':
            distances, query_ids = self.lookup_db.run_embedding_lookup_euclidean(querys)
        elif distance == 'cosine':
            distances, query_ids = self.lookup_db.run_embedding_lookup_cosine(querys)
        else:
            sys.exit("{} is not a correct distance".format(distance))

        for i in range(0, len(query_ids)):
            query = query_ids[i].split()[0]
            dists = distances[i, :].squeeze().numpy()
            for h in hits:
                prediction = dict()
                if criterion == 'dist':  # extract hits within a certain distance
                    indices = numpy.nonzero(dists <= h)
                elif criterion == 'num':  # extract h closest hits
                    indices_tmp = numpy.argpartition(dists, h)[0:h]
                    dists_tmp = [dists[i] for i in indices_tmp]
                    max_dist = numpy.amax(dists_tmp)
                    indices = numpy.nonzero(dists <= max_dist)[0]

                    if len(indices) > h:
                        print("Multiple hits with same distance found, resulting in {} hits".format(len(indices)))

                else:
                    sys.exit("No valid criterion defined, valid criterions are [dist|num]")

                num_hits = len(indices)

                for ind in indices:
                    lookup_id = self.lookup_db.ids[ind]
                    go_terms = self.go_db[lookup_id]
                    dist = dists[ind]

                    if distance == 'euclidean':
                        dist = 2 / (2 + dist)
                    elif distance == 'cosine':
                        dist = 1 - dist

                    for g in go_terms:
                        if g in prediction.keys():
                            # if multiple hits are included RIs get smaller --> predictions retrieved for different
                            # numbers of hits are not directly comparable
                            prediction[g] += dist / num_hits
                        else:
                            prediction[g] = dist / num_hits

                    if query not in hit_ids[h].keys():
                        hit_ids[h][query] = dict()
                    hit_ids[h][query][lookup_id] = round(dist, 2)

                # round ri and remove hits with ri == 0.00
                keys_for_deletion = set()
                for p in prediction:
                    ri = round(prediction[p], 2)
                    if ri == 0.00:
                        keys_for_deletion.add(p)
                    else:
                        prediction[p] = ri

                for k in keys_for_deletion:
                    del prediction[k]

                # reduce prediction to leaf terms
                parent_terms = []
                for p in prediction.keys():
                    parents = self.go.get_parent_terms(p)
                    parent_terms += parents
                # exclude terms that are parent terms, i.e. there are more specific terms also part of this prediction
                keys_for_deletion = set()
                for p in prediction.keys():
                    if p in parent_terms:
                        keys_for_deletion.add(p)

                for k in keys_for_deletion:
                    del prediction[k]

                predictions[h][query] = prediction

        return predictions, hit_ids

    @staticmethod
    def write_predictions_cafa(predictions, out_file, model_num):
        """
        Write prediictions in CAFA format
        :param predictions: predictions to write
        :param out_file: output file
        :param model_num: number of model that is used
        :return:
        """
        with open(out_file, 'w') as out:
            out.write('AUTHOR\tRostlab2\nMODEL\t{}\nKEYWORDS\thomolog, machine learning, natural language processing.'
                      '\n'.format(model_num))
            for p in predictions.keys():
                prediction = predictions[p]
                for pred in prediction.keys():
                    ri = prediction[pred]
                    out.write('{}\t{}\t'.format(p, pred))
                    out.write('{:0.2f}\n'.format(float(ri)))
            out.write('END')

    @staticmethod
    def write_hits(hits, out_file):
        with open(out_file, 'w') as out:
            out.write('Query\tHit\tRI\n')
            for q in hits.keys():
                h = hits[q]
                for k in h.keys():
                    ri = h[k]
                    out.write('{}\t{}\t{}\n'.format(q, k, ri))
