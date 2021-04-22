import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as m
#
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
from csv import reader
from reportlab.lib.units import inch


# Created on April 20, 2021 by Brendan Lee
# This script takes in .xyz files and:
#   1. Converts them to a .csv file
#   2. Genereates a topological heatmap of the plate based on the xyz values
#   3. Generates a histogram of the thickness of the plates

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
        #print(line)
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
    (plate_z) = (plate_i)
    (fixtu_z) = (fixture_i)
    thickness_list.append(plate_z - fixtu_z)
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
  f = open(filename, 'w')
  for i in range(11):
    currline = ''
    for j in range(11):
      currline += str("%.3f" % thickness_z_list[loc])
      if j < 10:
        currline += ','
      elif j == 10:
        currline += '\n'
      loc += 1
      # end for j
    f.write(currline)
    # end for i
  (avg, std) = get_stats(thickness_z_list)
  curr_avg = avg
  curr_std = std
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

  # Generate Heatmap
  cdict = {
  'red'  :  ( (0.0, 0.25, .25), (0.02, .59, .59), (1., 1., 1.)),
  'green':  ( (0.0, 0.0, 0.0), (0.02, .45, .45), (1., .97, .97)),
  'blue' :  ( (0.0, 1.0, 1.0), (0.02, .75, .75), (1., 0.45, 0.45))
  }

  cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)

  #cont = plt.contourf(X,Y,Z, cmap='jet', vmin=np.min(Z), vmax=np.max(Z))
  cont = plt.contourf(X,Y,Z, cmap='jet', vmin=0.17, vmax=0.23)
  plt.xlim(0, 280)
  plt.ylim(0, 280)
  plt.colorbar(label='mm')
  plt.scatter(X, Y, marker=".", c='black')
  #plt.show()              # uncomment to see the graph instead of saving it
  plt.savefig(filename + "_heatmap.png")   # comment to not save the graph
  plt.clf()

  # Generate Thickness Histogram
  count, bins = np.histogram(thickness_z_list)
  plt.hist(bins[:-1], bins, weights=count, ec='black')
  plt.xlabel('mm')
  plt.ylabel('frequency')
  plt.title('Distribition of Thickness')
  plt.savefig(filename + ".png")
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
  print("In IND_PLATE: {}".format(filename))
  # 1. Extract values from fixture and plate
  plate_x, plate_y, plate_z = extract_xyz(filename) # ../raw_xyz/C3-69-12345-6-P21-1.xyz

  # 2. Get Thickness from the two measurement values
  thickness_z_list = get_thickness(fix_z, plate_z)

  # 2.5 Strip the filename so there is only the actual name left
  filename = os.path.splitext(filename)[0] # filename = C3-69-12345-6-P21-1 -> C3-69-12345-6-P21-1 (no more extentio)
  filename = os.path.basename(filename)
  print(filename)
  # 3. Generate the CSV
  generate_csv(thickness_z_list, g_output_path + '/' + filename + ".csv") # ../outputs/C3-69-12345-6-P21-1.csv

  # 4. Generate the plot
  generate_plot(plate_x, plate_y, thickness_z_list, g_output_path + '/' + filename) # ../outputs/C3-69-12345-6-P21-1.pdf
  # end process_plate()

