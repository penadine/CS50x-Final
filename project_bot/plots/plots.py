import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter


class Plotter:
    def make_plot_all(self, id, data):
        fig = plt.figure(figsize=(9,9))
        ax = fig.subplots()
        plt.title('Expenses')
        plt.xlabel('Date')
        plt.ylabel('Total summ')
        servises_set = {i['Expense'] for i in data}
        for servise in servises_set:
            x = np.array([np.datetime64(i['Date'], 'M') for i in data if i['Expense'] == servise])
            y = np.array([i['Total'] for i in data if i['Expense'] == servise])
            plt.plot(x, y, label = f"{servise}", marker='o')
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f$"))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'{id}-all.png', format='png')
        plt.clf()
        return f'{id}-all.png'

    def make_plot_name(self, id, data):
        fig = plt.figure(figsize=(9,9))
        ax = fig.subplots()
        plt.title(data[0]['Expense'])
        plt.xlabel('Date')
        plt.ylabel('Quantity')
        x = np.array([np.datetime64(i['Date']) for i in data])
        y_summ = np.array([i['Total'] for i in data])
        plt.plot(x, y_summ, label = "Total", marker='o')
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f$"))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.savefig(f'{id}-by-name.png', format='png')
        plt.clf()
        return f'{id}-by-name.png'

    def make_plot_date(self, id, data):
        fig = plt.figure()
        ax = fig.add_subplot()
        summ_all = sum([i['Total'] for i in data])
        plt.title(f"Servises summ = {summ_all:.2f}$")
        labels = [f"{i['Expense']}\n{i['Total']:.2f}$, {round((i['Total'] / summ_all * 100), 2)}%" for i in data]
        vals = [i['Total'] for i in data]
        ax.pie(vals, labels=labels)
        ax.grid()
        plt.savefig(f'{id}-by-date.png', format='png')
        plt.clf()
        return f'{id}-by-date.png'