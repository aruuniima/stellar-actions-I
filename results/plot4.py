##data not publicly available for this so code just for reference

import numpy as np
import h5py
imoprt matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

#read everything for one star ID (R,z,J_R,J_phi,J_z,M,t,A):
def load_onestar_data_hdf5(i,k,file_path_list, sampled_ids):
    """
    Loads star data for sampled IDs from the HDF5 file in time order.
    
    :param file_path: Path to the HDF5 file.
    :param sampled_ids: List or array of sampled star IDs.
    :return: Arrays for the required star data at each snapshot for the sampled stars.
    """
    # Initialize lists to store the data for each variable
    J_list, A_list, C_list,V_list,M = [], [],[],[],[]
    
    # Convert sampled_ids to a numpy array for efficient comparison
    sampled_ids = np.array(sampled_ids)
    for file_path in file_path_list:
        with h5py.File(file_path, 'r') as hdf:
            # Collect snapshot names and sort them
            snapshot_names = sorted(hdf['snapshots'].keys(), key=lambda x: int(x.split('_')[1]))
            print(np.shape(snapshot_names))
            # Loop through snapshots in time order
            for snapshot_name in snapshot_names[i:][::k]:
                grp = hdf[f'snapshots/{snapshot_name}']
                
                # Get IDs of stars in the current snapshot
                snapshot_ids_in_snapshot = grp['ID'][:]
                
                # Create a mask to select data for the sampled_ids present in the snapshot
                ID_mask = np.isin(sampled_ids, snapshot_ids_in_snapshot)
    
                # Initialize arrays for the current snapshot with NaN values
                J_snapshot = np.full((len(sampled_ids), 3), np.nan)  # Shape: (number_of_sampled_stars, 3)
                C_snapshot = np.full((len(sampled_ids), 3), np.nan)  # Shape: (number_of_sampled_stars, 3)
                V_snapshot = np.full((len(sampled_ids), 3), np.nan)  # Shape: (number_of_sampled_stars, 3)

                A_snapshot = np.full(len(sampled_ids), np.nan)       # Shape: (number_of_sampled_stars)
                M_snapshot = np.full(len(sampled_ids), np.nan) 
                
                
                # Find the indices of the sampled IDs in the snapshot
                star_indices = np.where(np.isin(snapshot_ids_in_snapshot, sampled_ids))[0]
                if len(star_indices) > 0:
                    # Map star_indices to the position in sampled_ids
                    id_to_position = {id_: idx for idx, id_ in enumerate(sampled_ids)}
                    mapped_indices = [id_to_position[snapshot_ids_in_snapshot[idx]] for idx in star_indices]
                    
                    # Assign data to the correct positions
                    J_snapshot[mapped_indices] = grp['actions'][:].T[star_indices]
                    C_snapshot[mapped_indices] = grp['coordinates'][:][star_indices]
                    V_snapshot[mapped_indices] = grp['velocities'][:][star_indices]
                    A_snapshot[mapped_indices] = grp['age'][:][star_indices]
                    M_snapshot[mapped_indices] = grp['mass'][:][star_indices]
                    
                    
                # Append the current snapshot data to the lists
                J_list.append(J_snapshot)
                C_list.append(C_snapshot)
                V_list.append(V_snapshot)
                A_list.append(A_snapshot)
                M.append(M_snapshot)
               
                print(f"Loaded {snapshot_name}", end="\r")

    # Convert the lists to numpy arrays for efficient processing
    J_list = np.array(J_list)  # Shape: (number_of_snapshots, number_of_sampled_stars, 3)
    A_list = np.array(A_list)  # Shape: (number_of_snapshots, number_of_sampled_stars)
    C_list = np.array(C_list)
    V_list = np.array(V_list)
    M= np.array(M)
    
    return J_list,A_list,C_list,V_list,M

k=1
i=101
J,A,C,V,M = load_onestar_data_hdf5(i,k,['/g/data/jh2/ax8338/action/results/NEW_nodupes.h5'],[22878914])
J=J/M      #getting specific actions
R=C[:,:,1].flatten()
z=C[:,:,2].flatten()
times = np.arange(R.shape[0])

# Butterworth filter setup
fs = 1.0  # Sampling frequency (1/snapshot interval)
cutoff = 1 / 30  # Desired cutoff frequency (inverse of time period in snapshots)
order = 10  # Filter order

# Design the filter
b, a = butter(order, cutoff / (0.5 * fs), btype='low', analog=False)

class Counter:
    def __init__(self):
        self.value = 0  # Initialize the counter

    def increment(self):
        self.value += 1  # Increment the counter


# Define a function to filter a single time series while ignoring NaNs
def filter_time_series(ts, b, a, counter):
    finite_mask = ~np.isnan(ts)  # Mask for valid (non-NaN) values
    filtered = np.full_like(ts, np.nan) # Initialize output with NaNs
    if finite_mask.sum() > max(len(a), len(b)) * 3:  
        filtered[finite_mask] = filtfilt(b, a, ts[finite_mask])  # Apply filter to valid data
        counter.increment()  # Increment the counter
    return filtered

data_JR = J[:,0,0]
counter=Counter()
filtered_data_JR=np.apply_along_axis(filter_time_series, axis=0, arr=data_JR, b=b, a=a, counter=counter)

data_Jphi = J[:,0,1]
counter=Counter()
filtered_data_Jphi=np.apply_along_axis(filter_time_series, axis=0, arr=data_Jphi, b=b, a=a, counter=counter)

data_Jz = J[:,0,2]
counter=Counter()
filtered_data_Jz=np.apply_along_axis(filter_time_series, axis=0, arr=data_Jz, b=b, a=a, counter=counter)


SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 18

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


fig, axs = plt.subplots(5, 1, figsize=(6,15),sharex='all')

ax1 = axs[0]
ax1.plot(times, R, color="purple")

ax1.set_ylabel("R (pc)")# (kpc km/s)")


ax2=axs[1]
ax2.plot(times, z, color="purple")
ax2.set_ylabel("z(pc)")


axs[2].plot(times, data_JR,label='data',color="grey")
axs[2].plot(times, filtered_data_JR,label='filtered', color="magenta")

axs[2].set_ylabel("$J_R$ (kpc km/s)")
axs[2].legend(loc='upper left')

ax1 = axs[3]
ax1.plot(times, data_Jphi, label='data',color="grey")
ax1.plot(times, filtered_data_Jphi, label='filtered', color="magenta")


ax1.set_ylabel("$J_{\phi}$ (kpc km/s)")
ax1.legend(loc='upper left')


ax2=axs[4]
ax2.plot(times, data_Jz,label='data',color="grey")
ax2.plot(times, filtered_data_Jz, label='filtered', color="magenta")

ax2.set_ylabel("$J_z$ (kpc km/s)")
ax2.set_xlabel("Time (Myr)")
ax2.legend(loc='upper right')

plt.tight_layout()

plt.savefig('/g/data/jh2/ax8338/action/heatmap/orbit_paper.pdf')
    
