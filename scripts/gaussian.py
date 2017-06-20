import pandas
import subprocess

def _get_data(column):
    seriesList = []

    for filename in ["container.values", "host.values", "namespace.values"]:
        try:
            series = pandas.read_csv(filename, header=None, delimiter=' ')
            mean = series[column].mean()
            std = series[column].std()
            label = filename.split(".")[0]
            label = label[0].upper() + label[1:]
            seriesList.append({"std": std, "mean": mean, "label": label})
        except IOError:
            pass

    return seriesList


def _set_xrange(seriesList):
    means = []
    stds = []

    for series in seriesList:
        means.append(series["mean"])
        stds.append(series["std"])

    bottom = min(means) - 4 * max(stds)
    top = max(means) + 4 * max(stds)

    options = ["set xrange [%.2f:%.2f]" % (bottom, top)]

    return options

def setup(options):
    head = ["set grid",            
            "set term png"]
    return "\n".join(head + options) + "\n"


def plot(seriesList):    
    plotCommands = [] 
    for series in seriesList:
        plotCommand = "1/(sqrt(2*pi)*{std})*exp(-(x-{mean})**2/(2*{std}**2)) t '{label}'"\
            .format(std=series["std"], mean=series["mean"], label=series["label"])
        plotCommands.append(plotCommand)
    return "plot " + ",".join(plotCommands)


def gnuplot(plotFile, output):
    subprocess.call(["gnuplot", "-e", "set output '%s'" % output, plotFile])


def create_plot_file(column, title, options):
    seriesList = _get_data(column)    

    options = _set_xrange(seriesList)

    output = setup(options)
    output += "set title '%s'\n" % title
    output += plot(seriesList)
    
    filename = "%s.gp" % title
    with open(filename, 'w') as f:
        f.write(output)

    return filename


if __name__ == "__main__":
    plotTitles = ["Request per second", "Transfer rate", "Time per request"]
    options = [
        ["set xrange [800:1000]"],
        ["set xrange [100000: 200000]"],
        ["set xrange [0.9:1.3]"]
    ]

    for i in range(len(plotTitles)):
        if i == 1:
            continue # skip "Transfer rate"
        column = i
        title = plotTitles[i]
        plotFile = create_plot_file(column, title, options[column])
        gnuplot(plotFile, output="%s.png" % title)
