import numpy as np

n_liver = 0
n_bladder = 0
n_lungs = 0
n_kidneys = 0
n_bones = 0

divider = '------------------------------'


def explode_img(img, num_classes=6):
    exploded = np.zeros(shape=img.shape + (num_classes,), dtype=np.uint8)
    for i in range(num_classes):
        exploded[:, :, i] = (img[:, :] == i).astype(np.uint8)
    return exploded


def prepare_prediction(pred):
    mask = np.argmax(pred, axis=-1)
    mask = mask.astype('uint8')
    return mask


def dice_single(pred, true):
    intersection = np.sum(pred * true)
    union = np.sum(pred + true)
    return (2 * intersection + 1) / (union + 1)


def dice_total(pred, true):
    # true = explode_img(true)
    dice_background = dice_single(pred == 0, true[:, :, 0])
    dice_liver = dice_single(pred == 1, true[:, :, 1])
    dice_bladder = dice_single(pred == 2, true[:, :, 2])
    dice_lungs = dice_single(pred == 3, true[:, :, 3])
    dice_kidneys = dice_single(pred == 4, true[:, :, 4])
    dice_bones = dice_single(pred == 5, true[:, :, 5])

    background_w = np.sum(true[:, :, 0])
    liver_w = np.sum(true[:, :, 1])
    bladder_w = np.sum(true[:, :, 2])
    lungs_w = np.sum(true[:, :, 3])
    kidneys_w = np.sum(true[:, :, 4])
    bones_w = np.sum(true[:, :, 5])

    global n_liver
    n_liver += liver_w
    global n_bladder
    n_bladder += bladder_w
    global n_lungs
    n_lungs += lungs_w
    global n_kidneys
    n_kidneys += kidneys_w
    global n_bones
    n_bones += bones_w

    return ((liver_w * dice_liver + bladder_w * dice_bladder + lungs_w * dice_lungs +
             kidneys_w * dice_kidneys + bones_w * dice_bones + 1) / (liver_w + bladder_w + lungs_w + kidneys_w +
                                                                     bones_w + 1)), \
           dice_liver * liver_w, dice_bladder * bladder_w, dice_lungs * lungs_w, dice_kidneys * kidneys_w, \
           dice_bones * bones_w


def evaluate_results(list_pred, list_true):
    dices = []
    dice = 0
    dice_liver_total = []
    dice_bladder_total = []
    dice_lungs_total = []
    dice_kidneys_total = []
    dice_bones_total = []
    for i in range(len(list_pred)):
        pred = list_pred[i]
        true = list_true[i]
        pred = prepare_prediction(pred)
        current_dice, dice_liver, dice_bladder, dice_lungs, dice_kidneys, dice_bones = dice_total(pred, true)

        dice_liver_total.append(dice_liver)
        dice_bladder_total.append(dice_bladder)
        dice_lungs_total.append(dice_lungs)
        dice_kidneys_total.append(dice_kidneys)
        dice_bones_total.append(dice_bones)
        dice += current_dice
        dices.append(current_dice)

    print(divider)
    print('Global Dice:')
    print("Mean on slices: %.2f +- %.2f" % (np.mean(dices)*100, np.std(dices)*100))

    global n_liver
    global n_bladder
    global n_lungs
    global n_kidneys
    global n_bones

    std_organs = ((np.std(dice_liver_total) + np.std(dice_bladder_total) + np.std(dice_lungs_total) +
                   np.std(dice_kidneys_total) + np.std(dice_bones_total)) / (n_liver + n_bladder + n_lungs +
                                                                             n_kidneys + n_bones))
    print('Weighted Mean on organs: %.2f +- %.2f' % (
          (np.sum(dice_liver_total) + np.sum(dice_bladder_total) + np.sum(dice_lungs_total) + np.sum(dice_kidneys_total)
           + np.sum(dice_bones_total)) / (n_liver + n_bladder + n_lungs + n_kidneys + n_bones) * 100, std_organs * 100))
    print(divider)

    print('Organs Dices:')
    print('Liver: %.2f +- %.2f' % (np.sum(dice_liver_total) / n_liver * 100, np.std(dice_liver_total) / n_liver * 100))
    print('Bladder: %.2f +- %.2f' % (np.sum(dice_bladder_total) / n_bladder * 100, np.std(dice_bladder_total) / n_bladder * 100))
    print('Lungs: %.2f +- %.2f' % (np.sum(dice_lungs_total) / n_lungs * 100, np.std(dice_lungs_total) / n_lungs * 100))
    print('Kidneys: %.2f +- %.2f' % (np.sum(dice_kidneys_total) / n_kidneys * 100, np.std(dice_kidneys_total) / n_kidneys * 100))
    print('Bones: %.2f +- %.2f' % (np.sum(dice_bones_total) / n_bones * 100, np.std(dice_bones_total) / n_bones * 100))
    print(divider)
