# -*- coding: utf-8 -*-
# @Author: 二月三
# @Date:   2021-01-22 15:57:45
# @Last Modified by:   二月三
# @Last Modified time: 2021-01-23 14:25:39

'''展示两种边界框的表示的代码演示
    
    1. 完成边界框的表示转换
    2. 完成边界框的绘制（默认边界框是不超过边界的）
'''
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image


def BoundingBox_Denote(bbox=[], mode=True):
    '''边界框的表示形式的转换
        bbox: 包含(x1, y1, x2, y2)四个位置信息的数据格式
        mode: 边界框数据表示的模式
             True:  to (x1,y1,x2,y2)
             False: to (x,y,w,h)
        
        return: 返回形式转换后的边界框数据
    '''
    denote_bbox = [] # 转换表示的边界框

    if mode is True:  # 保持原形式
        denote_bbox = bbox
    else:  # 转换为(center_x, center_y, w, h)
        center_x = (bbox[0]+bbox[2]) / 2.0
        center_y = (bbox[1]+bbox[3]) / 2.0
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        denote_bbox = [center_x, center_y, w, h]
    
    # 返回表示转换的边界框表示
    denote_bbox = np.asarray(denote_bbox,  dtype='float32')
    return denote_bbox
    

def test_bbox_denote(bbox=[], mode=True):
    '''测试边界框的表示转换
        mode: 边界框数据表示的模式
             True:  to (x1,y1,x2,y2)
             False: to (x,y,w,h)
    '''
    test_bbox = bbox
    denote_mode = mode
    transform_denote_bbox = BoundingBox_Denote(bbox=test_bbox, mode=denote_mode)
    
    print('当前表示模式：', 1 if denote_mode else 2)
    print('原始的边界框表示: ', test_bbox)
    print('表示转换后的边界框: ', transform_denote_bbox)


def draw_rectangle(bbox=[], mode=True, color='k', fill=False):
    '''绘制矩形框
        bbox：边界框数据（默认框数据不超过图片边界）
        mode: 边界框数据表示的模式
             True:  to (x1,y1,x2,y2)
             False: to (x,y,w,h)
        color: 边框颜色
        fill: 是否填充
    '''
    if mode is True: # to (x1,y1,x2,y2)
        x = bbox[0]
        y = bbox[1]
        w = bbox[2] - bbox[0] + 1
        h = bbox[3] - bbox[1] + 1
    else: # to (x,y,w,h)
        # 默认绘制的框不超出边界
        x = bbox[0] - bbox[2] / 2.0
        y = bbox[1] - bbox[3] / 2.0
        w = bbox[2]
        h = bbox[3]
    
    # 绘制边界框
    # patches.Rectangle需要传入左上角坐标、矩形区域的宽度、高度等参数
    # 获取绘制好的图形的返回句柄——用于添加到当前的图像窗口中
    rect = patches.Rectangle((x, y), w, h, 
                             linewidth=1,
                             edgecolor=color,
                             facecolor='y',
                             fill=fill, linestyle='-')
    
    return rect


def img_draw_bbox(bbox=[10, 20, 90, 100], mode=True):
    '''将边界框绘制到实际图片上
        bbox: 需要绘制的边界框
        mode: 边界框数据表示的转换模式
             True:  to (x1,y1,x2,y2)
             False: to (x,y,w,h)
    '''
    fig = plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 图片路径
    img_path = os.path.join(os.getcwd(), 'img', '1.jpg')
    img = image.imread(img_path) # 读取图片数据
    plt.imshow(img)  # 展示图片

    # 边界框数据转换
    denote_mode = mode  # 边界框表示形式——确定数据格式
    # 经过转换后的边界框数据
    bbox1 = BoundingBox_Denote(bbox=bbox, mode=denote_mode)

    # 绘制表示模式2的边界框
    rect1 = draw_rectangle(bbox=bbox1, mode=denote_mode, color='r')
    ax.add_patch(rect1)

    plt.show()


def main():
    # 边界框真实数据
    test_bbox = [160, 60, 460, 260]

    # 边界框数据表示模式——输入的bbox数据必须是[x1,y1,x2,y2]
    # True:  to (x1,y1,x2,y2)
    # False: to (x,y,w,h)
    # denote_mode = True
    denote_mode = False

    # 测试边界框的转换是否成功
    test_bbox_denote(bbox=test_bbox, mode=denote_mode)

    # 测试边界框的绘制
    img_draw_bbox(bbox=test_bbox, mode=denote_mode)


if __name__ == "__main__":
    main()
