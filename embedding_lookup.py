from two_sample_util import pdist, cosine_dist
import torch
import numpy


class EmbeddingLookup(object):

    def __init__(self, embedding_db):
        self.embedding_db = dict()

        for e in embedding_db.keys():
            embedding = embedding_db[e][0]
            self.embedding_db[e] = embedding

        # prepare tensor
        self.ids, raw_data = zip(*self.embedding_db.items())
        self.data_tensor = torch.tensor(raw_data).squeeze()

    def run_embedding_lookup_euclidean(self, querys):
        """
        Calculate embedding distance using Euclidean distance of all querys against the lookup database
        :param querys: querys for which distances should be calculated
        :return: 
        """

        if isinstance(querys, dict):
            query_ids, raw_data_query = zip(*querys.items())
        else:
            raw_data_query = querys
            query_ids = range(0, numpy.shape(querys)[0])
            
        query_tensor = torch.tensor(raw_data_query).squeeze()
        if len(query_ids) == 1:
            query_tensor = query_tensor.unsqueeze(0)

        distances = pdist(query_tensor, self.data_tensor, 2)

        return distances, query_ids

    def run_embedding_lookup_cosine(self, querys):
        """
        Calculate embedding distance using cosine distance of all querys against the lookup database
        :param querys: 
        :return: 
        """

        if isinstance(querys, dict):
            query_ids, raw_data_query = zip(*querys.items())
        else:
            raw_data_query = querys
            query_ids = range(0, numpy.shape(querys)[0])
            
        query_tensor = torch.tensor(raw_data_query).squeeze()
        if len(query_ids) == 1:
            query_tensor = query_tensor.unsqueeze(0)

        distances = cosine_dist(query_tensor, self.data_tensor)

        return distances, query_ids
