# `results` Directory

This directory contains scripts for generating the figures and plots presented in the associated paper. The scripts are organised as follows:

### Plot scripts before the Results section:
The scripts `plot1.py`, `plot2.py`, `plot3.py` and `plot4.py` correspond to the first four figures which are appear before the results section of the paper. Of these, only `plot4.py` can be executed using publicly available data (i.e., the `actions.h5` file, which can be downloaded from the provided [website](https://www.mso.anu.edu.au/~arunima/stellar-actions-I-data/). The remaining three scripts (`plot1.py`, `plot2.py`, and `plot3.py`) require data that is only available upon request from the authors.

### Plot scripts from the Results section:
The `RplotX.py` scripts correspond to the figures in the results section of the paper, with the number in the script name referring to the figure number in the paper. With the exception of `Rplot4.py`, `Rplot5.py`, and `Rplot11.py`, the other scripts can be run as-is to reproduce the figures, as they use data already available in the `data` directory. The file paths in these scripts are correctly configured.

For `Rplot4.py`, `Rplot5.py`, and `Rplot11.py`, you will need to download the necessary data from this [website](https://www.mso.anu.edu.au/~arunima/stellar-actions-I-data/). After downloading the data, you must update the file paths in the corresponding scripts to point to the location of the downloaded files.

