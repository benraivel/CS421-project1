import random
from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import numpy as np


def generate_fixations_left_skip_regression(aois_with_tokens):
    '''
        function to generate fixations at each word
    '''

    fixations = []
    word_count = 0
    skip_count = 0
    regress_count = 0

    aoi_list = aois_with_tokens.values.tolist()

    index = 0

    while index < len(aoi_list):
        x, y, width, height, token = (aoi_list[index][2], aoi_list[index][3],
                                      aoi_list[index][4], aoi_list[index][5],
                                      aoi_list[index][7])

        word_count += 1

        fixation_x = x + width / 3 + random.randint(-10, 10)
        fixation_y = y + height / 2 + random.randint(-10, 10)

        last_skipped = False

        # skipping
        if len(token) < 5 and random.random() < 0.3:
            skip_count += 1  # fixations.append([fixation_x, fixation_y])
            last_skipped = True
        else:
            fixations.append([fixation_x, fixation_y, len(token) * 50])
            last_skipped = False

        # regressions
        if random.random() > 0.96:
            index -= random.randint(1, 10)

            if index < 0:
                index = 0

            regress_count += 1

        index += 1

    skip_probability = skip_count / word_count

    return fixations


# write a function generate offset error as described in the paper
def error_offset(x_offset, y_offset, fixations):
    '''creates error to move fixations (shift in dissertation)'''

    pass


def error_noise(y_noise_probability, y_noise, duration_noise, fixations):
    '''creates a random error moving a percentage of fixations '''

    results = []

    for fix in fixations:

        x, y, duration = fix[0], fix[1], fix[2]

        # should be 0.1 for %10
        duration_error = int(duration * duration_noise)

        duration += random.randint(-duration_error, duration_error)

        if duration < 0:
            duration *= -1

        if random.random() < y_noise_probability:
            results.append([x, y + random.randint(-y_noise, y_noise),
                            duration])
        else:
            results.append([x, y, fix[2]])

    return results


def slope_distortion(fixations, d_slope):

    results = []

    initial_x = fixations[0][0]

    for fix in fixations:

        x, y, duration = fix[0], fix[1], fix[2]

        results.append([x, y + (x - initial_x)*d_slope, duration])

    return results


def shift_distortion(fixations, d_shift):

    results = []

    initial_y = fixations[0][1]

    for fix in fixations:

        x, y, duration = fix[0], fix[1], fix[2]

        results.append([x, y + (y - initial_y)*d_shift, duration])

    return results


def within_line_regression(fixations, reg_prob):

    rng = np.random.default_rng()

    results = []

    n_fix = len(fixations)
    fix_index = 0
    line_start = 0
    prev_x = 0

    while fix_index < n_fix:

        x, y, duration = (fixations[fix_index][0],
                          fixations[fix_index][1],
                          fixations[fix_index][2])

        # check for new line
        if x < prev_x:
            line_start = fix_index

        # roll dice on regression
        if random.random() < reg_prob:

            try:
                # choose how far to regress
                reg_index = int(rng.triangular(line_start, fix_index,
                                               fix_index, 1)[0])

                # add fixations for regression
                results.extend(fixations[reg_index:fix_index])

            # triangular throws a ValueError if left == right
            except ValueError:

                # regression at first fixation in line: do nothing
                pass

        # add the current fixation
        results.append(fixations[fix_index])

        prev_x = x
        fix_index += 1

    return results


def between_line_regression(fixations, reg_prob):

    rng = np.random.default_rng()

    results = []

    n_fix = len(fixations)
    fix_index = 0
    n_lines = 0
    line_start = 0
    line_to_indices = {}
    prev_x = 0

    while fix_index < n_fix:

        x, y, duration = (fixations[fix_index][0],
                          fixations[fix_index][1],
                          fixations[fix_index][2])

        # check for new line
        if x < prev_x:

            # record (start, end) indices for the previous line
            line_to_indices[n_lines] = np.arange(line_start, fix_index, 1)

            n_lines += 1  # update line counter

            line_start = fix_index  # update line starting index

        if random.random() < reg_prob:

            try:
                # choose how far to regress
                line = int(rng.triangular(0, n_lines, n_lines, 1)[0])

                indices = line_to_indices[line]

                selection = rng.choice(indices, 2, replace=False)

                selection.sort()

                results.extend(fixations[selection[0]:selection[1]])

            except ValueError:
                pass

        results.append(fixations[fix_index])

        prev_x = x
        fix_index += 1

    return results


