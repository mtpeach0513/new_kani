#!/bin/bash

cd /opt
pwd

#fprefix=`basename ${1} | awk -F'.' '{print $1}'`
#cp -f ${1} /opt/ocr.bmp
#sleep 2

# bit depthを1か2にする
convert ocr.bmp -depth 1 ocr1.bmp

# 前処理
./IMG_toGray.py ocr1.bmp

# OCR --psm page segmentation mode 8 or 13
# --psm 4 単一カラムの様々なサイズのテキストとみなす
# --psm 6 単一カラムの均一ブロックテキストとみなす
# --psm 7 画像を単一行のテキストとして扱う
#tesseract grayocr1.bmp stdout --psm 6

# --psm 8 画像を単語1つのみ含まれるものとして扱う
# --psm 13 Raw line：内部の処理をバイパスしつつ画像内にテキストが1行だけあるものとして扱う
#tesseract /opt/grayocr1 /opt/ocr --psm 8
tesseract grayocr1.bmp stdout --psm 8 | sed 's/,//g'

#echo "-999.9"
