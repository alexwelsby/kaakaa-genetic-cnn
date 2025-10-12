- Pre-processing: Contains the FIFTYONE script I used to prune too-similar images from the dataset. All other pre-processing referenced Ferreira's pre-processing methods found in Ferreira's [Bird_individualID](https://github.com/AndreCFerreira/Bird_individualID/tree/35ef0bff7ab537486239276197dc89fdfb29a58f).
- instance segmentation: Contains the script I used to evaluate Mask_RCNN and the training script for YOLOv11.
- finding_optimal_cnn: Contains scripts for training the benchmark CNN for both the Ferreira Great Tits dataset (undiscussed in the paper) and the kaakaa dataset B, as well as scripts for utilising CGP-CNN on Ferreira's Great Tits dataset and the kaakaa dataset B.
- embeddings_faiss: contains scripts for accessing embeddings and evaluating k-NN using FAISS for CNN and DINOv2.


