import subprocess
import sys
import json


def compute_mean(filename, column):
    values = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            splitted = line.split(' ')
            value = splitted[column - 1]
            values.append(float(value))
    mean = sum(values)/len(values)
    return mean


def run_gnuplot(options, series):
    commands = [
        "set grid",
        "set key outside",
        "set title \"{title}\"",
        "set ylabel \"{ylabel}\"",
        "set term png",
        "set output \"{output}\""]    
    
    if options.has_key("yrange"):
        commands.append("set yrange {yrange}")

    commands = [cmd.format(**options) for cmd in commands]

    plotSeriesCommands = []

    for s in series:
        plotSeriesCmd = "%s" % s['input']
        plotSeriesCmd += " u %s" % s["using"] if s.has_key("using") else ""
        plotSeriesCmd += " t '%s'" % s['title'] if s.has_key("title") else ""
        plotSeriesCmd += " pt %s" % s['pt'] if s.has_key("pt") else ""
        plotSeriesCmd += " lt rgb '%s'" % s['color'] if s.has_key("color") else ""        
        plotSeriesCommands.append(plotSeriesCmd)
    plotSeriesCommands = "plot " + ", ".join(plotSeriesCommands)

    commands.append(plotSeriesCommands)
    commands = "; ".join(commands)

    subprocess.call(["gnuplot", "-e", commands])


def obtain_params(plot):
    options = {
        "title": plot["options"]["title"],
        "ylabel": plot["options"]["ylabel"],
        "output": plot["options"]["output"]
    }

    series = []

    for s in plot["series"]:
        series.append({
            'input': "\"%s\"" % s["input"],
            'using': s["column"],
            "title": s["title"],
            "pt": s["pt"],
            "color": s["color"]
        })
        
        if s.has_key("show mean") and s["show mean"]:
            series.append({
                "input": "%.2f" % compute_mean(s["input"], s["column"]),
                "title": s["title"] + " mean",
                "color": s["color"]
            })

    return (options, series)

        
if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as fp:
        conf = json.load(fp, encoding="utf-8")
        for plot in conf["plots"]:
            (options, series) = obtain_params(plot)
            run_gnuplot(options, series)    
