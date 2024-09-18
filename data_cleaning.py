import pandas as pd

def skip_irrelevant_rows(df):
    """
    Remove irrelevant rows like timestamps and URLs.
    """
    # Assuming 'Sl' column is supposed to be numeric; remove rows where 'Sl' is not a number
    irrelevant_row_condition = df['Sl'].apply(lambda x: pd.to_numeric(x, errors='coerce')).isna()
    df_cleaned = df[~irrelevant_row_condition]
    return df_cleaned

def clean_data(df):
    """
    Clean the dataset by removing unnecessary rows, converting the 'month' field to datetime, 
    and handling mixed types.
    """
    # Ensure column names are standardized
    df.columns = df.columns.str.strip().str.lower()

    # Remove irrelevant rows
    df = skip_irrelevant_rows(df)

    # Convert columns to appropriate types
    df['month'] = pd.to_datetime(df['month'], errors='coerce')

    numeric_columns = [
        'sales', 'qty', 'strategy1', 'strategy2', 'strategy3', 
        'salesvisit1', 'salesvisit2', 'salesvisit3', 'salesvisit4', 'salesvisit5'
    ]

    # Only convert columns that exist in the DataFrame
    existing_numeric_columns = [col for col in numeric_columns if col in df.columns]
    df[existing_numeric_columns] = df[existing_numeric_columns].apply(pd.to_numeric, errors='coerce')

    if 'accid' in df.columns:
        df['accid'] = df['accid'].astype(str)
    
    # Drop rows where 'month' could not be converted to datetime
    df = df.dropna(subset=['month'])

    return df
