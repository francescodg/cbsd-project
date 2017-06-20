import pandas


def get_data(column):
    seriesList = []

    for filename in ["container.data", "host.data", "namespace.data"]:
        try:
            series = pandas.read_csv(filename, header=None, skiprows=1)
            mean = series[column].mean()
            std = series[column].std()
            label = filename.split(".")[0]
            label = label[0].upper() + label[1:]
            seriesList.append({"std": std, "mean": mean, "label": label})
        except IOError:
            pass

    return seriesList
