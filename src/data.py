#load data and do undersampling
import pandas as pd
import numpy as np

def load_data (train_path, test_path): 
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def undersampling (train_df, activity_col,n_splits=19, seed=42):
    active = train_df[train_df[activity_col]==1]
    inactive = train_df[train_df[activity_col]==0]
    inactive_shuffle = inactive.sample(frac=1, random_state=seed)

    chunks =[]
    for c in np.array_split(inactive_shuffle, n_splits):
        chunks.append(pd.DataFrame(c))

    subsets = []
    for chunk in chunks: 
        combined = pd.concat([active, chunk], ignore_index=True)
        combined = combined.sample(frac=1, random_state=seed)         
        subsets.append(combined.reset_index(drop=True))      
    return subsets



    


