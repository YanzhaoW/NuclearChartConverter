import re

import numpy as np
import pandas as pd


class DecayChart:
    def __init__(self, filepath: str, is_gamma: bool):
        self._filepath = filepath
        self._headers = {}
        self._dataframe = pd.DataFrame()
        self._is_gamma = is_gamma

    @property
    def headers(self):
        return self._headers

    @property
    def filepath(self):
        return self._filepath

    @property
    def dataframe(self):
        return self._dataframe

    @headers.setter
    def headers(self, names: dict):
        self._headers = names

    @filepath.setter
    def filepath(self, path: str):
        self._filepath = path

    def print(self):
        print(self._dataframe)

    def parse_csv(self):
        csv_data = pd.read_csv(
            self._filepath, engine="python", sep=r"\s*,\s*", header="infer", index_col=False, skipinitialspace=True
        )
        self._dataframe = pd.DataFrame(csv_data)
        self._dataframe.rename(columns=self.__trim_header_names(self._dataframe.columns.values), inplace=True)
        self.__change_header_name(self._dataframe)
        self.__add_null_headers(self._dataframe)
        # fmt: off
        self._dataframe = self._dataframe[[column for column in self._headers.values()]]  # pylint: disable=unnecessary-comprehension
        # fmt: on
        self.__filter(self._dataframe)
        self._dataframe["is_gamma"] = self._is_gamma

    def __trim_header_names(self, headers):
        new_headers = [re.sub(r"[ ]+", " ", x) for x in headers]
        return dict(zip(headers, new_headers))

    def __filter(self, dataframe: pd.DataFrame):
        dataframe = dataframe[dataframe["init_level_energy"].notnull()]
        dataframe = dataframe[dataframe["final_level_energy"].notnull()]
        dataframe = dataframe[dataframe["energy"].notnull()]

    def __add_null_headers(self, dataframe: pd.DataFrame):
        absent_headers = [header for header in self._headers.values() if header not in dataframe.columns.values]
        if len(absent_headers) == 0:
            return
        dataframe[absent_headers] = np.NaN

    def __change_header_name(self, dataframe: pd.DataFrame):
        keys = [key for key, value in self._headers.items() if key is not value]
        not_found_headers = [key for key in keys if key not in dataframe.columns.values]
        if len(not_found_headers) != 0:
            raise ValueError(f"Following headers {not_found_headers} are not present in the file {self._filepath}")
        existed_header_map = {key: value for key, value in self._headers.items() if key in dataframe.columns.values}
        dataframe.rename(columns=existed_header_map, inplace=True)
