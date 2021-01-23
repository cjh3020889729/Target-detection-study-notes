# -*- coding: utf-8 -*-
# @Author: 二月三
# @Date:   2021-01-23 11:04:41
# @Last Modified by:   二月三
# @Last Modified time: 2021-01-23 14:52:28
'''完成IoU的计算演示

    1. 计算IoU的值
    2. 展示交集可视化
'''
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as image
from bounding_box_show import BoundingBox_Denote, draw_rectangle  # bbox数据格式转换，绘制矩形框


def bbox_2leftup_2rightdown(bbox):
    '''计算bbox的左上右下顶点
        bbox：框数据——xywh
    '''
    x1 = bbox[0] - bbox[2] / 2.0
    y1 = bbox[1] - bbox[3] / 2.0
    x2 = bbox[0] + bbox[2] / 2.0
    y2 = bbox[1] + bbox[3] / 2.0
    
    return x1, y1, x2, y2


def box_iou_solve(bbox1, bbox2, mode=True):
    '''计算两个框之间的IoU值
        bbox1: 框数据
        bbox2: 框数据
        mode: 框数据表示形式
              True: xyxy
              False: xywh

        IoU的intersection的左上右下顶点: 左上点为

        return IoU, (r_bbox1, r_bbox2, inter_bbox)
             PS：
                IoU： 交并比值
                r_bbox1：转换为xyxy形式的bbox1
                r_bbox2：转换为xyxy形式的r_bbox2
                inter_bbox: 形式为xyxy的交集位置
    '''
    if mode is True:  # bbox数据格式: xyxy
        # 左上右下顶点坐标
        b1_x1, b1_y1, b1_x2, b1_y2 = bbox1[0], bbox1[1], bbox1[2], bbox1[3]
        b2_x1, b2_y1, b2_x2, b2_y2 = bbox2[0], bbox2[1], bbox2[2], bbox2[3]
        # 框的长宽:长度由具体的像素个数决定，因此需要加1
        b1_w, b1_h = bbox1[2] - bbox1[0] + 1.0, bbox1[3] - bbox1[1] + 1.0
        b2_w, b2_h = bbox2[2] - bbox2[0] + 1.0, bbox1[3] - bbox1[1] + 1.0
    else:  # bbox数据格式: xywh
        # 左上右下顶点坐标
        b1_x1, b1_y1, b1_x2, b1_y2 = bbox_2leftup_2rightdown(bbox1)
        b2_x1, b2_y1, b2_x2, b2_y2 = bbox_2leftup_2rightdown(bbox2)
        # 框的长宽
        b1_w, b1_h = bbox1[2], bbox1[3]
        b2_w, b2_h = bbox2[2], bbox2[3]

    # 各自的面积
    s1 = b1_w * b1_h
    s2 = b2_w * b2_h

    # 交集面积
    # 如果考虑多个框进行计算交集——那么应该使用np.maximum——进行逐位比较
    inter_x1 = max(b1_x1, b2_x1)  # 交集区域的左上角
    inter_y1 = max(b1_y1, b2_y1)
    inter_x2 = min(b1_x2, b2_x2)  # 交集区域的右下角
    inter_y2 = min(b1_y2, b2_y2)

    # 长度由具体的像素个数决定，因此需要加1
    inter_w = max(inter_x2 - inter_x1 + 1.0, 0)
    inter_h = max(inter_y2 - inter_y1 + 1.0, 0)
    intersection = inter_w * inter_h

    # 并集面积
    union_area = s1 + s2 - intersection

    # 计算IoU交并集
    IoU = intersection / union_area

    # 整合坐标信息——用于展示交集可视化
    # 返回数据均以xyxy表示
    r_bbox1 = b1_x1, b1_y1, b1_x2, b1_y2
    r_bbox2 = b2_x1, b2_y1, b2_x2, b2_y2
    inter_bbox = inter_x1, inter_y1, inter_x2, inter_y2

    return IoU, (r_bbox1, r_bbox2, inter_bbox)


def main():
    fig = plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # 图片路径
    img_path = os.path.join(os.getcwd(), 'img', '1.jpg')
    img = image.imread(img_path) # 读取图片数据
    plt.imshow(img)  # 展示图片

    bbox1 = [240, 70, 380, 240] 
    bbox2 = [300, 100, 440, 300]
    denote_mode = True  # 数据格式模式
    denote_bbox1 = BoundingBox_Denote(bbox=bbox1, mode=denote_mode)  # 形式转换
    denote_bbox2 = BoundingBox_Denote(bbox=bbox2, mode=denote_mode)
    iou, bboxs = box_iou_solve(bbox1, bbox2, mode=denote_mode)  # 计算IoU交并比

    # 取出IoU转换解析后的bbox数据
    r_bbox1 = bboxs[0]   
    r_bbox2 = bboxs[1]
    inter_bbox = bboxs[2]

    # 利用数据进行绘制矩形框
    # mode=True: bbox数据应该输入_xyxy
    rect1 = draw_rectangle(r_bbox1, mode=True, color='b')
    rect2 = draw_rectangle(r_bbox2, mode=True, color='b')
    rect3 = draw_rectangle(inter_bbox, mode=True, color='y', fill=True)

    ax.add_patch(rect1)  # 将绘制的矩形添加到图片上
    ax.add_patch(rect2)
    ax.add_patch(rect3)

    plt.show()


if __name__ == "__main__":
    main()
