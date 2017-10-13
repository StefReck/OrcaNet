#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Placeholder"""

import keras as ks
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution3D, BatchNormalization, MaxPooling3D, Convolution2D, MaxPooling2D

def define_3d_model_xyz_test(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0.1

    model = ks.models.Sequential()
    model.add(Dense(512, input_shape=(n_bins[0], n_bins[1], n_bins[2], 1) ,activation="relu"))
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", input_shape=(n_bins[0], n_bins[1], n_bins[2], 1), padding="same"))
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(1,1,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    #model.add(BatchNormalization())
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Dropout(dropout_val))
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    #model.add(Dense(128, activation="relu"))
    #model.add(Dense(64, activation="relu"))
    #model.add(Dense(32, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='sigmoid'))

    return model

def define_3d_model_xyz(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0.1

    model = ks.models.Sequential()
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", input_shape=(n_bins[0], n_bins[1], n_bins[2], 1), padding="same"))
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(1,1,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    #model.add(normal.BatchNormalization())
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(Dropout(dropout_val))
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same"))
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax'))

    return model

    #if number_parallel > 1:
    #	model = make_parallel(model, number_parallel)

    # model.add(layers.core.Permute((4,3,2,1)))
    # model.add(layers.core.Reshape((128, 8)))

def define_3d_model_xzt(number_of_classes, n_bins, dropout=0):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3


    model = ks.models.Sequential()
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", input_shape=(n_bins[0], n_bins[2], n_bins[3], 1),
                            padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution3D(n_filters_1, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(MaxPooling3D(strides=(1,1,2)))
    model.add(Dropout(dropout))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(Convolution3D(n_filters_2, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Dropout(dropout))
    model.add(Convolution3D(n_filters_3, (kernel_size,kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(MaxPooling3D(strides=(2,2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(dropout))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax')) #activation='sigmoid'

    return model


def define_2d_model_yz(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0

    model = ks.models.Sequential()
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", input_shape=(n_bins[1], n_bins[2], 1),
                            padding="same", kernel_initializer='he_normal'))
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(MaxPooling2D(strides=(2,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(normal.BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax')) #activation='sigmoid'

    return model


def define_2d_model_yz_test(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0

    model = ks.models.Sequential()
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", input_shape=(n_bins[1], n_bins[2], 1),
                            padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization()) # set use_bias=False
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    #model.add(MaxPooling2D(strides=(2,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    #model.add(BatchNormalization())
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal'))
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax')) #activation='sigmoid'

    return model

def define_2d_model_yz_test_batch_norm(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0.1

    model = ks.models.Sequential()
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", input_shape=(n_bins[1], n_bins[2], 1),
                            padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    #model.add(MaxPooling2D(strides=(2,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax')) #activation='sigmoid'

    return model


def define_2d_model_zt_test_batch_norm(number_of_classes, n_bins):
    n_filters_1 = 64
    n_filters_2 = 64
    n_filters_3 = 128
    kernel_size = 3
    dropout_val = 0.2

    model = ks.models.Sequential()
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", input_shape=(n_bins[2], n_bins[3], 1),
                            padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_1, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    #model.add(MaxPooling2D(strides=(2,2)))
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(strides=(1,2)))
    model.add(Convolution2D(n_filters_2, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(BatchNormalization())
    model.add(Dropout(dropout_val))
    model.add(Convolution2D(n_filters_3, (kernel_size,kernel_size), activation="relu", padding="same", kernel_initializer='he_normal', use_bias=False))
    model.add(MaxPooling2D(strides=(2,2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(number_of_classes, activation='softmax')) #activation='sigmoid'

    return model