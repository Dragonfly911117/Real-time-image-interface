import cv2
import numpy
import socket

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

transparentImg = cv2.imread("transparentImg.png")
output = transparentImg.copy()
ix, iy = 0, 0
R = 150
G = 0
B = 150
color = (B, G, R)

def drawLine(event, x, y, flag):
    global ix, iy, R, G, B, color
    if event == cv2.EVENT_FLAG_LBUTTON:
        ix = x
        iy = y
    elif event == cv2.EVENT_FLAG_RBUTTON:
        cv2.line(transparentImg, (ix,iy), (x, y), color, )















def server_run():
    TCP_IP = "25.16.122.103"
    TCP_PORT = 8002
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

    conn, addr = s.accept()

    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while ret:
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        s = str(len(stringData)).ljust(16)
        byt = s.encode()
        conn.send(byt)
        conn.send(stringData)

        ret, frame = capture.read()
        decImg = cv2.imdecode(data, 1)
        cv2.imshow('SERVER2', decImg)
        if cv2.waitKey(30) == 27:
            break

    conn.close()
    cv2.destroyAllWindows()


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


server_run()
