from sklearn.metrics import pairwise_distances, pairwise
import torch
import numpy
import sys


class EmbeddingLookup(object):

    def __init__(self, embedding_db):
        self.embedding_db = dict()

        for e in embedding_db.keys():
            embedding = embedding_db[e][0]
            self.embedding_db[e] = embedding

        # prepare data
        self.ids, self.raw_data = zip(*self.embedding_db.items())

    def run_embedding_lookup_distance(self, querys, metric):
        """
        Calculate embedding distance of all querys against the lookup database
        :param querys: querys for which distances should be calculated
        :param metric: metric to use to calculate distances
        :return: distances, query ids
        """

        if metric in pairwise.distance_metrics():
            if isinstance(querys, dict):
                query_ids, raw_data_query = zip(*querys.items())
            else:
                raw_data_query = querys
                query_ids = range(0, numpy.shape(querys)[0])
            
            raw_data_query = numpy.array(raw_data_query).squeeze()
            if len(query_ids) == 1:
                raw_data_query = raw_data_query.reshape(1, -1)

            distances = pairwise_distances(raw_data_query, self.raw_data, metric=metric)
        else:
            sys.exit("{} is not a correct distance metric\n"
                     "See <sklearn.metrics.pairwise.distance_metrics()> "
                     "for all possible distance metrics".format(metric))
            
        return distances, query_ids
