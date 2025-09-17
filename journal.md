# Journal

### 7/14

* Downloaded Mask\_RCNN and a trained mask\_rcnn to follow along with the second step in Bird\_IndividualID.
* Determined the pre-trained model identifies 'birds' well in field photos, but includes the feeder nozzle when identifying kaakaa as 'birds' in feeder photos.
* Determined model would need fine-tuning on the kaakaa dataset with annotated files to achieve good results (good=exclusion of the nozzle when identifying a bird).
* Annotated 300 kaakaa photos randomly chosen across Dataset B, C, and the Cornell Dataset.
* Began trouble-shooting appropriate library and Python versions for venv to run Mask\_RCNN.

### 7/15

* Ran Mask\_RCNN for 10 epochs in the morning. Did not achieve convergence.
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



### 8/1

* SSD began burning out; received replacement a few days ago and swapped it out
* going to download YOLO and presumably have some issues with it identifying the background as a fridge but we'll see
* https://github.com/mjhassan/VIA-to-YOLO-annotation-converter
* i can limit yolo to only label birds by doing ```yolo predict model=yolo11n.pt source="E:\\Datasets\\test video\\GH013646.MP4" classes=14```... useful, but want it to differentiate kaakaa as a species from other birds.
* could concatenate my dataset of the new kaakaa class with equal numbers of the original coco dataset classes? to avoid the catastrophic forgetting that happened when I did transfer learning with mask-rcnn coco heads-only using a kaakaa-only dataset... 
* https://github.com/ultralytics/ultralytics/issues/1707 and this comment explains in detail what they found to work for them re: catastrophic forgetting
* should probably consider how 'perfect' is reasonable for a 300-level project but we'll give it a go and see what happens
* bird-only dataset sounds fun too https://github.com/LeeYi-user/BIRDS-525-SPECIES-IMAGE-CLASSIFICATION with https://www.leafwindow.com/en/train-ultralytics-yolov8-with-birds-525-dataset-en/ ... but we don't need to be able to identify other birds at this stage of the project. coco dataset it is
* converted vgg annotations to yolo format, gave Kaakaa the class # 80 as coco classes end at 79, downloaded 580 training images and 145 validation images for each coco class (for a total of 58k images), plus the annotated kaakaa images (725 before val/split). based the size of the classes on the number of kaakaa images I have currently

### 8/3

* Got dataset working with YOLO on Google Colab.
* Trained YOLOv11 on Coco+Kaakaa dataset; restricted Coco dataset further, down to ~1100 images, to avoid overpowering Kaakaa dataset. used class=[80] (Kaakaa class)
* Trained for 200 epochs, left overnight. Tested it the next morning

### 8/4

* The model from the previous night performs well on kaakaa, but also identifies all birds as kaakaa.
* Changed how I split Coco; instead of eliminating Coco files randomly until I'm down to 1100 images, check if a Coco image has a bird, and add it to a set. Once the set size is equal to the Kaakaa dataset size, delete the rest. Add the other 1100 Coco images, as well.
* Trained YOLOv11-seg on 2:1:1 ratio of NegativeCoco:BirdCoco:Kaakaa class (classes=[14,80]). Got poor results on birds, middling results on kaakaa segmentation. Took an absolutely abhorrent amount of time (200 epochs) to get to 1.2 loss (train9)
* Took the best model from the previous run (train9). Trained it on the same split dataset, but this time with classes=[80] (Kaakaa only) - figured it might have learned differences between Kaakaa and other birds that might help it in fine-tuning now.
* This new model (train13) is wildly successful. Ignores all birds I've tested, contours and segments kaakaa perfectly.
* really makes me wonder how good it would be on an AI camera
* may be able to exit the instance segmentation stage and enter pre-processing

### 8/5
* Proposal presentation happened today
* Model is fantastic at ID'ing kaakaa that are the focus of an image, but can't ID them if they're in-context at a distance. I don't really need to fix this for my purposes but it offends my sensibilities as an ecologist so I've given myself until tomorrow morning to keep fiddling before moving on to pre-processing
* annotated 200 frames from a field recording I took at Zealandia of a feeder at a distance. only had 1 video to work with (and 1 video to use as a test) but i'm hoping the kaakaa moving throughout the video will help off-set any potential issues. 
* split 80/20 train/val, used roboflow to convert VGG annotations to YOLO, added it to original dataset
* used the train13 best model to train with the new data for 100 epochs

