import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
import seaborn as sns


def show_feature_similarity(df: pd.DataFrame):

	# Get the correlation matrix
	corr_matrix = df.select_dtypes(include=["number"]).corr()

	# Mask the upper triangle (diagonal of 1): Ignore comparaison between 2 same features
	mask = np.triu(np.ones(corr_matrix.shape), k=0).astype(bool)
	reduced_matrix = corr_matrix.where(~mask)

	most_similar_feature = reduced_matrix.abs().unstack().idxmax()
	correlation_score = reduced_matrix.abs().unstack().max()
	
	print(f"The two most similar features are: {most_similar_feature}")
	print(f"Correlation: {correlation_score:.4f}")

	feat1, feat2 = most_similar_feature

	plt.figure(figsize=(10, 7))

	sns.scatterplot(
		data=df,
		x=feat1,
		y=feat2,
		hue="Hogwarts House",
		alpha=0.6,
		palette='Set1'
	)

	plt.title(f"Scatter Plot: {feat1}, vs {feat2}")
	plt.xlabel(feat1)
	plt.ylabel(feat2)

	plt.savefig('scatter_plot.png', bbox_inches='tight')
	print("Created scatter_plot.png")

def get_data():
	if len(sys.argv) != 2:
		print("Usage: python script.py <path_to_dataset>")
		sys.exit(1)
	
	data_path = sys.argv[1]
	try:
		data = pd.read_csv(data_path, index_col=0)
		return data

	except FileNotFoundError:
		raise FileNotFoundError(f"The file at path: {data_path} was not found")

	except pd.errors.EmptyDataError:
		raise pd.errors.EmptyDataError(f"The file at path: {data_path} is empty")

	except pd.errors.ParserError:
		raise pd.errors.ParserError(f"The file at path: {data_path} is not a valid CSV")

	except Exception as e:
		raise RuntimeError(f"An unexpected error occured while reading for the data: {e}")


def main():
	data = get_data()
	show_feature_similarity(data)

if __name__ == "__main__":
	main()