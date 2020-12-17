# goPredSim - Inference based on embedding similarity

goPredSim is a new method to predict GO terms through annotation transfer annotation transfer not using sequence similarity, but similarity in embedding space. To this end, the method uses SeqVec [1] or ProtBert-BFD [2] embeddings. goPredSim is a fast, simple, and easy-to-use inference method that achieves performance superior to commonly used homology-based inference.

## How goPredSim works
goPredSim takes a lookup dataset of proteins with known GO annotations and a set of target proteins for which GO predictions should be made. Both of these sets are encoded as SeqVec embeddings. Then, all pairwise distances between proteins in the lookup set and the target set are calculated. Annotations for the target proteins are transferred from proteins in the lookup set that are similar to the targets. Similarity can be defined using 2 different modi

1. The *k*-nearest neighbors to a target protein are defined as similar proteins.
2. All proteins with a certain distance *d* to the target protein are defined as similar proteins.

For both modi, all annotations are combined. The distance is converted into a similarity which can be used as a reliability score for the prediction (proteins closer to the target, i.e. with a higher similiarity, are expected to provide more trustworthy predictions). If multiple neighbors are considered, GO terms annotated to more than one neighbor get higher reliability scores than GO terms only annotated to one.

## How to use goPredSim
All important files and parameters have to be specificed in `config.txt`. The parameters and options are:

- `go`: Gene Ontology (GO) [3] to use. The GO from CAFA3 is included as an example
- `lookup_set`: Embeddings for lookup set. The embeddings for the `annotations` set are included as an example
- `annotations`: Annotations to use for transfer. The expected format is one line per protein with 1st column: identifer, 2nd column: comma-separated list of annotated GO terms. The GOA [4] version from 2017 with all Swiss-Prot sequences is included as an example.
- `targets`: Embeddings for target proteins for which GO term predictions should be calculated
- `onto`: Ontology for which predictions should be made `[all|bpo|mfo|cco]`
- `thresh`: Defines *k* (Number of neighbors to consider) or *d* (Distance threshold). Can be a comma-separated list of different values (all for the same modus)
- `modus`: If hits should be identified as the *k*-nearest neighbors (`num`) or by a distance threshold (`dist`)
- `output`: File prefix were output should be written to, will be extended by `_thresh_onto.txt`

For a given config-file, GO term prediction can be performed with the following command:

`python predict_go_embedding_inference.py config.txt`

## Embeddings

Embeddings were calculated using the pre-trained models SeqVec, publicly available [in the SeqVec repository](https://github.com/Rostlab/SeqVec), or ProtBert-BFD, publicly available [in the ProtTrans repository](https://github.com/agemagician/ProtTrans).

The pre-computed embeddings (npy-files) for GOA2020 and GOA2017 can be downloaded from [ftp://rostlab.org/goPredSim](ftp://rostlab.org/goPredSim).

The corresponding ids for the embeddings can be found in `data/`. To successfully run goPredSim both the .npy-file and the .txt-file containing the ids have to be in the same directory.

## Requirements
goPredSim is written in Python3. In order to execute goPredSim, Python3 has to be installed locally. Additionally, the following Python packages have to be installed:

- torch
- numpy
- pathlib
- scikit-learn

## Availability as web service
If you are interested in running only a few sequences, goPredSim is also available as a web service: https://embed.protein.properties/ or as part of PredictProtein [5]: https://predictprotein.org/

## Cite
If you are using this method and find it helpful, we would appreciate if you could cite the following preprint:

Littmann M, Heinzinger M, Dallago C, Olenyi T, Rost B (2020). Embeddings from deep learning transfer GO annotations beyond homology. bioRxiv. (doi:  https://doi.org/10.1101/2020.09.04.282814)


## References
[1] Heinzinger M, Elnaggar A, Wang Y, Dallago C, Nechaev D, Matthes F, Rost B (2019). Modeling aspects of the language of life through transfer-learning protein sequences. BMC Bioinformatics, **20**:73.

[2] Elnaggar A, Heinzinger M, Dallago C, Rihawi G, Wang Y, Jones L, Gibbs T, Feher T, Angerer C, Bhowmik D, Rost B (2020). ProtTrans: towards cracking the language of life's code through self-supervised deep learning and high performance computing. bioRxiv.

[3] Ashburner M, Ball CA, Blake JA, Botstein D, Butler H, Cherry JM, Davis AP, Dolinski K, Dwight SS, Eppig JT (2000). Gene ontology: tool for the unification of biology. Nature genetics, **25**(1):25-29.

[4] Camon E, Magrane M, Barrell D, Lee V, Dimmer E, Maslen J, Binns D, Harte N, Lopez R, Apweiler R (2004). The Gene Ontology Annotation (GOA) Database: sharing knowledge in Uniprot with Gene Ontology. Nucleic Acids Res, **32**(Database issue):D262-266.

[5] Yachdav, G. et al. (2014). PredictProtein--an open resource for online prediction of protein structural and functional features. Nucleic Acids Res, **42**(Webserver issue):W337-43
