from DatabaseManager import db_read, db_write
from TimeConverter import TimeConverter as Tc
from StatisticsManager import StatisticsManager as Sm
from Exporter import Exporter as Ex
from NetworkHandler import NetworkHandler as Nh


dtu = Tc.date_to_unix
utd = Tc.unix_to_date


if __name__ == '__main__':
    # times = [[1611772200, 1611773100],
    #          [dtu('27/01/2021 18:35:00'), dtu('27-01-2021 18.50')],
    #          [dtu('27.01.2021'), dtu('28.01.2021')]]
    # headings = ['temperature',
    #             'carbon_monoxide, nitric_oxide, nitrogen_dioxide, sulphur_dioxide',
    #             'carbon_monoxide, sulphur_dioxide']
    # graph_file_paths = ['test1.svg', 'test2.svg', 'test3.svg']
    # csv_file_paths = ['test1.csv', 'test2.csv', 'test3.csv']
    # stats = []
    #
    # for i in range(len(times)):
    #     raw, time, data = db_read(times[i], headings[i], plot_graph=True, graph_file_path=graph_file_paths[i])
    #     if i == 1:
    #         Ex.export(headings[i], raw, csv_file_paths[i], unix=True)
    #     else:
    #         Ex.export(headings[i], raw, csv_file_paths[i], unix=False)
    #     stats.append([])
    #     for j in range(len(data)):
    #         stats[i].append(Sm(data[j], time))
    #
    # stats[0][0].print_statistics()
    json_strings = [r'[{"timeAlive": 1611773460, "temperature": 4.4, "carbonMonoxide": 0.10, "nitricOxide": 5.0, "nitrogenDioxide": 15.5, "sulphurDioxide": 2.1}, {"timeAlive": 1611773520, "temperature": 4.4, "carbonMonoxide": 0.12, "nitricOxide": 4.9, "nitrogenDioxide": 15.4, "sulphurDioxide": 2.2}]',
                    r'[{"timeAlive": 1611773580, "temperature": 4.5, "carbonMonoxide": 0.12, "nitricOxide": 5.1, "nitrogenDioxide": 15.6, "sulphurDioxide": 2.1}]',
                    'Test',
                    '{fake}']
    for i in range(len(json_strings)):
        obj = Nh.parse_json(json_strings[i])
        db_write(obj)
        print(i)
