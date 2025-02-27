# `action_calculation` Directory

This directory contains the complete code for computing the actions of stars, initial stars, or dark matter particles using simulation data and a precomputed gravitational potential grid. These datasets are not included in the repository but can be provided upon reasonable request from the authors.

The scripts here serve as a guide, but modifications are required before running them—in particular, file paths must be updated to match your setup.

The main script, `action_FINAL.py`, calculates the radial, vertical, and azimuthal actions for particles at a specific time snapshot. It integrates functions from other scripts within the `action_calculation` directory and saves the output as an HDF5 file.

#### Usage:
```
python action_FINAL.py <snapshot_time_in_Myr> <particle_type>
```
where,
- `<snapshot_time_in_Myr>`: The snapshot in Myr
- `<particle_type>`: The type of particle (0: initial stars, 1: simulation stars, 2: dark matter particles).

For the rest of the scripts, very short descriptions are provided below. See the paper for details of the entire methodology.
### 1. `actioncalc.py`: 
This script defines the `action_func()` function, which calculates the actions for stars using the provided potential grid, velocities, and positions. It also calculates `kappa` and `nu` (epicyclic frequencies), which are used in the action calculation.
### 2. `kappa.py`:
This file contains the `kappa()` function that calculates the radial epicyclic frequency $\kappa$, a key quantity used in the radial action $J_R$ computation.
### 3. `nu.py`:
The `nu.py` script defines the functions responsible for calculating the vertical epicyclic frequency $\nu$ for stars, which is used in the vertical action $J_z$ calculation.
### 4. `potential_der.py`:
This file defines functions for fitting the gravitational potential as a function of radius $R$ and vertical height $z$ by using the potential grid we have calculated from the simulation potential output. 
### 5. `mid_res_info.py`:
This script processes the raw simulation data (positions, velocities, masses) for each star or particle in the list of IDs inputted and provides them in a format ready for action calculation.

## Result format
The results of the action calculations for each snapshot are stored in an HDF5 file in the following structure:
### Group Name: `snapshots/snapshot_<i>`
where `<i>` is the snapshot time in Myr.
### Datsets in each group:
#### 1. `ID`:
The unique ID of each star or particle (array of integers).
#### 2. `J` ($J$):
An array of shape (n_stars, 3) representing the calculated actions for each star in the order: Radial ($J_R$), Azimuthal ($J_{\phi}$), and Vertical ($J_z$) in units M_sun kpc km/s.
#### 3. `V` ($V$):
The velocities of the stars/particles in cylindrical coordinates (array of shape (n_stars, 3)), representing the velocity components: ($V_{\phi}$, $V_R$, $V_z$) in units km/s.
#### 4. `C` ($C$):
The positions of the stars in cylindrical coordinates (array of shape (n_stars, 3)), respresenting coordinates: ($\phi,R,z$) in units of pc for $R,z$.
#### 5. `M` ($M$):
An array of masses for each star/particle (array of shape (n_stars,)) in units of solar masses. 
#### 6. `A` ($A$):
An array of age of each star at that snapshot of shape (n_stars,) in units Myr.
#### 7. `Kappa` ($\kappa$):
The radial epicyclic frequency (array of shape (n_stars,)) in units km/s kpc.
#### 8. `Nu_low` ($\nu_l$):
The vertical epicyclic frequency calculated by using a linear fit to the first derivative of the potential in $z$ (array of shape (n_stars,)) in units km/s kpc. This is the epicyclic frequency that has been used for the vertical action calculation.
#### 9. `Nu_middle` ($\nu$):
The vertical epicyclic frequency calculated for each star/particle (array of shape (n_stars,)) in units km/s kpc.
#### 10. `R_g` ($R_g$):
The guiding radius for each star/particle (array of shape (n_stars,)).
#### 11. `L_z` ($L_z$):
The azimuthal angular momentum for each star/particle (array of shape (n_stars,)) in units kpc km/s.
#### 12. `L_z_gal`:
The circular galactic motion contribution to the azimuthal angular momentum, calculated as $R_g^2 \times \Omega(R_g)/1000$ (in units kpc km/s). It is an array of shape (n_stars,).
