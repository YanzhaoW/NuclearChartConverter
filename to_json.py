from decay_charts import DecayCharts

eu_152_header_map = {
    "energy": "energy",
    "unc_en": "energy_error",
    "intensity_%": "intensity",
    "unc_i": "intensity_error",
    "end level energy [keV]": "init_level_energy",
    "end level H-l [sec]": "final_level_energy",
    "conversion coeff.": "alpha",
    "symbol": "parent_nuclide",
    "parent Z": "parent_z",
    "N": "parent_n",
    "parent energy [keV]": "parent_energy",
    "symbol.1": "child_nuclide",
    "Z": "child_z",
    "N.1": "child_n",
    "half_life [s]": "half_life_sec",
}

eu_152_ng_header_map = {
    "energy EC [keV]": "energy",
    "unc.2": "energy_error",
    "intensity EC": "intensity",
    "unc.3": "intensity_error",
    "daughter level energy [keV]": "final_level_energy",
    "symbol": "parent_nuclide",
    "parent Z": "parent_z",
    "N": "parent_n",
    "parent energy [keV]": "parent_energy",
    "symbol.1": "child_nuclide",
    "Z": "child_z",
    "N.1": "child_n",
    "half_life [s]": "half_life_sec",
}

if __name__ == "__main__":
    charts = DecayCharts()
    charts.add_chart(filename="152Eu.csv", is_gamma=True, header_map=eu_152_header_map)
    charts.add_chart(filename="152Eu_ng.csv", is_gamma=False, header_map=eu_152_ng_header_map)

    charts.process()
    charts.print()
