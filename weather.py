import wget, os, multiprocessing as mp#, time as tm
from functools import partial
from os import path

target = "./out.mp4"

configSRC = {
  'sw':'https://www.goes.noaa.gov/sohemi/sohemiloops/irgmsw.cfg',
  'nw':'https://www.goes.noaa.gov/dimg/jma/nhem/nwpac/txtfiles/rb_names.txt'
}

imageSRC = {
  'sw':'https://www.goes.noaa.gov/sohemi/sohemiloops/',
  'nw':'http://www.ssd.noaa.gov/jma/nwpac/'
}

region = {
  'sw':'./weather/img/sw/',
  'nw':'./weather/img/nw/'
}

config = {
  'sw':'./weather/irgmsw.cfg',
  'nw':'./weather/rb_names.txt'
}

filenames = {
  'sw':'./weather/filesw.txt',
  'nw':'./weather/filenw.txt'
}

class SwitcherNoneType(Exception):
  pass

def weather( regionCode='sw' ):
  regionDIR = region.get(regionCode,None)
  configDIR = config.get(regionCode,None)
  filenameList = filenames.get(regionCode,None)
  configURL = configSRC.get(regionCode,None)
  baseURL = imageSRC.get(regionCode,None)

  if regionDIR is None:
    raise SwitcherNoneType("regionCode not found or out of bounds.")
  if configDIR is None:
    raise SwitcherNoneType("Configuration directory is missing.")
  if filenameList is None:
    raise SwitcherNoneType("List of filename is missing in directory.")
  if configURL is None:
    raise SwitcherNoneType("Configuration URL cannot be found.")
  if baseURL is None:
    raise SwitcherNoneType("Base URL for images not specified.")

  if( os.listdir( regionDIR ) != [] ):
    os.system( "rm " + regionDIR + "*" )
  if( path.exists( configDIR ) ):
    os.system( "rm " + configDIR )

  wget.download( configURL, configDIR )

  if regionCode == 'nw':
    os.system(f"cat {configDIR} | cut -d ' ' -f1 > {filenameList}")
  if regionCode == 'sw':
    os.system( f"cat {configDIR} | grep 'filenames = ' | sed 's|filenames = ||' > {filenameList}.temp" )
    with open(filenameList,'w') as f:
      for line in [i.strip('\n').split(', ') for i in open(f"{filenameList}.temp")][0]:
        f.write(f"{line}\n")
    os.system(f"rm {filenameList}.temp")

  names = list(map(str,open(filenameList)))
  p = mp.Pool(mp.cpu_count())
  part = partial(dl_start, regionDIR)
  p.map(part,[[str(baseURL+i)] for i in [names[j].strip('\n') for j in range(0,len(names))]])
  p.close()

  imageFiles = [os.path.join(regionDIR,files) for files in os.listdir(regionDIR)]
  c=0
  for i in imageFiles:
    if regionCode == 'sw':
      os.rename(i,str(os.path.join(regionDIR,f"0{str(c)}.jpg")))
    if regionCode == 'nw':
      os.system(f"ffmpeg -i {i} -c:v mjpeg {regionDIR}0{str(c)}.jpg")
      #os.rename(i,str(os.path.join(regionDIR,f"0{str(c)}.jpg")))
    c+=1
  os.system( f"ffmpeg -i {regionDIR}0%d.jpg -c:v libx264 -pix_fmt yuv420p -an -filter_complex '[0]setpts=3*PTS' -preset veryfast -y {target}" )
  clean(regionCode)

def dl_start(regionDIR, frames):
  for j in frames:
    os.system("wget -P "+regionDIR+" "+j)

def clean(pathCode):
  if pathCode != "target":
    if path.exists(region.get(pathCode)): os.system("rm "+region.get(pathCode)+"*")
    if path.exists(filenames.get(pathCode)): os.system("rm "+filenames.get(pathCode))
    if path.exists(config.get(pathCode)): os.system( "rm "+config.get(pathCode))
  elif path.exists(target) and pathCode == "target": os.system("rm "+target)
  else: return