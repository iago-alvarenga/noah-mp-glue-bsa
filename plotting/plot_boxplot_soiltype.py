import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vtypes  =  {'sandyloam':'Sandy Loam',
            'loam':'Loam',
            'sandyclay':'Sandy Clay Loam',
            'clayloam':'Clay Loam'}

stype_dic ={'sandyloam':3,
            'loam':6,
            'sandyclay':7,
            'clayloam':9}

variables={'smcmax':'SMCMAX',
           'smcref':'SMCREF',
           'smcwlt':'SMCWLT',
           'bb':'BB'}

values_dic={'sandyloam':{'smcmax':0.434,
                         'smcref' :0.312,
                         'smcwlt':0.047,
                         'bb'  :  4.47}, 
            'loam'     :{'smcmax':0.439,
                         'smcref' :0.329,
                         'smcwlt':0.066,
                         'bb'  :  5.25}, 
       'sandyclay'     :{'smcmax':0.404,
                         'smcref' :0.315,
                         'smcwlt':0.069,
                         'bb'  :  6.77},
       'clayloam'     :{'smcmax':0.465,
                         'smcref' :0.382,
                         'smcwlt':0.103,
                         'bb'  :  8.17}}

filtered_lhs=pd.read_hdf('../data/filtered_parameters_soil.h5','data')
fig, ax = plt.subplots(4,1,figsize=(6,8),sharex=True)


for n,var in enumerate(variables):
    df=pd.DataFrame()
    for v,vtype in enumerate(vtypes):
        param=filtered_lhs[filtered_lhs[f'nse_{vtype}']>filtered_lhs[f'nse_{vtype}'].quantile(0.995)]
        nse=filtered_lhs[f'nse_{vtype}'].quantile(0.995)
        df['{} \n (NSE: {:.2f})'.format(vtypes[vtype],nse)]=list(param[f'{var}_{stype_dic[vtype]}'])

        ax[n].scatter(v,values_dic[vtype][var],marker='x',color='r')
    
    sns.boxplot(ax=ax[n],data=df,boxprops={"facecolor": 'lightgrey'},medianprops={"color": "black"},width=0.5)
    ax[n].set_ylabel(variables[var])
    ax[n].yaxis.tick_right()

    ax[0].set_ylim(0.350,0.558)
    ax[1].set_ylim(0.035,0.558)
    ax[2].set_ylim(0.035,0.322)
    ax[3].set_ylim(2.31,15.48)

plt.subplots_adjust(hspace=0.2,top=0.95,bottom=0.06,left=0.05)
fig.savefig('../figures/box_plot_soil_type.jpg',dpi=1000)

