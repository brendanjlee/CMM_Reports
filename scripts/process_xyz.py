import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as m

# Created on April 20, 2021 by Brendan Lee


# Process the individual .xyz file and returns a list of xyz tuple values
#   filename: name of the .xyz file to be processed
#
# Returns:
#   xyz_list: list of tuples containing (x,y,z) values
def extract_xyz(filename):
  xyz_list = []
  x_list = []
  y_list = []
  z_list = []
  try:
    with open(filename) as f:
      for line in f.readlines():
        line = line.split(' ')
        xyz_list.append((line[0], line[1], line[2])) # x,y,z format
        x_list.append(float(line[0]))
        y_list.append(float(line[1]))
        z_list.append(float(line[2]))
  except FileNotFoundError as e:
    print(e)
  return x_list, y_list, z_list
  # end process_xyz()

# Calculate the difference, mean and std of the plates using the measurements of the fixture and the plate
#   fixture_z_list: list containing the z-values of the fixture
#   plate_z_list:   list containing the z-values of the plate
#
# Returns:
#   thickness_list: a list of z-values for thickness of the plate
def get_thickness(fixture_z_list, plate_z_list):
  thickness_list = []
  zip_obj = zip(fixture_z_list, plate_z_list)
  for fixture_i, plate_i in zip_obj:
    plate_z = (plate_i)
    fixtu_z = (fixture_i)
    thickness_list.append(plate_z - fixtu_z)
  #print(thickness_list)
  return thickness_list
  # end get_thickness()

# Calculates and returns the mean and stdev of the plate thickness
#   thickness_z_list: list containing the z-values for plate thickness
#
# Returns:
#   float(mean thickness)
#   float(stdev thickness)
def get_stats(thickness_z_list):
  return (np.mean(thickness_z_list), np.std(thickness_z_list))
  # end get_stats()

# Generates a csv file with the given thickness list of z values. Names the csv file with filename
# thickness_list: list of just z-values that represent the thickness of the plate
# filename: name of the file
#   eg: C3-69-12345-6-P21-1.csv
#
# Returns: nil
def generate_csv(thickness_z_list, filename):
  loc = 0
  #print("CSV Filename: {}\n".format(filename))
  f = open(filename, 'w')
  for i in range(11):
    currline = ''
    for j in range(11):
      currline += str(thickness_z_list[loc])
      if j < 10:
        currline += ','
      elif j == 10:
        currline += '\n'
      loc += 1
      # end for j
    f.write(currline)
    # end for i
  (avg, std) = get_stats(thickness_z_list)
  f.write('Thickness_Mean, {}\n'.format(avg))
  f.write('Thickness_StdDev, {}\n'.format(std))
  f.close()
  # end generate_csv()

# Generates a plot from the given measurements and saves it to filename
#   plate_x: list of x values of the plate
#   plate_y: list of y values of the plate
#   thickness_z_list: list of z-values for the thickness of the plate
#   filename: string that is the filename
#
# Returns: nil. Saves a pdf plot with filename.
def generate_plot(plate_x, plate_y, thickness_z_list, filename):
  # Convert to np array from list
  x = np.asarray(plate_x)
  y = np.asarray(plate_y)
  z = np.asarray(thickness_z_list)

  # Set number of columns
  cols = 11

  # Reshape the 11x11 points
  X = x.reshape(-1, cols)
  Y = y.reshape(-1, cols)
  Z = z.reshape(-1, cols)

  # Graph
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
  #plt.show()              # uncomment to see the graph instead of saving it
  plt.savefig(filename)   # comment to not save the graph
  plt.clf()
# end generate_plot()

# Takes in the filenames for the fixture and plate and generates both the csv and pdf of the thickness of plates
#   fix_x, fix_y, fix_z = each is a list that contains xyz values of the fixture
#   filename will be in format: C3-69-12345-6-P21-1.xyz
#
# Process function for each plate:
# 1. extract values from fixture and plate:   extract_xyz()
# 2. Get thickness from the two measurements: get_thickness()
# 3. Genearte a csv:                          generate_csv()
#                                              - get_stat()
# 4. Generate a graph                         generate_plot()
def process_ind_plate(fix_x, fix_y, fix_z, filename):
  # 1. Extract values from fixture and plate
  plate_x, plate_y, plate_z = extract_xyz("../raw_xyz/" + filename) # ../raw_xyz/C3-69-12345-6-P21-1.xyz

  # 2. Get Thickness from the two measurement values
  thickness_z_list = get_thickness(fix_z, plate_z)

  # 2.5 Strip the filename so there is only the actual name left
  filename = filename.split('.')[0] # filename = C3-69-12345-6-P21-1 (no more extentio)

  # 3. Generate the CSV
  generate_csv(thickness_z_list, "../outputs/" + filename + ".csv") # ../outputs/C3-69-12345-6-P21-1.csv

  # 4. Generate the plot
  generate_plot(plate_x, plate_y, thickness_z_list, "../outputs/" + filename + ".pdf") # ../outputs/C3-69-12345-6-P21-1.pdf
  # end process_plate()

# Runner fuction. Calls process_ind_plate() for every .xyz file in the directory for the plates.
# The path to the fixutre.xyz is hardcoded and may need changing to run on local enviroments. We take this once
# since we use the same fixture.
def process_all():
  directory = "../raw_xyz"  # directory where all the xyz files for measurement are
  (fix_x, fix_y, fix_z) = extract_xyz('fixutre.xyz')
  for filename in os.listdir(directory):
    if filename == '.DS_Store':
      continue
    print(filename)
    process_ind_plate(fix_x, fix_y, fix_z, "../raw_xyz/" + filename) # filename=C3-69-12345-6-P21-1.xyz
  # end process_all()

# Test function
process_all()