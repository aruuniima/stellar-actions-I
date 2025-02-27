# `analysis` Directory

This directory contains scripts used for analysing our simulation data for the paper. These scripts assume that the actions of all particles across all snapshots—along with additional information such as coordinates, velocities, and ages—are available.

Please note that all of these scripts require modifications before use. You’ll need to update details like input and output file paths. They are not plug-and-play but serve as references. You can use these scripts as standalone tools or combine them into a single script tailored to your specific analysis needs. A small, randomly selected subset of stars from our full simulation sample is provided in the `data` directory (described separately). This can be used to experiment with these scripts.

## `utils.py` 
This script contains general utility functions used across multiple analysis scripts. It includes functions for: changing coordinate systems, applying a given filter to time series data, fitting a straight line, reading and writing data, etc. Each function is well-documented with comments explaining its purpose, input parameters, and returned outputs.

## `median_change.py`
This script computes and stores histograms of changes in stellar actions ($J_R, J_{\phi}, J_z$) over time, binned by stellar age and time interval ($\delta t$). The change can be either absolute ($\Delta J_i (t,\Delta t) = \left | J_i(t+\Delta t) - J_i(t) \right |$) or relative ( $\delta_i (\Delta t) = \Delta J_i (t,\Delta t)/J_i(t)$ ) where $i = (R,z,\phi)$ is the component, $t$ is the time of the snapshot, $\Delta t$ is the time interval between the two snapshots and $J_i(t)$ is the $i$ component of the star's action action at time $t$ in the simulation.

  Since our full dataset ($\sim 2$ million stars) is too large to process at once, the script does not calculate the median directly and instead, stores histograms of $\Delta J$ values binned by stellar age and time interval ( $\Delta t$ ), which can later be processed by a separate script to compute medians. Before processing, the script applies a Butterworth filter to smooth action time series before computing the change in actions. To manage memory and processing time, the script allows processing in batches of 80,000 stars at a time. This is controlled using the variable `l`, where `l=1` processes the first 80k stars, `l=2` the next 80k, and so on. The output is saved as HDF5 files, with `l` included in the filename, allowing results from multiple runs to be later combined. Each batch of 80,000 stars is divided into more chunks (4 by default) which are processed parallely to speed up computation. The histograms for all 4 chunks in a batch are saved together in a single HDF5 file. These HDF5 files are later used in another script to compute the median of the data. To analyse more than 80,000 stars, histograms from multiple HDF5 files can be combined in that script.

  #### Input data:
  - `J.npy`: 3D array of stellar actions ($J_R, J_{\phi}, J_z$) of stars across time snapshots- shape:(snapshots, stars, 3)
  - `A.npy`: 2D array of stellar ages across time snapshots- shape: (snapshots, stars).
    
  Before running the script, you must update the paths in the `main()` function to match the locations of the datasets: path to `J.npy` and `A.npy` as well as the path to save the HDF5 output file. These locations are marked in the script with comment `#change path here`.
#### Output data:
- HDF5 file that contains histograms of $\Delta J$ binned by both stellar age and time interval. The median is not computed in this script but in a separate script that has the function to read and combine the HDF5 files as well.
#### Usage:
Once the file paths have been changed, the script can be run using:
```
python3 median_change.py <which_J> <l> <relative>
```
where:
- `<which_J>` specifies the action component with 0 for $J_R$, 1 for $J_{\phi}$ and 2 for $J_z$.
- `<l>` specifies the batch number with `l=1` for first 80k stars, `l=2` for stars 80k-160k, etc.
- `<relative>` specifies if it computes relative change in action (1) or absolute change in action (0).

## `agg_hist_t_delt.py`
This script aggregates histograms of changes in stellar actions ($J_R, J_{\phi}, J_z$) that were previously stored in HDF5 files, computes the median change as a function of stellar age and time interval ($\Delta t$), and saves the results as a compressed NumPy archive (.npz).

The script reads multiple HDF5 files matching a given filename pattern (`glob_word`), processes the histograms, and calculates the median $\Delta J$ for each age and $\Delta t$ bin. For each combination of stellar age and time interval, the script constructs a cumulative distribution function (CDF) from the summed up histograms across all different processing chunks. The median change is extracted as the value corresponding to the 50th percentile in the CDF. The computed median values, along with the corresponding age and $\Delta t$ bin edges, are saved in a compressed NumPy file (.npz). The output filename is constructed using `glob_word`, ensuring consistency with input files.

#### Input data:
- HDF5 files: These contain the histograms of change in action binned by stellar age and time interval. The script searches for the files automatically useing `glob_word` which should be based on the file naming pattern from the previous script. For example, if you saved files as `rel_JR{l}.h5` for realtive changes in radial action across batches (`l=1,2,...`), setting `glob_word = '*rel_JR*.h5'` will include all matching HDF5 files, allowing you to compute medians across all batches.
- Bin size(`bin_size`): Specifies the resolution of bins for age and time interval, default value=5999.
  
