#!/usr/bin/env python
# coding: utf-8

# In[31]:


# Import libraries
from plantcv import plantcv as pcv 
import matplotlib


# In[32]:


class options:
    def __init__(self):
        self.image = "upload/input2/input.jpg"
        self.debug = "plot"
        self.writeimg= False
        self.result = "upload/output_imgs2"
        self.outdir = "upload/Results12" # Store the output to the current directory
        
# Get options
args = options()

# Set debug to the global parameter 
pcv.params.debug = args.debug


# In[33]:


# Read image

# Inputs:
#   filename - Image file to be read in 
#   mode - How to read in the image; either 'native' (default), 'rgb', 'gray', or 'csv'
img, path, filename = pcv.readimage(filename=args.image)


# In[34]:


# Convert RGB to HSV and extract the saturation channel

# Inputs:
#   rgb_image - RGB image data 
#   channel - Split by 'h' (hue), 's' (saturation), or 'v' (value) channel
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
pcv.print_image(img=s, filename="upload/output_imgs2/R2H.jpg")


# In[35]:


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
pcv.print_image(img=s_thresh, filename="upload/output_imgs2/Bthresh_img.jpg")


# In[36]:


# Median Blur to clean noise 

# Inputs: 
#   gray_img - Grayscale image data 
#   ksize - Kernel size (integer or tuple), (ksize, ksize) box if integer input,
#           (n, m) box if tuple input 
s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
pcv.print_image(img=s_mblur, filename="upload/output_imgs2/Mblur_img.jpg")


# In[37]:


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
pcv.print_image(img=gaussian_img, filename="upload/output_imgs2/Blur_img.jpg")


# In[38]:


# Convert RGB to LAB and extract the blue channel ('b')

# Input:
#   rgb_img - RGB image data 
#   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

# Threshold the blue channel image 
b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, 
                                object_type='light')
pcv.print_image(img=b_thresh, filename="upload/output_imgs2/Extracted_img.jpg")
pcv.print_image(img=b, filename="upload/output_imgs2/Gray_img.jpg")


# In[39]:


# Join the threshold saturation and blue-yellow images with a logical or operation 

# Inputs: 
#   bin_img1 - Binary image data to be compared to bin_img2
#   bin_img2 - Binary image data to be compared to bin_img1
bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_thresh)
pcv.print_image(img=bs, filename="upload/output_imgs2/BSature_img.jpg")


# In[40]:


# Appy Mask (for VIS images, mask_color='white')

# Inputs:
#   rgb_img - RGB image data 
#   mask - Binary mask image data 
#   mask_color - 'white' or 'black' 
rgb_img=img
masked = pcv.apply_mask(rgb_img, mask=bs, mask_color='white')
pcv.print_image(img=masked, filename="upload/output_imgs2/VIS_img.jpg")


# In[41]:


# Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels

masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')
pcv.print_image(img=masked_b, filename="upload/output_imgs2/GrayScale_img.jpg")
pcv.print_image(img=masked_a, filename="upload/output_imgs2/Green-Magenta.jpg")


# In[42]:


cropped_mask = pcv.threshold.binary(gray_img=masked_a, threshold=115, 
                                      max_value=255, object_type='dark')
pcv.print_image(img=cropped_mask, filename="upload/output_imgs2/R2H_img.jpg")


# In[43]:


#cropped_mask = maskeda_thresh[1150:1750, 900:1550]


# In[44]:


# Skeletonize the mask 
#%matplotlib notebook
# To enable the zoom feature to better see fine lines, uncomment the line above ^^ 

# Inputs:
#   mask = Binary image data
skeleton = pcv.morphology.skeletonize(mask=cropped_mask)
pcv.print_image(img=skeleton, filename="upload/output_imgs2/Skeleton_img.jpg")


# In[45]:


# Prune the skeleton  
# Generally, skeletonized images will have barbs (this image is particularly ideal, 
# that's why it's the example image in the tutorial!), 
# representing the width, that need to get pruned off. 

# Inputs:
#   skel_img = Skeletonized image
#   size     = Size to get pruned off each branch
#   mask     = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
img1, seg_img, edge_objects = pcv.morphology.prune(skel_img=skeleton, size=10, mask=cropped_mask)
pcv.print_image(img=img1, filename="upload/output_imgs2/img.jpg")
pcv.print_image(img=seg_img, filename="upload/output_imgs2/Seg_img.jpg")


# In[46]:


# Identify branch points   

