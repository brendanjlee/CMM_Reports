import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as m
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
from csv import reader
from reportlab.lib.units import inch
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

def resource_path(relative_path):
    ''' Return the relative path of the file

        param relative_path:  the pathname to file (str)
        type relative_path:  string
        rtype: string
    '''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

### process ###

def extract_xyz(filename):
    ''' Return a list of tuples containing (x,y,z) values

        param filename: name of the .xyz file
        type filename: string
        rtype: list of tuples of floats
    '''
    xyz_list = []
    x_list = []
    y_list = []
    z_list = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                # print(line)
                line = line.split(' ')
                xyz_list.append((line[0], line[1], line[2]))  # x,y,z format
                x_list.append(float(line[0]))
                y_list.append(float(line[1]))
                z_list.append(float(line[2]))
    except IOError as e:
        print(e)
    return x_list, y_list, z_list
    # end process_xyz()

def get_thickness(fixture_z_list, plate_z_list):
    ''' Return a list of z-values representing the thickness of the plates at
        each coordinate

        param fixture_z_list: list of floats containing the z-value of fixtures
        type fixture_z_list:  list
        param plate_z_list:   list of floats containing the z-values of a plate
        type plate_z_list:    list
        rtype:                list
    '''
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

# Generates a csv file with the given thickness list of z values.Names the
# csv file with filename
# thickness_list: list of just z-values that for the thickness of the plate
# filename:       name of the file
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
    cont = plt.contourf(X,Y,Z, cmap='jet', vmin=np.min(Z), vmax=np.max(Z))
    plt.xlim(0, 280)
    plt.ylim(0, 280)
    plt.colorbar(label='mm')
    plt.scatter(X, Y, marker=".", c='black')
    # plt.show()              # uncomment to see the graph instead of saving it
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

# Takes in the filenames for the fixture and plate and generates both the csv
# and pdf of the thickness of plates
#   fix_x, fix_y, fix_z = each is a list containing xyz values of the fixture
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
    plate_x, plate_y, plate_z = extract_xyz(
        filename)  # ../raw_xyz/C3-69-12345-6-P21-1.xyz

    # 2. Get Thickness from the two measurement values
    thickness_z_list = get_thickness(fix_z, plate_z)

    # 2.5 Strip the filename so there is only the actual name left
    # filename = C3-69-12345-6-P21-1 -> C3-69-12345-6-P21-1 (no more extentio)
    filename = os.path.splitext(filename)[0]
    filename = os.path.basename(filename)
    print(filename)
    # 3. Generate the CSV
    # ../outputs/C3-69-12345-6-P21-1.csv
    generate_csv(thickness_z_list, g_output_path + '/' + filename + ".csv")

    # 4. Generate the plot
    generate_plot(plate_x, plate_y, thickness_z_list, g_output_path +
                  '/' + filename)  # ../outputs/C3-69-12345-6-P21-1.pdf
    # end process_plate()


# This function takes in the plate filename and uses reportlabs to generate and
# save the actual PDF report in the reports directory.
def generate_pdf(filename):
    csv_fullpath = g_output_path + '/' + filename + '.csv'  # change windows
    heatmap_fullpath = g_output_path + '/' + filename + '_heatmap.png'
    histo_fullpath = g_output_path + '/' + filename + '.png'
    report_fullpath = g_report_path + '/' + filename + '.pdf'
    print('Report (csv fullpath):{}'.format(csv_fullpath))
    print('Report (heatmat fullpath):{}'.format(heatmap_fullpath))
    print('Report (hisogram fullpath):{}'.format(histo_fullpath))
    print('Report (report fullpath):{}'.format(report_fullpath))

    can = canvas.Canvas(report_fullpath, pagesize=letter) # 612, 792
    w, h = letter
    left_margin = inch

    # Prelim report string write
    can.setFont("Times-Bold", 16)
    can.drawString(left_margin, 680, "Report on {}".format(filename))

    # Purdue Logo
    im = Image.open(resource_path('logos/purdue_logo.png'))
    can.drawInlineImage(im, 20, 740, width=100.44, height=30)

    # Fermi Logo
    im = Image.open(resource_path('logos/fermi_logo.png'))
    can.drawInlineImage(im, 173, 740, width=100, height=41)

    # CMS Logo
    im = Image.open(resource_path('logos/cms_logo.png'))
    can.drawInlineImage(im, 326, 720, width=70, height=70)

    # CMSC Logo
    im = Image.open(resource_path('logos/cmsc_logo.png'))
    can.drawInlineImage(im, 461, 720, width=90, height=90)

    # Write Date
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    can.setFont('Times-Roman', 12)
    can.drawString(left_margin, 650, today)

    # Write Name
    can.drawString(left_margin, 630, scanner_name)

    # Write layup
    can.drawString(
        left_margin, 600, 'The plate was laid up and cured and post cured as'
                        + 'per the manufacturer recommended procedure.')
    can.drawString(
        left_margin, 590, 'It was then measured on a Hexagon coordinate'
                        + 'measuring machine for the thickness measurements')

    # Write Units
    can.setFont('Times-Bold', 12)
    can.drawString(left_margin, 550, "Units in mm")

    # Enter heatmap
    im = Image.open(heatmap_fullpath)
    can.drawInlineImage(im, 40, 300, 280, 210)

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
    data = [["Average Thickness: ", avg_str], [
        "Thickness Standard Deviation: ", avg_std]]
    t = Table(data)
    t.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    t.wrapOn(can, 0, 0)
    t.drawOn(can, left_margin, h/4)

    # Next Page
    can.showPage()

    # Print Plate name again
    can.setFont('Times-Bold', 16)
    can.drawCentredString(
        w/2, 730, "11x11 Thickness Measurements for " + filename)

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
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        t.wrapOn(can, 0, 0)
        t.drawOn(can, 110, h/2)

    can.save()

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
        print('Testing for rawpath={}'.format(raw_xyz_path))
        print('Testing for filename={}'.format(filename))
        concatstring = raw_xyz_path + '/'
        concatstring += filename
        print('Testing for concatstring={}'.format(concatstring))

        # process_ind_plate(fix_x, fix_y, fix_z, raw_xyz_path + '/' + filename) # change for windows
        process_ind_plate(fix_x, fix_y, fix_z, concatstring)
        generate_pdf(os.path.splitext(filename)[0])


