#to change dir:  import os; os.chdir('/home/hv/harsh/uuv_body_study/UUV_body_study/')
#to run exe: exec(open('stl_to_image.py').read())


import os
import glob 
import Mesh

#stl_loc= u"/home/hv/harsh/uuv_body_study/UUV_body_study/cad_sim/stl_dump/"
#png_loc= "/home/hv/harsh/uuv_body_study/UUV_body_study/cad_sim/img_dump/"

stl_loc= "./stl_optimal2_processed/"
png_loc= "./img_optimal2/"


file_loc= stl_loc
#files = glob.glob(file_loc)
files= os.listdir(file_loc)
for f in files:
 print('f is:',f)
 stl_file=stl_loc+f
 Mesh.open(stl_file)
 App.setActiveDocument("Unnamed")
 App.ActiveDocument=App.getDocument("Unnamed")
 Gui.ActiveDocument=Gui.getDocument("Unnamed")
 Gui.SendMsgToActiveView("ViewFit")

 #save image
 img_name= png_loc+f+'.png'
 Gui.activeDocument().activeView().saveImage(img_name,1376,750,'Current')
 Gui.runCommand('Std_CloseActiveWindow',0)
 App.closeDocument("Unnamed")
