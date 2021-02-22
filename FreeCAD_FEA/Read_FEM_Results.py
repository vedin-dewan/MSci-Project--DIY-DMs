# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



#%% Reading in csv file
file="/Users/vedindewan/Desktop/MSci Project (AO)/FEM/Result(50mm_circular)_0.5-1.csv" #path for file
pd_df = pd.read_csv(file,header=None,encoding ='utf-8' ,dtype='a')
#Original Location of points
z_point=pd_df.iloc[1:,17].tolist()
z_point=[float(i) for i in z_point]

x_point=pd_df.iloc[1:,16].tolist()
x_point=[float(i) for i in x_point]

y_point=pd_df.iloc[1:,15].tolist()
y_point=[float(i) for i in y_point]

#displacement of points in the z-direction/normal to mirror surface
z_disp=pd_df.iloc[1:,2].tolist()
z_disp=[float(i) for i in z_disp]

# Finding points just on the surface of the mirror and their displacement (i.e where z_point=0)
indices=np.where(np.isclose(z_point, 0.0, 0.000001))#last argument is the tolerence
indices=indices[0]#quirk of np.where

x_point_surf=np.take(x_point,indices)
y_point_surf=np.take(y_point,indices)
z_disp=np.take(z_disp,indices)



#3D PLOT OF SURFACE

fig=plt.figure(1)
Z=z_disp
X=x_point_surf
Y=y_point_surf
mycmap = plt.get_cmap('viridis')
ax = plt.axes(projection='3d')
surf=ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False, cmap=mycmap)
#ax.view_init(60, 35)
ax.set_title('mirror surface 50mm (609.75N force by each actuator)')
ax.set_xlabel('x(mm)')
ax.set_ylabel('y(mm)')
ax.set_zlabel('z(mm)')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=15)

