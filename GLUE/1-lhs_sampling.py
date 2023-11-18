import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import LHS

rmf=[0, 1]
vcmx=[0, 1]
dilefw=[0, 1]
ltovrc=[0, 1]
sla=[0, 1]
qe=[0, 1]
bb=[0, 1]
smcdry=[0, 1]
smcmax=[0, 1]
smcref=[0, 1]
smcwlt=[0, 1]

xlimits = np.array([rmf, vcmx, dilefw,ltovrc,sla,qe,bb,smcdry,smcmax,smcref,smcwlt])
sampling = LHS(xlimits=xlimits)

num = 5000
x = sampling(num)

print(x.shape)

df = pd.DataFrame(x)

df.columns = ['rmf_frac', 'vcmx_frac', 'dilefw_frac','ltovrc_frac','sla_frac','qe_frac','bb_frac','smcdry_frac','smcmax_frac','reffrac','wltfrac']

# Ranges
rmf_range=[0, 3] 
vcmx_range=[10, 100]
dilefw_range=[0, 1]
ltovrc_range=[0,2]
sla_range=[10,90]
qe_range=[0.04,0.18]

smcmax_range_2=[0.35,0.442] #loamy sand
smcmax_range_3=[0.357,0.469] #sandy loam
smcmax_range_6=[0.38,0.5] #loam
smcmax_range_7=[0.362,0.47] #sandy clay loam
smcmax_range_9=[0.396,0.502] #clay loam
smcmax_range_12=[0.454,0.558] #clay

smcwlt_range_2=[0.035,0.079]
smcwlt_range_3=[0.036,0.126]
smcwlt_range_6=[0.092,0.164]
smcwlt_range_7=[0.126,0.21]
smcwlt_range_9=[0.158,0.234]
smcwlt_range_12=[0.238,0.322]

bb_range_2=[2.31,6.21]
bb_range_3=[3.34,6.14]
bb_range_6=[3.59,6.91]
bb_range_7=[3.38,10.16]
bb_range_9=[4.43,11.91]
bb_range_12=[7.62,15.48]

df['smcmax_2']=df['smcmax_frac']*(smcmax_range_2[1]-smcmax_range_2[0])+smcmax_range_2[0]
df['smcmax_3']=df['smcmax_frac']*(smcmax_range_3[1]-smcmax_range_3[0])+smcmax_range_3[0]
df['smcmax_6']=df['smcmax_frac']*(smcmax_range_6[1]-smcmax_range_6[0])+smcmax_range_6[0]
df['smcmax_7']=df['smcmax_frac']*(smcmax_range_7[1]-smcmax_range_7[0])+smcmax_range_7[0]
df['smcmax_9']=df['smcmax_frac']*(smcmax_range_9[1]-smcmax_range_9[0])+smcmax_range_9[0]
df['smcmax_12']=df['smcmax_frac']*(smcmax_range_12[1]-smcmax_range_12[0])+smcmax_range_12[0]

df['smcwlt_2']=df['wltfrac']*(smcwlt_range_2[1]-smcwlt_range_2[0])+smcwlt_range_2[0]
df['smcwlt_3']=df['wltfrac']*(smcwlt_range_3[1]-smcwlt_range_3[0])+smcwlt_range_3[0]
df['smcwlt_6']=df['wltfrac']*(smcwlt_range_6[1]-smcwlt_range_6[0])+smcwlt_range_6[0]
df['smcwlt_7']=df['wltfrac']*(smcwlt_range_7[1]-smcwlt_range_7[0])+smcwlt_range_7[0]
df['smcwlt_9']=df['wltfrac']*(smcwlt_range_9[1]-smcwlt_range_9[0])+smcwlt_range_9[0]
df['smcwlt_12']=df['wltfrac']*(smcwlt_range_12[1]-smcwlt_range_12[0])+smcwlt_range_12[0]

df['smcref_2']= (df['smcmax_2']-df['smcwlt_2'])*df['reffrac']+df['smcwlt_2']
df['smcref_3']= (df['smcmax_3']-df['smcwlt_3'])*df['reffrac']+df['smcwlt_3']
df['smcref_6']= (df['smcmax_6']-df['smcwlt_6'])*df['reffrac']+df['smcwlt_6']
df['smcref_7']= (df['smcmax_7']-df['smcwlt_7'])*df['reffrac']+df['smcwlt_7']
df['smcref_9']= (df['smcmax_9']-df['smcwlt_9'])*df['reffrac']+df['smcwlt_9']
df['smcref_12']= (df['smcmax_12']-df['smcwlt_12'])*df['reffrac']+df['smcwlt_12']

df['smcdry_2']=df['smcwlt_2']
df['smcdry_3']=df['smcwlt_3']
df['smcdry_6']=df['smcwlt_6']
df['smcdry_7']=df['smcwlt_7']
df['smcdry_9']=df['smcwlt_9']
df['smcdry_12']=df['smcwlt_12']

df['bb_2']=df['bb_frac']*(bb_range_2[1]-bb_range_2[0])+bb_range_2[0]
df['bb_3']=df['bb_frac']*(bb_range_3[1]-bb_range_3[0])+bb_range_3[0]
df['bb_6']=df['bb_frac']*(bb_range_6[1]-bb_range_6[0])+bb_range_6[0]
df['bb_7']=df['bb_frac']*(bb_range_7[1]-bb_range_7[0])+bb_range_7[0]
df['bb_9']=df['bb_frac']*(bb_range_9[1]-bb_range_9[0])+bb_range_9[0]
df['bb_12']=df['bb_frac']*(bb_range_12[1]-bb_range_12[0])+bb_range_12[0]

df['sla']=df['sla_frac']*(sla_range[1]-sla_range[0])+sla_range[0]
df['rmf']=df['rmf_frac']*(rmf_range[1]-rmf_range[0])+rmf_range[0]
df['dilefw']=df['dilefw_frac']*(dilefw_range[1]-dilefw_range[0])+dilefw_range[0]
df['ltovrc']=df['ltovrc_frac']*(ltovrc_range[1]-ltovrc_range[0])+ltovrc_range[0]
df['vcmx']=df['vcmx_frac']*(vcmx_range[1]-vcmx_range[0])+vcmx_range[0]
df['qe']=df['qe_frac']*(qe_range[1]-qe_range[0])+qe_range[0]

df.to_csv ('../data/scenarios_lhs.csv', index=False, header=True)