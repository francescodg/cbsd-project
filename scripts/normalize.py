import pandas
import sys
import utils

def normalize(dataframe):
    return (dataframe - dataframe.mean()) / dataframe.std()

if __name__ == "__main__":
    filename = sys.argv[1]
    dataframe = utils.read_dataframe(filename)
 
    for value in normalize(dataframe).values:
        print value[0], value[1], value[2]

        
    
