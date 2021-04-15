import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import process_data

fixture_name = 'test_points/fixutre.xyz'
plate_name = 'test_points/C3-69-12345-6-P21-1.xyz'


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
def get_thickness(fixture, plate):
    zippo = zip(fixture, plate)
    diff = []
    for fi,pi in zippo:
        diff.append(pi - fi)
    return diff
    # enf get_thickness()

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
  plt.contourf(X,Y,Z, cmap='jet')
  plt.scatter(X, Y, marker=".", c='black')
  plt.colorbar(label='mm')
  plt.show()
# end generate_plot()

generate_plot(fixture_name, plate_name)