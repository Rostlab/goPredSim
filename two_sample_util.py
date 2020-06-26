import torch
import numpy as np


def pdist(sample_1, sample_2, norm=2, eps=1e-5):
    r"""Compute the matrix of all squared pairwise distances.
    Arguments
    ---------
    sample_1 : torch.Tensor or Variable
        The first sample, should be of shape ``(n_1, d)``.
    sample_2 : torch.Tensor or Variable
        The second sample, should be of shape ``(n_2, d)``.
    norm : float
        The l_p norm to be used.
    eps :
    Returns
    -------
    torch.Tensor or Variable
        Matrix of shape (n_1, n_2). The [i, j]-th entry is equal to
        ``|| sample_1[i, :] - sample_2[j, :] ||_p``."""
    n_1, n_2 = sample_1.size(0), sample_2.size(0)
    norm = float(norm)
    if norm == 2.:
        norms_1 = torch.sum(sample_1**2, dim=1, keepdim=True)
        norms_2 = torch.sum(sample_2**2, dim=1, keepdim=True)
        norms = (norms_1.expand(n_1, n_2) +
                 norms_2.transpose(0, 1).expand(n_1, n_2))
        distances_squared = norms - 2 * sample_1.mm(sample_2.t())
        return torch.sqrt(eps + torch.abs(distances_squared))
    else:
        dim = sample_1.size(1)
        expanded_1 = sample_1.unsqueeze(1).expand(n_1, n_2, dim)
        expanded_2 = sample_2.unsqueeze(0).expand(n_1, n_2, dim)
        differences = torch.abs(expanded_1 - expanded_2) ** norm
        inner = torch.sum(differences, dim=2, keepdim=False)
        return (eps + inner) ** (1. / norm)


def cosine_dist(sample_1, sample_2, eps=1e-8):

    sample_1 = torch.tensor(sample_1) if isinstance(sample_1, np.ndarray) else sample_1
    sample_2 = torch.tensor(sample_2) if isinstance(sample_2, np.ndarray) else sample_2

    n_1, n_2 = sample_1.norm(dim=1)[:, None], sample_2.norm(dim=1)[:, None]
    norms_1 = sample_1 / torch.max(n_1, eps * torch.ones_like(n_1))
    norms_2 = sample_2 / torch.max(n_2, eps * torch.ones_like(n_2))
    sim_mt = torch.mm(norms_1, norms_2.transpose(0, 1))
    dist_mt = torch.sub(1, sim_mt)
    dist_mt = torch.div(dist_mt, 2)

    return dist_mt