### 8/6 
* woke up at 4am and checked results in Google Drive... train14 now worse at capturing the beak in images from the Cornell dataset
* added another 150 epochs and went back to bed
* woke up; train16 is worse, mAP50-95 has plateaued at 0.85. i'd likely need more in-context videos/distance shots of kaakaa which is not in the scope of my project. decided to abandon this line of inquiry and return to train13
* generated a fully masked version of Dataset B and Dataset C

### 8/16
* games capstone finally calmed down so now I can return to this
* pre-processed Dataset B and C using Bird_IndividualID
* additionally offline augmented classes <500 images up to 500 using torchvision transformations
* to make the 'mini dataset' for ENAS, created a copy of the augmented/preprocessed full dataset; for all classes >500 images, delete images at random until we reach 500
* not the most high-tech solution as i wanted to do on-the-fly augmentation instead but i'm a bit pressed for time to troubleshoot
* training a preliminary CNN on the dataset and it's converging far too fast. validation curve is already nearing 100%. absolutely perfect and frightening curves. data leakage? did i augment too much and now it's just memorizing?
* deleting my custom local augmentations did not have a huge impact, left Ferreira's Individual_BirdID augs in... still already converging at epoch 4
* did Ferreira have data leakage?!
* OH i pre-processed everything which meant the val/test set got transformed. forgot about that. means i lost time though
* Ferreira also had the method to check for image similarity.
* mustn't forget i get stupid when time is short
* might put an unofficial deadline to start ENAS by Wednesday so i do not yank my hair out and lose time doing so. and if i can start it before then i'll start it before then

### 8/17
* been spending today and yesterday attempting to create a baseline CNN and failing, mostly due to overfitting issues
* currently trying: 200 epochs, early stopping, ReduceLROnPlateau, Adam Optimizer with lr=1e5, class_weights disabled, planning to run until it stops itself and then starting again from the saved model
* https://karpathy.github.io/2019/04/25/recipe/#2-set-up-the-end-to-end-trainingevaluation-skeleton--get-dumb-baselines reading this
* double-checking with Ferreira's paper and they lowered dropout to 0.2 for great tits
* trying again, dropout lowered to 0.2, class weights disabled. val_loss still seesaws around 0.90 
* notably Ferreira does not mention or stress about this but their ibpyn file shows a perfect curve downwards while mine is... uh..
* now attempting dropout(0.1) with class weights which will most assuredly kill all learning but let's see if something has changed: results are that learning took place, but we ended with training loss of 0.02 and val_loss of 1.17
* with same parameters but reduceLrOnPlataeu removed, imported weights of last bullet point and trained for 22 epochs; achieved val_loss of 0.64
* with same parameters but SDG instead of Adam, imported weights of last bullet point and trained for ~5 epochs; achieved val_loss of 0.59
* imported weights of last bullet point and trained for ~10 epochs; achieved val_loss of 0.51
* further attempt with 3e-5 learning rate was unstable. reduced back to 1e-5. val_loss of 0.47
* might be getting tunnel vision, it's 1am. should run a test
* dropout01_classweights_047valloss.h5 gets 96% accuracy on the test set, 63% accuracy on the entirety of Dataset C (LATER NOTE: I WAS OVERTIRED AND ONLY RAN IT ON A FRACTION OF EITHER DATASET INSTEAD OF THE FULL BATCH.)


