import numpy as np

from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score, matthews_corrcoef, confusion_matrix

from sklearn.inspection import permutation_importance

from tabulate import tabulate



def scores(y_true, y_pred):
    
    '''Produce dict with a selection of binary classification performance metrics'''
    
    roc_auc = roc_auc_score(y_true, y_pred)
    
    recall = recall_score(y_true, y_pred)
    
    cmx = confusion_matrix(y_true, y_pred)
    
    tnr = cmx[0][0]/(cmx[0][0] + cmx[0][1])
    
    precision = precision_score(y_true, y_pred)
    
    mcc = matthews_corrcoef(y_true, y_pred)
    
    npp = cmx[0][0]/(cmx[0][0] + cmx[1][0])
    
    pos_pred = cmx[0][1] + cmx[1][1]
    
    neg_pred = cmx[1][0] + cmx[0][0]
    
    scores = {'AUROC': roc_auc, 'Sensitivity': recall, 'Specificity': tnr, 'Precision': precision, 'MCC': mcc, 'Neg Predictive Power': npp, \
              'Predicted 1': pos_pred, 'Predicted 0': neg_pred}

    return scores




def permimp_ranking(model, X, y_true, scorer: str):
    
    '''Produce ranking of features by mean permutation importance from 5 repeats. 
    model is a fitted sklearn binary classifier; X is a pandas df; y_true can be any list of ground truth labels.
    See https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter for sklearn scorer names.'''
    
    permimp = permutation_importance(model, X, \
                       y_true, scoring=scorer, n_repeats=5, random_state=69)['importances_mean']
        
    permimp_dict = {}
    for i in range(len(permimp)):
        permimp_dict[i] = permimp[i]
    
    permimp_rankings = {}
    
    for feat_index in sorted(permimp_dict, key=lambda dict_key: permimp_dict[dict_key], reverse=True)[:10]:
        permimp_rankings[X.columns[feat_index]] = permimp_dict[feat_index]
        
    return permimp_rankings




def print_metrics_table(results, metric_keys, round_decimals=4, means=False):
    """Prints metrics in tabular format with mean values. Ensure each metric is available for each result.

    Args:
        results (dict): A dictionary containing a set of results.
        metric_keys (list): List of metrics to tabulate
        round_decimals (int, optional): Number of decimals to round to. Defaults to 4.
        means (Bool): Whether to add a final row with average metrics. Defaults to False
    """

    table_data = []

    # Create rows for each split
    for row_name, row_results in results.items():
        row = [row_name] + [round(row_results[metric], round_decimals) for metric in metric_keys]
        table_data.append(row)

    # Calculate and add a row for mean values

    if means==True:
        mean_values = [round(np.mean([results[row][metric] for row in results]), round_decimals) 
                   for metric in metric_keys]
        table_data.append(["Mean"] + mean_values)

    # Print the table
    headers = ["Result ID"] + metric_keys
    print(tabulate(table_data, headers, tablefmt="fancy_grid", floatfmt=f".{round_decimals}f"))
