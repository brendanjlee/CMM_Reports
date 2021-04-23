# CMM Flatplate Report Generator

This script extracts data from xyz files and generates a csv and pdf plot.

## Installation

Install needed packages with pip

```bash
pip install pandas
pip install numpy 
```

### Packges
Import these packages 
```python
import os, sys
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
from __main__ import *
import tkinter as tk
from tkinter.filedialog import asksaveasfile
```

## Usage

In terminal, navigate to the "scripts" folder. Once you are in, type
```bash
python process_xyz.py
```
it should generate a both a csv and pdf of every plate .xyz file in the directory.

### Changing Directories or Running on Windows (as of now)
[Will become automatic]

All directory locations are hardcoded in at the moment. In order to be able to run this script on windows, you will have to make changes to the path.

## Files
```
CMM_Reports
|
|─ outputs
|─ raw_xyz
|─── ..
|─── plate.xyz files to process
|─── .. 
|─ scripts
|─── fixture.xyz
|─── geneate_heatmap.py -> do not use
|─── process_data.py -> do not use
|─── process_xyz.py
```



