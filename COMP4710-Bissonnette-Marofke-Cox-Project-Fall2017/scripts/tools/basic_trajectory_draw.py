"""
A Hurricane Trajectory-Rendering script based on examples from matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.basemap import Basemap
from apriori_utils import *
from matplotlib.patches import Rectangle 

def drawTrajectory():
  fraction = int(sys.argv[2])
  showRegions = bool(int(sys.argv[3]))
  # Lambert Conformal Conic map.
  m = Basemap(llcrnrlon=-101.,llcrnrlat=-5.5,urcrnrlon=-0.,urcrnrlat=50.9,
              projection='lcc',lat_1=0.,lat_2=39.,lon_0=-60.,
              resolution ='l',area_thresh=1000.)
  # read shapefile.
  # Need to write a longtitudional line as opposed to a euclidean horizontal line

  with open(sys.argv[1], 'r') as inputFile:
    i = 0
    for line in inputFile.readlines():
      color = 'r'
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

        m.plot(gisXCoords, gisYCoords, linewidth=1.0, color=color)
      i += 1


  with open(sys.argv[4], 'r') as otherInput:
    i = 0
    for line in otherInput.readlines():
      if True or i % fraction == 0: # Render 1 in fraction trajectories (nonzero)
        lineVector = line.split(' ')[1].split(",")[:-1]

        parsedVector = [item.replace("(", "").replace(")", "") for item in lineVector]
        trajectoryVector = [ (float(item.split(":")[0]), float(item.split(":")[1])) for item in parsedVector]
        gisXCoords = []
        gisYCoords = []
        for coord in trajectoryVector:
          newCoord = m(coord[1], coord[0]) # Flip the input coordinates only on conversion
          gisXCoords.append(int(newCoord[0]))
          gisYCoords.append(int(newCoord[1]))

        m.plot(gisXCoords, gisYCoords, linewidth=1.0, color='b')
      i += 1

  m.drawcoastlines()
  m.drawmapboundary(fill_color='#99ffff')
  m.fillcontinents(color='#cc9966',lake_color='#99ffff')
  m.drawparallels(np.arange(0,60,10),labels=[1,0,0,0])
  m.drawmeridians(np.arange(-100,-10,10),labels=[0,0,0,1])

  # m.drawmeridians(np.arange(-100, -10, 80),dashes=[1,0],color=(0, 0, 0),linewidth=2)
  # m.drawparallels(np.arange(0, 60, 50),dashes=[1,0],color=(0, 0, 0),linewidth=2)
  # lat = [the list of lat coordinates here] 
  # lon = [the list of lon coordinates here] 

  # x, y = m(lon, lat)
  # m.plot(x, y, 'o-', markersize=5, linewidth=1)


  lat = [50, 50]
  lon = [-100, -20]
  x, y = m(lon, lat)
  #m.plot(x, y, 'o-', markersize=5, linewidth=2, color=(0, 0, 0))
# xs = [lower_left[0], upper_left[0],
#           lower_right[0], upper_right[0],
#           lower_left[0], lower_right[0],
#           upper_left[0], upper_right[0]]
#     ys = [lower_left[1], upper_left[1],
#           lower_right[1], upper_right[1],
#           lower_left[1], lower_right[1],
#           upper_left[1], upper_right[1]]
#     bmap.plot(xs, ys, latlon = True)

  lat = [0, 0]
  lon = [-100, -20]
  x, y = m(lon, lat)
#  m.plot(x, y, 'o-', markersize=5, linewidth=2, color=(0, 0, 0),latlon=True)
 # m.drawparallels(range(0, 51, 50), linewidth=2, dashes=[1, 0], labels=[0,0,0,0], color=(0,0,0), xoffset=-50, yoffset=-50 )

 # line = retval[0][0][0]
 # x, y = line.get_data()

  #map.drawparallels(range(-90, 100, 10), linewidth=5, dashes=[1, 0], labels=[0,0,0,0], color=(0,0,0) )

  if showRegions:
    div = 5
    m.drawmeridians(np.arange(-140, -0, div),dashes=[1,0],color='b')
    div2 = 5
    m.drawparallels(np.arange(0, 70, div2),dashes=[1,0],color='b')

  lat = [0, 50]
  lon = [-100, -100]
  x, y = m(lon, lat)
  m.plot(x, y, 'o-', markersize=5, linewidth=2, color=(0, 0, 0))

  lat = [0, 50]
  lon = [-20, -20]
  x, y = m(lon, lat)
  m.plot(x, y, 'o-', markersize=5, linewidth=2, color=(0, 0, 0))
  plt.title('')
  plt.show()

def main():
  if False and len(sys.argv) != 4:
    print "Usage: {0} <VectorsInput> <FilterFraction> <RegionOverlaySwitch>".format(sys.argv[0])
  else:
    drawTrajectory()

if __name__ == '__main__':
  main()
else:
  print __name__