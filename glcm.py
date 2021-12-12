import numpy as np
import math
import cv2
import json

def calcAsm(glcm0, glcm45, glcm90, glcm135) :
    asm0, asm45, asm90, asm135 = 0.0, 0.0, 0.0, 0.0

    for a in range(0, 255):
        for b in range(0, 255):
            asm0 = asm0 + (glcm0[a+1, b+1] * glcm0[a+1, b+1])
            asm45 = asm45 + (glcm45[a+1, b+1] * glcm45[a+1, b+1])
            asm90 = asm90 + (glcm90[a+1, b+1] * glcm90[a+1, b+1])
            asm135 = asm135 + (glcm135[a+1, b+1] * glcm135[a+1, b+1])
    return [asm0, asm45, asm90, asm135]

def calcContrast(glcm0, glcm45, glcm90, glcm135) :
    kontras0, kontras45, kontras90, kontras135 = 0.0, 0.0, 0.0, 0.0

    for a in range(0, 255):
        for b in range(0, 255):
            kontras0 = kontras0 + (a-b) * (a-b) * (glcm0[a+1, b+1])
            kontras45 = kontras45 + (a-b) * (a-b) * (glcm45[a+1, b+1])
            kontras90 = kontras90 + (a-b) * (a-b) * (glcm90[a+1, b+1])
            kontras135 = kontras135 + (a-b) * (a-b) * (glcm135[a+1, b+1])
    return [kontras0, kontras45, kontras90, kontras135]

def calcIdm(glcm0, glcm45, glcm90, glcm135) :
    idm0, idm45, idm90, idm135 = 0.0, 0.0, 0.0, 0.0

    for a in range(0, 255):
        for b in range(0, 255):
            idm0 = idm0 + (glcm0[a+1, b+1] / (1+(a-b)*(a-b)))
            idm45 = idm45 + (glcm45[a+1, b+1] / (1+(a-b)*(a-b)))
            idm90 = idm90 + (glcm90[a+1, b+1] / (1+(a-b)*(a-b)))
            idm135 = idm135 + (glcm135[a+1, b+1] / (1+(a-b)*(a-b)))
    return [idm0, idm45, idm90, idm135]

def calcEntropi(glcm0, glcm45, glcm90, glcm135) :
    entropi0, entropi45, entropi90, entropi135 = 0.0, 0.0, 0.0, 0.0

    for a in range(0, 255):
        for b in range(0, 255):
            if (glcm0[a+1, b+1] != 0):
                entropi0 = entropi0 - \
                    (glcm0[a+1, b+1] * (math.log(glcm0[a+1, b+1])))

            if (glcm45[a+1, b+1] != 0):
                entropi45 = entropi45 - \
                    (glcm45[a+1, b+1] * (math.log(glcm45[a+1, b+1])))

            if (glcm90[a+1, b+1] != 0):
                entropi90 = entropi90 - \
                    (glcm90[a+1, b+1] * (math.log(glcm90[a+1, b+1])))

            if (glcm135[a+1, b+1] != 0):
                entropi135 = entropi135 - \
                    (glcm135[a+1, b+1] * (math.log(glcm135[a+1, b+1])))
    return [entropi0, entropi45, entropi90, entropi135]

def calcPxPy(glcm0, glcm45, glcm90, glcm135) :
    px0, py0, px45, py45, px90, py90, px135, py135 = 0, 0, 0, 0, 0, 0, 0, 0
    for a in range(0, 255):
        for b in range(0, 255):
            px0 = px0 + a * glcm0[a+1, b+1]
            py0 = py0 + b * glcm0[a+1, b+1]

            px45 = px45 + a * glcm45[a+1, b+1]
            py45 = py45 + b * glcm45[a+1, b+1]

            px90 = px90 + a * glcm90[a+1, b+1]
            py90 = py90 + b * glcm90[a+1, b+1]

            px135 = px135 + a * glcm135[a+1, b+1]
            py135 = py135 + b * glcm135[a+1, b+1]
    return [px0, py0, px45, py45, px90, py90, px135, py135]

def calcStDev(glcm0, glcm45, glcm90, glcm135, px0, py0, px45, py45, px90, py90, px135, py135) :
    stdevx0, stdevy0, stdevx45, stdevy45, stdevx90, stdevy90, stdevx135, stdevy135 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for a in range(0, 255):
        for b in range(0, 255):
            stdevx0 = stdevx0 + (a-px0) * (a-px0) * glcm0[a+1, b+1]
            stdevy0 = stdevy0 + (b-py0) * (b-py0) * glcm0[a+1, b+1]

            stdevx45 = stdevx45 + (a-px45) * (a-px45) * glcm45[a+1, b+1]
            stdevy45 = stdevy45 + (b-py45) * (b-py45) * glcm45[a+1, b+1]

            stdevx90 = stdevx90 + (a-px90) * (a-px90) * glcm90[a+1, b+1]
            stdevy90 = stdevy90 + (b-py90) * (b-py90) * glcm90[a+1, b+1]

            stdevx135 = stdevx135 + (a-px135) * (a-px135) * glcm135[a+1, b+1]
            stdevy135 = stdevy135 + (b-py135) * (b-py135) * glcm135[a+1, b+1]
    return [stdevx0, stdevy0, stdevx45, stdevy45, stdevx90, stdevy90, stdevx135, stdevy135]

