# encoding=utf8
import argparse
import cv2
import numpy as np
import os
import random
import shutil

import openface
import openface.helper
from openface.data import iterImgs

fileDir = os.path.dirname(os.path.realpath(__file__))


class Aligner:
    def __init__(self, args):

        self.args = args
        #if os.path.exists(args.outputDir):
        #    shutil.rmtree(args.outputDir)
        #openface.helper.mkdirP(args.outputDir)

        landmarkMap = {
            'outerEyesAndNose': openface.AlignDlib.OUTER_EYES_AND_NOSE,
            'innerEyesAndBottomLip': openface.AlignDlib.INNER_EYES_AND_BOTTOM_LIP
        }
        if args.landmarks not in landmarkMap:
            raise Exception("Landmarks unrecognized: {}".format(args.landmarks))

        self.landmarkIndices = landmarkMap[args.landmarks]
        self.dlib = openface.AlignDlib(args.dlibFacePredictor)

    def align(self, imgName):

        if not os.path.isfile(imgName):
            raise Exception("no file")

        rgb = cv2.imread(imgName)
        if rgb is None:
            if args.verbose:
                raise Exception(" Unable to load.")

        outRgb = self.dlib.align(self.args.size, rgb,
                                 landmarkIndices=self.landmarkIndices,
                                 skipMulti=self.args.skipMulti)
        if outRgb is not None:
            #outBgr = cv2.cvtColor(outRgb, cv2.COLOR_RGB2BGR)
            #cv2.imwrite(imgName, outBgr)

            #cv2.imwrite(imgName, outRgb)
            return outRgb

        if outRgb is None and self.args.verbose:
            print("  + Unable to align.")
            if args.fallbackLfw and outRgb is None:
                deepFunneled = "{}/{}.jpg".format(os.path.join(self.args.fallbackLfw,
                                                               imgObject.cls),
                                                  imgObject.name)
                shutil.copy(deepFunneled, "{}/{}.jpg".format(os.path.join(self.args.outputDir,
                                                                          imgObject.cls),
                                                             imgObject.name))
