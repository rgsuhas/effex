Skip to content
Navigation Menu
rgsuhas
effex

Type / to search
Code
Issues
Pull requests
Actions
Projects
Security
8
Insights
Settings
Owner avatar
effex
Public
rgsuhas/effex
Go to file
t
Name		
rgsuhas
rgsuhas
Create setup.sh
0e4b04c
 · 
7 months ago
processed
refactor
7 months ago
sample_img
refactor
7 months ago
README.md
Update README.md
7 months ago
app.py
multiple iterations
7 months ago
app_minimalist.py
use_column_width deprecated
7 months ago
app_sidebside.py
multiple iterations
7 months ago
requirements.txt
Update requirements.txt
7 months ago
setup.sh
Create setup.sh
7 months ago
Repository files navigation
README
Image Filter Application
Description
This is a Streamlit-based web application that allows users to apply artistic filters to their images. Users can upload an image and apply effects like watercolor sketch, pencil sketch, cartoon, sepia, HDR, and sharpen effects. The application supports dark and light modes for better user experience.

Features
Artistic Filters:
Watercolor Sketch 🖌️
Pencil Sketch ✏️
Cartoon Effect 🎨
Sepia Effect 📜
HDR Effect 🌄
Sharpen Effect 🔍
Dark Mode and Light Mode toggle for customizable appearance.
Real-time Filter Preview of all effects.
Download Processed Images with a single click.
Feedback submission for user input.
Installation
Clone this repository:

git clone https://github.com/rgsuhas/Image-Filter-Application
cd Image-Filter-Application
Install the required dependencies:

pip install -r requirements.txt
Run the application:

streamlit run app.py
Usage
Upload an Image:

Use the "Upload Your Image" section to select an image (PNG, JPG, or JPEG format).
Choose a Filter:

Select one of the filters from the available options.
View Previews:

View real-time previews of all filters in the "Filter Previews" section.
Process and Download:

The selected filter is applied, and the result is displayed alongside the original image.
Use the "Download Processed Image" button to save the edited image.
Filters Description
Watercolor Sketch 🖌️:

Creates a vibrant watercolor effect with enhanced edges.
Pencil Sketch ✏️:

Converts the image into a grayscale pencil sketch.
Cartoon Effect 🎨:

Applies a cartoon-like effect with bold colors and edges.
Sepia Effect 📜:

Gives the image a vintage, warm sepia tone.
HDR Effect 🌄:

Enhances image contrast and texture for a high dynamic range effect.
Sharpen Effect 🔍:

Sharpens image details by enhancing edges.
File Structure
📁 Image-Filter-App
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
Dependencies
Streamlit: For the web interface.
OpenCV: For image processing.
Pillow: For image file handling.
NumPy: For numerical operations.
Install dependencies with:

pip install -r requirements.txt
Example Output
Original Image:
Original

Processed Image (Watercolor Sketch):
Watercolor

Feedback
If you have suggestions or encounter issues, feel free to submit feedback through the application or open an issue on the repository.

Enjoy creating beautiful artistic images! 🎨

About
simple image filter app

Resources
 Readme
 Activity
Stars
 1 star
Watchers
 1 watching
Forks
 1 fork
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Languages
Python
99.6%
 
Shell
0.4%
Suggested workflows
Based on your tech stack
Publish Python Package logo
Publish Python Package
Publish a Python Package to PyPI on release.
Python package logo
Python package
Create and test a Python package on multiple Python versions.
Django logo
Django
Build and Test a Django Project
More workflows
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
