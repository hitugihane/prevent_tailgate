from django.shortcuts import render

# Create your views here.

#======import======

from django.contrib.auth.views import LoginView
from django.urls import path,reverse_lazy

from django.views.generic import TemplateView

import cv2
import numpy as np
import imutils
import os
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse

# # 学習済みの人物検出モデルを読み込む（例：HOG + SVMを使ったもの）
# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



# class TailgateDetectionView(View):
#     def get(self, request, *args, **kwargs):
#         cap = cv2.VideoCapture(0)  # カメラを開く
#         ret, frame = cap.read()    # 1フレームをキャプチャ
        
#         # 人物を検出
#         found, _ = hog.detectMultiScale(frame)
        
#         if len(found) > 1:
#             # ここで認証のロジックを追加
#             for person in found:
#                 # personは各検出された人物の座標を表す。認証処理を行う。
#                 pass
            
#             # 認証されていない人がいたらアラート
#             return JsonResponse({"status": "alert"})
        
#         return JsonResponse({"status": "all_clear"})

#==================

#======Views=======

class CustmLoginView(LoginView):
  template_name = 'login.html'
  redirect_authenticated_user = True

  def get_success_url(self):
        return reverse_lazy('home')


class HomeView(TemplateView):
  template_name="home.html"

class WebcamView(TemplateView):
    template_name = "webcam.html"

prototxt = 'deploy.prototxt'
model = 'res10_300x300_ssd_iter_140000.caffemodel'
net = cv2.dnn.readNetFromCaffe(prototxt, model)

class FaceDetectionView(View):
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['image']

        image_data = uploaded_file.read()
        numpy_array = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(numpy_array, cv.IMREAD_COLOR)

        img = imutils.resize(img, width=400)
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

        net.setInput(blob)
        detections = net.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(img, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        # 画像をレスポンスとして返す
        response = HttpResponse(content_type="image/jpeg")
        cv2.imwrite(response, img)
        return response