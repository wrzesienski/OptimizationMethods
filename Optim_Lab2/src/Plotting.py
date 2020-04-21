import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

class Comtrade:
    """ класс записи результатов"""

    def __init__(self):
        self.alfa = []
        self.betta = []
        self.p = []
        self.time = []
        self.shortest_way = []

    def set_coefficients(self, alfa, betta, p):
        self.alfa.append(alfa)
        self.betta.append(betta)
        self.p.append(p)

    def get_coefficients(self):
        return self.alfa, self.betta, self.p

    def record_results(self, time, way_length):
        self.time.append(time)
        self.shortest_way.append(way_length)

    def show_results(self):
        return self.time, self.shortest_way

    def get_time(self):
        return self.time

def to_plot(comtrade:Comtrade):

    a, b, p = comtrade.get_coefficients()
    time, way = comtrade.show_results()

    markersize = [150-i for i in way]
    markercolor = time

    fig1 = go.Scatter3d(x=a,
                        y=b,
                        z=p,
                        marker=dict(size=markersize,
                                    color=markercolor,
                                    opacity=1,
                                    reversescale=True,
                                    colorscale='Reds'),
                        line=dict(width=1),
                        mode='markers')

    mylayout = go.Layout(scene=dict(xaxis=dict(title="alfa"),
                                    yaxis=dict(title="betta"),
                                    zaxis=dict(title="p")), )

    plotly.offline.plot({"data": [fig1],
                         "layout": mylayout},
                        auto_open=True,
                        filename=("5D Plot.html"))