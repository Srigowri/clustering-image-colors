# clustering-image-colors
KNN is written from scratch to find the dominant color in a given colored image.

Input colored image is resized to smaller size (still working on better way to resize, currently using Thumbnail module of PIL).
The getcolors module of PIL is used to read pixel values in terms of RGB. 
A KNN module is developed to find the 3 most dominant colors (RGB) in the given image.

Pending working:
Time comparision between the available knn libraries and this one. 
Image rescaling
Adding results
