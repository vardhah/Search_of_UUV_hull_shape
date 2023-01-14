import numpy as np
import glob
import os

data_loc= u"./data/*.csv"
stl_dump_loc= u"./cad_sim/stl_dump"
files = glob.glob(data_loc)


print('Files are:',files) 
flag=0; storage=[]
for f in files: 
  print('--> clearfile is:',f)
  run_data = np.loadtxt(f,delimiter=',')
  print('Run data shape:',run_data.shape)
  index=np.argmin(run_data[:,-1], axis=0)
  print('Index is:',index)
  optimal_data= run_data[index,:].reshape(1,-1)
  print('optimal data:',optimal_data)
  if flag==0: 
     storage=optimal_data
     flag=1
  else: 
     storage= np.concatenate((storage,optimal_data),axis=0)

print('Shape of storage:',storage.shape)
#np.savetxt('best_designs.csv', storage,delimiter=',') 

best_designs=[]
for i in range(storage.shape[0]): 
   a= storage[i][6]
   first_y= storage[i][0]
   u = storage[i][7]
   k= storage[i][8]
   w= storage[i][9]
   name= "swordfish_a"+str(a)+'fy_'+str(first_y)+'u_'+str(u)+'k_'+str(k)+'w_'+str(w)+".stl"
   best_designs.append(name)

#print('best designs:', best_designs)

stl_files= os.listdir(stl_dump_loc)
print('stl files:',len(stl_files),'best designs:',len(best_designs))

c=set(best_designs) & set(stl_files)
print('c is:',c)

