import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K

epsilon = 1e-5
smooth = 1
alpha = 0.7


# 0 background
# 1 liver
# 2 bladder
# 3 lungs
# 4 kidneys
# 5 bone

def tversky_liver(y_true, y_pred, num_channel=1):
    true_pos = K.sum(y_true[:, :, :, num_channel] * y_pred[:, :, :, num_channel])
    false_neg = K.sum(y_true[:, :, :, num_channel] * (1 - y_pred[:, :, :, num_channel]))
    false_pos = K.sum((1 - y_true[:, :, :, num_channel]) * y_pred[:, :, :, num_channel])
    return K.mean((true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth))


def tversky_bladder(y_true, y_pred, num_channel=2):
    true_pos = K.sum(y_true[:, :, :, num_channel] * y_pred[:, :, :, num_channel])
    false_neg = K.sum(y_true[:, :, :, num_channel] * (1 - y_pred[:, :, :, num_channel]))
    false_pos = K.sum((1 - y_true[:, :, :, num_channel]) * y_pred[:, :, :, num_channel])
    return K.mean((true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth))


def tversky_lungs(y_true, y_pred, num_channel=3):
    true_pos = K.sum(y_true[:, :, :, num_channel] * y_pred[:, :, :, num_channel])
    false_neg = K.sum(y_true[:, :, :, num_channel] * (1 - y_pred[:, :, :, num_channel]))
    false_pos = K.sum((1 - y_true[:, :, :, num_channel]) * y_pred[:, :, :, num_channel])
    return K.mean((true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth))


def tversky_kidneys(y_true, y_pred, num_channel=4):
    true_pos = K.sum(y_true[:, :, :, num_channel] * y_pred[:, :, :, num_channel])
    false_neg = K.sum(y_true[:, :, :, num_channel] * (1 - y_pred[:, :, :, num_channel]))
    false_pos = K.sum((1 - y_true[:, :, :, num_channel]) * y_pred[:, :, :, num_channel])
    return K.mean((true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth))


def tversky_bones(y_true, y_pred, num_channel=5):
    true_pos = K.sum(y_true[:, :, :, num_channel] * y_pred[:, :, :, num_channel])
    false_neg = K.sum(y_true[:, :, :, num_channel] * (1 - y_pred[:, :, :, num_channel]))
    false_pos = K.sum((1 - y_true[:, :, :, num_channel]) * y_pred[:, :, :, num_channel])
    return K.mean((true_pos + smooth) / (true_pos + alpha * false_neg + (1 - alpha) * false_pos + smooth))


# 0 background
# 1 liver
# 2 bladder
# 3 lungs
# 4 kidneys
# 5 bones

background_w = 0.0
liver_w = 1.15
bladder_w = 1.95
lungs_w = 1
kidneys_w = 1.55
bones_w = 1
weights_sum = liver_w + bladder_w + lungs_w + kidneys_w + bones_w


def tversky_index(y_true, y_pred):
    return ((liver_w * tversky_liver(y_true, y_pred) + bladder_w * tversky_bladder(y_true, y_pred) +
             lungs_w * tversky_lungs(y_true, y_pred) + kidneys_w * tversky_kidneys(y_true, y_pred) +
             bones_w * tversky_bones(y_true, y_pred)) / weights_sum)


def foc_tversky_loss(y_true, y_pred):
    y_true = K.cast(y_true, 'float32')
    pt_2 = tversky_index(y_true, y_pred)
    gamma = 4.0 / 3.0
    return K.pow((1 - pt_2), gamma)


# averaging across batch axis, 0-dimension:

def dice_background(y_true, y_pred, smooth=1, num_class=0):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


def dice_liver(y_true, y_pred, smooth=1, num_class=1):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


def dice_bladder(y_true, y_pred, smooth=1, num_class=2):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


def dice_lungs(y_true, y_pred, smooth=1, num_class=3):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


def dice_kidneys(y_true, y_pred, smooth=1, num_class=4):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


def dice_bones(y_true, y_pred, smooth=1, num_class=5):
    intersection = K.sum(y_true[:, :, :, num_class] * y_pred[:, :, :, num_class])
    union = K.sum(y_true[:, :, :, num_class]) + K.sum(y_pred[:, :, :, num_class])
    return K.mean((2. * intersection + smooth) / (union + smooth))


# 0 background
# 1 liver
# 2 bladder
# 3 lungs
# 4 kidneys
# 5 bone

# Weights have been extracted by counting how many pixels of each organ were present in the dataset
def dice(y_true, y_pred, smooth=1):
    return ((0.23212333520332026 * dice_liver(y_true, y_pred) + 0.04549370195613813 * dice_bladder(y_true, y_pred)
             + 0.37348887454707363 * dice_lungs(y_true, y_pred) + 0.05246318852416101 * dice_kidneys(y_true, y_pred)
             + 0.2964308997693069 * dice_bones(y_true, y_pred)) / (0.23212333520332026 + 0.04549370195613813 +
                                                                   0.37348887454707363 + 0.05246318852416101 +
                                                                   0.2964308997693069))


def dice_loss(y_true, y_pred):
    y_true = K.cast(y_true, 'float32')
    return (1 - dice(y_true, y_pred))

