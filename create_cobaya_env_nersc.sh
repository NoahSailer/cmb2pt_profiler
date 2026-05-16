#!/bin/bash
PACKDIR=$SCRATCH/cobaya_packages
if [ -d $PACKDIR ]; then
    rm -rf $PACKDIR/*
else
    mkdir -p $PACKDIR
fi
module load python
if conda env list | awk '{print $1}' | grep -qx "cobaya"; then
    conda env remove -n cobaya -y
fi
conda create --name cobaya --clone nersc-mpi4py -y
conda activate cobaya
python -m ipykernel install --user --name cobaya --display-name cobaya
python -m pip install cobaya candl-like
cobaya-install cosmo -p $PACKDIR
cd $PACKDIR
git clone https://github.com/SouthPoleTelescope/spt_candl_data.git
cd spt_candl_data
python -m pip install .
cd ..
git clone https://github.com/Lbalkenhol/candl_data.git
cd candl_data
python -m pip install .