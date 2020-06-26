import cv2
import numpy
import socket
capture = cv2.VideoCapture(0)

def server_run():
    TCP_IP = "25.16.122.103"
    TCP_PORT = 8002
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(True)

    conn, addr = s.accept()

    ret, frame = capture.read()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

    while ret:
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        s = str(len(stringData) ).ljust(16)
        byt=s.encode()
        conn.send(byt);
        conn.send( stringData );

        ret, frame = capture.read()
        decimg=cv2.imdecode(data,1)
        cv2.imshow('SERVER2',decimg)
        if(cv2.waitKey(30)==27):
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
def client_run():
    TCP_IP = "25.16.122.103"
    TCP_PORT = 8002

    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    while 1:
        length = recvall(sock,16)
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        cv2.imshow('CLIENT2',decimg)
        if(cv2.waitKey(1)==27):
            break

    sock.close()
    cv2.destroyAllWindows()

client_run()