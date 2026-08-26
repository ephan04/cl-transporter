from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.base import clone
from src.metrics import compute_ccr
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import make_scorer


def build_rf(n_estimator=100, max_depth=10, seed=42):
    """Random Forest classifier."""
    return RandomForestClassifier(
        n_estimators=n_estimator,
        max_depth=max_depth,
        random_state=seed
    )

def build_nn(seed=42):
    """Neural Network with standard scaling."""
    return make_pipeline(
        StandardScaler(),
        MLPClassifier(max_iter=1000, random_state=seed))

def run_experiment (subsets, test_X,test_y, classifier, activity_col, feature_fn):
    """Run the 19-split training loop for one classifier (RF or NN) and one feature set (either RDKit or SMI-TED).
    Return a list of 19 CCR values """
    ccr_list=[]

    for i, subset in enumerate (subsets):

        #Get feature for this subset
        train_X = feature_fn(subset) 
        train_y = subset[activity_col].tolist()

        #Use clone to create indepedent training for each split 
        clf = clone(classifier)
        clf.fit(train_X, train_y)

        y_pred = clf.predict(test_X)
        ccr= compute_ccr (test_y, y_pred)
        ccr_list.append(ccr)
    return ccr_list


def run_crossval(subsets, classifier, activity_col, feature_fn, n_folds=5, seed=42):
    """
    Runs 5-fold cross-validation on each undersampling subset.
    This replicates the evaluation shown in Figure 3 of the paper.
    
    Returns a list of CCR values — one per fold per subset.
    So with 19 subsets × 5 folds = up to 95 CCR values total.
    """
    from src.metrics import compute_ccr
    
    ccr_list = []
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=seed)

    for i, subset in enumerate(subsets):
        X = feature_fn(subset)
        y = subset[activity_col].tolist()

        for fold_train_idx, fold_val_idx in skf.split(X, y):
            X_train_fold = X[fold_train_idx]
            y_train_fold = [y[j] for j in fold_train_idx]
            X_val_fold   = X[fold_val_idx]
            y_val_fold   = [y[j] for j in fold_val_idx]

            clf = clone(classifier)
            clf.fit(X_train_fold, y_train_fold)

            y_pred = clf.predict(X_val_fold)
            ccr = compute_ccr(y_val_fold, y_pred)
            ccr_list.append(ccr)

    return ccr_list