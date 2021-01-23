# -*- coding: utf-8 -*-
# @Author: 二月三
# @Date:   2021-01-22 15:57:34
# @Last Modified by:   二月三
# @Last Modified time: 2021-01-23 14:45:09
'''展示锚框的代码演示
    
    1. 完成锚框的绘制
'''
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
from bounding_box_show import draw_rectangle  # 绘制矩形——返回一个窗体句柄
from bounding_box_show import BoundingBox_Denote # 框数据表示的转换形式


def draw_anchor(ax, center, length, scales, ratios, img_height, img_width, color='r'):
    '''绘制锚框————同一中心点三个不同大小的锚框
        ax: plt的窗体句柄——用于调用矩形绘制
        center：中心点坐标
        length：基本长度
        scales：尺寸
        ratios：长宽比
        img_height: 图片高
        img_width: 图片宽

        一个锚框的大小，由基本长度+尺寸+长宽比有关
        同时锚框的最终计算值与图片实际大小有关——不能超过图片实际范围嘛
    '''

    bboxs = []  # 这里的边界框bbox是指的锚框

    for scale in scales: # 遍历尺寸情况
        for ratio in ratios: # 同一尺寸下遍历不同的长宽比情况
            # 利用基本长度、尺寸与长宽比进行锚框长宽的转换
            h = length * scale * np.math.sqrt(ratio)
            w = length * scale / np.math.sqrt(ratio)
            # 利用求得的长宽，确定绘制矩形需要的左上角顶点坐标和右下角顶点坐标
            # 不同的绘制API可能有不同的参数需要，相应转换即可
            x1 = max(center[0] - w / 2., 0.)
            y1 = max(center[1] - h / 2., 0.)
            x2 = min(center[0] + w / 2. - 1.0, img_width - 1.)  # center[0] + w / 2 -1.0 是考虑到边框不超过边界
            y2 = min(center[1] + h / 2. - 1.0, img_height - 1.)
            
            bbox = [x1, y1, x2, y2]
            print('An Anchor: ', bbox)
            bboxs.append(bbox)  # 押入生成的anchor

    for bbox in bboxs:

        denote_mode = True  # 当前的目标数据形式： True: (x1, y1, x2, y2)
        denote_bbox = BoundingBox_Denote(bbox=bbox, mode=denote_mode)

        # 绘制anchor的矩形框
        rect = draw_rectangle(bbox=denote_bbox, mode=True, color=color)
        
        ax.add_patch(rect)


def main():
    # 先读取图像，再绘制
    fig = plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 图片路径
    img_path = os.path.join(os.getcwd(), 'img', '1.jpg')
    img = image.imread(img_path) # 读取图片数据
    plt.imshow(img)  # 展示图片
    print(img.shape[0])
    print(img.shape[1])

    # # center: [310, 160]
    # draw_anchor(ax=ax, center=[310, 160], 
    #             length=200, scales=[1.0], ratios=[0.5, 1.0, 2.0], 
    #             img_height=img.shape[0], img_width=img.shape[1],
    #             color='b')

    # # center: [200, 200]
    # draw_anchor(ax=ax, center=[200, 200], 
    #             length=100, scales=[1.0], ratios=[0.5, 1.0, 2.0], 
    #             img_height=img.shape[0], img_width=img.shape[1],
    #             color='r')

    # 每间隔100个像素上绘制三个基本长度为120的锚框
    for i in range(0, img.shape[0], 100):  # y值
        for j in range(0, img.shape[1], 100): # x值
            # center: x, y
            y = i 
            x = j
            draw_anchor(ax=ax, center=[x, y], 
                        length=120, scales=[1.0], ratios=[0.5, 1.0, 2.0], 
                        img_height=img.shape[0], img_width=img.shape[1],
                        color='b')

    # # center: [310, 160]
    # draw_anchor(ax=ax, center=[310, 160], 
    #             length=200, scales=[1.0], ratios=[0.5, 1.0, 2.0], 
    #             img_height=img.shape[0], img_width=img.shape[1],
    #             color='r')
                        
    plt.show()

if __name__ == "__main__":
    main()
