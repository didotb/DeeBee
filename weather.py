import wget
import os
from os import path

config = './weather/irgmsw.cfg'
filenames = './weather/filenames.txt'
imageDIR = './weather/img/'
target = "./out.mp4"

def weather( time='latest' ):
  if( time == 'latest' ):
    configURL = 'https://www.goes.noaa.gov/sohemi/sohemiloops/irgmsw.cfg'
    baseURL = 'https://www.goes.noaa.gov/sohemi/sohemiloops/'
    k = 0

    if( os.listdir( imageDIR ) != [] ):
      os.system( "rm " + imageDIR + "*" )
    if( path.exists( config ) ):
      os.system( "rm " + config )

    wget.download( configURL, config )
    os.system( "cat " + config + " | grep 'filenames = ' | sed 's|filenames = ||' > " + filenames )

    with open( filenames ) as names:
      for i in names:
        temp = i.strip('\n').split( ', ' )
        for j in temp:
          k = k + 1
          directory = imageDIR + "0" + str( k ) + ".jpg"
          os.system( "wget -O " + directory + " " + baseURL + j )
      names.close()

    os.system( "ffmpeg -i " + imageDIR + "0%d.jpg -c:v libx264 -pix_fmt yuv420p -an -filter_complex '[0]setpts=3*PTS' -preset veryfast -y " + target )

def clean():
	if path.exists( target ): os.system( "rm " + target )
	if path.exists( imageDIR ): os.system( "rm " + imageDIR + "*" )
	if path.exists( filenames ): os.system( "rm " + filenames )
	if path.exists( config ): os.system( "rm " + config )