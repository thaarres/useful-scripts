import os
from optparse import OptionParser
import ConfigParser

parser = OptionParser()
parser.add_option("-f",'--file', action="store",type="string",dest="infile",default="", help="My input")
(options, args) = parser.parse_args()

infile = options.infile

config = ConfigParser.ConfigParser()
config.read(infile)
nfiles = config.getint('JobsConfig','nfiles')
src = config.get('JobsConfig','src')
outdir = config.get('JobsConfig','outdir')
localjobdir = config.get('JobsConfig','localjobdir')
jobname = config.get('JobsConfig','jobname')
outfile = config.get('JobsConfig','outfile')
cmsswdir = config.get('JobsConfig','cmsswdir')
cfg = config.get('JobsConfig','cfg')
bashfile = config.get('JobsConfig','bashfile')
xmlfile = config.get('JobsConfig','xmlfile')
prefix = config.get('JobsConfig','prefix')
newdir = config.get('JobsConfig','newdir')

# assert (True==False),"File doesn't exist"
 

if not infile:
  print "ABORT! No CFG passed"
  os._exit(0)

inXML = infile.replace("cfg","xml")
file = open(inXML, 'r')

array = []
for line in file:
  if line.find("Jobs ID")!=-1:
    jobID = line.split("InputFiles=")[0].split("ID=")[1].replace("\"","")
    array.append(int(jobID))
file.close()

resubID = []
for i in array:
  fnameIN = "/pnfs/psi.ch/cms/trivcat/store/user/thaarres/%s/%s-%i/flatTuple.root" %(outdir,jobname,i)
  fnameOUT = "%s/%s_%i.root" %(newdir,prefix,i)
  if os.path.isfile(fnameOUT):
    # print "File exist, do not recopy!"
    continue
  if not os.path.isfile(fnameIN):
    print "File %s does not exist in your job temp! Resubmit!"  %fnameIN
    resubID.append(i)
    continue
  else:
    copyCMD = "gfal-copy srm://t3se01.psi.ch:8443/srm/managerv2?SFN="
    dest = "srm://t3se01.psi.ch:8443/srm/managerv2?SFN="
    cmd = "%s%s %s%s" %(copyCMD,fnameIN,dest,fnameOUT)
    print cmd
    os.system(cmd)

if resubID:
  print "Do:"
  print "python submitJobsOnT3batch.py -C %s -r %s" %(infile,resubID)

else:
  print "All your files should be copied!"  