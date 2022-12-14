# This Python file uses the following encoding: utf-8
import pandas as pd


from ui.processor import Processor


class DataProvider:
    def __init__(self):
        #data_file = pd.read_csv("/home/mukola/Projects/intelligent-interfaces-lab/Intelligent-Interfaces-lab-1/data/kyiv_flats_final.csv")
        data_file = pd.read_csv("data/kyiv_flats_final.csv")
        self.data = [data_file["total_area"].values, data_file["district_uk"].values, data_file["room_count"].values, data_file["subway_time"].values, data_file["quality"].values]

        processor = Processor()
        estimations = []
        prices = []
        for i in range(len(self.data[0])):
            output = processor.process(self.data[0][i], self.data[1][i], self.data[2][i], self.data[3][i], self.data[4][i])
            estimations.append(output.price_fuzz)
            prices.append(output.price)
        self.data.append(estimations)
        self.data.append(prices)

    def getData(self):
        return self.data

    def filter(self, estimation_str: str):
        if estimation_str == "all":
            return self.data

        filtered_data = [[], [], [], [], [], [], []]
        for i in range(len(self.data[0])):
            if self.data[5][i] == estimation_str:
                for j in range(7):
                    filtered_data[j].append(self.data[j][i])
        return filtered_data

