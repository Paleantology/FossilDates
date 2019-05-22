#!/bin/bash
#PBS -q workq
#PBS -l nodes=1:ppn=20
#PBS -l walltime=1:00:00
#PBS -N FBD40
#PBS -o FBD40.out
#PBS -j oe
#PBS -A loni_june2019
#PBS -m abe
#PBS -M tyler   


module load gcc

datapath=/work/tyler333/FossilDates/TT/40
cd $datapath
mpirun -np 5 ~/rb-mpi mcmc_TEFBD.Rev

