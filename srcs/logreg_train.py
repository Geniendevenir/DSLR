import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

from collections.abc import Sequence

features_to_drop = [
	"Arithmancy",
	"Potions",
	"Care of Magical Creatures"
]

class Preprocessor:
	def __init__(self, features_to_drop: Sequence[str]):
		self.features_to_drop = features_to_drop

	def clean(self, df: pd.DataFrame):

		# 1. Save the labels
		labels = df['Hogwarts House']

		# 2. Keep only numerical features
		df_num = df.select_dtypes(include=["number"])

		# 3. Keep only selected features (see pair plot)
		df_select = df_num.drop(columns=features_to_drop)

		# 4. Concatenate back the numerical features with the labels
		df_cleaned = pd.concat([df_select, labels], axis=1)

		return df_cleaned

	# Calculate the mean of training features
	def fit(self, train: pd.DataFrame):
		self.train_mean = train.select_dtypes(include=["number"]).mean()

	# Apply the mean for the given set (train, test or validation)
	def transform(self, df: pd.DataFrame):
		df = df.fillna(self.train_mean)

class DataLoader:
	def __init__(self, df: pd.DataFrame, batch_size: int, shuffle: bool):
		self.df = df
		self.batch_size = batch_size
		self.shuffle = shuffle

	@staticmethod
	def load(path: str) -> pd.DataFrame:
		raw_df = pd.read_csv(path)	

		return raw_df

	def normalization(self):
		return

def split_dataset(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42) -> tuple[pd.DataFrame]:
	"""
	Split a Dataset into three sets: training set, testing set and validation set.
	Returns: A tuple with the three sets as pd.Dataframe
	"""

	if sum([train_ratio, test_ratio, val_ratio]) != 1:
		raise ValueError("Splitting Ratio don't add up to one")

	# Shuffle dataset using the seed for reproductibility
	df_shuffled = df.sample(frac=1, random_state=seed).reset_index(drop=True)

	# Calculate split indices
	train_end = int(len(df_shuffled) * train_ratio)
	val_end = train_end + int(len(df_shuffled) * val_ratio)

	# Slice sets
	df_train = df_shuffled.iloc[:train_end]	
	df_val = df_shuffled.iloc[train_end:val_end]	
	df_test = df_shuffled.iloc[val_end:]	

	return (df_train, df_val, df_test)

	


def main():
	if len(sys.argv) != 2:
		raise ValueError("Please provide the dataset path to train the model")

	data_path = sys.argv[1]

	if data_path != "data/dataset_train.csv":
		raise ValueError("You should use the 'dataset_train.csv' to train the model")
	

	print("STEP 1: Loading Data")
	raw_data = DataLoader.load(data_path)

	print("STEP 2: Clean Data (Keep numerical features and labels")
	preprocessor = Preprocessor(features_to_drop)
	cleaned_data = preprocessor.clean(raw_data)

	print("STEP 3: Splitting Dataset (X_train, X_val, Y)")
	train_set, val_set, test_set = split_dataset(cleaned_data)

	print("STEP 4: Calculate the mean of X_train features")
	preprocessor.fit(train_set)

	print("STEP 5: Fill NaN Values of all sets by X_train mean")
	preprocessor.transform(train_set)
	preprocessor.transform(val_set)
	preprocessor.transform(test_set)


	print(test_set.describe())
	print(val_set.describe())
	print(test_set.describe())

if __name__ == "__main__":
	main()