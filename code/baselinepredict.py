#!/usr/bin/env python

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def classifier100(df, shapval=False, shapinteract=False):
    aucrocs = []
    meanabsshaps = pd.DataFrame()
    mean_shap_interacts = pd.DataFrame(index=df.columns)
    random_state = 1
    for random_state in range(100):
        model = RandomForestClassifier(n_jobs=-1, random_state=random_state)
        X, y = df, df.index
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state, stratify=y)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        aucrocs.append(roc_auc_score(y_test, y_prob))
    return aucrocs

output[name] = classifier100(tdf)[0]