def calcCorrelation(glcm0, glcm45, glcm90, glcm135) :
    korelasi0, korelasi45, korelasi90, korelasi135 = 0.0, 0.0, 0.0, 0.0
    px0, py0, px45, py45, px90, py90, px135, py135 = calcPxPy(glcm0, glcm45, glcm90, glcm135)
    stdevx0, stdevy0, stdevx45, stdevy45, stdevx90, stdevy90, stdevx135, stdevy135 = calcStDev(glcm0, glcm45, glcm90, glcm135, px0, py0, px45, py45, px90, py90, px135, py135)
    for a in range(0, 255):
        for b in range(0, 255):
            korelasi0 = korelasi0 + ((a-px0) * (b-py0) * glcm0[a+1, b+1]/(stdevx0*stdevy0))
            korelasi45 = korelasi45 + ((a-px45) * (b-py45) * glcm45[a+1, b+1]/(stdevx45*stdevy45))
            korelasi90 = korelasi90 + ((a-px90) * (b-py90) * glcm90[a+1, b+1]/(stdevx90*stdevy90))
            korelasi135 = korelasi135 + ((a-px135) * (b-py135) * glcm135[a+1, b+1]/(stdevx135*stdevy135))
    return [korelasi0, korelasi45, korelasi90, korelasi135]

def glcm(img):
    height, width = img.shape[:2]

    # bentuk glcm
    glcm0 = np.zeros([256,256],dtype=np.uint8)
    glcm0.fill(0)
    totalPiksel0 = 0
    glcm45 = np.zeros([256,256],dtype=np.uint8)
    totalPiksel45 = 0
    glcm90 = np.zeros([256,256],dtype=np.uint8)
    totalPiksel90 = 0
    glcm135 = np.zeros([256,256],dtype=np.uint8)
    totalPiksel135 = 0

    for y in range(2, height-1):
        for x in range(2, width-1):
            # sudut 0
            a = img[y, x]
            b = img[y, x+1]
            glcm0[a+1, b+1] = glcm0[a+1, b+1] + 1
            totalPiksel0 = totalPiksel0 + 1

            # sudut 45
            a = img[y, x]
            b = img[y-1, x+1]
            glcm45[a+1, b+1] = glcm45[a+1, b+1] + 1
            totalPiksel45 = totalPiksel45 + 1

            # sudut 90
            a = img[y, x]
            b = img[y-1, x]
            glcm90[a+1, b+1] = glcm90[a+1, b+1] + 1
            totalPiksel90 = totalPiksel90 + 1

            # sudut 135
            a = img[y, x]
            b = img[y-1, x-1]
            glcm135[a+1, b+1] = glcm135[a+1, b+1] + 1
            totalPiksel135 = totalPiksel135 + 1

    glcm0 = glcm0 / totalPiksel0
    glcm45 = glcm45 / totalPiksel45
    glcm90 = glcm90 / totalPiksel90
    glcm135 = glcm135 / totalPiksel135

    asm0, asm45, asm90, asm135 = calcAsm(glcm0, glcm45, glcm90, glcm135)
    kontras0, kontras45, kontras90, kontras135 = calcContrast(glcm0, glcm45, glcm90, glcm135)
    idm0, idm45, idm90, idm135 = calcIdm(glcm0, glcm45, glcm90, glcm135)
    entropi0, entropi45, entropi90, entropi135 = calcEntropi(glcm0, glcm45, glcm90, glcm135)
    korelasi0, korelasi45, korelasi90, korelasi135 = calcCorrelation(glcm0, glcm45, glcm90, glcm135)


    g0 = {'asm': asm0, 'kontras': kontras0, 'idm': idm0, 'entropi': entropi0, 'korelasi': kontras0}
    g45 = {'asm': asm45, 'kontras': kontras45, 'idm': idm45, 'entropi': entropi45, 'korelasi': kontras45}
    g90 = {'asm': asm90, 'kontras': kontras90, 'idm': idm90, 'entropi': entropi90, 'korelasi': kontras90}
    g135 = {'asm': asm135, 'kontras': kontras135, 'idm': idm135, 'entropi': entropi135, 'korelasi': kontras135}

    return [g0, g45, g90, g135]
