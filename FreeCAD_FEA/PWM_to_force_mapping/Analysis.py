# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 15:56:03 2021

@author: maxim
"""

import PWM_to_force_V2 as PWM_force
import numpy as np
import reading_xyz_data_tilt_v2 as read_xyz
import matplotlib.pyplot as plt

act_1_120='Result_3_120N.csv'
act_1_240='Result_3_240N.csv'
act_1_360='Result_3_360N.csv'
act_1_480='Result_3_480N.csv'
act_1_600='Result_3_600N.csv'
FEM=[act_1_120,act_1_240,act_1_360,act_1_480,act_1_600]



act_0=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_00.xyz'
act_1A=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_1A.xyz'
act_1B=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_1B.xyz'
act_1C=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_1C.xyz'
act_1D=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_1D.xyz'

act_2A=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_2A.xyz'
act_2B=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_2B.xyz'
act_2C=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_2C.xyz'
act_2D=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_2D.xyz'

act_3A=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_3A.xyz'
act_3B=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_3B.xyz'
act_3C=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_3C.xyz'
act_3D=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_3D.xyz'

act_4A=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_4A.xyz'
act_4B=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_4B.xyz'
act_4C=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_4C.xyz'
act_4D=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_4D.xyz'

act_5A=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_5A.xyz'
act_5B=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_5B.xyz'
act_5C=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_5C.xyz'
act_5D=r'C:\Users\maxim\OneDrive\Documents\Imperial college Physics\Mirror Project\Interferometry data\5_Element_DM_XYZ_Data\5_Element_DM_Test_21_11_2020_5D.xyz'

# z_act_0=read_xyz.main(act_0)
# z_act_1A=read_xyz.main(act_1A,1)
# z_act_1B=read_xyz.main(act_1B,1)
# z_act_1C=read_xyz.main(act_1C,1)
# z_act_1D=read_xyz.main(act_1D,1)

# z_1=[z_act_0,z_act_1A,z_act_1B,z_act_1C,z_act_1D]

# z_act_0=read_xyz.main(act_0)
# z_act_2A=read_xyz.main(act_2A,2)
# z_act_2B=read_xyz.main(act_2B,2)
# z_act_2C=read_xyz.main(act_2C,2)
# z_act_2D=read_xyz.main(act_2D,2)

# z_2=[z_act_0,z_act_2A,z_act_2B,z_act_2C,z_act_2D]

z_act_0=read_xyz.main(act_0)
z_act_3A=read_xyz.main(act_3A,3)
z_act_3B=read_xyz.main(act_3B,3)
z_act_3C=read_xyz.main(act_3C,3)
z_act_3D=read_xyz.main(act_3D,3)

z_3=[z_act_0,z_act_3A,z_act_3B,z_act_3C,z_act_3D]
#%%
for i in range(len(z_3)):
    plt.figure(i)
    plt.imshow(z_3[i])
    plt.colorbar()

print(np.min(z_act_0[z_act_0>0]))

#%%
import PWM_to_force_V2 as PWM_force
FEM=[act_1_120,act_1_240,act_1_360,act_1_480,act_1_600]

PWM=[0,1024,2048,3072,4095]
forces=[120,240,360,480,600]


act_1_120='Result_1_120N.csv'
act_1_240='Result_1_240N.csv'
act_1_360='Result_1_360N.csv'
act_1_480='Result_1_480N.csv'
act_1_600='Result_1_600N.csv' 

act_3_120='Result_3_120N.csv'
act_3_240='Result_3_240N.csv'
act_3_360='Result_3_360N.csv'
act_3_480='Result_3_480N.csv'
act_3_600='Result_3_600N.csv'


FEM_3=[act_3_120,act_3_240,act_3_360,act_3_480,act_3_600]


act_3=PWM_force.PWM_to_force(FEM_3,z_3,PWM,forces,3)
force_test_3=PWM_force.PWM_force_output(act_3[0],act_3[1],4095)


#%%
#ft_2=PWM_force.PWM_force_output(act_2[0],act_2[1],4095)
#ft_4=PWM_force.PWM_force_output(act_2[0],act_4[1],4095)
#print(ft_2/2+ft_4/2)
#%%
force_test_3=PWM_force.PWM_force_output(act_3[0],act_3[1],4095)
print(force_test_3)


