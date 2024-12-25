import pandas as pd

DATASET_PATH = "datasets/Songs.csv"

def load_song_dataset():
    """
    Loads the music dataset from songs.csv.
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        print(f"\nLoaded {len(df)} songs from the dataset.")
        return df
    except FileNotFoundError:
        print("\nNo dataset found. Start by adding songs.")
        return pd.DataFrame()  # Return an empty DataFrame


from sklearn.preprocessing import LabelEncoder



def load_and_prepare_data():
    """
    Loads the music dataset and prepares the features for the model.
    Ensures that 'User-Rating' is numeric before performing operations.
    """
    df = pd.read_csv(DATASET_PATH)

    # Debug: Print initial dataset shape and first few rows
    print(f"Initial dataset shape: {df.shape}")
    print(df.head())

    # Clean 'User-Rating' by removing '/10' and converting to numeric
    df['User-Rating'] = df['User-Rating'].str.replace(r'/10', '', regex=True)  # Remove '/10'
    df['User-Rating'] = pd.to_numeric(df['User-Rating'], errors='coerce')  # Convert to numeric, force errors to NaN

    # Debug: Check after cleaning 'User-Rating'
    print(f"After cleaning 'User-Rating', dataset shape: {df.shape}")
    print(df.head())

    # Drop rows where 'User-Rating' is NaN after conversion
    df = df.dropna(subset=['User-Rating'])

    # Debug: Check after dropping NaN values
    print(f"After dropping NaN values, dataset shape: {df.shape}")
    print(df.head())

    # Encode 'Genre' using LabelEncoder
    le = LabelEncoder()
    df['Genre_encoded'] = le.fit_transform(df['Genre'])

    # Normalize 'User-Rating'
    df['User-Rating_normalized'] = (df['User-Rating'] - df['User-Rating'].min()) / (df['User-Rating'].max() - df['User-Rating'].min())

    # Debug: Final dataset check
    print(f"Final dataset shape: {df.shape}")
    print(df.head())

    return df, le



