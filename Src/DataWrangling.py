import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import logging

def preprocess_data(file_path, output_path):
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Load the dataset
    df = pd.read_excel(file_path)

    # Handle missing values
    df.fillna(df.median(numeric_only=True), inplace=True)

    # One-Hot Encoding for 'Genre'
    if 'Genre' in df.columns:
        df = pd.get_dummies(df, columns=["Genre"], drop_first=True)
    
    # Set genre columns to zero for players who haven't listened to music
    genre_columns = [col for col in df.columns if col.startswith('Genre_')]
    if "Music Listened" in df.columns:
        df.loc[df["Music Listened"] == 0, genre_columns] = 0

    # Outlier Detection & Removal using IQR
    def remove_outliers(df, columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound, upper_bound = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df
    
    outlier_columns = ["Final Net Worth", "Kills", "Deaths", "Assists", "APM", "GPM", "XPM"]
    df = remove_outliers(df, outlier_columns)
    
    # Normalize continuous features, including Game Duration
    scaler = StandardScaler()
    continuous_features = ["Final Net Worth", "APM", "GPM", "XPM", "Game Duration"]
    df[continuous_features] = scaler.fit_transform(df[continuous_features])
    
    # Ensure categorical stats remain integers
    categorical_columns = ["Kills", "Deaths", "Assists", "WinOrLose"]
    df[categorical_columns] = df[categorical_columns].astype(int)
    
    # Balance Data for Fair Comparisons
    df_music = df[df["Music Listened"] == 1]
    df_no_music = df[df["Music Listened"] == 0]
    df_music_upsampled = resample(df_music, replace=True, n_samples=len(df_no_music), random_state=42)
    df = pd.concat([df_no_music, df_music_upsampled])
    
    # Save preprocessed dataset
    df.to_excel(output_path, index=False)
    
    logging.info(f'Preprocessing complete. Cleaned data saved to: {output_path}')
    return df

# Usage
input_file = "Data_with_music.xlsx"
output_file = "preprocessed_data.xlsx"
df_cleaned = preprocess_data(input_file, output_file)
