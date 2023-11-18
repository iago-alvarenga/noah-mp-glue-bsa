import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

vtypes  ={'sav':'Savannas',
          'wsa':'Woody Savannas',
          'gld':'Grasslands',
          'shr':'Open Shrublands'}

variables={'vcmx':'VCMX25',
           'rmf':'RMF25',
           'dilefw':'DILEFW',
           'ltovrc':'LTOVRC',
           'sla':'SLA'}


values_dic={'sav':{'ltovrc':0.65,
                   'dilefw':0.50,
                   'rmf' :0.80,
                   'sla'   :  50,
                   'vcmx'  :  40}, 
            'wsa':{'ltovrc':0.65,
                   'dilefw':0.20,
                   'rmf' :0.26,
                   'sla'   :  60,
                   'vcmx'  :  40},
            'gld':{'ltovrc':0.50,
                   'dilefw':0.10,
                   'rmf' :1.80,
                   'sla'   :  60,
                   'vcmx'  :  40}, 
            'shr':{'ltovrc':0.65,
                   'dilefw':0.20,
                   'rmf' :0.26,
                   'sla'   :  60,
                   'vcmx'  :  40}}

filtered_lhs=pd.read_hdf('../data/filtered_parameters.h5','data')

fig, ax = plt.subplots(5,1,figsize=(6,8),sharex=True)

df=pd.DataFrame()
for n,var in enumerate(variables):
    for v,vtype in enumerate(vtypes):
        param=filtered_lhs[filtered_lhs[f'nse_{vtype}']>filtered_lhs[f'nse_{vtype}'].quantile(0.995)]
        nse=filtered_lhs[f'nse_{vtype}'].quantile(0.995)
        df['{} \n (NSE: {:.2f})'.format(vtypes[vtype],nse)]=list(param[var])
        ax[n].scatter(v,values_dic[vtype][var],marker='x',color='r')
  


    sns.boxplot(ax=ax[n],data=df,boxprops={"facecolor": 'lightgrey'},medianprops={"color": "black"},width=0.5)
    ax[n].set_ylabel(variables[var])
    ax[n].yaxis.tick_right()

    ax[0].set_ylim(10, 100)
    ax[1].set_ylim(0, 3)
    ax[2].set_ylim(0, 1)
    ax[3].set_ylim(0, 2)
    ax[4].set_ylim(10, 90)
    
plt.subplots_adjust(hspace=0.2,top=0.95,bottom=0.06,left=0.05)
fig.savefig('../figures/box_plot_vegtype.jpg',dpi=1000)

