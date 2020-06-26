import numpy as np


def get_dataset(npz_path, use_cath=True):
    raw_data_path = npz_path.parent / npz_path.name.replace('.npz', '.npy')
    ids_path = npz_path.parent / npz_path.name.replace('.npz', '_ids.txt')

    # Load raw data from two seperate files if already created
    # IDs are stored as txt and embeddings are stored as npz (uncompressed)
    # Row-Indices in .npz correspond to line number in IDs file to keep track of ID-Embedding pairs
    if raw_data_path.is_file() and ids_path.is_file():
        raw_data = np.load(raw_data_path)
        with open(ids_path, 'r') as id_f:
            ids = [line.strip() for line in id_f]
        dataset = {seq_id: np.expand_dims(raw_data[idx], axis=0)
                   for idx, seq_id in enumerate(ids)}

    # Otherwise, if only npy file (compressed dictionary) exists:
    # Load dictionary, split Key/Value pairs and write Keys as txt and
    # concatenated embeddings as npz
    else:
        dataset = dict(np.load(npz_path, mmap_mode='r'))
        ids, raw_data = zip(*dataset.items())

        _write_files(ids_path, raw_data_path, ids, raw_data, use_cath)
        dataset = {seq_id: np.expand_dims(embd, axis=0)
                   for seq_id, embd in dataset.items()}

    return dataset


def get_dataset_uncompressed(npy_file, id_file):
    raw_data = np.load(npy_file)
    with open(id_file, 'r') as read_in:
        ids = [line.strip() for line in read_in]

    dataset = {seq_id: np.expand_dims(raw_data[idx], axis=0)
               for idx, seq_id in enumerate(ids)}

    return dataset


def write_dataset_speedup(path, data, use_cath=False):
    ids, raw_data = zip(*data.items())

    raw_data_path = path.parent / path.name.replace('.npz', '.npy')
    ids_path = path.parent / path.name.replace('.npz', '_ids.txt')

    _write_files(ids_path, raw_data_path, ids, raw_data, use_cath)


def _write_files(ids_path, raw_data_path, ids, raw_data, use_cath=False):

    with open(ids_path, 'w+') as id_f:
        for seq_id in ids:
            if use_cath:
                seq_id = seq_id.split('|')[2].split('/')[0]
            id_f.write(seq_id + '\n')
    np.save(raw_data_path, raw_data)
