import argparse
import math
import numpy as np
import cv2 as cv

def sample_pixel(sourceWeights: list[float], sourceWidth: int, sourceHeight: int, targetWidth: int, targetHeight: int, x: int, y: int) -> float:
    scale_x = sourceWidth / targetWidth
    scale_y = sourceHeight / targetHeight

    rx, ry = x + 0.5, y + 0.5

    weight_sum = 0
    weight_count = 0
    for i in range(math.floor(rx * scale_x), math.ceil((rx + 0.5) * scale_x)):
        for j in range(math.floor((ry - 0.5) * scale_y), math.ceil((ry + 0.5) * scale_y)):
            if i < 0 or i >= sourceWidth or j < 0 or j > sourceHeight:
                continue

            weight_sum += sourceWeights[j * sourceWidth + i]
            weight_count += 1

    return weight_sum / weight_count

def get_pixel_brightness(r: int, g: int, b: int) -> float:
    return ((r/255 + g/255 + b/255) / 3)

def brightness_to_ascii(brightnessList: list[chr], brightness: float) -> chr:
    length: int = len(brightnessList)
    asciiIndex: int = math.floor(brightness * length)

    if asciiIndex == -1:
        asciiIndex = 0
    
    if asciiIndex >= length:
        asciiIndex = length - 1

    return brightnessList[asciiIndex]

def get_image_info(filePath: str) -> list[float]:
    image: np.ndarray = cv.imread(filePath, cv.IMREAD_COLOR)
    height, width, _ = image.shape

    data = []

    for i in range(height):
        for j in range(width):
            k = image[i, j]
            value = get_pixel_brightness(k[0], k[1], k[2])
            data.append(value)

    return width, height, data

def image_to_ascii_array(brightnessList: list[int], info, width: int, height: int) -> list[chr]:
    image_width, image_height, data = info

    array = []
    for y in range(height):
        for x in range(width):
            brightness = sample_pixel(data, image_width, image_height, width, height, x, y)
            array.append(brightness_to_ascii(brightnessList, brightness))

    return array

def ascii_array_add_frame(array: list[chr], width: int, height: int) -> list[chr]:
    framed: list[chr] = []
    
    borderSize = 1
    doubleBorderSize = borderSize*2

    for y in range(0, height + doubleBorderSize):
        for x in range(0, width + doubleBorderSize):
            if x < borderSize or x > (width - 1 + borderSize) or y == (height - 1) + doubleBorderSize or y < borderSize:
                framed.append('█')
                continue

            idx = x - borderSize + (y - borderSize) * width
            framed.append(array[idx])

    return framed

def print_ascii_array(array: list[chr], width: int, includeFrame: bool):
    borderSize = 1
    sqrBorderSize = borderSize*2
    for i in range(0, len(array)):
        framedWidth = width
        if includeFrame:
            framedWidth = framedWidth + sqrBorderSize

        if i % framedWidth == 0 and i != 0:
            print()

        print(array[i], end='')

    print(f'\n{len(array)} characters')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', type=str, help='path to image')
    parser.add_argument('target_width', nargs='+', type=int, help='target ascii image width')
    parser.add_argument('target_height', nargs='+', type=int, help='target ascii image height')
    parser.add_argument('include_frame', nargs='+', type=int, help='1 (yes), 0 (no)')

    args = parser.parse_args()

    ascii: chr = [
        # ' ',
        '.',
        '-',
        '+',
        '#'
    ]

    info = get_image_info(args.path[0])
    width, height, data = info
    array: list[chr] = image_to_ascii_array(ascii, info, args.target_width[0], args.target_height[0])

    if args.include_frame[0] == 1:
        array = ascii_array_add_frame(array, args.target_width[0], args.target_height[0])

    print_ascii_array(array, args.target_width[0], args.include_frame[0])
