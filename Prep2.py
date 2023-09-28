import pandas

csv='csv_FakeM'

print('reading in data')
data_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Data16_loose'+'.csv')
print(len(data_16))
data_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Data17_loose'+'.csv')
print(len(data_17))
data_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Data18_loose'+'.csv')
print(len(data_18))

print('concating data')
data=pandas.concat([data_16,data_17,data_18])

print('saving data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
data.to_csv('/eos/user/c/cbeier/'+csv+'/Data_loose'+'.csv', index=False)


print('reading in WZ')
WZ_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/WZ16_loose'+'.csv')
print(WZ_16['weight'].sum())
WZ_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/WZ17_loose'+'.csv')
print(WZ_17['weight'].sum())
WZ_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/WZ18_loose'+'.csv')
print(WZ_18['weight'].sum())

print('concating WZ')
WZ=pandas.concat([WZ_16,WZ_17,WZ_18])

print('saving WZ')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
WZ.to_csv('/eos/user/c/cbeier/'+csv+'/WZ_loose'+'.csv', index=False)


print('reading in MC')
MC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/MC16_loose'+'.csv')
print(MC_16['weight'].sum())
MC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/MC17_loose'+'.csv')
print(MC_17['weight'].sum())
MC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/MC18_loose'+'.csv')
print(MC_18['weight'].sum())

print('concating MC')
MC=pandas.concat([MC_16,MC_17,MC_18])

print('saving MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
MC.to_csv('/eos/user/c/cbeier/'+csv+'/MC_loose'+'.csv', index=False)

'''
print('reading in regions data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_Data16_loose'+'.csv')
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_Data17_loose'+'.csv')
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_Data18_loose'+'.csv')
print(len(regdata_18))

print('concating regions data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving regions data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/csv/Regions_Data_loose'+'.csv', index=False)

print('reading in regions MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_MC16_loose'+'.csv')
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_MC17_loose'+'.csv')
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/csv/Regions_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating regions MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving regions data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/csv/Regions_MC_loose'+'.csv', index=False)
'''