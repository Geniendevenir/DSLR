import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import seaborn as sns


def get_house_std(data: pd.DataFrame):

	#Get the name of the features that contains numerical data
	numerical_features = data.select_dtypes(include=["number"]).columns

	#Group the data per house, then keep only numerical features (class) and calculate the std per class
	house_std = data.groupby('Hogwarts House')[numerical_features].agg(lambda x: np.std(x, ddof=1))

	print(house_std)

	return house_std

def show_score_distribution(df: pd.DataFrame):

	courses = df.select_dtypes(include=["number"]).columns

	n_courses = len(courses)

	rows = (n_courses // 4) + 1

	_, axes = plt.subplots(rows, 4, figsize=(20, rows * 4))
	axes = axes.flatten()


	for i, course in enumerate(courses):

		show_legend = True if i == 0 else False

		sns.histplot(
			data=df,
			x=course,
			hue="Hogwarts House",
			kde=True,
			element="step",
			ax=axes[i],
			legend=show_legend,
			palette='Set1'
		)
		axes[i].set_title(f'Distribution of {course}')


	for j in range(i + 1, len(axes)):
		axes[j].set_visible(False)

	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	plt.savefig('histogram.png')
	print("Histogram saved as histogram.png")


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
	show_score_distribution(data)
if __name__ == "__main__":
	main()