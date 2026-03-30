import numpy as np
import pandas as pd
import sys


#Set precision to match describe() output format
pd.options.display.float_format = '{:,.6f}'.format

class TinyStatistician:
	def __init__(self):
		pass

	#Return the number of elements in a column Vector
	def count(self, x_col: np.ndarray) -> float:
		if x_col.size == 0:
			return None
		return x_col.shape[0]

	#Return the mean of a column Vector
	def mean(self, x_col: np.ndarray) -> float:
		if x_col.size == 0:
			return None

		sum_x_col = np.sum(x_col)

		return sum_x_col / x_col.shape[0]

	#Return the variance (Sample Variance) of a column vector
	def var(self, x_col: np.ndarray) -> float:
		if x_col.size <= 1:
			return None

		m = self.mean(x_col)
		x_raised = (x_col - m) ** 2

		return float(np.sum(x_raised) / (x_col.size - 1))

	#Return the standard Deviation of a column vector
	def std(self, x_col: np.ndarray) -> float:
		if x_col.size == 0:
			return None

		return pow(self.var(x_col), 0.5)

	#Return the smallest value of a column vector
	def min(self, x_col: np.ndarray) -> float:
		if x_col.size == 0:
			return None

		smallest = x_col[0]
		for nbr in x_col:
			if smallest > nbr:
				smallest = nbr

		return smallest

	#Return the biggest value of a column vector
	def max(self, x_col: np.ndarray) -> float:
		if x_col.size == 0:
			return None

		biggest = x_col[0]
		for nbr in x_col:
			if biggest < nbr:
				biggest = nbr

		return biggest

	#Return the quartile of a column vector
	def quartile(self, x_col: np.ndarray) -> list:
		if x_col.size == 0:
			return None

		x_sorted = np.sort(x_col)
		x_len = x_sorted.size

		def get_percentile(p):
			#Calculate the virtual index
			virtual_index = p * (x_len - 1)

			#Split into integer and fraction
			idx = int(virtual_index)
			fraction = virtual_index - idx

			#Interpolate between idx and idx + 1
			if idx + 1 < x_len:
				return x_sorted[idx] + fraction * (x_sorted[idx + 1] - x_sorted[idx])
			else:
				return float(x_sorted[idx])
			
		return [get_percentile(0.25), get_percentile(0.50), get_percentile(0.75)]

	#Return a value that measures the "lack of symmetry" of a column vector 
	def skewness(self, x_col: np.ndarray) -> float:
		if x_col.size < 3:
			return 0.0

		n = x_col.shape[0]

		mean = self.mean(x_col)
		std = self.std(x_col)

		if std == 0:
			return 0.0

		skew = np.sum((x_col - mean) ** 3) / n

		return float((skew / (std ** 3)))

	#Return a value that tells us if there are extreme outliers in a column vector 
	def kurtosis(self, x_col: np.ndarray) -> float:
		if x_col.size < 4:
			return 0.0

		n = x_col.shape[0]
		mean = self.mean(x_col)
		std = self.std(x_col)
		if std == 0:
			return 0.0

		kurt = np.sum((x_col - mean) ** 4) / n

		return float((kurt / (std ** 4)) - 3)

	#Returns a value that shows the range between the max and min value of a column vector
	def range(self, x_col: np.ndarray) -> float:
		if x_col.size < 2:
			return 0.0
		
		return float(self.max(x_col) - self.min(x_col))
	
	#Returns a value that shows the range between the third and first quartile of a column vector
	def iqr(self, x_col: np.ndarray) -> float:
		if x_col.size < 2:
			return 0.0
		
		q1, _, q3 = self.quartile(x_col)

		return float(q3 - q1)





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

def data_analysis():
	data = get_data()
	print(data.shape)

	#Get all Numerical Features
	numerical_features = data.select_dtypes(include=["number"])

	tstat = TinyStatistician()

	results = {}

	for col_names in numerical_features.columns:
		#Parse Column
		raw_col = numerical_features[col_names].values

		#Use boolean mask to get rid of NaN values
		clean_col = raw_col[~np.isnan(raw_col)]

		q1, median, q3 = tstat.quartile(clean_col)

		results[col_names] = {
			"Count": tstat.count(clean_col),
			"Mean": tstat.mean(clean_col),
			"Std": tstat.std(clean_col),
			"Min": tstat.min(clean_col),
			"25%": q1,
			"50%": median,
			"75%": q3,
			"Max":  tstat.max(clean_col),
			"Skewness": tstat.skewness(clean_col),
			"Kurtosis": tstat.kurtosis(clean_col),
			"Range": tstat.range(clean_col),
			"IQR": tstat.iqr(clean_col)
		}

	summary_df = pd.DataFrame(results)
	print(summary_df)

	#To compare results
	#print(numerical_features.describe())


def main():
	data_analysis()

if __name__ == "__main__":
	main()