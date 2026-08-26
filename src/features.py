import numpy as np
import warnings
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Descriptors import CalcMolDescriptors

def compute_rdkit_descriptors(smiles_list, nan_mask=None):
    """Returns (X array, column mask).
    Pass nan_mask from training call into test call
    so both have identical columns.
    """
    rows = []
    for smi in smiles_list:
        mol = MolFromSmiles(smi)
        if mol is None:
            print(f"Warning: bad SMILES skipped: {smi}")
            rows.append([np.nan] * 210)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                rows.append(list(CalcMolDescriptors(mol).values()))

    X = np.array(rows, dtype=float)

    if nan_mask is not None:
        return X[:, nan_mask], nan_mask
    
    valid_rows = ~np.isnan(X).all(axis=1)
    mask = ~np.isnan(X[valid_rows]).any(axis=0)
    return X[:, mask], mask


def compute_smited_embeddings(train_smiles, test_smiles,
                               model_type="SMI-TED"):
    """Returns (train_emb, test_emb) as numpy arrays."""
    import sys
    from src.config import PROJECT_ROOT, CFG
    sys.path.append(str(PROJECT_ROOT / CFG["external"]["fm4m_root"]))
    sys.path.append(str(PROJECT_ROOT / CFG["external"]["fm4m_dir"]))

    import fm4m
    import torch

    train_raw, test_raw = fm4m.get_representation(
        train_smiles, test_smiles, model_type, return_tensor=True
    )

    def to_numpy(t):
        if isinstance(t, torch.Tensor):
            return t.detach().cpu().numpy()
        return np.array([
            x.detach().cpu().numpy() if isinstance(x, torch.Tensor)
            else np.array(x) for x in t
        ])

    return to_numpy(train_raw), to_numpy(test_raw)