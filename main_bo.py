  # -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:20:18 2022

@author: Vardhan Harsh (Vanderbilt University)
"""
import argparse
import os
import numpy as np
from utils import *
import pandas as pd
import shutil
import glob 
import subprocess
import time
import sys 
from cfd_sim.run_dexof import *
from cfd_sim.dexof_reader_class import parse_dex_file
import GPyOpt
from subprocess import PIPE, run
import random
from numpy.random import seed
#from single_myring import myring_hull_ds

sys.dont_write_bytecode = True
cad_storage_name= './cad_sim/design_points.csv'
cfd_storage_name= './cfd_sim/design_points.csv'


src= './cad_sim/stl_repo'
dst='./cfd_sim/stl_cfd'

a=500; b=500;r=100;u=2;k=0.01;w=10 


def delete_dir(loc):
    print('*Deleted directory:',loc)
    shutil.rmtree(loc)

def copy_dir(src,dst):
	print('*Copied directory from',src,'to destination:',dst)
	shutil.copytree(src, dst)

def deletefiles(loc):
	print('Deleted files from location:',loc)
	file_loc= loc+'/*'
	files = glob.glob(file_loc)
	for f in files:
		os.remove(f)

def copy_file(src,dst):
	print('*Copied file from',src,'to destination:',dst)
	shutil.copy(src, dst)

def save_design_points(x):
    np.savetxt(cad_storage_name,x,  delimiter=',')
    np.savetxt(cfd_storage_name,x,  delimiter=',')

def run_cad_cfd(x):
	global u,k,w
	print('shape of x:',x.shape)
	print('--> u is:',u,'k is:',k,'w is:',w)
	save_design_points(np.array([x[0][0],x[0][1],x[0][2],x[0][3],x[0][4],x[0][5],x[0][6],u,k,w,r]))
	delete_dir(dst)
	subprocess.call('./cad_sim/run_cad.sh')
	copy_dir(src,dst)
	deletefiles(src)
	prev = os.path.abspath(os.getcwd()) # Save the real cwd
	print('prev is',prev)
	cfd_sim_path= prev+'/cfd_sim'
	print('func path is:',cfd_sim_path)
	os.chdir(cfd_sim_path)
	result = main_run()
	os.chdir(prev)
	return result



def run_bo(bounds,aquistion='EI',seeds=0,run_id=0):
	##############################################
    print('Bound is:',bounds)
	################################################

    #max_time  = None 
    max_iter  = 100
    num_iter=20
    batch= int(max_iter/num_iter)
    #tolerance = 1e-8     # distance between two consecutive observations 
    data_file_name='./data/bo_'+aquistion+str(run_id)   
	#################################################
    already_run = len(glob.glob(data_file_name))
    print('file exist?:',already_run)
    print('Batch is:',batch)
    seed(seeds)
    for i in range(num_iter): 
        if already_run==1:
            evals = pd.read_csv(data_file_name, index_col=0, delimiter="\t")
            Y = np.array([[x] for x in evals["Y"]])
            X = np.array(evals.filter(regex="var*"))
            myBopt2D = GPyOpt.methods.BayesianOptimization(run_cad_cfd, bounds,model_type = 'GP',X=X, Y=Y,
                                              acquisition_type=aquistion,  
                                              exact_feval = True) 
            print('In other runs run')
        else: 
            myBopt2D = GPyOpt.methods.BayesianOptimization(f=run_cad_cfd,
                                              domain=bounds,
                                              model_type = 'GP',
                                              acquisition_type=aquistion,  
                                              exact_feval = True) 
            already_run=1
            print('In 1st run')
        print('------Running iteration is:',i) 
        # --- Run the optimization
        try:
            myBopt2D.run_optimization(batch,verbosity=True) 
        except KeyboardInterrupt:
            pass
        myBopt2D.save_evaluations(data_file_name) 


if __name__=='__main__':  

    seedz=11
    aqu1='EI'; aqu2='LCB'
    
    bound = [{'name': 'first_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'second_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'third_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'fourth_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'fifth_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'sixth_y', 'type': 'continuous', 'domain': (10,100)},
	         {'name': 'a', 'type': 'continuous', 'domain': (50,950)}]


    print('-> Bound is:',bound)	
    experiments= np.loadtxt('exp_setting.csv',delimiter=',',skiprows=1)    
    print('Experiemnts are:', experiments,'num_of_exp:',experiments.shape)
    for i in range(experiments.shape[0]):	
        u=experiments[i][1]; k=experiments[i][2];w=experiments[i][3]
        run_bo(bound,aqu2,seedz,i)  
		#print('In BO run')
	


	
	
