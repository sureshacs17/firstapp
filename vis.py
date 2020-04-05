#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Libraries 
from plantcv import plantcv as pcv
import matplotlib
import os 


# In[2]:


class options:
    def __init__(self):
        self.image = "upload/input/input.jpg"
        self.debug = "plot"
        self.writeimg= False
        self.result = "upload/output_imgs"
        self.outdir = "upload/Results" # Store the output to the current directory
        
# Get options
args = options()

# Set debug to the global parameter 
pcv.params.debug = args.debug


# In[3]:


# Read image

# Inputs:
#   filename - Image file to be read in 
#   mode - How to read in the image; either 'native' (default), 'rgb', 'gray', or 'csv'
img, path, filename = pcv.readimage(filename=args.image)


# In[4]:


# Convert RGB to HSV and extract the saturation channel

# Inputs:
#   rgb_image - RGB image data 
#   channel - Split by 'h' (hue), 's' (saturation), or 'v' (value) channel
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
pcv.print_image(img=s, filename="upload/output_imgs/R2H.jpg")


# In[5]:


# Take a binary threshold to separate plant from background. 
# Threshold can be on either light or dark objects in the image. 

# Inputs:
#   gray_img - Grayscale image data 
#   threshold- Threshold value (between 0-255)
#   max_value - Value to apply above threshold (255 = white) 
#   object_type - 'light' (default) or 'dark'. If the object is lighter than 
#                 the background then standard threshold is done. If the object 
#                 is darker than the background then inverse thresholding is done. 
s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')
pcv.print_image(img=s_thresh, filename="upload/output_imgs/Bthresh_img.jpg")


# In[6]:


# Median Blur to clean noise 

# Inputs: 
#   gray_img - Grayscale image data 
#   ksize - Kernel size (integer or tuple), (ksize, ksize) box if integer input,
#           (n, m) box if tuple input 
s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
pcv.print_image(img=s_mblur, filename="upload/output_imgs/Mblur_img.jpg")


# In[7]:


# An alternative to using median_blur is gaussian_blur, which applies 
# a gaussian blur filter to the image. Depending on the image, one 
# technique may be more effective than others. 

# Inputs:
#   img - RGB or grayscale image data
#   ksize - Tuple of kernel size
#   sigma_x - Standard deviation in X direction; if 0 (default), 
#            calculated from kernel size
#   sigma_y - Standard deviation in Y direction; if sigmaY is 
#            None (default), sigmaY is taken to equal sigmaX
gaussian_img = pcv.gaussian_blur(img=s_thresh, ksize=(5, 5), sigma_x=0, sigma_y=None)
pcv.print_image(img=gaussian_img, filename="upload/output_imgs/Blur_img.jpg")


# In[8]:


# Convert RGB to LAB and extract the blue channel ('b')

# Input:
#   rgb_img - RGB image data 
#   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

# Threshold the blue channel image 
b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                object_type='light')
pcv.print_image(img=b_thresh, filename="upload/output_imgs/Extracted_img.jpg")
pcv.print_image(img=b, filename="upload/output_imgs/Gray_img.jpg")


# In[9]:


# Join the threshold saturation and blue-yellow images with a logical or operation 

# Inputs: 
#   bin_img1 - Binary image data to be compared to bin_img2
#   bin_img2 - Binary image data to be compared to bin_img1
bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
pcv.print_image(img=bs, filename="upload/output_imgs/BSature_img.jpg")


# In[10]:


# Appy Mask (for VIS images, mask_color='white')

# Inputs:
#   rgb_img - RGB image data 
#   mask - Binary mask image data 
#   mask_color - 'white' or 'black' 
rgb_img=img
masked = pcv.apply_mask(rgb_img, mask=bs, mask_color='white')
pcv.print_image(img=masked, filename="upload/output_imgs/VIS_img.jpg")


# In[11]:


# Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels

masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
pcv.print_image(img=masked_b, filename="upload/output_imgs/GrayScale_img.jpg")
pcv.print_image(img=masked_a, filename="upload/output_imgs/Green-Magenta.jpg")


# In[12]:


maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, 
                                      max_value=255, object_type='dark')
maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, 
                                       max_value=255, object_type='light')
maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, 
                                      max_value=255, object_type='light')
pcv.print_image(img=maskeda_thresh, filename="upload/output_imgs/Upper_img.jpg")
pcv.print_image(img=maskeda_thresh1, filename="upload/output_imgs/Lower_img.jpg")
pcv.print_image(img=maskedb_thresh, filename="upload/output_imgs/Combine_img.jpg")


# In[13]:


# Join the thresholded saturation and blue-yellow images (OR)

ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskeda_thresh)
ab = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=ab1)
pcv.print_image(img=ab1, filename="upload/output_imgs/Thresh_img.jpg")
#pcv.print_image(img=ab1, filename="upload/output_imgs/Thresh_img.jpg")


# In[14]:


# Opening filters out bright noise from an image.

# Inputs:
#   gray_img - Grayscale or binary image data
#   kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None (default),
#   uses cross-shaped structuring element.
opened_ab = pcv.opening(gray_img=ab)
pcv.print_image(img=opened_ab, filename="upload/output_imgs/Fliter_img.jpg")


# In[15]:


# Depending on the situation it might be useful to use the 
# exclusive or (pcv.logical_xor) function. 

# Inputs: 
#   bin_img1 - Binary image data to be compared to bin_img2
#   bin_img2 - Binary image data to be compared to bin_img1
xor_img = pcv.logical_xor(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
pcv.print_image(img=xor_img, filename="upload/output_imgs/root_img.jpg")


# In[16]:


# Fill small objects (reduce image noise) 

# Inputs: 
#   bin_img - Binary image data 
#   size - Minimum object area size in pixels (must be an integer), and smaller objects will be filled
ab_fill = pcv.fill(bin_img=ab, size=200)
pcv.print_image(img=ab_fill, filename="upload/output_imgs/NoiseRe_img.jpg")


# In[17]:


# Closing filters out dark noise from an image.

# Inputs:
#   gray_img - Grayscale or binary image data
#   kernel - Optional neighborhood, expressed as an array of 1's and 0's. If None (default),
#   uses cross-shaped structuring element.
closed_ab = pcv.closing(gray_img=ab_fill)
pcv.print_image(img=closed_ab, filename="upload/output_imgs/DarkNoise_img.jpg")


# In[18]:


# Apply mask (for VIS images, mask_color=white)
rgb_img=masked
masked2 = pcv.apply_mask(rgb_img, mask=ab_fill, mask_color='white')
pcv.print_image(img=masked2, filename="upload/output_imgs/Masked_img.jpg")
pcv.print_image(img=img, filename="upload/output_imgs/tag.jpg")


# In[19]:


import cv2
import numpy as np
import glob 

## Read

images = glob.glob(( "upload/output_imgs/tag" + "*.JPG"  ) ) 
images.sort()

i = 1
for mname in images:
    img = cv2.imread(mname)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save 
    cv2.imwrite("upload/output_imgs/Crop.png", green)
    i = i+1
filename = pcv.readimage(filename="upload/output_imgs/Crop.png")    


# In[20]:


# Identify objects

# Inputs: 
#   img - RGB or grayscale image data for plotting 
#   mask - Binary mask used for detecting contours 
id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)


# In[21]:


# Define the region of interest (ROI) 

# Inputs: 
#   img - RGB or grayscale image to plot the ROI on 
#   x - The x-coordiate of the upper left corner of the rectangle 
#   y - The y-coordinate of the upper left corner of the rectangle 
#   h - The height of the rectangle 
#   w - The width of the rectangle 
roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=200, y=300, h=200, w=200)


# In[22]:


