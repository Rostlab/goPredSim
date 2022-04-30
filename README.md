# goPredSim - Inference based on embedding similarity

goPredSim is a method to predict GO terms through annotation transfer annotation transfer not using sequence similarity, but similarity in embedding space. To this end, the method uses SeqVec [1], ProtBert-BFD [2], or ProtT5 [2] embeddings. goPredSim is a fast, simple, and easy-to-use inference method that achieves performance superior to commonly used homology-based inference.

## How goPredSim works
goPredSim takes a lookup dataset of proteins with known GO annotations and a set of target proteins for which GO predictions should be made. Both of these sets are encoded as embeddings. Then, all pairwise distances between proteins in the lookup set and the target set are calculated. Annotations for the target proteins are transferred from proteins in the lookup set that are similar to the targets. Similarity can be defined using 2 different modi

1. The *k*-nearest neighbors to a target protein are defined as similar proteins.
2. All proteins with a certain distance *d* to the target protein are defined as similar proteins.

For both modi, all annotations are combined. The distance is converted into a similarity which can be used as a reliability score for the prediction (proteins closer to the target, i.e., with a higher similiarity, are expected to provide more trustworthy predictions). If multiple neighbors are considered, GO terms annotated to more than one neighbor get higher reliability scores than GO terms only annotated to one.

## How to use goPredSim
All important files and parameters have to be specificed in `config.txt`. The parameters and options are:

- `go`: Gene Ontology (GO) [3] to use. The GO from CAFA3, CAFA4, and from March 2022 are included as examples
- `lookup_set`: Embeddings for lookup set. The embeddings for the `annotations` set are included as examples
- `annotations`: Annotations to use for transfer. The expected format is one line per protein with 1st column: identifer, 2nd column: comma-separated list of annotated GO terms. The GOA [4] version from 2017, 2020, and 2022 with all Swiss-Prot sequences and only sequences with experimentally verified annotations are included as examples.
- `targets`: Embeddings for target proteins for which GO term predictions should be calculated. SeqVec, ProtBERT, and ProtT5 embeddings for the CAFA3 targets are included as examples.
- `onto`: Ontology for which predictions should be made `[all|bpo|mfo|cco]`
- `thresh`: Defines *k* (Number of neighbors to consider) or *d* (Distance threshold). Can be a comma-separated list of different values (all for the same modus)
- `modus`: If hits should be identified as the *k*-nearest neighbors (`num`) or by a distance threshold (`dist`)
- `output`: File prefix were output should be written to, will be extended by `_thresh_onto.txt`

For a given config-file, GO term prediction can be performed with the following command:

`python predict_go_embedding_inference.py config.txt`

## Performance Assessment
We show performance for the CAFA3 targets and 3 different versions of lookup sets (GOA2017, GOA2020, GOA2022) for SeqVec, ProtBert, and ProtT5 embeddings, respectively. 
Performance is measured using the Fmax score following the CAFA assessment.

| **Fmax**| | **BPO**|**MFO**|**CCO**|
|-|-|-|-|-|
||*SeqVec*|37±2%|50±3%|57±2%|
|**GOA2017**|*ProtBERT*|36±2%|49±3%|59±2%|
||*ProtT5*|38±2%|52±3%|59±2%|
||*SeqVec*|51±2%|61±3%|65±2%|
|**GOA2020**|*ProtBERT*|50±2%|59±2%|65±2%|
||*ProtT5*|52±2%|61±2%|67±2%|
||*SeqVec*|49±2%|59±2%|64±2%|
|**GOA2022**|*ProtBERT*|49±2%|59±2%|64±2%|
||*ProtT5*|51±2%|61±2%|66±2%|

While originally, goPredSim was developed and assessed using SeqVec embeddings, we recommend to use ProtT5 embeddings now which were not available yet at the point of development of goPredSim.
The improvement using those embeddings is only small, but consistent throughout all ontologies and datasets.

Also, while the performance of goPredSim does not improve for the CAFA3 targets using the GOA2022 lookup set, we still recommend using this set. It contains the most and most recent annotations. Apparently, no new information was gained regarding the CAFA3 targets between 2020 and 2022, but in general, we assume that goPredSim benefits from more annotations available for annotation transfer.

## Embeddings

Embeddings were calculated using the [bio_embeddings pipeline] [5].

The pre-computed embeddings (h5-files) for GOA2017, GOA2020, and GOA2022 (full and filtered with 100% sequence identity against the CAFA3 targets) can be downloaded from [ftp://rostlab.org/goPredSim](ftp://rostlab.org/goPredSim).

## Annotations
We provide the GOA annotations for Swiss-Prot sequences using
- all annotations from 2017
- all annotations from 2020
- all annotations from 2022
- only experimental annotations from 2017
- only experimental annotations from 2020
- only experimental annotations from 2022

in the `data/goa_annotations` folder.

## Requirements
goPredSim is written in Python3. In order to execute goPredSim, Python3 has to be installed locally. Additionally, the following Python packages have to be installed:

- numpy
- pathlib
- scikit-learn
- h5py

## Availability as web service
If you are interested in running only a few sequences, goPredSim is also available as a web service: https://embed.protein.properties/ or as part of PredictProtein [6]: https://predictprotein.org/

## Cite
If you are using this method and find it helpful, we would appreciate if you could cite the following publication:

Littmann, M., Heinzinger, M., Dallago, C. et al. Embeddings from deep learning transfer GO annotations beyond homology. Sci Rep 11, 1160 (2021). https://doi.org/10.1038/s41598-020-80786-0

## References
[1] Heinzinger M, Elnaggar A, Wang Y, Dallago C, Nechaev D, Matthes F, Rost B (2019). Modeling aspects of the language of life through transfer-learning protein sequences. BMC Bioinformatics, **20**:73.

[2] Elnaggar A, Heinzinger M, Dallago C, Rihawi G, Wang Y, Jones L, Gibbs T, Feher T, Angerer C, Steinegger, M, Bhowmik D, Rost B (2021). ProtTrans: Towards Cracking the Language of Lifes Code Through Self-Supervised Deep Learning and High Performance Computing. IEEE Transactions on Pattern Analysis and Machine Intelligence.

[3] Ashburner M, Ball CA, Blake JA, Botstein D, Butler H, Cherry JM, Davis AP, Dolinski K, Dwight SS, Eppig JT (2000). Gene ontology: tool for the unification of biology. Nature genetics, **25**(1):25-29.

[4] Camon E, Magrane M, Barrell D, Lee V, Dimmer E, Maslen J, Binns D, Harte N, Lopez R, Apweiler R (2004). The Gene Ontology Annotation (GOA) Database: sharing knowledge in Uniprot with Gene Ontology. Nucleic Acids Res, **32**(Database issue):D262-266.

[5] Dallago C, Schütze K, Heinzinger M, Olenyi T, Littmann M, Lu AX, Yang KK, Min S, Yoon S, Morton JT, Rost B (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, **1**, e113.

[6] Yachdav, G. et al. (2014). PredictProtein--an open resource for online prediction of protein structural and functional features. Nucleic Acids Res, **42**(Webserver issue):W337-43
