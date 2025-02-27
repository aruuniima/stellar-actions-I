# `data` Directory

This directory contains various data files resulting from the scripts in the `analysis` directory, which use simulation data. These files are used in scripts located in the `results` directory to generate the plots featured in the associated paper.

Most of the scripts in the `results` directory already have the paths to these data files configured, so no changes are typically required. However, there are a few scripts that may require additional data, though these are mostly related to simulation plots and are not directly linked to the Results section of the paper. The files that are not available in the `data` directory are: `actions.h5` and `radial_bin.zip`, which can both be downloaded from [this webpage](https://www.mso.anu.edu.au/~arunima/stellar-actions-I-data/). `actions.h5` is used in the scripts `plot4.py` and `Rplot5.py` in the `results` directory whereas `radial_bin.zip` is used in the `Rplot11.py` script in the same directory. 

## Data files present in this directory:
#### 1. Absolute change in actions
`abs_JR.npz`, `abs_Jphi.npz` and `abs_Jz.npz` contains absolute change in actions as function of both stellar ages and time interval $\Delta t$ and are used in scripts `Rplot6.py` and `Rplot7.py`. Their structure can be found in those scripts.

#### 2. Relative change in actions (as function of both age and $\Delta t$)
`rel_JR.npz` and `rel_Jz.npz` are the files containing the relative change in actions as function of both stellar ages and time interval $\Delta t$ and are used in scripts `Rplot8.py`, `Rplot9.py` and `Rplot12.py`.

#### 3. Relative change in actions (as function of only $\Delta t$)
`rel_JR_delt.npz` and `rel_Jz_delt.npz` are the files containing the relative change in actions as function of only the time interval $\Delta t$ and are used in scripts `Rplot9.py`and `Rplot10.py`.

#### 4. Relative change in actions for stars born in different density regions
The following files contain the relative change in actions for stars born in different density regions as function of only time interval $\Delta t$: `dense_JR.npz`, `sparse_JR.npz`, `verysparse_JR.npz`, `dense_Jz.npz`, `sparse_Jz.npz`, and `verysparse_Jz.npz`. These are used in the script `Rplot10.py`.

#### 5. Relative change in actions for initial stars
`init_JR.npz` and `init_Jz.npz` are the files containing the relative change in actions for initial stars (really old stars present in the intial conditions of the simulation) as a function of only the time interval $\Delta t$ and are used in the script `Rplot12.py`.
#### 6. Orbit data for simulation stars and initial stars
`star.npz` and `initial_star.npz` contain orbital data (vertical height `z` and vertical velocity `vz`) for stars born in the simulation and initial stars. They are used in the script `Rplot13.py`.

The structure for all the data files can be seen in the respective scripts.
