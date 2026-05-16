To reproduce the figures:

```
chmod +x create_cobaya_env_nersc.sh
./create_cobaya_env_nersc.sh
salloc --nodes 1 --qos interactive --time 04:00:00 --constraint cpu
module load python
conda activate cobaya
rm chains/*lock*
export COBAYA_USE_FILE_LOCKING=false
export OMP_NUM_THREADS=4
srun -N 1 -n 32 -c 4 python run_tau_profile.py cmb2pt_lite
srun -N 1 -n 32 -c 4 python run_tau_profile.py cmb2pt_lite_alens
python plot_tau_profile.py cmb2pt_lite
python plot_tau_profile.py cmb2pt_lite_alens
```