### 8/18
* does not recognize birds if they're not masked. but that's... fine... assuming YOLO will always be run...
* dropout increased to 0.4. old weights do not work w new dropout, learning completely collapses with 0.4 dropout as it did with 0.5 dropout
* val_loss stabilizes at a higher place higher with a lower batch size (8) and destabilizes with a higher batch size (32)
* might be fine to move on as the benchmark performs well enough on test evaluation (with the exception of the backgrounds)
* cloning EEEA-Net and giving myself until tomorrow to figure out how to add a custom dataset to it
* the EEEA-Net datasets are under EEEA/nameofdataset/eeea/data/datasets.py ... looks like i might run over time if I attempt to pull the file structure apart to make it take a custom dataset
* decided to modernize cgp-cnn instead... aaaand got it working(?) 
* letting it run for a little bit on cifar10 to try to benchmark how long it will take
* seems to go okay. i'll test it with 224x224 kaakaa images just to see. the code is so old that it uses np.random.permutation() instead of chainer's iterator class to randomize the data.
* https://github.com/chainer/chainer/blob/master/chainer/datasets/cifar.py will take some work to get the custom dataset congruent with how chainer sets up datasets though. chainer makes me regret my math skills (lack thereof)
* seem to have gotten it working. quite surprising. the train and validation are not too stable though but it is using SDG instead of Adam
* tomorrow: change the generation population from 20 to 8, change total epochs to 10. and introduce a method to save a population to disk (and load it. again. somehow)
*  each cgp-cnn epoch is averaging around 30 seconds which puts us well below my estimate of 20 minutes per 10-epoch model hallelujah
* also: tomorrow, set a generation target of 1 and a population of 1 to see what it saves to evaluate the model
* need to quit now as i'm unwell

### 8/20
* took yesterday off due to a stomach bug
* cgp-cnn fork now has arguments for generation # and epoch #
* also verified my method of turning the images into numpy arrays was correct by grabbing the dataset and converting back into a format cv2 could display (and the images look fine, great even)
* we run into cuda out of memory problems with 224x224 kaakaa images... might see if I can use a more powerful GPU because i'd rather the models are evaluated as close to the benchmark as possible
* added a size argument so i can test that
* since the genetic algorithm will take less time than i budgeted for, i may have time to experiment with re-making the dataset with randomized backgrounds to see if that fixes the issue where it can't recognize non-masked images or whether the primary issue is due to the non-masked dataset C not being cropped to the kaakaa's region... my instinct is that it's partly due to the cropping but Ferreira tested against multiple different backgrounds so ?
* used chatgpt to make a script that outputs kaakaa against random coco backgrounds, cropped to the kaakaa bounding box: 0.0% accuracy
* weirdly enough the non-cropped coco kaakaa images had an accuracy of 1%... so it seems to largely be a function of the background
* this feels too stupid to be science. and yet i'm compelled
* late and i'm getting nonsensical. break for today
* tomorrow: split a new copy of the dataset, mask train, provide coco random background to train, add Ferreira augmentations and keras augmentations, train another model and see what happens

