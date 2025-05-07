import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
import shap
import logging

def feature_engineering(file_path, output_path):
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Load the dataset
    df = pd.read_excel(file_path)

    # Feature Engineering

    # Weighted metric for overall performance
    df['Performance Score'] = ((df['Kills'] * 0.8) + (df['Assists'] * 1.2) - 
                               (df['Deaths'] * 1.5) + (df['GPM'] / 3) + 
                               (df['XPM'] / 10) + (df['WinOrLose'] * 5))


    # Success rate in crucial fights
    df['Clutch_Factor'] = (df['Kills'] * 0.8 + df['Assists'] * 1.2) / (df['Deaths'] * 1.5 + 1)

    # % of time spent in fights vs. farming
    df['Engagement_Level'] = (df['Kills'] * 0.8 + df['Assists'] * 1.3)

    # Frustration during match
    df['Tilt_Factor'] = (df['Kills'] * 0.8 + df['Assists'] * 1.2 - df['Deaths'] * 1.5)


    # Convert categorical columns to numeric if necessary
    df = pd.get_dummies(df, drop_first=True)

    # Define target variable
    y = df['Performance Score']

    # Select only engineered features for X
    engineered_features = [
        'Clutch_Factor','Engagement_Level', 'Tilt_Factor'
    ]
    X = df[engineered_features]

    # Mutual Information
    mi_scores = mutual_info_regression(X, y, random_state=42)
    mi_scores = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
    selected_features_mi = mi_scores.head(10).index.tolist()

    # Permutation Feature Importance
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    perm_importance = permutation_importance(model, X, y, n_repeats=10, random_state=42)
    perm_scores = pd.Series(perm_importance.importances_mean, index=X.columns).sort_values(ascending=False)
    selected_features_perm = perm_scores.head(10).index.tolist()

    # SHAP Feature Importance
    explainer = shap.Explainer(model)
    shap_values = explainer(X)
    shap_importance = pd.Series(np.abs(shap_values.values).mean(axis=0), index=X.columns).sort_values(ascending=False)
    selected_features_shap = shap_importance.head(10).index.tolist()

    # Combine selected features
    selected_features = set(selected_features_mi) | set(selected_features_perm) | set(selected_features_shap)

    # Keep only selected features
    final_df = df[list(selected_features) + ['Performance Score']]

    # Sort columns alphabetically
    final_df = final_df.reindex(sorted(final_df.columns), axis=1)

    # Save the final dataset with selected features in alphabetical order
    final_df.to_excel(output_path, index=False)
    logging.info(f"Feature Engineering Complete. Data saved to: {output_path}")

    return final_df

# Usage
input_file = "preprocessed_data.xlsx"
output_file = "selected_features.xlsx"
df_final = feature_engineering(input_file, output_file)