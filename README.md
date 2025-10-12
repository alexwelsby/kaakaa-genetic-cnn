# Convolutional Neural Networks as Kaakaa Embedding Extractors: A Comparison with a Canonical DINOv2 Approach, fka kaakaa-genetic-cnn

....no longer a genetic CNN project, as my cgp-cnn-fork did not produce a model that outshone VGG-19's capabilities.

This is the project repo for my AIML339 capstone project. All associated repos are included here as submodules.

Submodules:
- [Bird_individualID](https://github.com/AndreCFerreira/Bird_individualID/tree/35ef0bff7ab537486239276197dc89fdfb29a58f): Used. Ferreira et al.'s original implementation for identifying individual birds with deep learning. I utilised the [code for blur and noise augmentations](https://github.com/AndreCFerreira/Bird_individualID/blob/35ef0bff7ab537486239276197dc89fdfb29a58f/Data_pre-processing/Blur_noise_transformation.ipynb) and based my CNN training notebook off Ferreira's [here](https://github.com/AndreCFerreira/Bird_individualID/blob/35ef0bff7ab537486239276197dc89fdfb29a58f/Train_CNN/TRAIN_CNN.ipynb).
- [cgp-cnn-fork](https://github.com/alexwelsby/cgp-cnn/tree/c3004312570f93868d2ac98d1d64ee1e5ea42b91): Unmentioned in the paper. A fork of the original implementation of [cgp-cnn](https://github.com/sg-nm/cgp-cnn). I updated it to Chainer 7.8.1 and Python 3.10 for modern CUDA, in addition to adding some custom arguments (and even a branch for additional augmentations (which slowed evolution to a crawl...)). While it runs and even 'works', I did not manage to get a competitive model from it, and chose to pivot my project to embeddings. It remains a submodule as evidence that I worked on this project more extensively than the paper perhaps hints at.
- [Kaakaa Spotter](https://github.com/alexwelsby/kaakaa-spotter/) Unmentioned in the paper. A 'for fun' Django/React web server that hosts the [models I've trained](https://github.com/alexwelsby/kaakaa-genetic-cnn/tree/main/models) and copies of the FAISS database. Users can upload images of kaakaa; uploaded images can be masked by YOLO. Users can also get the class of their images 'predicted', with the caveat that FAISS isn't awesome at detecting unknown birds (and it's an image similarity search, so a known bird in a dissimilar image might look like a new bird...). **The Kaakaa Spotter is not finished; I aim to complete it by October 22nd.**

Directories:
- [helper scripts](https://github.com/alexwelsby/kaakaa-genetic-cnn/tree/main/helper_scripts): All notebooks I used to preprocess data or train models. Note that I haven't included scripts that I don't feel I 'own' here - so LLM scripts for automated file moving are not present. Notebooks I didn't write but where the output may be useful have been included - such as the Mask-RCNN evaluate_new_model.ipbyn. 
- [models](https://github.com/alexwelsby/kaakaa-genetic-cnn/tree/main/models): Models I've trained. DINOv2 was excluded, as I did not fine-tune or train the model in any way.



A journal of day-to-day changes and reasoning for them can be found [here](https://github.com/alexwelsby/kaakaa-genetic-cnn/blob/main/journal.md).



