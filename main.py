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

def image_to_ascii_string(brightnessList, info, width, height):
    image_width, image_height, data = info

    imageString = []
    for y in range(height):
        for x in range(width):
            brightness = sample_pixel(data, image_width, image_height, width, height, x, y)
            imageString.append(brightness_to_ascii(brightnessList, brightness))

        imageString.append('\n')

    return "".join(imageString)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', type=str, help='')
    parser.add_argument('target_width', nargs='+', type=int, help='')
    parser.add_argument('target_height', nargs='+', type=int, help='')

    args = parser.parse_args()

    ascii: chr = [
        ' ',
        '.',
        '-',
        '+',
        '#',
    ]

    info = get_image_info(args.path[0])
    width, height, data = info

    print(image_to_ascii_string(ascii, info, args.target_width[0], args.target_height[0]))
