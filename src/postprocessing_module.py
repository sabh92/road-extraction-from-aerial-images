import numpy as np
import scipy

import trainDictionary as dict_train
import denoise_dictionary as dict_denoise
import denoise_low_rank as lowrank_denoise

# labels - 1 hot array of labels for each patch
# returned mask has size (# of patches) x (# of patches)
# (e.g. 25x25 for 16x16 patches and 400x400 image)
def prediction_to_mask(labels, width, height):
    mask = np.zeros([height, width])
    idx = 0
    for i in range(0,height):
        for j in range(0,width):
            mask[i][j] = 0 if labels[idx][0] > 0.5 else 1
            idx = idx + 1
    return mask

# Inverse of prediction_to_mask
def mask_to_prediction(mask):
    (height, width) = mask.shape;
    prediction = np.zeros([height * width, 2])
    idx = 0
    for i in range(0,height):
        for j in range(0,width):
            if mask[i][j] == 1:
                prediction[idx][1] = 1
            else:
                prediction[idx][0] = 1
            idx = idx + 1
    return prediction

# Basic 4 connectivity neighbour filtering
def set_to_zero_if_no_neighbours(mask):
    (height, width) = mask.shape
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            num_of_zero_neighbours = 0
            if mask[i - 1][j] == 0:
                num_of_zero_neighbours += 1
            if mask[i + 1][j] == 0:
                num_of_zero_neighbours += 1
            if mask[i][j - 1] == 0:
                num_of_zero_neighbours += 1
            if mask[i][j + 1] == 0:
                num_of_zero_neighbours += 1

            num_of_one_neighbours = 4 - num_of_zero_neighbours         
            if mask[i][j] == 1 and num_of_zero_neighbours >= 3:
                mask[i][j] = 0
            if mask[i][j] == 0 and num_of_one_neighbours >= 3:
                mask[i][j] = 1
    return mask

# prediction - 1 hot array of labels for each patch
def postprocess_prediction(prediction,  width, height):
    mask = prediction_to_mask(prediction, width, height);
    # scipy.misc.imsave('test_before.png', mask)
    mask = set_to_zero_if_no_neighbours(mask)
    # mask = scipy.signal.medfilt(mask, 3)
    # scipy.misc.imsave('test_after.png', mask)
    
    # dictionary based denoising
#    D = dict_train.get_dictionary()
#    mask = np.zeros(mask.shape)
#    mask[dict_denoise.denoiseImg(prediction[:][1], D) >= 0.5] = 1
    
    # simple low rank approximation
#    mask = np.zeros(mask.shape)
#    mask[lowrank_denoise.denoiseImg(prediction[:][1]) >= 0.5] = 1
    
    return mask_to_prediction(mask)