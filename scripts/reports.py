import os
from plate import Plate

class Report(object):
  def __init__(self, plate_filename, fixture_filename):
    plate_raw = self.extract_xyz(plate_filename)
    fix_raw = self.extract_xyz(fixture_filename)

    #self.plate = Plate.__init__(plate_raw[0], plate_raw[1], plate_raw[2], fix_raw[2])
  # _init_()

  def extract_xyz(self, filename):
    """Process the individual xyz file from the filename

    Args:
        filename (str): name of the xyz file to open

    Returns:
        tuple of list of float: each list contains the values of the plate
    """
    x_list = []
    y_list = []
    z_list = []

    try:
      with open(filename) as f:
        for line in f.readlines():
          line = line.split(' ')
          x_list.append(float(line[0]))
          y_list.append(float(line[1]))
          z_list.append(float(line[2]))
    except IOError as e:
      print(e)

    return x_list, y_list, z_list
  # extract_xyz()

rep = Report('C3-76-018726-1-A21-0050.xyz', 'fixture.xyz')