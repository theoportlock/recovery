#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imblearn.over_sampling import SMOTE
from itertools import permutations
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score, mean_absolute_error, r2_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import argparse
import numpy as np
import os
import pandas as pd
import shap
import sys

def load(subject):
    if os.path.isfile(subject):
        return pd.read_csv(subject, sep='\t', index_col=0)
    return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def load_predictor(predictor_file, target_column):
    if os.path.isfile(predictor_file):
        df = pd.read_csv(predictor_file, sep='\t', index_col=0)
    elif os.path.isfile(f'../results/{predictor_file}.tsv'):
        df = pd.read_csv(f'../results/{predictor_file}.tsv', sep='\t', index_col=0)
    else:
        raise FileNotFoundError(f"Predictor file {predictor_file} not found.")

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in {predictor_file}.")

    return df[target_column]

def save(df, subject, index=True):
    output_path = f'../results/{subject}.tsv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep='\t', index=index)

def predict(df, y, analysis, subject, shap_val=False, shap_interact=False, n_iter=30):
    outputs = []
    aucrocs = []
    fpr_tpr = []
    maes = []
    r2s = []
    meanabsshaps = pd.DataFrame()
    shap_interacts = pd.DataFrame(index=pd.MultiIndex.from_tuples(permutations(df.columns, 2)))

    random_state = 1
    for random_state in range(n_iter):
        if analysis.lower() == 'classifier':
            model = RandomForestClassifier(
                n_jobs=-1, random_state=random_state,
                bootstrap=False, max_depth=None,
                min_samples_leaf=8, min_samples_split=20, n_estimators=400
            )
        elif analysis.lower() == 'regressor':
            model = RandomForestRegressor(
                n_jobs=-1, random_state=random_state
            )
        else:
            raise ValueError("Invalid analysis type. Choose 'classifier' or 'regressor'.")

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)

        stratify = y if analysis.lower() == 'classifier' else None
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, random_state=random_state, stratify=stratify)

        if analysis.lower() == 'classifier':
            smoter = SMOTE(random_state=random_state)
            X_train, y_train = smoter.fit_resample(X_train, y_train)

        model.fit(X_train, y_train)

        if analysis.lower() == 'classifier':
            y_prob = model.predict_proba(X_test)[:, 1]
            aucrocs.append(roc_auc_score(y_test, y_prob))
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            aucrocdata = pd.DataFrame({
                'fpr': fpr,
                'tpr': tpr,
                'random_state': random_state
            })
            fpr_tpr.append(aucrocdata)

        if analysis.lower() == 'regressor':
            y_pred = model.predict(X_test)
            maes.append(mean_absolute_error(y_test, y_pred))
            r2s.append(r2_score(y_test, y_pred))

        if shap_val:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer(X_scaled)
            meanabsshaps[random_state] = pd.Series(
                np.abs(shap_values.values).mean(axis=0),
                index=df.columns
            )

        if shap_interact:
            explainer = shap.TreeExplainer(model)
            inter_shaps_values = explainer.shap_interaction_values(X_scaled)
            sum_shap_interacts = pd.DataFrame(
                data=inter_shaps_values.sum(axis=0),
                columns=df.columns,
                index=df.columns
            )
            shap_interacts[random_state] = sum_shap_interacts.stack()

    # Save outputs
    if analysis.lower() == 'classifier':
        save(pd.Series(aucrocs).to_frame(f'{subject}'), f'{subject}aucrocs', index=False)
        save(pd.concat(fpr_tpr), f'{subject}fpr_tpr')
    else:
        save(pd.Series(maes).to_frame(f'{subject}_mae'), f'{subject}maes', index=False)
        save(pd.Series(r2s).to_frame(f'{subject}_r2'), f'{subject}r2s', index=False)

    if shap_val:
        save(meanabsshaps, f'{subject}meanabsshaps')
    if shap_interact:
        save(shap_interacts, f'{subject}shap_interacts')

def parse_args(args):
    parser = argparse.ArgumentParser(
       prog='predict.py',
       description='Random Forest Classifier/Regressor with options'
    )
    parser.add_argument('analysis', type=str, help='Regressor or Classifier')
    parser.add_argument('subject', type=str, help='Data name or full filepath')
    parser.add_argument('--target', required=True, type=str, help='Name of the column to predict')
    parser.add_argument('--predictor_file', type=str, default=None, help='Optional separate predictor file (default: subject)')
    parser.add_argument('-n','--n_iter', type=int, help='Number of iterations for bootstrapping', default=10)
    parser.add_argument('--shap_val', action='store_true', help='SHAP interpreted output')
    parser.add_argument('--shap_interact', action='store_true', help='SHAP interaction interpreted output')
    return parser.parse_args(args)

arguments = sys.argv[1:]
args = parse_args(arguments)

# Identify subject
if os.path.isfile(args.subject):
    subject = Path(args.subject).stem
else:
    subject = args.subject

df = load(args.subject)

# Determine y (target variable)
if args.predictor_file:
    y = load_predictor(args.predictor_file, args.target)
else:
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in {args.subject}.")
    y = df.pop(args.target)

# 🔥 Align samples
common_samples = df.index.intersection(y.index)
df = df.loc[common_samples]
y = y.loc[common_samples]

print(f"After alignment: {df.shape[0]} samples")

analysis = args.analysis
shap_val = args.shap_val
shap_interact = args.shap_interact
n_iter = args.n_iter

predict(df, y, analysis, subject, shap_val=shap_val, shap_interact=shap_interact, n_iter=n_iter)

