import pandas

csv='csv'
'''
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['SRSelection']==1)]
print(len(regMC_17))

print('saving VR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC_17.to_csv('/eos/user/c/cbeier/'+csv+'/SR_MC17_loose'+'.csv', index=False)

del regMC_17

regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_addMC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['SRSelection']==1)]
print(len(regMC_17))

print('saving VR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC_17.to_csv('/eos/user/c/cbeier/'+csv+'/SR_addMC17_loose'+'.csv', index=False)
'''
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_add2MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['SRSelection']==1)]
print(len(regMC_17))

print('saving VR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC_17.to_csv('/eos/user/c/cbeier/'+csv+'/SR_add2MC17_loose'+'.csv', index=False)
'''
######
print('here')
regMC_18_part=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC18_loose'+'.csv')
print('here')

regMC_18_VR=regMC_18_part[(regMC_18_part['VRSelection']==1)]
regMC_18_VR.to_csv('/eos/user/c/cbeier/'+csv+'/VR_MC18_loose'+'.csv', index=False)
regMC_18_SR=regMC_18_part[(regMC_18_part['SRSelection']==1)]
regMC_18_SR.to_csv('/eos/user/c/cbeier/'+csv+'/SR_MC18_loose'+'.csv', index=False)
regMC_18_WyCR=regMC_18_part[(regMC_18_part['WyCRSelection']==1)]
regMC_18_WyCR.to_csv('/eos/user/c/cbeier/'+csv+'/WyCR_MC18_loose'+'.csv', index=False)
regMC_18_WjetsCR=regMC_18_part[(regMC_18_part['WjetsCRSelection']==1)]
regMC_18_WjetsCR.to_csv('/eos/user/c/cbeier/'+csv+'/WjetsCR_MC18_loose'+'.csv', index=False)
regMC_18_ZyCR=regMC_18_part[(regMC_18_part['ZyCRSelection']==1)]
regMC_18_ZyCR.to_csv('/eos/user/c/cbeier/'+csv+'/ZyCR_MC18_loose'+'.csv', index=False)
regMC_18_ZjetsCR=regMC_18_part[(regMC_18_part['ZjetsCRSelection']==1)]
regMC_18_ZjetsCR.to_csv('/eos/user/c/cbeier/'+csv+'/ZjetsCR_MC18_loose'+'.csv', index=False)

del regMC_18_part, regMC_18_VR, regMC_18_SR, regMC_18_WyCR, regMC_18_WjetsCR, regMC_18_ZyCR, regMC_18_ZjetsCR
'''
######
'''
print('reading in VR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['VRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['VRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['VRSelection']==1)]
print(len(regdata_18))

print('concating VR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving VR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/VR_Data_loose'+'.csv', index=False)

print('reading in VR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['VRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['VRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/VR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating VR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving VR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/VR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC

###################

print('reading in SR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['SRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['SRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['SRSelection']==1)]
print(len(regdata_18))

print('concating SR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving SR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/SR_Data_loose'+'.csv', index=False)

print('reading in SR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['SRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['SRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/SR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating SR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving SR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/SR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC


###################

print('reading in WyCR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['WyCRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['WyCRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['WyCRSelection']==1)]
print(len(regdata_18))

print('concating WyCR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving WyCR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/WyCR_Data_loose'+'.csv', index=False)

print('reading in WyCR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['WyCRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['WyCRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/WyCR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating WyCR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving WyCR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/WyCR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC

###############

print('reading in WjetsCR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['WjetsCRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['WjetsCRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['WjetsCRSelection']==1)]
print(len(regdata_18))

print('concating WjetsCR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving WjetsCR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/WjetsCR_Data_loose'+'.csv', index=False)

print('reading in WjetsCR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['WjetsCRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['WjetsCRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/WjetsCR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating WjetsCR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving WjetsCR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/WjetsCR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC

###################

print('reading in ZyCR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['ZyCRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['ZyCRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['ZyCRSelection']==1)]
print(len(regdata_18))

print('concating ZyCR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving ZyCR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/ZyCR_Data_loose'+'.csv', index=False)

print('reading in ZyCR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['ZyCRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['ZyCRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/ZyCR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating ZyCR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving ZyCR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/ZyCR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC

###############

print('reading in ZjetsCR data')
regdata_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data16_loose'+'.csv')
regdata_16=regdata_16[(regdata_16['ZjetsCRSelection']==1)]
print(len(regdata_16))
regdata_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data17_loose'+'.csv')
regdata_17=regdata_17[(regdata_17['ZjetsCRSelection']==1)]
print(len(regdata_17))
regdata_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_Data18_loose'+'.csv')
regdata_18=regdata_18[(regdata_18['ZjetsCRSelection']==1)]
print(len(regdata_18))

print('concating ZjetsCR data')
regdata=pandas.concat([regdata_16,regdata_17,regdata_18])

print('saving ZjetsCR data')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regdata.to_csv('/eos/user/c/cbeier/'+csv+'/ZjetsCR_Data_loose'+'.csv', index=False)
'''
'''
print('reading in ZjetsCR MC')
regMC_16=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC16_loose'+'.csv')
regMC_16=regMC_16[(regMC_16['ZjetsCRSelection']==1)]
print(len(regMC_16))
regMC_17=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/Regions_MC17_loose'+'.csv')
regMC_17=regMC_17[(regMC_17['ZjetsCRSelection']==1)]
print(len(regMC_17))
regMC_18=pandas.read_csv('/eos/user/c/cbeier/'+csv+'/ZjetsCR_MC18_loose'+'.csv')
print(len(regMC_18))

print('concating ZjetsCR MC')
regMC=pandas.concat([regMC_16,regMC_17,regMC_18])

print('saving ZjetsCR MC')
#tight.to_csv('csv/'+name+'_tight'+'.csv', index=False)
regMC.to_csv('/eos/user/c/cbeier/'+csv+'/ZjetsCR_MC_loose'+'.csv', index=False)

del regdata_16, regdata_17, regdata_18, regMC_16, regMC_17, regMC_18, regdata, regMC
'''