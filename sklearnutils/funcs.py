from sklearn.model_selection import train_test_split

def split_datasets(df, col_name, test_size=0.2):
  """
  Splits a DataFrame into training and test sets, stratified by a specified column.

  Args:
    df: The input DataFrame.
    col_name: The name of the column used to identify different datasets.
    test_size: The proportion of data to include in the test set (default: 0.2).

  Returns:
    A tuple containing two DataFrames: (train_df, test_df).
  """

  train_df = pd.DataFrame()
  test_df = pd.DataFrame()

  for dataset_id in df[col_name].unique():
    dataset = df.loc[df[col_name] == dataset_id]
    
    # Split the dataset into train and test sets
    train_dataset, test_dataset = train_test_split(
        dataset, test_size=test_size, stratify=dataset[col_name], random_state=68
    )

    # Append to the overall train and test DataFrames
    train_df = pd.concat([train_df, train_dataset])
    test_df = pd.concat([test_df, test_dataset])

  return train_df, test_df
