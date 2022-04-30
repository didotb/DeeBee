import wget, os, multiprocessing as mp, time as tm
from os import path

config = './weather/irgmsw.cfg'
filenames = './weather/filenames.txt'
imageDIR = './weather/img/'
target = "./out.mp4"

def weather( time='latest' ):
  if( time == 'latest' ):
    configURL = 'https://www.goes.noaa.gov/sohemi/sohemiloops/irgmsw.cfg'
    baseURL = 'https://www.goes.noaa.gov/sohemi/sohemiloops/'

    if( os.listdir( imageDIR ) != [] ):
      os.system( "rm " + imageDIR + "*" )
    if( path.exists( config ) ):
      os.system( "rm " + config )

    wget.download( configURL, config )
    os.system( "cat " + config + " | grep 'filenames = ' | sed 's|filenames = ||' > " + filenames )

    p = mp.Pool(mp.cpu_count())
    with open( filenames ) as names:
      for i in names:
        temp = i.strip('\n').split( ', ' )
        p.map(dl_start, [[str(baseURL+i)] for i in temp])
      names.close()
    p.close()

    imageFiles = [os.path.join(imageDIR,files) for files in os.listdir(imageDIR)]
    c=0
    for i in imageFiles:
      os.rename(i,str(os.path.join(imageDIR,"0"+str(c)+".jpg")))
      c+=1
    os.system( "ffmpeg -i " + imageDIR + "0%d.jpg -c:v libx264 -pix_fmt yuv420p -an -filter_complex '[0]setpts=3*PTS' -preset veryfast -y " + target )

def dl_start(frames):
  for j in frames:
    os.system("wget -P "+imageDIR+" "+j)

def clean():
	if path.exists( target ): os.system( "rm " + target )
	if path.exists( imageDIR ): os.system( "rm " + imageDIR + "*" )
	if path.exists( filenames ): os.system( "rm " + filenames )
	if path.exists( config ): os.system( "rm " + config )