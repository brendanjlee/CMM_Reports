from __main__ import *
import process_xyz
import tkinter as tk
from tkinter.filedialog import asksaveasfile
import os
import sys


class reportGenerator(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.parent.geometry("500x500")  # the size of the canvas
        self.parent.title("Report Generator for Flatplates")

        # Title Label
        intro_string = 'You must locate the following files:\nfixture.xyz (.xyz measurement for the vacuum fixture)'
        lab1 = tk.Label(self.parent, text="You must locate the following files: ", fg='purple', bg="yellow", relief='solid', font=("Helvetica", "14", "bold"))
        lab1.place(x=10 , y=10)

        # Ask for person who wrote this
        self.name_lab = tk.Label(self.parent, text="Name of Person Scanning:", fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.name_lab.place(x=10, y=50)
        self.name_param = tk.Entry(self.parent)
        self.name_param.place(x=240, y=50)

        # Ask for fixture path
        self.fixture_lab = tk.Label(self.parent, text='1. Get the location of the fixutre file (in .xyz format)', fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.fixture_lab.place(x=10, y=85)
        # Fixture path button
        global fixture_button
        fixture_button = tk.Button(self.parent, text='Find Fixutre', fg='black', bg='green', relief="ridge", font=("Helvetica", "14", "bold"), command=self.get_fixture_loc)
        fixture_button.place(x=360, y=85)

        # Ask for path of raw files
        self.plates_label = tk.Label(self.parent, text='2. Get the folder location of the .xyz files of plates', fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.plates_label.place(x=10, y=130)
        # Plate path button
        global plates_button
        plates_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=("Helvetica", "14", "bold"), command=self.get_plate_loc)
        plates_button.place(x=360, y=130)

        # Ask for output directory
        self.output_label = tk.Label(self.parent, text='3. Select Folder to save outputs to', fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.output_label.place(x=10, y=175)
        # Output path button
        global output_button
        output_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=("Helvetica", "14", "bold"), command=self.get_output_loc)
        output_button.place(x=360, y=175)

        # Ask for report output directory
        self.report_path_label = tk.Label(self.parent, text='4. Select Folder to save reports to', fg='black', relief='sunken', font=('Helvetica', '14', 'bold'))
        self.report_path_label.place(x=10, y=220)
        # Output path button
        global report_path_button
        report_path_button = tk.Button(self.parent, text='Find', fg='black', bg='green', relief="ridge", font=("Helvetica", "14", "bold"), command=self.get_report_path)
        report_path_button.place(x=360, y=220)

        # Run Button
        global run
        run = tk.Button(self.parent, text="Generate Reports", fg='black', bg='green', relief='ridge', font=('Helvetica', '14', 'bold'), command=self.generate)
        run.place(x=175, y=435)
        # end initialize_user_interface():

    def get_fixture_loc(self):
      self.fixture_path = tk.filedialog.askopenfilename(initialdir='/', title = "Select file", filetypes = (("xyz files","*.xyz"),("all files","*.*")))
      print('Fixture Location={}'.format(self.fixture_path))

    def get_plate_loc(self):
      self.raw_plate_path = tk.filedialog.askdirectory(title='Select Folder with .xyz files of plates')
      print('Plate Directory={}'.format(self.raw_plate_path))

    def get_output_loc(self):
      self.output_path = tk.filedialog.askdirectory(title='Select Folder where you want to save the outputs (csv, heatmap, and histogram)')
      print('Output Directory={}'.format(self.output_path))

    def get_report_path(self):
      self.report_path = tk.filedialog.askdirectory(title='Select Folder wher eyou want to save the PDF reports of your scans')
      print('Report Output Directory={}'.format(self.report_path))

    def generate(self):
      process_xyz.run_from_gui(self.fixture_path, self.raw_plate_path, self.output_path, self.get_report_path, self.name_param)

if __name__ == '__main__':
    root = tk.Tk()
    run = reportGenerator(root)
    root.mainloop()
