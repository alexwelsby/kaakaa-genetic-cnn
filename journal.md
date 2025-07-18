# Journal

### 7/14

* Downloaded Mask\_RCNN and a trained mask\_rcnn to follow along with the second step in Bird\_IndividualID.
* Determined the pre-trained model identifies 'birds' well in field photos, but includes the feeder nozzle when identifying kaakaa as 'birds' in feeder photos.
* Determined model would need fine-tuning on the kaakaa dataset with annotated files to achieve good results (good=exclusion of the nozzle when identifying a bird).
* Annotated 300 kaakaa photos randomly chosen across Dataset B, C, and the Cornell Dataset.
* Began trouble-shooting appropriate library and Python versions for venv to run Mask\_RCNN.

### 7/15

* Ran Mask\_RCNN for 10 epochs in the morning. Did not achieve validation loss convergence.
* Implemented augmentation from imgaug per Mask\_RCNN guide.
* Trained for another 10 epochs in the evening to trouble-shoot whether the issue was a too-short training time. Did not successfully reach convergence.
* Identified small dataset of 244/67 train/val for fine-tuning as a potential source of overfitting (and wild yo-yoing val loss by extension).
* Annotated a further 200 kaakaa images. Trained Mask\_RCNN overnight on the larger dataset, continuing from that morning's epoch 10 checkpoint.

### 7/16

* Validation loss convergence was not successfully reached overnight. Began trouble-shooting.
* Turned to online implementations of custom datasets at github.com/soumyaiitkgp/Custom\_MaskRCNN/tree/master/samples/custom.
* Re-sized all images above 2000px in either dimension and re-sized annotations to match. Checked resized annotations in VGG to ensure they continued to correctly outline birds.
* It may be the images from the Cornell dataset that are making it difficult for the model to generalize, even with augmentation - there are 80 images from the Cornell dataset and the rest are single-pose, single-view shots in the feeder.
* Due to a conversation with Rachael Shaw today regarding an upcoming dataset with more natural environs and poses, chose to 'stick it out' with the Cornell dataset anyway in hopes that it may still be usable.
* Might remove it to test convergence if convergence is not reached tonight.
* Will need to begin working on brief pdf.
