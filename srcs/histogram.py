import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

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

if __name__ == "__main__":