import argparse
import os
import numpy as np
from utils import *
import pandas as pd
import shutil
import glob 
import subprocess
import time
#from run_dexof import *
import sys 
from cfd_sim.run_dexof import run_dex
from cfd_sim.dexof_reader_class import parse_dex_file
import GPyOpt
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.factory import get_termination
from pymoo.algorithms.soo.nonconvex.nelder_mead import NelderMead
sys.dont_write_bytecode = True



input_size=2                             # input size may change if integer/ordinal type variable and represented by one-hot encoding
cad_storage_name= './cad_sim/design_points.csv'
cfd_storage_name= './cfd_sim/design_points.csv'

num_iteration=20                        # Number of iteration of sampling
init_samples=50 
budget_samples=50                        # Number of samples-our budget
ranges=[-10,0,-6.5,0]                    # ranges in form of [low1,high1,low2,high2,...]

src= './cad_sim/stl_repo'
dst='./cfd_sim/stl_cfd'


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
    #np.savetxt(cfd_storage_name,x,  delimiter=',')

def run_cad_cfd(x):
	save_design_points(x)

	delete_dir(dst)
	subprocess.call('./cad_sim/run_cad.sh')
	copy_file(cad_storage_name,cfd_storage_name)
	copy_dir(src,dst)
	deletefiles(src)
	prev = os.path.abspath(os.getcwd()) # Save the real cwd
	print('prev is',prev)
	cfd_sim_path= prev+'/cfd_sim'
	print('func path is:',cfd_sim_path)
	os.chdir(cfd_sim_path)
	result = run_dex()
	os.chdir(prev)
	return result



from pymoo.core.problem import ElementwiseProblem

class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=4,
                         n_obj=1,
                         n_constr=0,
                         xl=np.array([10,10,10,1]),
                         xu=np.array([573,573,50,50]))

    def _evaluate(self, x, out, *args, **kwargs):
        save_design_points(x)
        delete_dir(dst)
        subprocess.call('./cad_sim/run_cad.sh')
        copy_file(cad_storage_name,cfd_storage_name)
        copy_dir(src,dst)
        deletefiles(src)
        prev = os.path.abspath(os.getcwd()) # Save the real cwd
        print('prev is',prev)
        cfd_sim_path= prev+'/cfd_sim'
        print('func path is:',cfd_sim_path)
        os.chdir(cfd_sim_path)
        result = run_dex()
        os.chdir(prev)
        #g1 = 1

        out["F"] = [result]
        #out["G"] = [g1]




if __name__=='__main__':
	
	############################
	data_file_name='pymoo_nm.csv'   
	b=654;D=191;
	dim=4;n=100;

	pop_size=5
	n_gen=100
	#################################################
	#given b & D => need to find a,c,n,theta
	problem = MyProblem() 
    
	already_run = len(glob.glob(data_file_name))
	print('file exist?:',already_run)
	#############
	"""
	###########Genetic algorithm ######################
	algorithm = GA(pop_size=pop_size,eliminate_duplicates=True)
	termination = get_termination("n_eval", n)
	res = minimize(problem,algorithm,termination,seed=1,verbose=True, save_history=True)
	##################################
    """
	######### Nealder Mead ###########################
	algorithm = NelderMead()
	termination = get_termination("n_eval", 100)
	res = minimize(problem,algorithm, termination,seed=1,verbose=False,save_history=True)
	###################################################


	sample=[]
	result=[]
	for i in range(len(res.history)):
		if i==0: 
			sample= res.history[i].pop.get("X")
			result= res.history[i].pop.get("F")
		else: 
			sample= np.concatenate((sample,res.history[i].pop.get("X")),axis=0)
			result= np.concatenate((result,res.history[i].pop.get("F")),axis=0)
	print("Sample is:",sample.shape)
	print("Result is:",result.shape)

	total_result= np.concatenate((sample,result),axis=1)
	np.savetxt(data_file_name,total_result,  delimiter=',')