# GUI
class reportGenerator(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.parent.geometry("700x500")  # the size of the canvas
        self.parent.title("Report Generator for Flatplates")

        # Title Label
        intro_string = 'You must locate the following files:\nfixture.xyz (.xyz measurement for the vacuum fixture)'
        lab1 = tk.Label(self.parent, text="You must locate the following files: ",
                        fg='purple', bg="yellow", relief='solid', font=("Helvetica", "14", "bold"))
        lab1.place(x=10, y=10)

        # Ask for person who wrote this
        self.name_lab = tk.Label(self.parent, text="Name of Person Scanning:",
                                 fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.name_lab.place(x=10, y=50)
        self.name_param = tk.Entry(self.parent)
        self.name_param.place(x=300, y=50)

        # Ask for fixture path
        self.fixture_lab = tk.Label(self.parent, text='1. Get the location of the fixutre file (in .xyz format)',
                                    fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.fixture_lab.place(x=10, y=85)
        # Fixture path button
        global fixture_button
        fixture_button = tk.Button(self.parent, text='Find Fixutre', fg='black', bg='green', relief="ridge", font=(
            "Helvetica", "14", "bold"), command=self.get_fixture_loc)
        fixture_button.place(x=500, y=85)

        # Ask for path of raw files
        self.plates_label = tk.Label(self.parent, text='2. Get the folder location of the .xyz files of plates',
                                     fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.plates_label.place(x=10, y=130)
        # Plate path button
        global plates_button
        plates_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=(
            "Helvetica", "14", "bold"), command=self.get_plate_loc)
        plates_button.place(x=500, y=130)

        # Ask for output directory
        self.output_label = tk.Label(self.parent, text='3. Select Folder to save outputs to',
                                     fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.output_label.place(x=10, y=175)
        # Output path button
        global output_button
        output_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=(
            "Helvetica", "14", "bold"), command=self.get_output_loc)
        output_button.place(x=360, y=175)

        # Ask for report output directory
        self.report_path_label = tk.Label(self.parent, text='4. Select Folder to save reports to',
                                          fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.report_path_label.place(x=10, y=220)
        # Output path button
        global report_path_button
        report_path_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=(
            "Helvetica", "14", "bold"), command=self.get_report_path)
        report_path_button.place(x=360, y=220)

        # Run Button
        global run
        run = tk.Button(self.parent, text="Generate Reports", fg='black', bg='green',
                        relief='ridge', font=('Helvetica', '14', 'bold'), command=self.generate)
        run.place(x=175, y=435)
        # end initialize_user_interface():

    def get_fixture_loc(self):
        self.fixture_path = tk.filedialog.askopenfilename(
            initialdir='/', title="Select file", filetypes=(("xyz files", "*.xyz"), ("all files", "*.*")))
        print('Fixture Location={}'.format(self.fixture_path))
        messagebox.showinfo(
            'Fixture', "Fixture Location={}".format(self.fixture_path))

    def get_plate_loc(self):
        self.raw_plate_path = tk.filedialog.askdirectory(
            title='Select Folder with .xyz files of plates')
        print('Plate Directory={}'.format(self.raw_plate_path))
        messagebox.showinfo(
            'Plates', "Plates Location={}".format(self.raw_plate_path))

    def get_output_loc(self):
        self.output_path = tk.filedialog.askdirectory(
            title='Select Folder where you want to save the outputs (csv, heatmap, and histogram)')
        print('Output Directory={}'.format(self.output_path))
        messagebox.showinfo(
            'Output', "Output Directory={}".format(self.output_path))

    def get_report_path(self):
        self.report_path = tk.filedialog.askdirectory(
            title='Select Folder wher eyou want to save the PDF reports of your scans')
        print('Report Output Directory={}'.format(self.report_path))
        messagebox.showinfo(
            'Reports', "Reports Directory={}".format(self.report_path))

    def generate(self):
        run_from_gui(self.fixture_path, self.raw_plate_path,
                     self.output_path, self.report_path, self.name_param.get())
        messagebox.showinfo("Report Generator", "Reports Generated!")


def main():
    root = tk.Tk()
    run = reportGenerator(root)
    root.mainloop()

#im = Image.open(resource_path('logos/purdue_logo.png'))
#print('hello')