# `functions` Directory

This directory contains utility scripts that are used across multiple directories in the project, such as `action_calculation`, `analysis` and `results`.  The functions are not intended to be executed directly but are designed to support calculations and analyses throughout the project. Each script focuses on a specific aspect:

- `coordinate_conversion.py`: Contains functions for converting between coordinate systems.
- `data_reading.py`:  Includes functions for reading data related to star particles, gas particles, etc., from raw simulation files, as well as reading values from the potential grid file and CSV files.
- `grid_functions.py`: Provides functions related to grid operations, which are used in the `action_calculation` directory.
- `utils.py`: Contains general utility functions that support various tasks across the project, such as taking derivatives, calculating weighted quantiles, determining the centre of mass, etc.

Each script contains descriptions within the functions to provide information about their definitions and usage.
