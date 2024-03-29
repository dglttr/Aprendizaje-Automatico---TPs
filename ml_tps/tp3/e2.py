# Trabajo Practico 3 - Ejercicio 2
import datetime
import pandas as pd
import numpy as np
import os
from sklearn import svm

from ml_tps.utils.hyperparameter_tuning import test_svm_configurations
from ml_tps.utils.evaluation import getConfusionMatrix, computeAccuracy
from ml_tps.utils.data_processing import divide_in_training_test_datasets, scale_dataset, separate_dataset_objective_data

dir_path = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FILEPATH = f"{dir_path}/../tp3/data/acath.xls"
DEFAULT_OBJECTIVE = "sigdz"
DEFAULT_TRAIN_PCTG = 0.6
DEFAULT_CV_PCTG = 0.2


def main():
    # a)  Divide dataset randomly into training and evaluation set
    dataset = pd.read_excel(DEFAULT_FILEPATH)
    dataset = dataset.dropna()
    dataset = dataset.drop("tvdlm", axis=1)   # Drop tvdlm columns which does not add information
    dataset_scaled = scale_dataset(dataset=dataset, objective=DEFAULT_OBJECTIVE, scaling_type="minmax")

    train, testing_sets = divide_in_training_test_datasets(dataset_scaled, train_pctg=DEFAULT_TRAIN_PCTG)
    cv_set, test = divide_in_training_test_datasets(testing_sets, train_pctg=DEFAULT_CV_PCTG/(1-DEFAULT_TRAIN_PCTG))

    X_train, y_train = separate_dataset_objective_data(train, DEFAULT_OBJECTIVE)
    X_cv_set, y_cv_set = separate_dataset_objective_data(cv_set, DEFAULT_OBJECTIVE)
    X_test, y_test = separate_dataset_objective_data(test, DEFAULT_OBJECTIVE)

    # b)  Classify categorical variable "sigdz" using default SVC SVM
    words_then = datetime.datetime.now()
    c_value1 = 1
    kernel1 = "rbf"
    clf1 = svm.SVC(kernel=kernel1, gamma='scale', C=c_value1)      # using default parameters, written down for illustrative purposes
    clf1.fit(X_train, y_train)

    predictions_cv1 = pd.Series(clf1.predict(X_cv_set).T)
    confusion_matrix = getConfusionMatrix(predictions_cv1, y_cv_set)
    predictions_train1 = pd.Series(clf1.predict(X_train))
    accuracy_train1 = computeAccuracy(predictions_train1, y_train)

    predictions_cv1 = pd.Series(clf1.predict(X_cv_set))
    accuracy_cv1 = computeAccuracy(predictions_cv1, y_cv_set)

    data_default_svm = pd.DataFrame(columns=["Kernel", "C value", "Training set accuracy", "CV set accuracy"])
    data_default_svm.loc[0] = [kernel1, c_value1, accuracy_train1, accuracy_cv1]

    words_now = datetime.datetime.now()
    print("Runtime Default SVM fitting and testing: ", divmod((words_now - words_then).total_seconds(), 60), "\n")

    # c)  Evaluate different values for C and different nuclei to find best performing classifier
    kernels = ["rbf", "poly", "linear", "sigmoid"]
    c_values = list(np.logspace(-3, 2, 6))
    svm_values, best_svm = test_svm_configurations(kernels, c_values, X_train, y_train, X_cv_set, y_cv_set)

    time_now = datetime.datetime.now()
    print("\n\nRuntime parameter and kernel testing: ", divmod((time_now - words_now).total_seconds(), 60), "\n")

    # Calculate real performance on test set
    best_svm.fit(X_train, y_train)
    predictions_best_clf = pd.Series(best_svm.predict(X_test))
    winner_test_accuracy = computeAccuracy(predictions_best_clf, y_test)

    a = 1


if __name__ == '__main__':
    main()
