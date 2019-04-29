from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http.response import StreamingHttpResponse
from django.views.decorators.gzip import gzip_page
import json
import cv2
# Create your views here.


class VideoCamera(object):
    def __init__(self, addr):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(addr)
        # self.video = cv2.VideoCapture('rtsp://admin:1234qwer@192.168.16.51:554')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)

        # 对于 python2.7 或者低版本的 numpy 请使用 jpeg.tostring()
        return jpeg.tobytes('')

    def update(self):
        while True:
            success, image = self.video.read()
            # image = image.resize(image, (640, 360))
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            ret, jpeg = cv2.imencode('.jpg', image)
            # 对于 python2.7 或者低版本的 numpy 请使用 jpeg.tostring()
            frame = jpeg.tobytes('')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


@gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(
            VideoCamera('rtsp://admin:1234qwer@192.168.16.202:554').update(),
            content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
