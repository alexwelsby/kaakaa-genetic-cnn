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



### 7/18

* changed to AdamW optimizer, decreased learning rate, shrank Cornell images to largest dimension of dataset C images, fixed issue where tensorflow wasn't utilizing the GPU properly, steps now take half a second vs 10



### 7/19

* AdamW optimizer performed worse across three runs when compared to SGD, changed back. annotated 200 more wildlife photographs. added them to the dataset to provide dataset with a 40% wildlife/60% feeder split. val\_loss shot up from 0.19 to 0.40 on average.
* introduced keras.EarlyStopping



### 7/20

* split dataset into feeder and wildlife images to test theory that majority of loss came from wildlife photos. model trained off feeder-only images reached 0.14 val\_loss before plateau. model trained off wildlife-only images plateaued at 0.40 val\_loss. attempted to introduce wildlife-only images using feeder-only weights; exploded the loss.
* added alarm bell that plays when model stops training
* added automatic shutdown boolean



### 7/21

* might be in best interest to focus on feeder images for now. :(
* continued training feeder-only model using the best-of previous session with LR/10, then LR/100. reached 0.096 val\_loss (with 0.13 train on avg), plateaued there.
* added keras ReduceLROnPlateau
* while the model performs passably on masking feeder images (and sometimes wildlife photos), the resolution of the mask appears to be too low to capture the beak accurately - this is an issue when the dominant theory about kaakaa individual ID revolves around using the beak as a feature.
* may be an issue with how i masked as well - i added many anchors close to each other around the beak to be sure i captured the beak and not the nozzle - that fine-detailing seems to be getting lost
* from here: https://github.com/matterport/Mask\_RCNN/issues/635 others fixed this issue by changing mask\_shape to 56 and adding a convtranspose2d layer. as i have 8gb of GPU to work with i'll need to be careful about CUDA out of memory but it may work.
* model.py: MASK\_SHAPE=\[56,56] from \[28,28]; added additional Conv2DTranspose added under the existing one in build\_fpn\_mask\_graph (per the github guide). started training feederplusconvtrans2d
* stopped feederplusconvtrans2d at epoch 30 with val\_loss:0.0745 and loss:0.1125, epoch 30 (last epoch) was the best epoch using val\_loss as metric. opened it in view\_custom\_model.ibpyn and it's generating a polka-dotted checkerboard mask in the bbox instead of detecting the bird.
* ....it's actually doing that to all models i load into view\_custom\_model.ibpyn, so it's likely related to the convtrans2d layer not working out fsr?
* turned mini\_mask back on, moved the new convtranspose2d layer to the top of build\_fpn\_mask\_graph per https://stackoverflow.com/questions/65928571/how-can-i-improve-mask-prediction-by-mask-rcnn
* hving the same issue as this comment https://github.com/matterport/Mask\_RCNN/issues/635#issuecomment-817324793 and no suggested fixes help
* after 1 hour the issue was that custom.py was pulling the config a cached copy that got installed in my venv. had a scream and now i'm good. MASK\_SHAPE=\[56,56] now causes OOM error. decreased IMAGES\_PER\_GPU from 2 to 1.
* began training Feedermask52extraConv for 200 epochs with early stopping, ReduceLROnPlateau, leaving overnight
* GOOD TO NOTE: models developed with MASK\_SHAPE\[28,28] and read with an extra convtranspose2d layer will have the checkerboard pattern due to how conv/upsampling works



### 7/22

* Feedermask52extraConv performs well on feeder images BUT still either loses the thin tip of the beak or (if the beak tips are closer) sees the mouth as one big 'loop' that includes the nozzle. performs somewhat poorly on wildlife images but that's to be expected... since the current theory is that beaks are used to ID individuals, missing the beak tip is not great - but might be a limitation of mask\_rcnn itself
* talked to Bastiaan, I can look at other mask models if this one is not achieving what I want; may be reaching the limits of mask\_RCNN. I should also look at limiting the wildlife dataset to certain poses perhaps? kaakaa in flight definitely need to go
* the pointrend paper may be relevant as it addresses the issue of mask\_Rcnn masks being low resolution: https://arxiv.org/abs/1912.08193 but they don't offer an astonishing amount of support for custom datasets. may be a lot of trouble-shooting for an uncertain payoff... (especially since it's unclear whether my laptop can handle pointrend)
* ultralytics YOLO as well https://github.com/ultralytics/ultralytics - paula maddigan had good success with that on this project and it's extremely light-weight. wanted to present a novel-to-the-project approach but perhaps the novel aspect could be with regards to the genetic CNN bit.
* segment anything as well but it seems to be less light-weight
* https://github.com/SharpAI/DeepCamera good to keep in mind... might be fun to rip apart? would be cool if i could get a working AI camera (pipe dream for if this project was significantly longer)
* it also predicts one class for every image....... might not be an issue if I'm just using it to generate a masked dataset though 
* i need to take a break for a few days to do other assignments
* TODO: check out alternatives, write project plan pdf
