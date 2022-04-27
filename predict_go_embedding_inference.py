import sys
import file_utils as fu
from gene_ontology import GeneOntology
from function_prediction import FunctionPrediction
from pathlib import Path


def main():
    # read in information
    config_file = sys.argv[1]
    config_data = fu.read_config_file(config_file)
    print(config_data)

    # read in embeddings, annotations, and GO
    test_embeddings = fu.read_embeddings(config_data['targets'])
    embeddings = fu.read_embeddings(config_data['lookup_set'])

    go = GeneOntology(config_data['go'])
    go_annotations = fu.read_go_annotations(config_data['annotations'])

    # set ontologies
    if config_data['onto'] == 'all':
        ontologies = ['bpo', 'mfo', 'cco']
    else:
        ontologies = [config_data['onto']]
        
    # set dist cutoffs:
    cutoffs = config_data['thresh']
    dist_cutoffs = cutoffs.split(',')

    # perform prediction for each ontology individually
    for o in ontologies:
        predictor = FunctionPrediction(embeddings, go_annotations, go, o)
        predictions_all, _ = predictor.run_prediction_embedding_all(test_embeddings, 'euclidean', dist_cutoffs,
                                                                    config_data['modus'])

        # write predictions for each distance cutoff
        for dist in predictions_all.keys():
            predictions = predictions_all[dist]
            predictions_out = '{}_{}_{}.txt'.format(config_data['output'], dist, o)
            FunctionPrediction.write_predictions(predictions, predictions_out)


main()
