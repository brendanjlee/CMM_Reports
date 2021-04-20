import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''









DISCARD. The functions from this file have been moved to process_xyz









'''

# Main executing function that takes in the filename (or path) to the .xyz file and returns the z-values in a list
# filename: name of the xyz file to process
def process_line(filename):
  z_vals = []
  # Catch missing files
  try:
    with open(filename) as f:
      for line in f.readlines():
        line = line.split(' ')
        z_vals.append(line[2])
        # end for
  except FileNotFoundError as e:
    print(e)
  return z_vals
  # end process_line()

# Takes in z-values list and generates a csv file from it.
# z_vals: the thickness values of the plate
# avg:    the average thickness of the plate
# std:    the standard deviation of the thickness of the plate
def write_to_csv(z_vals, avg, std):
  loc = 0
  f = open('demo.csv', 'w')
  for i in range(11):
    currline = ''
    for j in range(11):
      currline += str(z_vals[loc])
      if j < 10:
        currline += ','
      elif j == 10:
        currline += '\n'
      loc += 1
      # end for j
    f.write(currline)
  f.write('Thickness_Mean, {}\n'.format(avg))
  f.write('Thickness_StdDev, {}'.format(std))
  f.close()
  # end write_to_csv()

# Calculate the difference, mean and std of the plates using the measurements of the fixture and the plate
# fixutre: list containing the z-values of the fixture
# plate:   list containing the z-values of the plate
def get_mean_std(fixture, plate):
  diff = []
  zip_obj = zip(fixture, plate)
  for fixture_i, plate_i in zip_obj:
    diff.append(float(plate_i) - float(fixture_i))
  return (diff, np.mean(diff), np.std(diff))
  # end get_mean_std()

# Main executing function
def run(fixture_name, plate_name):
  fixture_points = process_line(fixture_name)
  plate_points = process_line(plate_name)
  (diff, avg, std) = get_mean_std(fixture_points, plate_points)

  write_to_csv(diff, avg, std)

  # also generate a histogram
  count, bins = np.histogram(diff)
  plt.hist(bins[:-1], bins, weights=count, ec='black')
  #plt.title(fname)
  plt.xlabel('mm')
  plt.ylabel('frequency')
  plt.show()

  #plt.savefig(fname)
  # end run()


fixture_name = 'test_points/fixutre.xyz'
plate_name = 'test_points/C3-69-12345-6-P21-1.xyz'
# run(fixture_name, plate_name)
