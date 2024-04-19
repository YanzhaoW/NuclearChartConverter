# Generation of JSON data file for G4Horus simulation

The program generates the JSON data file from the csv files downloaded from [Live Chart of Nuclides](https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html). The csv file download link can be found at the "Decay Radiation" tab of each nuclide. Two csv files from each nuclide should be downloaded: one for of gamma decays and the other for the non-gamma decays (e.g. EC, beta decay or alpha decay).
An example of Eu-152 can be found in [this folder](./csv).

## Program usage
1. Import the class from the module `decay_charts_json` with:
```python
from decay_charts_json import Charts
```

2. Add each csv file to the class with a valid header mapping (see the [section](#header-mapping) below):
```python
charts = Charts()

charts.add_chart(filename="csv/152Eu.csv", is_gamma=True, header_map=eu_152_header_map)
charts.add_chart(filename="csv/152Eu_ng.csv", is_gamma=False, header_map=eu_152_ng_header_map)
```
`is_gamma` is `True` if the csv file contains the gamma (isomeric) transitions and `False` otherwise.

3. Generate JSON file:
```python
charts.parse_to_json_file("result.json")
```
An example can be found in the file [main.py](./main.py).

## Header mapping
To generate the JSON data file from csv files, user needs to provide a valid header mapping with the dictionary type (key value pairs). it's used to connect the csv headers to the corresponding JSON headers. See `eu_152_header_map` and `eu_152_ng_header_map` in [main.py](./main.py) as the examples.

### Key
Its keys must be found among the headers in the corresponding csv file.
> [!NOTE]
> The program automatically trims the unnecessary spaces from the csv headers. Therefore, for headers in the csv files like " energy " and "parent  level ", the keys should be "energy" and "parent level" respectively.

> [!IMPORTANT]
> Headers in the csv file may not be correct for their values. Please valify the values and use the header they belong to.

### Value
The value corresponding to each key must be one of the following strings:
* energy
* energy_error
* intensity
* intensity_error
* init_level_energy
* final_level_energy
* alpha
* parent_nuclide
* parent_z
* parent_n
* parent_energy
* child_nuclide
* child_z
* child_n
* half_life_sec