def draw_fixation(Image_file, fixations):
    """Private method that draws the fixation, also allow user to draw eye
    movement order

    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image

    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for fixation in fixations:

        if len(fixations[0]) == 3:
            duration = fixation[2]
            if 5 * (duration / 100) < 5:
                r = 3
            else:
                r = 5 * (duration / 100)
        else:
            r = 8
        x = fixation[0]
        y = fixation[1]

        bound = (x - r, y - r, x + r, y + r)
        outline_color = (50, 255, 0, 0)
        fill_color = (50, 255, 0, 220)
        draw.ellipse(bound, fill=fill_color, outline=outline_color)

        bound = (x0, y0, x, y)
        line_color = (255, 155, 0, 155)
        penwidth = 2
        draw.line(bound, fill=line_color, width=5)

        x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def draw_correction(Image_file, fixations, match_list):
    """Private method that draws the fixation, also allow user to draw eye
    movement order

    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image

    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for index, fixation in enumerate(fixations):

        if len(fixations[0]) == 3:
            duration = fixation[2]
            if 5 * (duration / 100) < 5:
                r = 3
            else:
                r = 5 * (duration / 100)
        else:
            r = 8

        x = fixation[0]
        y = fixation[1]

        bound = (x - r, y - r, x + r, y + r)
        outline_color = (50, 255, 0, 0)

        if match_list[index] == 1:
            fill_color = (50, 255, 0, 220)
        else:
            fill_color = (255, 55, 0, 220)

        draw.ellipse(bound, fill=fill_color, outline=outline_color)

        bound = (x0, y0, x, y)
        line_color = (255, 155, 0, 155)
        penwidth = 2
        draw.line(bound, fill=line_color, width=5)

        # text_bound = (x+random.randint(-10, 10), y+random.randint(-10, 10))
        # text_color = (0, 0, 0, 225)
        # font = ImageFont.truetype("arial.ttf", 20)
        # draw.text(text_bound, str(index), fill=text_color,font=font)

        x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def find_lines_Y(aois):
    ''' returns a list of line Ys '''

    results = []

    for index, row in aois.iterrows():
        y, height = row['y'], row['height']

        if y + height / 2 not in results:
            results.append(y + height / 2)

    return results


def find_word_centers(aois):
    ''' returns a list of word centers '''

    results = []

    for index, row in aois.iterrows():
        x, y, height, width = row['x'], row['y'], row['height'], row['width']

        center = [int(x + width // 2), int(y + height // 2)]

        if center not in results:
            results.append(center)

    return results


def find_word_centers_and_duration(aois):
    ''' returns a list of word centers '''

    results = []

    for index, row in aois.iterrows():
        x, y, height, width, token = (row['x'], row['y'], row['height'],
                                      row['width'], row['token'])

        center = [int(x + width // 2), int(y + height // 2), len(token) * 50]

        if center not in results:
            results.append(center)

    # print(results)
    return results


def overlap(fix, AOI):
    """checks if fixation is within AOI"""

    box_x = AOI.x
    box_y = AOI.y
    box_w = AOI.width
    box_h = AOI.height

    if (fix[0] >= box_x and fix[0] <= box_x + box_w
       and fix[1] >= box_y and fix[1] <= box_y + box_h):

        return True

    else:
        return False


def correction_quality(aois, original_fixations, corrected_fixations):

    match = 0
    total_fixations = len(original_fixations)
    results = [0] * total_fixations

    for index, fix in enumerate(original_fixations):

        for _, row in aois.iterrows():

            if overlap(fix, row) and overlap(corrected_fixations[index], row):
                match += 1
                results[index] = 1

    return match / total_fixations, results