def generate_pdf(filename):
  csv_name = filename + ".csv"
  heatmap_name = filename + "_heatmap.png"
  histo_name = filename + ".png"
  report_name = filename + ".pdf"

  csv_fullpath = g_output_path + '/' + filename + '.csv' # change for windows
  heatmap_fullpath = g_output_path + '/' + filename + '_heatmap.png'
  histo_fullpath = g_output_path + '/' + filename + '.png'
  report_fullpath = g_report_path + '/' + filename + '.pdf'
  print('Report (csv fullpath):{}'.format(csv_fullpath))
  print('Report (heatmat fullpath):{}'.format(heatmap_fullpath))
  print('Report (hisogram fullpath):{}'.format(histo_fullpath))
  print('Report (report fullpath):{}'.format(report_fullpath))

  #can = canvas.Canvas('../reports/' + report_name, pagesize=letter) # 612, 792
  can = canvas.Canvas(report_fullpath, pagesize=letter)
  w, h = letter
  left_margin = inch

  # Prelim report string write
  can.setFont("Times-Bold", 16)
  can.drawString(left_margin, 680, "Report on {}".format(filename))

  # Purdue Logo
  im = Image.open('purdue_logo.png')
  can.drawInlineImage(im, 20, 740, width=100.44, height=30)

  # Fermi Logo
  im = Image.open('fermi_logo.png')
  can.drawInlineImage(im, 173, 740, width=100, height=41)

  # CMS Logo
  im = Image.open('cms_logo.png')
  can.drawInlineImage(im, 326, 720, width=70, height=70)

  # CMSC Logo
  im = Image.open('cmsc_logo.png')
  can.drawInlineImage(im, 461, 720, width=90, height=90)

  # Write Date
  today = date.today()
  today = today.strftime("%m/%d/%Y")
  can.setFont('Times-Roman', 12)
  can.drawString(left_margin, 650, today)

  # Write Name
  can.drawString(left_margin, 630, scanner_name)

  # Write layup
  can.drawString(left_margin, 600, 'The plate was laid up and cured and post cured as per the manufacturer recommended procedure.')
  can.drawString(left_margin, 590, 'It was then measured on a Hexagon coordinate measuring machine for the thickness measurements')

  # Write Units
  can.setFont('Times-Bold', 12)
  can.drawString(left_margin, 550, "Units in mm")

  # Enter heatmap
  im = Image.open(heatmap_fullpath)
  can.drawInlineImage(im, 40, 300, 300, 230)

  # Enter Histogram
  im = Image.open(histo_fullpath)
  can.drawInlineImage(im, w/2, 300, 230, 230)

  # Statistics
  can.setFont('Times-Bold', 14)
  can.drawString(left_margin, 260, "Statistics")

  # Print table by getting values from file
  f = open(csv_fullpath, 'r')
  avg = 0.0
  std = 0.0
  for line in f.readlines():
    line = line.split(',')
    if line[0] == 'Thickness_Mean':
      avg = float(line[1])
    if line[0] == 'Thickness_StdDev':
      std = float(line[1])
  f.close()

  avg_str = "%.3f" % avg
  avg_std = "%.3f" % std
  data = [["Average Thickness: ", avg_str], ["Thickness Standard Deviation: ", avg_std]]
  t = Table(data)
  t.setStyle(TableStyle([
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
  t.wrapOn(can, 0, 0)
  t.drawOn(can, left_margin, h/4)

  # Next Page
  can.showPage()

  # Print Plate name again
  can.setFont('Times-Bold', 16)
  can.drawCentredString(w/2, 730, "11x11 Thickness Measurements for " + filename)

  # print units
  can.setFont('Times-Bold', 12)
  can.drawCentredString(w/2, 700, "Units in mm")

  # Get table
  with open(csv_fullpath, 'r') as read_obj:
    csv_reader = reader(read_obj)
    values = list(csv_reader)
    values = values[:len(values) - 2]
    t = Table(values)
    t.setStyle(TableStyle([
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    t.wrapOn(can, 0, 0)
    t.drawOn(can, 110, h/2)

  can.save()

# Runner fuction. Calls process_ind_plate() for every .xyz file in the directory for the plates.
# The path to the fixutre.xyz is hardcoded and may need changing to run on local enviroments. We take this once
# since we use the same fixture.
def process_all():
  directory = "../raw_xyz"  # directory where all the xyz files for measurement are
  (fix_x, fix_y, fix_z) = extract_xyz('newfixture.xyz')
  for filename in os.listdir(directory):
    if filename == '.DS_Store' or filename == 'fixture.xyz':
      continue
    print("Processing: {}".format(filename))
    process_ind_plate(fix_x, fix_y, fix_z, "../raw_xyz/" + filename) # filename=C3-69-12345-6-P21-1.xyz

    # send in just the plate name no extentions
    generate_pdf(os.path.splitext(filename)[0])
  # end process_all()

# Allows you to run the above function from the GUI
def run_from_gui(fixture_path, raw_xyz_path, output_path, report_path, name):
  # Create Global
  global g_fixture_path
  g_fixture_path = fixture_path
  global g_raw_xyz_path
  g_raw_xyz_path = raw_xyz_path
  global g_output_path
  g_output_path = output_path
  global g_report_path
  g_report_path = report_path
  global scanner_name
  scanner_name = name

  (fix_x, fix_y, fix_z) = extract_xyz(fixture_path)

  # Iterate through the files
  for filename in os.listdir(raw_xyz_path):
    if filename == '.DS_Store' or filename == 'fixture.xyz':
      continue
    print('Processing: {}'.format(os.path.splitext(filename)[0]))
    process_ind_plate(fix_x, fix_y, fix_z, raw_xyz_path + '/' + filename) # change for windows
    generate_pdf(os.path.splitext(filename)[0])

'''
# Test function
#process_all()

Fixture_Location='/Users/brendanlee/Desktop/CSMC/CMM/CMM_Reports/raw_xyz/fixture.xyz'
Plate_Directory='/Users/brendanlee/Desktop/CSMC/CMM/CMM_Reports/raw_xyz'
Output_Directory='/Users/brendanlee/Desktop/CSMC/CMM/CMM_Reports/output2'
Report_Output_Directory='/Users/brendanlee/Desktop/CSMC/CMM/CMM_Reports/reports2'
name = 'Brendan lee'

run_from_gui(Fixture_Location, Plate_Directory, Output_Directory, Report_Output_Directory, name)
'''