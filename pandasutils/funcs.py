import pandas as pd

def insert_column(df, col_name, col_data, position):

    '''Insert array-like data as a Series into an existing DataFrame.
    Returns amended DF.'''

    # Ensure the column data is of the correct length
    if len(col_data) != len(df):
        raise ValueError("Length of column data must match the number of rows in the DataFrame.")

    # Create a new DataFrame with the new column
    new_col_df = pd.DataFrame({col_name: col_data})

    # Split the original DataFrame at the desired position
    left_df = df.iloc[:, :position].reset_index(drop=True)
    right_df = df.iloc[:, position:].reset_index(drop=True)

    # Concatenate the three DataFrames to create the final result
    result_df = pd.concat([left_df, new_col_df, right_df], axis=1)

    return result_df
