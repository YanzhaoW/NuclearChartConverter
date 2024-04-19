import json
from typing import List

import pandas as pd
from .chart import Chart

required_headers_default = [
    "energy",
    "energy_error",
    "intensity",
    "intensity_error",
    "init_level_energy",
    "final_level_energy",
    "alpha",
    "parent_nuclide",
    "parent_z",
    "parent_n",
    "parent_energy",
    "child_nuclide",
    "child_z",
    "child_n",
    "half_life_sec",
]


class DecayCharts:
    def __init__(self):
        self._dataframes: dict[str, pd.DataFrame] = {}
        self._dataframe = pd.DataFrame()
        self._headers = required_headers_default

    @property
    def required_headers(self):
        return self._headers

    @required_headers.setter
    def required_headers(self, headers: List[str]):
        self._headers = headers

    def add_chart(self, filename: str, is_gamma: bool, header_map: dict):
        chart = Chart(filename, is_gamma)
        chart.headers = self.__create_valid_header_map(header_map)
        chart.parse_csv()
        if chart.dataframe.empty:
            raise ValueError(f"Dataframe in the file {filename} is empty")
        self._dataframes[filename] = chart.dataframe

    def parse_to_json_file(self, filename: str):
        self.process()
        json_str = self._dataframe.to_json(orient="records")
        if json_str is not None:
            json_obj = json.loads(json_str)
            with open(filename, "w", encoding="utf-8") as output:
                json.dump(json_obj, fp=output, indent=4)
        else:
            raise ValueError("JSON parsing failed!")

    def print(self):
        print(self._dataframe.to_string(index=False))

    def print_dataframes(self):
        for filename, dataframe in self._dataframes.items():
            print(f"File: {filename}:")
            print(dataframe.to_string(index=False))

    def process(self):
        if not self.__check_headers():
            for dataframe in self._dataframes.values():
                print(f"headers: {self.__get_headers(dataframe)}")
            raise ValueError("Cannot concat dataframes: headers are different")
        self._dataframe = pd.concat(self._dataframes)

    def __check_headers(self):
        dataframes = list(self._dataframes.values())
        if len(dataframes) == 0:
            raise ValueError("Cannot check headers: no dataframe!")
        if any(dataframe.empty for dataframe in self._dataframes.values()):
            self.print_dataframes()
            raise ValueError("Some dataframes are empty")
        return all(all(self.__get_headers(dataframe) == dataframes[0]) for dataframe in dataframes)

    def __check_header_map(self, header_map: dict):
        return all(value in self._headers for value in header_map.values())

    def __get_headers(self, dataframe: pd.DataFrame):
        return dataframe.columns.values

    def __create_valid_header_map(self, header_map: dict):
        if not self.__check_header_map(header_map):
            raise ValueError(f"All key values in {header_map.values()} must be one of {self._headers}")
        swaped_map = {value: key for key, value in header_map.items()}
        valid_headers = [swaped_map[header] if header in swaped_map else header for header in self._headers]
        return dict(zip(valid_headers, self._headers))
