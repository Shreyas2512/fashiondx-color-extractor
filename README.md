# fdx-color-extractor
A repository containing core, cli and webapp packages for extracting colors from an image. Used 2 color extraction algorithms - color-thief and algolia color extractor.
Color thief is used for swatch fabric images and algolia color extractor for non swatch fabric images. Both use KNN algorithm to cluster colors.
The webapp allows user to upload images from frontend and specify the number of clusters (colors) if required. If user does not specify the number of clusters, default is 5 