# Decide which objects to keep

# Inputs:
#    img            = img to display kept objects
#    roi_contour    = contour of roi, output from any ROI function
#    roi_hierarchy  = contour of roi, output from any ROI function
#    object_contour = contours of objects, output from pcv.find_objects function
#    obj_hierarchy  = hierarchy of objects, output from pcv.find_objects function
#    roi_type       = 'partial' (default, for partially inside the ROI), 'cutto', or 
#                     'largest' (keep only largest contour)
roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')


# In[23]:


# Object combine kept objects

# Inputs:
#   img - RGB or grayscale image data for plotting 
#   contours - Contour list 
#   hierarchy - Contour hierarchy array 
obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
#pcv.print_image(img=s, filename="upload/output_imgs/HSV_img.jpg")


# In[24]:


############### Analysis ################ 
  
# Find shape properties, data gets stored to an Outputs class automatically

# Inputs:
#   img - RGB or grayscale image data 
#   obj- Single or grouped contour object
#   mask - Binary image mask to use as mask for moments analysis 
analysis_image = pcv.analyze_object(img=img, obj=obj, mask=mask)
pcv.print_image(img=analysis_image, filename="upload/output_imgs/object_img.jpg")


# In[25]:


# Shape properties relative to user boundary line (optional)

# Inputs:
#   img - RGB or grayscale image data 
#   obj - Single or grouped contour object 
#   mask - Binary mask of selected contours 
#   line_position - Position of boundary line (a value of 0 would draw a line 
#                   through the bottom of the image) 
boundary_image2 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, 
                                               line_position=370)


# In[26]:


# Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)

# Inputs:
#   rgb_img - RGB image data
#   mask - Binary mask of selected contours 
#   hist_plot_type - None (default), 'all', 'rgb', 'lab', or 'hsv'
#                    This is the data to be printed to the SVG histogram file  
color_histogram = pcv.analyze_color(rgb_img=img, mask=kept_mask, hist_plot_type='all')
# Print the histogram out to save it 
pcv.print_image(img=color_histogram, filename="upload/Results/color_hist.png")


# In[27]:


# Divide plant object into twenty equidistant bins and assign pseudolandmark points based upon their 
# actual (not scaled) position. Once this data is scaled this approach may provide some information 
# regarding shape independent of size.

# Inputs:
#   img - RGB or grayscale image data 
#   obj - Single or grouped contour object 
#   mask - Binary mask of selected contours 
top_x, bottom_x, center_v_x = pcv.x_axis_pseudolandmarks(img=img, obj=obj, mask=mask)


# In[28]:


top_y, bottom_y, center_v_y = pcv.y_axis_pseudolandmarks(img=img, obj=obj, mask=mask)


# In[29]:


# The print_results function will take the measurements stored when running any (or all) of these functions, format, 
# and print an output text file for data analysis. The Outputs class stores data whenever any of the following functions
# are ran: analyze_bound_horizontal, analyze_bound_vertical, analyze_color, analyze_nir_intensity, analyze_object, 
# fluor_fvfm, report_size_marker_area, watershed. If no functions have been run, it will print an empty text file 
pcv.print_results(filename='upload/Results/VIS_results.txt')


# In[30]:


# Python program to convert text 
# file to JSON 


import json 


# the file to be converted to 
# json format 
filename = 'upload/Results/VIS_results.txt'

# dictionary where the lines from 
# text will be stored 
dict1 = {} 

# creating dictionary 
with open(filename) as fh: 

	for line in fh: 

		# reads each line and trims of extra the spaces 
		# and gives only the valid words 
		command, description = line.strip().split(None, 1) 

		dict1[command] = description.strip() 

# creating json file 
# the JSON file is named as test1 
out_file = open("upload/Results/Jason_result.json", "w") 
json.dump(dict1, out_file, indent = 4, sort_keys = False) 
out_file.close() 


# In[ ]:




