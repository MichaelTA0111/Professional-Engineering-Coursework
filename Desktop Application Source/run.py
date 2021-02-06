from DatabaseManager import db_read
from TimeConverter import TimeConverter as Tc
from StatisticsManager import StatisticsManager as Sm


dtu = Tc.date_to_unix
utd = Tc.unix_to_date


if __name__ == '__main__':
    times = [[1611772200, 1611773100],
             [dtu('27/01/2021 18:35:00'), dtu('27-01-2021 18.50')],
             [dtu('27.01.2021'), dtu('28.01.2021')]]
    headings = ['temperature',
                'carbon_monoxide, nitric_oxide, nitrogen_dioxide, sulphur_dioxide',
                'carbon_monoxide, sulphur_dioxide']
    stats = []

    for i in range(3):
        raw, time, data = db_read(times[i], headings[i], plot_graph=True)
        stats.append([])
        for j in range(len(data)):
            stats[i].append(Sm(data[j], time))

    stats[0][0].print_statistics()