### 8/21
* worried about my benchmark. realized i input the batch_size for the test set wrong; true acc of best run was 85%, and class-by-class analysis shows it scores 0.0 precision on three rare classes even with class weighting
* no iteration I had of the coco random backgrounds ever learned a thing. coco random backgrounds likely had contrast that was too high; cnn focused on that instead of the lower-contrast kaakaa. no time to figure it out.
* out of frustration and a little fear began trying to hammer in benchmarks results on the original (masked/split by day) dataset again
* wasted the day fiddling with it in vain hopes of finding a combination of hyperparameters that would work for a tiny, and unbalanced, dataset
* I know Abby is using StratifiedKFold to do this but my understanding of that is that it trains 5 different versions of the same model on different iterations of the dataset and is used to evaluate an average acc while each model will have its weaknesses... so there is no 'one' model to use in the field. but she's also using it as a feature extractor on unlabeled images (? I think, also there are far more unlabeled images vs labelled ones) while i'm doing classification on labelled ones. ack
* regardless, engaged in the following fruitless endeavors:
* with dropout 0.1, started overfitting around epoch 6 (val_loss stopped decreasing)  
* with dropout 0.2, plateaus faster at around epoch 4(?!). increased learning rate to 1e-4  
* with learning rate 1e-4, learning did not occur. tried x = GlobalAveragePooling2D()(x) above dropout and removed flatten  
* learning did not occur. moved x = GlobalAveragePooling2D()(x) below dropout  
* learning did not occur. using dropout 0.1 with globalaveragepooling2d in same place  
* learning did not occur. decreased learning rate to 1e-5.  
* learning appeared to take place and then overfitting began at epoch 10, val_loss plateaued at around 1.0 with some stochasticity resulting in a 0.87 val_loss  
* added kernel_regularizer=l2(0.01), bias_regularizer=l2(0.01) to dense layer. val_loss plateaued at 2.6 around epoch 13  
* removed bias_regularizer. plateaued around epoch 7, swings from between 4 and 2.6 repeatedly  
* removed class_weights. possible it's conflicting with my oversampling.  
* with kernel_regularizer no bias_regularizer it seems it always has a big jump down for val_loss around epoch 7, and then immediately plateaus with rapid fluctuations between 4.0 and 2.6 or so  
* switched out kernel_regularizer for bias_regularizer. no class weights. notice things start at a more manageable loss (2.4) though below ln(17). learning speed is comparable to without regularizer. assuming overfitting will occur around the same time and the same val_loss value (epoch 10, ~0.80 range). plateau occurred around epoch 6. did not recover by 10, ended   
* replaced bias_regularizer with kernel_regularizer, reduced l2 to 0.001. enabled class weights. plateaued around epoch 9 at 1.49  
* commented out GlobalAveragePooling2D()(x) and replaced with Flatten()(x) again. set dropout to 0.15. plateaued around epoch 13, bouncing between 0.8 and 1.3  
* trying again but with W-BB removed, which only had 1 image in val. made no difference, actually made things slightly worse (plateaued at 0.97 instead). could just be down to stochasticity but i don't have time to confirm. replaced Dropout with SpatialDropout2D
* ran a few more desperate bids that were all fruitless. had one promising run where val_loss stabilized around 0.56 (class_weights, dropout(0.15), using SGD to polish) but SGD sank into a local minima and never improved beyond 0.98 training loss; further improvement on training loss resulted in val_loss increasing (could be learning augmentation patterns instead?)
* models without class_weights performed poorly on rare classes vs models with class_weights... so it appears the paranoia about it conflicting with oversampling was unfounded
* may have to bite the bullet for the sake of the project and consider comparing against another dataset just to prove I'm competent and am capable of running a CNN 
* also can't delay any longer re: the genetic algorithm. need it to get started tomorrow
* will be expensive to run my dataset and Ferreira but i haven't abandoned the dream that the issue might be the too-large model.

### 8/22
* copying Ferreira's 68.6GB(!) dataset 
* also starting the genetic algo on the kaakaa dataset today; 20 generations, 8 offspring, 10 epochs per model
* L4 GPU kept getting OOM CUDA errors, changed to A100 (eek expensive)
* should currently have twice the credits I actually need for A100 (knock on wood) to finish running the algo but murphy's law applies. I'll check throughout the day
* some of the models being generated are quite large; might want to decrease the offspring/lambda
* issues with how the new chainer version concat works and sum
* https://docs.chainer.org/_/downloads/en/v1.16.0/pdf/ holy hell
* misunderstood what they meant by 'dummy function' for concat so will need to roll that back potentially... actually it might be fine as the issue i thought was happening every time seems to be an edge case as a result of the evolution algo. carry on
* OOM is also expected as part of the algorithm. i need to stop panicking and start remembering the papers I've read
* the mean and loss I'm getting thusfar is nuts... 0.04 train and 0.04 valid by epoch 10
* a few too many oom for my liking, likely due to the larger image size (224 instead of 32), so decreased the batch_size to 64... which means i had to half my lambda as well to avoid getting smacked by colab's 24 hour limit but oh well
* current run: 20 generations, 4 offspring, 10 epochs per model
* the .model it outputs after re-training is... extremely difficult to use or do anything with. which defeats the purpose of all of this lol should have seen this coming when I used chainer
* made a new python script to analyse class accuracies
* added precision, recall, and f1 per class as well
* since that's done I guess I can justify doing cgp-cnn proper now... starting tomorrow
* double-checked that my labels are aligned with cifar (int instead of one-hot) and they are, so that's not what's causing the fast convergence. i think i just need to accept my model isn't going to be very good and get on with it
* also looking at Ferreira's dataset they DID crop val and test sets as well so I'm fine

