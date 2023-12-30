import winsound  # Windowsでの警告音用

import cv2


def is_overlapping(rect1, rect2, threshold=0.5):
    """ 二つの矩形が重なっているかを判定する関数 """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    overlap_x1 = max(x1, x2)
    overlap_y1 = max(y1, y2)
    overlap_x2 = min(x1 + w1, x2 + w2)
    overlap_y2 = min(y1 + h1, y2 + h2)

    if overlap_x1 >= overlap_x2 or overlap_y1 >= overlap_y2:
        return False

    overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
    smaller_area = min(w1 * h1, w2 * h2)

    return overlap_area / smaller_area > threshold

# カメラからのフレームを取得する
cap = cv2.VideoCapture(0)  # USBカメラを使用する場合は、適切なIDに変更してください。

# Haar Cascadeの顔検出器をロードする
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    profile_faces = profile_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    filtered_faces = []
    for face in faces:
        if not any(is_overlapping(face, profile_face) for profile_face in profile_faces):
            filtered_faces.append(face)

    for (x, y, w, h) in filtered_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    for profile_face in profile_faces:
        if not any(is_overlapping(profile_face, face) for face in faces):
            cv2.rectangle(frame, (profile_face[0], profile_face[1]), (profile_face[0]+profile_face[2], profile_face[1]+profile_face[3]), (0, 255, 0), 2)

    total_faces = len(filtered_faces) + len(profile_faces)
    cv2.putText(frame, f'Total Faces: {total_faces}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

    if total_faces >= 2:
        # 2人以上検出された場合、ビープ音を鳴らす
        winsound.Beep(1000, 500)  # 1000 Hzの音を500ミリ秒間鳴らす

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
