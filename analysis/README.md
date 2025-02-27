# `analysis` Directory

This directory conatins the scripts that are used to do all the analysis for our paper once the actions of all the particles at all snapshots along with other information like coordinates, velocities and ages of the particles are available to us. Please note that all of these scripts need to be edited and can't be used directly because you will need to change details like input and output file paths. So, these are more for reference than out of the box package. Or they could be used as functions and combined to get an entire script that does what you want. so i will describe each of the scripts and what it does so it could be useful. A small subset (randomly selected) of our entire sample of stars formed in the simulation is provided in the `data` directory (described in there) which can be used to play around with these codes.

## `utils.py` 
This contains general functions that are being used in other scripts in this directory. This conatins functions for things like changing coordinate systems, applying a given filter to a time series, fitting a straight line, readingf and writing oout data, etc. All the functions have descriptions in comments inside the script for what they do, the parameters inputted as well as the outputs they return.
## `median_change.py`
This script computes and stores histograms of changes in stellar actions ($J_R, J_{\phi}, J_z$) over time, binned by stellar age and time interval ($\delta t$). The change can be either absolute ($\Delta J_i (t,\Delta t) = \left | J_i(t+\Delta t) - J_i(t) \right |$) or relative ( $\delta_i (\Delta t) = \Delta J_i (t,\Delta t)/J_i(t)$ ) where $i = (R,z,\phi)$ is the component, $t$ is the time of the snapshot, $\Delta t$ is the time interval between the two snapshots and $J_i(t)$ is the $i$ component of the star's action action at time $t$ in the simulation.

  Since our full dataset ($\sim 2$ million stars) is too large to process at once, the script does not calculate the median directly and instead, stores histograms of $\Delta J$ values binned by stellar age and time interval ( $\Delta t$ ), which can later be processed by a separate script to compute medians. Before processing, the script applies a Butterworth filter to smooth action time series before computing the change in actions. To manage memory and processing time, the script allows processing in batches of 80,000 stars at a time. This is controlled using the variable `l`, where `l=1` processes the first 80k stars, `l=2` the next 80k, and so on. The output is saved as HDF5 files, with `l` included in the filename, allowing results from multiple runs to be later combined. Each batch of 80,000 stars is divided into more chunks (4 by default) which are processed parallely to speed up computation. The histograms for all 4 chunks in a batch are saved together in a single HDF5 file. These HDF5 files are later used in another script to compute the median of the data. To analyse more than 80,000 stars, histograms from multiple HDF5 files can be combined in that script.

  #### Input data:
  - `J.npy`: 3D array of stellar actions ($J_R, J_{\phi}, J_z$) of stars across time snapshots- shape:(snapshots, stars, 3)
  - `A.npy`: 2D array of stellar ages across time snapshots- shape: (snapshots, stars)
  Before running the script, you must update the paths in the `main()` function to match the locations of the datasets: path to `J.npy` and `A.npy` as well as the path to save the HDF5 output file. These locations are marked in the script with comment `#change path here`.
#### Output data
- HDF5 file that contains histograms of $\Delta J$ binned by both stellar age and time interval. The median is not computed in this script but in a separate script that has the function to read and combine the HDF5 files as well.
#### Usage
Once the file paths have been changed, the script can be run using:
```
python3 median_change.py <which_J> <l> <relative>
```
where:
- `<which_J>` specifies the action component with 0 for $J_R$, 1 for $J_{\phi}$ and 2 for $J_z$.
- `<l>` specifies the batch number with `l=1` for first 80k stars, `l=2` for stars 80k-160k, etc.
- `<relative>` specifies if it computes relative change in action (1) or absolute change in action (0).