### 8/23
* started cgp-cnn in earnest today at 11am. 20 generations, 4 offspring, 10 epochs per model. 
* algorithm was accidentally aborted at 7pm after 8 hours; due to cgp-cnn only saving the cgp-log.txt when the process exits successfully, no model could be saved from the run. 45 models in total lost to the abyss
* re-rolled cgp-cnn a few times to try to get a strong-ish starting model from which the other models will spring (sometimes it initializes with models that bounce wildly in excess of 14-30 loss and val_loss at every epoch with no apparent improvement in prediction confidence, and it was hard to justify the compute to iterate on that when my previous run initialized with reasonable values)
* new run officially started at 9:26PM. things seem reasonable (knock on wood), though of course not as good as the one that got away

### 8/24
* at 9:04AM, 11hrs35min of runtime: 62 models run thusfar. so approx 4 hours remaining on this run
* seems like we discovered a model that got 91% val_acc early on and have just been re-rolling from that model repeatedly
*...hopefully retraining can maintain that acc
* ended at 12:26PM. best model was the 91% acc one. retraining with 20 epochs regular training SGD optimizer, 10 val training...
* top val accuracy reached was 0.90 but never reached convergence. well that's fine i guess
* generated the graph of my new model using GraphvizOnline https://dreampuf.github.io/GraphvizOnline/
* per class acc/f1/recall/precision is abysmal for any class i had to significantly augment. 

### 8/28
* trying again with Ferreira's great tits dataset. all classes have 375-900 images in train and 100 images in val, but 4 of 10 classes are missing images in test... however, as this is how Ferreira evaluated the model, this should be fine for my purposes
* for train: oversampled locally (ie: copying randomly selected images in train until we reach 900 images per class). 'low tech' and not good practice for AI perhaps, but Ferreira never mentioned how they oversampled and this is proof of concept, so...
* feeling quite silly for my previous behavior as the local augs only took place for sociable weavers due to their test images having lower quality. I need to get better at reading words when I'm excited about a paper...
* with VGG16 and dropout 0.2 the model doesn't learn, but with VGG19 and dropout 0.2 the model seems to be learning well. seems VGG19 is 'about right' as far as model complexity goes for the great tits task; should be noted i switched to vgg16 for the kaakaa task but it was worth investigating the difference w/ great tits anyways
* accuracy of 81.9%... Should be noted that the great tits set uses the top perspective, and the original paper's acc is 85.1%
* despite following Ferreira's methods? i did correct what i felt was an error (Ferreira shuffles the validation set) but perhaps I should revert that..


### 8/29
* oversampling through copying  files manually: kaakaa dataset b split by day, train oversampled to 500 images per class. -B removed due to too few examples
* per https://arxiv.org/abs/1710.05381, "oversampling does not cause overfitting of CNNs"... though I'm doing it fairly aggressively...
* re-running kaakaa cnn benchmark with dataset that's locally oversampled to 500 images per class but not locally augmented. augmentation only takes place on the fly now and is only flips/rotation/zoom/rescale per the great tits augs.
* overfits within 2 epochs with dropout 0.2
* running with dropout 0.5: val_loss is wildly unstable, final accuracy was 84.1%, abysmal on small classes though
* after running Ferreira's dataset and seeing how it was impacted by shrinking the validation set, willing to draw the conclusion that this is due to the imbalance and size of the validation set
* running in parallel: dropout 0.75: froze at ln(num_classes), no further learning
* running in parallel: dropout 0.625: best loss was 0.77, val_loss wildly unstable
* forgot Y-MY is wildly unbalanced using the split script i have lol, 1 val vs 15 train
* rerunning 0.5 dropout with new re-balance, running 0.6 in parallel
* 0.5 achieved 0.85 acc, 0.6 achieved 0.75 acc

### 8/30
* running cgp-cnn using Ferreira great tits dataset
* evaluated best CNN on the ferreira-structured kaakaa dataset on dataset C. it gets 5% accuracy. vs the augmented vgg19 one that got 63%. tearing my hair out
* as the sociable weavers dataset had a general increase in acc after augmentation, i'll try changing augmentation first and see what that does..
* best loss w/ adam was 0.79, Sgd managed to improve incrementally for 11 epochs and got to 0.74, going to increase the lr for sgd and see if i can get it to learn/generalize a little faster
* increased lr to 5e-6, let's see what happens.. got it down to 0.68 val_loss .88 acc
* accuracy with dataset C is 16%... just realized that due to how CNNs works none of my evaluations on dataset C have meant anything because the classes/one-hot encodings don't align. not sure how I didn't remember that until. now. 2 weeks into classifying birds.
* why did i do supervised classification instead of feature extraction? 
* i need to eat dinner before I make drastic changes to my approach 
* banning myself from implementation until it's not 11pm and i'm not hypoglycemic but https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU

