# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:00:17 2021

@author: maxim
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zernike_polynomials as zp
import scipy.optimize as opt


def read_FEM(file):
    pd_df = pd.read_csv(file,header=None,encoding ='utf-8' ,dtype='a')
#Original Location of points
    z_point=pd_df.iloc[1:,17].tolist()
    z_point=[float(i) for i in z_point]

    x_point=pd_df.iloc[1:,15].tolist()
    x_point=[float(i) for i in x_point]

    y_point=pd_df.iloc[1:,16].tolist()
    y_point=[float(i) for i in y_point]

#displacement of points in the z-direction/normal to mirror surface
    z_disp=pd_df.iloc[1:,2].tolist()
    z_disp=[float(i) for i in z_disp]

# Finding points just on the surface of the mirror and their displacement (i.e where z_point=0)
    indices=np.where(np.isclose(z_point, 0.000, 0.000001))#last argument is the tolerence
    # indices=np.where(z_point ==0)
    indices=indices[0]#quirk of np.where

    x_point_surf=np.take(x_point,indices)
    y_point_surf=np.take(y_point,indices)
    z_disp=np.take(z_disp,indices)
    
    X=x_point_surf
    Y=y_point_surf
    Z=z_disp
    
    combined = np.vstack((X,Y,Z)).T
    
    x_range=int(np.round(np.max(X)-np.min(X)))
    y_range=int(np.round(np.max(Y)-np.min(Y)))
   

    z_2d=np.zeros((x_range+1,y_range+1))
    for i in range(len(combined)):
        y=int(np.round(combined[i,1])+25)
        x=int(np.round(combined[i,0])+25)
      
        z_2d[y,x]=combined[i,2]
    # plt.figure(1)
    # plt.imshow(z_2d)
    # fig=plt.figure(1)
    # Z=z_disp
    # X=x_point_surf
    # Y=y_point_surf
    # plt.figure(2)
    # mycmap = plt.get_cmap('viridis')
    # ax = plt.axes(projection='3d')

    # surf=ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False, cmap=mycmap)
    # ax.view_init(90, 0)
    # ax.set_title('mirror surface 50mm (609.75N force by each actuator)')
    # ax.set_xlabel('x(mm)')
    # ax.set_ylabel('y(mm)')
    # ax.set_zlabel('z(mm)')
    # fig.colorbar(surf, ax=ax, shrink=0.5, aspect=15)
    

    return z_2d

def zernike_decomposition(z,fig_number):
    popt=[]
    z_data=z#
    
    # plt.figure(1)
    # plt.imshow(z_data)
    x_len=len(z_data)
    y_len=len(z_data[0])
    # print(x_len)
    # print(y_len)
    x=np.linspace(-1,1,x_len)
    y=np.linspace(-1,1,y_len)
    z_x=np.tile(x,(len(y),1))
    #Z=np.vstack((x,y))
    Zernike_func=[zp.Zneg1_1,zp.Z1_1,zp.Zneg2_2,zp.Z0_2,zp.Z2_2,zp.Zneg3_3,zp.Zneg1_3,zp.Z1_3,zp.Z3_3,zp.Zneg4_4,zp.Zneg2_4,zp.Z0_4,zp.Z2_4,zp.Z4_4]
    for i in range(len(Zernike_func)):
        ZF=Zernike_func
        
        # Z=ZF[i](x,y,1,0,1)
        # plt.figure(3+i)
        # plt.imshow(Z)
        #print(len(Z.ravel()))
        def _ZF(M,radius,phase,amp):
            x=z_x[0]
            y=np.linspace(-1,1,len(z_x))
            Z_new=ZF[i](x,y,radius,phase,amp)
            return Z_new.ravel()
        
        p0=[1,0,1]
        popt_i,pcov_i=opt.curve_fit(_ZF,z_x,z_data.ravel(),p0)
        
        popt.append(popt_i)
        print(popt_i)
    z_guess=np.zeros((x_len,y_len))
    for i in range(len(Zernike_func)):
        z_guess+=Zernike_func[i](x,y,popt[i][0],popt[i][1],popt[i][2])
    
    z_guess_max=np.max(z_guess)
    z_guess_norm=z_guess/z_guess_max
    plt.figure(fig_number)
    plt.imshow(z_guess_norm)
    plt.colorbar()
    plt.title('added zernike terms')
    return popt,z_guess


