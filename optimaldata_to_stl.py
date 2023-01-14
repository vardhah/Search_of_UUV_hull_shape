#to change dir:  import os; os.chdir('/home/hv/harsh/uuv_body_study/UUV_body_study/')
#to run exe: exec(open('optimaldata_to_stl.py').read())




import numpy as np
import glob
import os
import mesh
sketch_params=[]

optimal_data = np.loadtxt('best_designs.csv',delimiter=',')

print('optimal data shape:',optimal_data.shape)



document= App.openDocument("/home/hv/harsh/uuv_body_study/UUV_body_study/cad_sim/seed_cad/free_hull.FCStd")

for c in sketch.Constraints:
   if c.Name:
      sketch_params.append(str(c.Name))
      print(str(c.Name))

def set_body(y_loc,rad_l=100):
      global document
      try:
        obj = document.getObject('Sketch')
       
        obj.setDatum('first_y', Units.Quantity(y_loc[0] , Units.Unit('mm')))
        obj.setDatum('second_y', Units.Quantity(y_loc[1] , Units.Unit('mm')))
        obj.setDatum('third_y', Units.Quantity(y_loc[2] , Units.Unit('mm')))
        obj.setDatum('fourth_y', Units.Quantity(y_loc[3] , Units.Unit('mm')))
      
        obj.setDatum('fifth_y', Units.Quantity(y_loc[4] , Units.Unit('mm')))
        obj.setDatum('sixth_y', Units.Quantity(y_loc[5] , Units.Unit('mm')))

        obj.setDatum('part_a', Units.Quantity(y_loc[6] , Units.Unit('mm')))
        obj.setDatum('part_b', Units.Quantity(1000-y_loc[6] , Units.Unit('mm'))) 
        obj.setDatum('radius', Units.Quantity(rad_l , Units.Unit('mm')))
        document.recompute()
      except: 
        print('failed in setting body y locations') 

def create_stl(self,a,first_y,u,k,w):  
        global document 
        try:
         __objs__=document.getObject("Body")
         stl_dumpfile= u"./stl_optimal/swordfish_a"+str(a)+'fy_'+str(first_y)+'u_'+str(u)+'k_'+str(k)+'w_'+str(w)+".stl"
         Mesh.export([__objs__], stl_dumpfile)
         del __objs__    
        except:
          print("An error occurred while creating stl file") 





for i in range(optimal_data.shape[0]):
    print(optimal_data[i,:])
    set_body(optimal_data[i,:])
    create_stl(optimal_data[i,6],optimal_data[i,0],optimal_data[i,7],optimal_data[i,8],optimal_data[i,9])
    
    
    