As with the previous script, before running the script, update the paths in the `main()` function: path to the histogram HDF5 files and the output path to where `.npz` files will be saved. These locations have been marked in the script with the comment `#change path here`.
#### Output data:
- Compressed NumPy archive (`.npz`) containing:
  - `dt`: Time interval ($\Delta t$) bin edges.
  - `J`: 2D array containing median $\Delta J$ values for each (stellar age, time interval) combination.
#### Usage:
Once the file paths have been changed, the script can be run using:
```
python3 agg_hist_t_delt.py <glob_word> <bin_size>
```
where:
- `<glob_word>` is the pattern used to find relevant HDF5 files.
- `<bin_size>` is the integer specifying age bin resolution for processing. Its default value is 5999 and hence, it only needs to be specified if you have changed the age bin resolution inside the `median_change.py` script's `process_chunk_filter` function

## `agg_hist_delt.py`
This script  is similar to `agg_hist_t_delt.py`, but instead of calculating the median change in stellar actions ($J_R, J_{\phi}, J_z$) as a function of both stellar age and time interval ($\Delta t$), it computes the median solely as a function of $\Delta t$.

Like the previous script, it searches for relevant HDF5 files using `glob_word`, processes the histograms read from these files, and calculates the median $\Delta J$ for $\Delta t$ bin. To do this, the values of $\Delta J$ across all age bins are combined into a single histogram for each $\Delta t$ bin. The remaining process is identical to `agg_hist_t_delt.py`.

#### Input data:
- The input HDF5 files and path structure are the same as in `agg_hist_t_delt.py`.
- Update the input (`hdf5_file_list`) and output (`np.savez_compressed()`) paths in `main()`, marked with `#change path here`.
#### Output data:
- Compressed NumPy archive (`.npz`) containing:
  - `dt`: Time interval ($\Delta t$) bin edges.
  - `J`: 1D array containing median $\Delta J$ values for each $\Delta t$.
#### Usage:
Once the file paths have been updated, the script can be run using:
```
python3 agg_hist_delt.py <glob_word> <bin_size>
```
where the variables are the same as in the previous script.

## `identify_dense_sparse.py`
This script identifies stars born in dense, sparse, and very sparse regions based on their 5th nearest neighbour (5NN) distances which act as proxy for the local stellar density at birth. The corresponding action (`J`) and age (`A`) data of these stars is then saved which can be used in `median_change.py` and `agg_hist_delt.py` scripts to compute action changes over time. 

The script reads star data from `actions.h5`, which can be downloaded from [this webpage](https://www.mso.anu.edu.au/~arunima/stellar-actions-I-data/) and contains actions, coordinates, velocities, ages, masses, and IDs for a subset of our entire sample at all snapshots. Positions at birth are used to calculate 5NN distance using `cKDTree` and stars are classified into density categories based on predefined 5NN distance (see the script or the paper). The values of actions and ages for the stars in different categories are saved in `.npy` format for further analysis.
#### Input data:
`stellar-actions-I/data/actions.h5` is the input path used in the script. The data can be downloaded from the previously specified link and the input path should match its location.
#### Output data:
- `J_sparse.npy`, `A_sparse.npy`: Actions and ages of stars in the sparse region.
- `J_very_sparse.npy`, `A_very_sparse.npy`: Actions and ages of stars in the very sparse region.
- `J_dense.npy`, `A_dense.npy`: Actions and ages of stars in the dense region.
  #### Usage:
  Before running the script, update the output file paths (`#change path here`). Once paths are set, run:
```
python3 identify_dense_sparse.py
  ```
## `identify_radial_bins_calculate_change.py`
This script identifies stars born in different radial bins and computes action changes over time for each bin. It also calculates and writes out the number of stars in each radial bin and their average orbital periods.
   
The script reads star data from `actions.h5`, which can be downloaded from [this webpage](https://www.mso.anu.edu.au/~arunima/stellar-actions-I-data/) and contains actions, coordinates, velocities, ages, masses, and IDs for a subset of our entire sample at all snapshots. The radial bins are defined from 0 to 18kpc in 1kpc steps are stars are assigned to these bins. For each bin, orbital period is estimated and action changes are calculated using `median_change.py` and the output HDF5 files are stored for each radial bin.

#### Input data:
`stellar-actions-I/data/actions.h5` is the input path used in the script. The data can be downloaded from the previously specified link and the input path should match its location.
#### Output data:
- Radial bin action change results (`.h5` files, one per radial bin) are saved as `file_path = f'path_to_results_J{which_J}_{l_R}kpcbin.h5'`
- Number of stars in each radial bin (`path_to_radial_bin_numbers.txt`)
- Average orbital period for each bin (`path_to_radial_period.txt`)
You should modify all the filepaths in the script (marked with `#change path here`) to set your desired save location.
  #### Usage:
  Run the script with a command-line argument specifying the action component: 
```
python3 identify_radial_bins.py <which_J>
  ```
where `<which_J>` is the same variable as in earlier scripts.
