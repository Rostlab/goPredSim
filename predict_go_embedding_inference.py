import sys
import file_utils as fu
import npy2npz as n2n
from gene_ontology import GeneOntology
from function_prediction import FunctionPrediction


def main():
    # read in information
    config_file = sys.argv[1]
    config_data = fu.read_config_file(config_file)
    print(config_data)

    # read in embeddings, annotations, and GO
    test_embeddings = n2n.get_dataset(config_data['targets'], False)
    embeddings = n2n.get_dataset(config_data['lookup_set'], False)
    go = GeneOntology(config_data['go'])
    go_annotations = fu.read_go_annotations(config_data['annotations'])

    # set ontologies
    if config_data['onto'] == 'all':
        ontologies = ['bpo', 'mfo', 'cco']
    else:
        ontologies = [config_data['onto']]

    for o in ontologies:
        predictor = FunctionPrediction(embeddings, go_annotations, go, o)

    # TODO
    # Workflow:
    # 1. Read in Config file with (1) GO, (2) Lookup table/embeddings, (3) Annotations, (4) Target embeddings
    # (5) Ontology for which predictions should be made (bpo, mfo, cco, all),
    # (6) Number of neighbors to include/Distance threshold, (7) Dist|Num
    # Is it needed that we have the GO? Could it be enough to just have an annotation set reduced to the leave
    # terms? Alternatively, do that implicitly in the code here
    # 2. Parse information and set parameters
    # 3. For each ontology, create FunctionPrediction object and call "run_prediction_embedding_all"
    # 4. For each number of neighbors and ontology, write results: 1. Only leaf terms 2. Reliability
    # TODO write different function to write results


main()