### 9/5
* when attempting to re-produce kaakaa benchmark ith .5 dropout.. learning stopped occurring
* nothing has changed. it's a duplicate ipbyn of the 'winning' one
* decreasing dropout makes learning take place again; 0.2 overfit, 0.3 in progress but will likely overfit
* why did 0.5 dropout get our 'best' outcome previously, and now result in totally decimated learning?
* 0.3 overfit faster than the original 0.5 run... going to try 0.35 because i want to get as close to the original dropout as possible
* 0.35 also learned fine but overfit quickly
* 0.5 began working... I forgot about keras seeds.
* seed 13 no learning, seed 14 no learning, seed 29 no learning, 1996... lost count of the seeds I tried which is my failure but any seed at dropout(0.5) resulted in no learning taking place. truly seems like i got the 1-in-a-million successful run unless something else somehow happened(?) despite the code being the same?
* said to hell with it, added the vgg19 preprocessing function that Ferreira's implementation did not use, removed Ferreira's resize() normalization, dropped dropout to 0.48 and after a few subpar seeds got a model with 90.6 OVERALL ACCURACY(!!!), with keras.utils.set_random_seed(3434343) 

### 9/15
* been working on the research paper in small 100-word chunks for the past week
* got my act together enough to write code that would get the classifier to match classes using a flow_from_directory where directories were out-of-order

### 9/16
* bastiaan confirmed i should not be using tp+tn/(tp+tn+fp+fn) to calculate per-class accuracy so i will not do that

### 9/17
* without tp+tn/(tp+tn+fp+fn) it gets 29% accuracy on dataset c...
* the hero10 has a higher resolution than the camera used in dataset b; maybe I should pre-process dataset c images to be lower quality, similar to what Ferreira did for sociable weavers?
* probably not going to do a huge amount for me tho lol
* beheaded model (removed classifier head), experimenting with vector outputs and FAISS... may move to DINOv2 due to the aforementioned 29% acc though
* up to 35.4% when using my own preprocessing function...
* notice that a lot of the 'bad' predictions are on B-, which is a small part of dataset b (45 original images) but a huge part of dataset c (nearly half of the dataset; 2k). wonder what happens if i cull B-... obviously not going to use the culled acc as a final acc I just think it would be interesting to discuss
* up to 51.9 without B- so it may just beef it on dataset C B- subset
* ...may be in the exciting yet unenviable position of training an entirely new model in week 9
* https://www.youtube.com/watch?v=APDU8p5O2yc and https://colab.research.google.com/github/pyresearch/notebooks/blob/main/notebook/dinov2_classification.ipynb
* https://github.com/csaroff/dinov2/tree/main/sky
* DINOv2 seems like it will potentially be quite expensive if csaroff's to be believed... maybe ViT-S will be different
* either way: the kaakaa project is currently working on embeddings, even if I do not have a model that will be epic at providing them, and Andrew mentioned wanting a website for it... 
* perhaps my model does not have to be good but simply has to be good enough for proof of concept with a React/Django?FAISS? website
* started work on React project that will act as an interface for uploading images
* eek. so scary.
* should have a dashboard (that shows the most recently uploaded images... ideally unmasked because I like to see greenery in my life), a page for uploading images (that will also show the generated vector (and maybe the YOLO masked image?) for fun), maybe a stats page? that lets you drill down on a label's associated images
* what's that disco Elysium quote that was like "it's remarkable, the shorter their time and less their money, the larger the game became". find my 'outcomes' in the abandoned commercial district 5 years from now
* much of the react code is going to be shamelessly copied from the dsa visualizer if only to speed things along (and because I'm not being evaluated on my web design...)
* should also begin fixing up the repo tomorrow if I'm doing this