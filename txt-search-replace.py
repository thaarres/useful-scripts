from ROOT import *
import fileinput

path = "/shome/thaarres/EXOVVAnalysisRunII/LimitCode/CMSSW_7_1_5/src/DijetCombineLimitCode/EXOVVSystematics/dijet/"

prefixDCin = "datacards_withPDFuncertainties/CMS_jj_"
prefixDCout = "datacards_newSF/CMS_jj_"

prefix = "EXOVVSystematics/dijet"

purities = ["LP","HP"]
channels = ["WW","WZ","ZZ"]
signals=["BulkWW","BulkZZ","WZ","ZprimeWW"]
masses_interpolated =[m*100 for m in range(12,40+1)]
# signals=["ZprimeWW"]
# channels = ["WW"]
# masses_interpolated = [1200]

oldHPSF = float(0.692*0.692)
newHPSF = float(0.951*0.951)
oldLPSF = float(1.00894) #0.692*1.458
newLPSF = float(0.951*1.261)


for purity in purities:
  if purity == "HP":
    oldSF = float(oldHPSF)
    newSF = float(newHPSF)
  elif purity == "LP":
    oldSF = float(oldLPSF)
    newSF = float(newLPSF)
    
  print "Replacing old %s SF = %f with new %s SF = %f" %(purity,oldSF,purity,newSF)    
  ii = -1
  for signal in signals:
    ii += 1
    for ch in channels:
        
      for m in masses_interpolated:
        print "Mass = %i: " %(m)
       
        fname_datacard_in = prefixDCin + "%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"
        fname_datacard_out = prefixDCout + "%s_%i"%(signal,m)+"_13TeV_CMS_jj_"+ch+purity+".txt"
        print "Input datacard:  %s" %fname_datacard_in
        print "Output datacard: %s"  %fname_datacard_out
        lines = []
        try:
          with open(fname_datacard_in) as infile:
            for line in infile:
              if not (line.find("rate")!=-1) and not line.find("# signal scaled") !=-1:
                lines.append(line)  
              if (line.find("rate")!=-1):  
                for token in line.split():
                  try:
                      # if this succeeds, you have your (first) float
                      if not (float(token)==0.0 or float(token)==1.0):
                        print token, "is float(!=0. and !=1.) and will be replaced"
                        newRate = float(float(token)/float(oldSF))
                        print "OLD rate = " ,float(token)
                        print "OLD SF   = " ,oldSF
                        newRate *=float(newSF)
                        print "NEW rate = " ,newRate
                        print "NEW SF = " ,newSF
                        print line
                        newRateLine = line.replace(token,"%.5f"%newRate)
                        print newRateLine
                        lines.append(newRateLine)
                  except ValueError:
                    print token, "Searching for floats"
        
              if line.find("# signal scaled") !=-1:
                print "Replacing SF %f with %f:" %(oldSF,newSF)
                print line
                newSFLine = line.replace("%.5f"%oldSF,"%f"%newSF)
                print newSFLine
                lines.append(newSFLine)
        except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
          print 'oops, datacard not found!'
        print "Writing to " ,fname_datacard_out
        with open(fname_datacard_out, 'w') as outfile:
          print "--------- PRINTING FULL DATACARD: ---------"; print "-------------------------------------------"
          for line in lines:
            # print line
            outfile.write(line)
          print "DONE!"
          print "-------------------------------------------"; print "-------------------------------------------"; print ""; print "";
      