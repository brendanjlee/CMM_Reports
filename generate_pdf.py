import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import date
# platypus stuff
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

# Created on April 22, 2021 by Brendan Lee
# This scrip uses process_xyz.py to parse through xyz files and extract the needed data. It then generates a
# pdf report based on the files.

'''
curr_filename = "C3-69-12345-6-P21-1"

can = canvas.Canvas('testing.pdf', pagesize=letter)
width, height = letter # (612.0, 792.0)

# Premlim report string write
can.setFont('Times-Bold', 16)
can.drawString(20, 680, "Preliminary report on {}".format(curr_filename))

# Purdue Logo
im = Image.open("scripts/purdue_logo.png")
can.drawInlineImage(im, 20, 740, width = 100.44, height=30) # logo aspect ratio: width = 167.4 * height

# CMSC Logo
im = Image.open("scripts/cmsc_logo.png")
can.drawInlineImage(im, 500, 720, width=70, height=70)

# Write Date
today = date.today()
today = today.strftime("%m/%d/%Y")
can.setFont('Times-Roman', 12)
can.drawString(20, 650, today)

# Write Name
can.drawString(20, 630, "Brendan Lee")

# Write heatmap
im = Image.open()

# Save page
can.showPage()
can.save()
'''

def run():
  for file in os.listdir('outputs'):
    print(file)

run()

'''
# Plat test'
title = "Hello World"
pageinfo = "platypus example"

curr_filename = "C3-69-12345-6-P21-1"

def myFirstPage(canvas, doc):
  canvas.saveState()
  # Purdue Logo
  im = Image.open("purdue_logo.png")
  canvas.drawInlineImage(im, 20, 740, width=100.44, height=30)

  # CMSC Logo
  im = Image.open("cmsc_logo.png")
  print(im.size)
  canvas.drawInlineImage(im, 500, 720, width=70, height=70)
  canvas.setFont('Times-Bold', 16)
  canvas.drawString(20, 650, "Preliminary report on {}".format(curr_filename))
  canvas.restoreState()

def myLaterPages(canvas, doc):
  canvas.saveState()
  canvas.setFont('Times-Roman',9)
  canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
  canvas.restoreState()

doc = SimpleDocTemplate("hello.pdf")
Story = [Spacer(1, 2*inch)]
style = styles["Normal"]
for i in range(10):
  sometext = ("This is paragprah %s. " % i) * 20
  p = Paragraph(sometext, style)
  Story.append(p)
  Story.append(Spacer(1, 0.2 * inch))
doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
'''