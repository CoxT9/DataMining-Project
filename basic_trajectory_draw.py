"""
A Hurricane Trajectory-Rendering script based on examples from matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.basemap import Basemap

def drawTrajectory():
  fraction = int(sys.argv[2])
  # Lambert Conformal Conic map.
  m = Basemap(llcrnrlon=-100.,llcrnrlat=0.,urcrnrlon=-20.,urcrnrlat=57.,
              projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
              resolution ='l',area_thresh=1000.)
  # read shapefile.
  with open(sys.argv[1], 'r') as inputFile:
    i = 0
    for line in inputFile.readlines():
      if i % fraction == 0: # Render 1 in fraction trajectories (nonzero)
        lineVector = line.split(' ')[1].split(",")[:-1]

        parsedVector = [item.replace("(", "").replace(")", "") for item in lineVector]
        trajectoryVector = [ (float(item.split(":")[0]), float(item.split(":")[1])) for item in parsedVector]

        gisXCoords = []
        gisYCoords = []
        for coord in trajectoryVector:
          newCoord = m(coord[1], coord[0]) # Flip the input coordinates only on conversion
          gisXCoords.append(int(newCoord[0]))
          gisYCoords.append(int(newCoord[1]))

        m.plot(gisXCoords, gisYCoords, linewidth=0.5, color='r')
      
      i += 1

  m.drawcoastlines()
  m.drawcountries()
  m.drawmapboundary(fill_color='#99ffff')
  m.fillcontinents(color='#cc9966',lake_color='#99ffff')
  m.drawparallels(np.arange(10,70,20),labels=[1,1,0,0])
  m.drawmeridians(np.arange(-100,0,20),labels=[0,0,0,1])
  plt.title('Atlantic Hurricane Tracks')
  plt.show()

def main():
  if len(sys.argv) != 3:
    print "Usage: {0} <VectorsInput> <FilterFraction>".format(sys.argv[0])
  else:
    drawTrajectory()

if __name__ == '__main__':
  main()
else:
  print __name__