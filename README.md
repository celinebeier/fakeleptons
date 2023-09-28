# fakeleptons

Welcome to the mess of code that was part of my Masters thesis. 

If you are a future possible employer: I would like to assure you I have learned from my mistakes some of which you can see here. I swear I will do better next time with code organisation.

If you are a student who for some reason now has to work with my code. Buckle up buddy, you're gonna have a bad time.

## General comments ##

- The data that this all works on, the ROOT files that are the output of the AnalysisTop code, is way too large to be stored here, it's in my CERN storage and will probably get deleted as soon as I finish my CERN membership, so good luck.
- Historically the code was developed for electrons and then adapted to muons. All files without _FakeM are the originals and work for electrons, everything with _FakeM is a copy of that adapted for muons. Yes, I should have renamed the original files but I didn't. Except for the composition ones, those are called FakeE.
- Everything with _PDF takes root files and makes nice PDF ROOT plots yay.
- Files with FakeN work for electrons and muons. 
- Everything in the pic/ folder is outdated, but documents my struggeling and looks nice so I'm keeping it. 

## Data Preparation ##

- Prep1_Data.py and Prep1_MC.py read in the root files and make them into csv files, this is done by year
- Prep2.py concats the different years them into a single csv file for each dataset
- Prep3.py selects the different regions and also saves that in a csv file
- They are meant to the run in the order above, the reason they are sepaprate files is because they can take really long to run and my computer crashes if I do all the steps in one file. 

## MC Weights ##

- MC_Weights.py does surprisingly exactly what you woul assume it does, it calculates MC weights!

## Calculation of the Fake Efficiency ##

- FakeEff.py calculates the FE for electrons
- FakeEff_FakeM.py for muons
- FakeEff_PDF.py makes pdf files

## 2d Fake Efficiency ##

- FakeEff2d.py makes the 2d projections for electrons 
- FakeEff2d_FakeM.py for muons 
- FakeEff2d_PDF.py plots it.

## Calculation of the Number of Fakes ##

- FakeE.py calculates the number of fakes for every region except the Zy CR
- FakeE_ZyCR.py takes care of that as it is the only 2 lepton region. 
- FakeM.py and FakeM_ZyCR.py work equivalently for muons. 
- FakeN_PDF.py plots for both electrons and muons

## Fake Lepton Composition ##

- FakeEComposition_CR.py makes the histograms for the electron coomposition in the fake efficiency CR
- FakeEComposition_SR.py does the same for VR and SR, this is a separate file because these regions are slightly different and I thought it would be easiest to make separate files.
- FakeMComposition_CR.py and FakeMComposition_SR.py do the same for muons. 
- FakeNComposition_PDF.py does the plotting.

## Results! ##

- Electron results are in the root/ folder, muon results in the root_FakeM/ folder.
- The sub folders, d0sig, IDMedium, IsoTight,... are the results for different cuts/ settinngs used to evaluate systematic uncertainties. 
- PNG files in the root/ folder are outdated, the PDFs are the new results. 
- And the .txt files have the fake estimates per bin, so probably what you're looking for.