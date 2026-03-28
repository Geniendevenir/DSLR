import numpy as np
import pandas as pd
import sys


class TinyStatistician:
	def __init__(self):
		pass

	def mean(self, x=[]):
		if x is None or not x:
			return None

		result = 0
		for elem in x:
			result += elem
		result /= len(x)
		return result

	def median(self, x):
		if x is None or not x:
			return None
		x.sort()
		if len(x) % 2 == 0:
			i = int((len(x) + 1) / 2)
			return float(x[i])
		else:
			i = int(len(x) / 2)
			return float(x[i])

	def quartile(self, x):
		if x is None or not x:
			return None
		x.sort()
		if len(x) % 2 == 0:
			firstQ = self.median(x[:int(len(x) / 2)])
			thirdQ = self.median(x[int(len(x) / 2):])
		else:
			firstQ = self.median(x[:int((len(x) - 1) / 2)])
			thirdQ = self.median(x[int((len(x) - 1) / 2):])
		return [firstQ, thirdQ]

	def var(self, x):
		if x is None or not x:
			return None

		m = self.mean(x)
		result = []

		for elem in x:
			result.append(pow(elem - m, 2))
		return self.mean(result)

	def std(self, x):
		if x is None or not x:
			return None

		return pow(self.var(x), 0.5)


def get_data():
	if len(sys.argv) != 2:
		print("Usage: python script.py <path_to_dataset>")
		sys.exit(1)
	
	data_path = sys.argv[1]
	try:
		data = pd.read_csv(data_path)
		return data

	except FileNotFoundError:
		raise FileNotFoundError(f"The file at path: {data_path} was not found")

	except pd.errors.EmptyDataError:
		raise pd.errors.EmptyDataError(f"The file at path: {data_path} is empty")

	except pd.errors.ParserError:
		raise pd.errors.ParserError(f"The file at path: {data_path} is not a valid CSV")

	except Exception as e:
		raise RuntimeError(f"An unexpected error occured while reading for the data: {e}")

def data_analysis():
	data = get_data()

	#Get all Numerical Features
	numerical_features = data.select_dtypes(include=["number"])

	#Geat features Name
	features = numerical_features.columns.tolist()
	metrics = {
		"Count",
		"Mean",
		"Std",
		"Min",
		"25%",
		"50%",
		"75%",
		"Max"
	}

	#
	tstat = TinyStatistician()

	#Print Data
	print(f"features






if __name__ == "__main__":
	data_analysis()