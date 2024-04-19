import re

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


class Chart:
    def __init__(self, filepath: str, is_gamma: bool):
        self._filepath = filepath
        self._csv_to_json_headers_map = {}
        self._json_dataframe = pd.DataFrame()
        self._is_gamma = is_gamma

    @property
    def headers_map(self):
        return self._csv_to_json_headers_map

    @property
    def filepath(self):
        return self._filepath

    @property
    def dataframe(self):
        return self._json_dataframe

    @headers_map.setter
    def headers_map(self, names: dict):
        self._csv_to_json_headers_map = names

    @filepath.setter
    def filepath(self, path: str):
        self._filepath = path

    def print(self):
        print(self._json_dataframe)

    def parse_csv(self):
        print(f"Parsing dataframe from the file {self._filepath}")
        csv_dataframe = self.__read_csv(self._filepath)
        self.__reformat_csv_header_names(csv_dataframe)
        self.__csv_headers_to_json_headers(csv_dataframe)
        self.__add_nan_headers(csv_dataframe)

        self._json_dataframe = self.__convert_to_json_dataframe(csv_dataframe)
        self.__filter_rows(self._json_dataframe)
        self._json_dataframe["is_gamma"] = self._is_gamma
        print(f"Parsing from the file {self._filepath} is successful!\n")

    def __read_csv(self, filepath: str):
        csv_data = pd.read_csv(
            filepath, engine="python", sep=r"\s*,\s*", header="infer", index_col=False, skipinitialspace=True
        )
        return pd.DataFrame(csv_data)

    def __reformat_csv_header_names(self, csv_dataframe: pd.DataFrame):
        raw_csv_headers = csv_dataframe.columns.values
        new_csv_headers = [re.sub(r"[ ]+", " ", x) for x in raw_csv_headers]
        header_conversion = dict(zip(raw_csv_headers, new_csv_headers))
        csv_dataframe.rename(columns=header_conversion, inplace=True)

    def __filter_rows(self, dataframe: pd.DataFrame):
        dataframe = dataframe[dataframe["init_level_energy"].notnull()]
        dataframe = dataframe[dataframe["final_level_energy"].notnull()]
        dataframe = dataframe[dataframe["energy"].notnull()]

    def __add_nan_headers(self, dataframe: pd.DataFrame):
        absent_headers = [
            header for header in self._csv_to_json_headers_map.values() if header not in dataframe.columns.values
        ]
        if len(absent_headers) != 0:
            dataframe[absent_headers] = np.NaN

    def __csv_headers_to_json_headers(self, csv_dataframe: pd.DataFrame):
        self.__check_user_given_csv_headers(csv_dataframe)
        existed_header_map = {
            key: value for key, value in self._csv_to_json_headers_map.items() if key in csv_dataframe.columns.values
        }
        csv_dataframe.rename(columns=existed_header_map, inplace=True)

    def __convert_to_json_dataframe(self, csv_dataframe: pd.DataFrame):
        # fmt: off
        return csv_dataframe[[column for column in self._csv_to_json_headers_map.values()]]  # pylint: disable=unnecessary-comprehension
        # fmt: on

    def __check_user_given_csv_headers(self, csv_dataframe: pd.DataFrame):
        keys = [key for key, value in self._csv_to_json_headers_map.items() if key is not value]
        not_found_csv_headers = [key for key in keys if key not in csv_dataframe.columns.values]
        if len(not_found_csv_headers) != 0:
            raise ValueError(f"Following headers {not_found_csv_headers} are not present in the file {self._filepath}")
