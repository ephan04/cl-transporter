from sklearn.metrics import confusion_matrix 
def compute_ccr (y_true, y_prediction): 
    """
    Calculate correct classification rate: a metric to evaluate how accurately a predictive model assigns catergory 
    CCR = (sensitivity + specificity) / 2, where
        sensitivity = true positive / (true positive + false negative)
        specificity = true negative / (true negative + false positive)
        tp = 1 in both test set and prediction 
        fp = 0 in test set and 1 in prediction 
    """
    tn,fp,fn,tp = confusion_matrix(y_true, y_prediction,labels=[0,1]).ravel()
    sensitivity = tp/ (tp+fn)
    specificity = tn/(tn+fp)
    ccr = (sensitivity + specificity) / 2 
    return ccr

    