# Inputs:
#   skel_img = Skeletonized image
#   mask     = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
branch_pts_mask = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=cropped_mask)
pcv.print_image(img=branch_pts_mask, filename="upload/output_imgs2/BPoints_img.jpg")


# In[47]:


# Identify tip points   

# Inputs:
#   skel_img = Skeletonized image
#   mask     = (Optional) binary mask for debugging. If provided, debug 
#              image will be overlaid on the mask.
tip_pts_mask = pcv.morphology.find_tips(skel_img=skeleton, mask=None)
pcv.print_image(img=tip_pts_mask, filename="upload/output_imgs2/Tipoint_img.jpg")


# In[48]:


# Adjust line thickness with the global line thickness parameter (default = 5),
# and provide binary mask of the plant for debugging. NOTE: the objects and
# hierarchies returned will be exactly the same but the debugging image (segmented_img)
# will look different.
pcv.params.line_thickness = 3 


# In[49]:


# Sort segments into primary (stem) objects and secondary (leaf) objects. 
# Downstream steps can be performed on just one class of objects at a time, 
# or all objects (output from segment_skeleton) 
  
# Inputs:
#   skel_img  = Skeletonized image
#   objects   = List of contours
#   mask      = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
leaf_obj, stem_obj = pcv.morphology.segment_sort(skel_img=skeleton, 
                                                 objects=edge_objects,
                                                 mask=cropped_mask)


# In[50]:


# Identify segments     

# Inputs:
#   skel_img  = Skeletonized image
#   objects   = List of contours
#   mask      = (Optional) binary mask for debugging. If provided, 
#               debug image will be overlaid on the mask.
segmented_img, labeled_img = pcv.morphology.segment_id(skel_img=skeleton,
                                                       objects=leaf_obj,
                                                       mask=cropped_mask)
pcv.print_image(img=segmented_img, filename="upload/output_imgs2/Segment.jpg")
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Labeled.jpg")


# In[51]:


# Similar to line thickness, there are optional text size and text thickness parameters 
# that can be adjusted to better suit images or varying sizes.
pcv.params.text_size=.8 # (default text_size=.55)
pcv.params.text_thickness=3 # (defaul text_thickness=2) 

segmented_img, labeled_img = pcv.morphology.segment_id(skel_img=skeleton,
                                                       objects=leaf_obj,
                                                       mask=cropped_mask)
pcv.print_image(img=segmented_img, filename="upload/output_imgs2/Segment1.jpg")
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Labeled1.jpg")


# In[52]:


# Measure path lengths of segments     

# Inputs:
#   segmented_img = Segmented image to plot lengths on
#   objects       = List of contours
labeled_img  = pcv.morphology.segment_path_length(segmented_img=segmented_img, 
                                                  objects=leaf_obj)
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Labeled_img.jpg")


# In[53]:


# Measure euclidean distance of segments      

# Inputs:
#   segmented_img = Segmented image to plot lengths on
#   objects       = List of contours
labeled_img = pcv.morphology.segment_euclidean_length(segmented_img=segmented_img, 
                                                      objects=leaf_obj)
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/EuclidDist_img.jpg")


# In[54]:


# Measure curvature of segments      

# Inputs:
#   segmented_img = Segmented image to plot curvature on
#   objects       = List of contours
labeled_img = pcv.morphology.segment_curvature(segmented_img=segmented_img, 
                                               objects=leaf_obj)
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Curvature_img.jpg")


# In[55]:


# Measure the angle of segments      

# Inputs:
#   segmented_img = Segmented image to plot angles on
#   objects       = List of contours
labeled_img = pcv.morphology.segment_angle(segmented_img=segmented_img, 
                                           objects=leaf_obj)
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Angle_img.jpg")


# In[56]:


# Measure the tangent angles of segments      

# Inputs:
#   segmented_img = Segmented image to plot tangent angles on
#   objects       = List of contours
#   size          = Size of ends used to calculate "tangent" lines
labeled_img = pcv.morphology.segment_tangent_angle(segmented_img=segmented_img, 
                                                   objects=leaf_obj, size=15)
pcv.print_image(img=labeled_img, filename="upload/output_imgs2/Tangent_img.jpg")


# In[61]:


# Python program to convert text 
# file to JSON 


import json 


# the file to be converted to 
# json format 
filename = 'upload/Results2/MOR_result.txt'

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
out_file = open("upload/Results2/Jason_result.json", "w") 
json.dump(dict1, out_file, indent = 4, sort_keys = False) 
out_file.close() 