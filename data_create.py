import cv2
import os
import random
import glob
import numpy as np
import tensorflow as tf

class datacreate:
    def __init__(self):
        self.mag = 2
        self.num = 0
        self.LR_num = 3
        self.low_img_list = self.LR_num * [None]
        self.high_img_list = [None]    

    def datacreate(self,
                    video_path,   #切り取る動画が入ったファイルのpath
                    data_number,  #データセットの生成数
                    cut_frame,    #1枚の画像から生成するデータセットの数
                    cut_height,   #LRの保存サイズ
                    cut_width):

        #データセットのリストを生成
        low_data_list = [[] for _ in range(self.LR_num)]  #LRは3枚で生成。
        high_data_list = []

        video_path = video_path + "/*"
        files = glob.glob(video_path)
    
        while self.num < data_number:
            file_num = random.randint(0, len(files) - 1)
            photo_files = glob.glob(files[file_num] + "/*")
            photo_num = random.randint(0, len(photo_files) - self.LR_num)

            for i in range(self.LR_num):
                img = cv2.imread(photo_files[photo_num + i])
                color_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

                if i == self.LR_num // 2 :
                    self.high_img_list = color_img[:, :, 0]

                height, width = color_img.shape[:2]
                low_bi = cv2.resize(color_img[:, :, 0], (int(width // self.mag), int(height // self.mag)), interpolation=cv2.INTER_CUBIC)
                self.low_img_list[i] = cv2.resize(low_bi, (width, height), interpolation=cv2.INTER_CUBIC)

            if cut_height > height or cut_width > width:
                break

            for p in range(cut_frame):          
                ram_h = random.randint(0, height - cut_height)
                ram_w = random.randint(0, width  - cut_width)

                for i in range(self.LR_num):
                    cut_low_bi = self.low_img_list[i][ram_h : ram_h + cut_height, ram_w: ram_w + cut_width]
                    low_data_list[i].append(cut_low_bi)

                    if i == self.LR_num // 2 :
                        high_data_list.append(self.high_img_list[ram_h : ram_h + cut_height, ram_w: ram_w + cut_width])

                self.num += 1

                if self.num == data_number:
                    break

        return low_data_list, high_data_list