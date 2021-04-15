import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import matplotlib as m
import process_data

fixture_name = 'test_points/fixutre.xyz'
plate_name = 'test_points/C3-69-12345-6-P21-1.xyz'

# Generation Set up:
# fixture.xyz
# plates(dir) -> contains the measurements
# | C3-......
# | C3-....
# | .........

# Procedure
# 1. open the fixture file and get the xyz values
# 2. go to the plates directory
#    for each file in plates:
#      - get thickness
#      - generate plot and save it in the plots directory
#         - heatmap
#         - historgram
#      - process the data and save it as csv


# get XYZ value from file
def get_xyz(filename):
  x = []
  y = []
  z = []
  # Catch missing files
  try:
    with open(filename) as f:
      for line in f.readlines():
        line = line.split(' ')
        x.append(float(line[0]))
        y.append(float(line[1]))
        z.append(float(line[2]))
  # end catch
  except FileNotFoundError as e:
    print(e)
  return (x, y, z)
# end process_line()

# get the thickness by subtracting plate and fixture
# fixture: list containing the z values of the fixture
# plate:   list containing the z values of the plate
def get_thickness(fixture, plate):
    zippo = zip(fixture, plate)
    diff = []
    for fi,pi in zippo:
        diff.append(pi - fi)
    return diff
    # enf get_thickness()
# end get_thickness()

# Executing Function
def generate_plot(fixture_name, plate_name):
  # Extract values
  fixture_x, fixture_y, fixture_z = get_xyz(fixture_name)
  plate_x, plate_y, plate_z = get_xyz(plate_name)
  diff = get_thickness(fixture_z, plate_z)

  # Assign coordinate values
  x = plate_x
  y = plate_y
  z = diff

  # Convert to np array from list
  x = np.asarray(x)
  y = np.asarray(y)
  z = np.asarray(z)

  # Set number of columns (11, 11)
  cols = 11

  # Reshape to 11x11 points
  X = x.reshape(-1, cols)
  Y = y.reshape(-1, cols)
  Z = z.reshape(-1, cols)

  lev = []

  # Graph
  # create a color mapping
  cdict = {
  'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
  'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
  'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
  }
  cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)


  cont = plt.contourf(X,Y,Z, cmap='jet', vmin=np.min(Z), vmax=np.max(Z))
  plt.xlim(0, 280)
  plt.ylim(0, 280)
  plt.colorbar(label='mm')
  plt.scatter(X, Y, marker=".", c='black')
  plt.show()
# end generate_plot()

generate_plot(fixture_name, plate_name)