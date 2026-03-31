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
		# 1. Keep only numerical features

		# 1. Keep only selected features (see pair plot)
		df = df.drop(columns=features_to_drop)

		# 2. Imptation: Replace NaN values by the mean of the 

	# Calculate the mean of training features
	def fit(self, train: pd.DataFrame):
		return

	# Apply the mean for the given set (test or validation)
	def transform(self, df: pd.DataFrame):
		return

class DataLoader:
	def __init__(self, df: pd.DataFrame, batch_size: int, shuffle: bool):
		self.df = df
		self.batch_size = batch_size
		self.shuffle = shuffle

	def load(self, path: str) -> pd.DataFrame:
		raw_df = pd.read_csv(path)	

		return raw_df

	def normalization(self):
		return

def split_dataset(df: pd.DataFrame, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42) -> tuple[pd.DataFrame]:
	"""
	Split a Dataset into three sets: training set, testing set and validation set.
	Returns: A tuple with the three sets as pd.Dataframe
	"""

	if sum(train_ratio, test_ratio, val_ratio) != 1:
		raise ValueError("Splitting Ratio don't add up to one")

	# Shuffle dataset using the seed for reproductibility
	df_shuffled = df.sample(frac=1, random_state=seed).reset_index(drop=True)

	# Calculate split indices
	train_end = int(len(df_shuffled) * train_ratio)
	val_end = train_end + int(len(df_shuffled) * val_ratio)
	test_start = train_end + val_end

	# Slice sets
	df_train = df.iloc[:train_end]	
	df_val = df.iloc[train_end:val_end]	
	df_test = df.iloc[test_start:]	

	return (df_train, df_val, df_test)

	


def main():
	if len(sys.argv) != 2:
		raise ValueError("Please provide the dataset path to train the model")

	data_path = sys.argv[1]

	if data_path != "data/dataset_train.csv":
		raise ValueError("You should use the 'dataset_train.csv' to train the model")
	

	raw_data = DataLoader.load(data_path)
	print("STEP 1: Data has been loaded succesfully")


if __name__ == "__main__":
	main()