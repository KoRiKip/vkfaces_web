#!/usr/bin/env python
# encoding=utf8
from __future__ import print_function
import warnings
warnings.filterwarnings("ignore")
import sys
import os
os.environ['GLOG_minloglevel'] = '3'
import numpy as np
import caffe

# The caffe module needs to be on the Python path; we'll add it here explicitly.
import argparse
import glob
import re
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import shutil
from align import Aligner


class Reidentifier:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--caffe', type=str, default=os.path.expanduser("~/caffe"), help='--caffe ~/caffe')
        parser.add_argument('--gpu', type=int, help='--gpu 0 . If --gpu not specified, then cpu will be used')
        parser.add_argument('--model', type=str, default='./', help='--model /root/model/')
        parser.add_argument('--train', type=str, default='train', help='--test /root/train')
        parser.add_argument('--descriptorLayer', type=str, default='embed', help='--descriptorLayer embed')
        parser.add_argument('--verbose', default='true', action='store_true')
        self.args = parser.parse_args()

        alignerArgs = properties()
        alignerArgs.inputDir = self.args.train
        alignerArgs.dlibFacePredictor = 'shape_predictor_68_face_landmarks.dat'
        alignerArgs.align = ''
        alignerArgs.landmarks = 'outerEyesAndNose'
        alignerArgs.size = 128
        alignerArgs.skipMulti = False
        alignerArgs.verbose = False
        alignerArgs.fallbackLfw = False
        print('Train folder:', self.args.train)
        alignerArgs.inputDir = self.args.train
        alignerArgs.outputDir = self.args.train
        self.aligner = Aligner(alignerArgs)

        #todo?
        #caffe_root = os.path.join(self.args.caffe, 'python')
        #sys.path.insert(0, caffe_root)
        #import caffe

        # Load the net, list its data and params, and filter an example image.
        if self.args.gpu:
            caffe.set_mode_gpu();
            caffe.set_device(self.args.gpu);
        else:
            caffe.set_mode_cpu();

        deployProtoPath = sorted(list(glob.glob(os.path.join(self.args.model, '*.deploy.prototxt'))))[-1]
        if self.args.verbose:
            print(deployProtoPath)
        caffeModelPath = human_numeric_sort(list(glob.glob(os.path.join(self.args.model, '*.caffemodel'))))[-1]
        if self.args.verbose:
            print(caffeModelPath)

        self.net = caffe.Net(deployProtoPath, caffeModelPath, caffe.TEST)
        if self.args.verbose:
            print("blobs {}\nparams {}".format(self.net.blobs.keys(), self.net.params.keys()))

        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost dimension
        self.transformer.set_mean('data', np.array([127.5, 127.5, 127.5]))  # subtract the dataset-mean value in each channel
        self.transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
        self.transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR


    #def set_reference_descriptors(self):
    #    pass

    def reindetify(self, testImagePath, train_image_dir):
        testImage = caffe.io.load_image(testImagePath)
        center = np.array([testImage.shape[0], testImage.shape[1]]) / 2.0
        crop_dims = np.array([self.net.blobs['data'].data.shape[2], self.net.blobs['data'].data.shape[3]])
        crop = np.tile(center, (1, 2))[0] + np.concatenate([
            -crop_dims / 2.0,
            crop_dims / 2.0
        ])
        crop = crop.astype(int)

        isCropNeeded = testImage.shape[0] != self.net.blobs['data'].data.shape[2] or testImage.shape[1] != \
                                                                                     self.net.blobs['data'].data.shape[3]
        trainImages = getImages(train_image_dir)
        print(trainImages)

        #testImages = {-1: testImagePath}
        if isCropNeeded:
            trainDescriptors = self.getDescriptors(self.args, trainImages, caffe, self.net, self.transformer, crop)
            #testDescriptors = self.getDescriptors(self.args, testImages, caffe, self.net, self.transformer, crop)
        else:
            trainDescriptors = self.getDescriptors(self.args, trainImages, caffe, self.net, self.transformer)
            #testDescriptors = self.getDescriptors(self.args, testImages, caffe, self.net, self.transformer)

        print('Results:')
        #testPath = testDescriptors.keys()[0]
        #similar = cosine_similarity(np.array(testDescriptors[testPath]).reshape(1,-1), trainDescriptors.values())[0]
        descriptor = self.get_descriptor(self.args, caffe, crop, testImagePath, self.net, self.transformer)
        similar = cosine_similarity(np.array(descriptor).reshape(1, -1), trainDescriptors.values())[0]
        idx = similar.argsort()[::-1]
        class_name = trainDescriptors.keys()[idx[0]]
        class_name = os.path.dirname(class_name)
        class_name = os.path.basename(class_name)
        return class_name

    def getDescriptors(self, args, images, caffe, net, transformer, crop=None):
        descriptors = {}
        for folder in images.keys():
            for index, imagePath in enumerate(images[folder]):
                if args.verbose:
                    print(folder, index, imagePath)

                output = self.get_descriptor(args, caffe, crop, imagePath, net, transformer)
                descriptors[imagePath] = output
        return descriptors

    def get_descriptor(self, args, caffe, crop, imagePath, net, transformer):
        self.aligner.align(imagePath)  # in-place aligner
        image = caffe.io.load_image(imagePath)
        if crop is not None:
            # central crop
            image = image[crop[0]:crop[2], crop[1]:crop[3], :]
        transformed_image = transformer.preprocess('data', image)
        # copy the image data into the memory allocated for the net
        net.blobs['data'].data[...] = transformed_image
        output = net.forward(end=args.descriptorLayer)[args.descriptorLayer][0].tolist()
        return output


class properties(object):
    pass


def human_numeric_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def getImages(path):
    images = {}
    for folder in glob.glob(os.path.join(path, '*')):
        images[folder] = []
        for imagePath in glob.glob(os.path.join(folder, '*')):
            images[folder].append(imagePath)
    return images

