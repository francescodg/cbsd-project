import pandas

def read_dataframe(filename):
    return pandas.read_csv(filename, skiprows=1, header=None)
