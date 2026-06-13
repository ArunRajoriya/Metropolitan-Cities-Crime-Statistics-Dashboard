import matplotlib.pyplot as plt

def generate_chart(data, title):

    plt.figure()
    data.plot(kind="bar")

    plt.title(title)

    chart_path = "static/charts/chart.png"

    plt.savefig(chart_path)

    return chart_path