from pytesseract import pytesseract
import cv2
import pyodbc

msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                      r'DBQ=C:\Users\laptop\Documents\Thesis\Thesis-electron-python\systems\student_data.accdb;')
cur = conn.cursor()

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
video = cv2.VideoCapture(0)
cntr = 0
while True:
    ret, capture = video.read()
    cntr = cntr + 1
    if ((cntr % 20) == 0):
        imgH, imgW, _ = capture.shape
        x1, y1, w1, h1 = 0, 0, imgH, imgW
        text = pytesseract.image_to_string(capture)
        box = pytesseract.image_to_boxes(capture)
        for boxes in box.splitlines():
            boxes = boxes.split(' ')
            x, y, w, h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(capture, (x, imgH - y), (w, imgH - h), (75, 255, 25), 2)
            cv2.putText(capture, "Hit ESC to stop the camera", (x1 + int(w1 / 50), y1 + int(h1 / 50)),
            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
            cv2.imshow('text detection', capture)
            if cv2.waitKey(1) % 256 == 27:
                video.release()
                cv2.destroyAllWindows()
                break
        if text == "" or text == " ":
            pass
        else:
            name = cur.execute("SELECT name FROM student_data")
            for i in name.fetchall():
                if str(text.strip()) in i:
                    sdata = cur.execute("SELECT * FROM student_data")
                    for x in sdata.fetchall():
                        if str(text.strip()) in x:
                            uni = cur.execute("SELECT * FROM Attendance")
                            if x not in uni.fetchall(): 
                                tups = (x)
                                cur.execute("INSERT INTO Attendance VALUES(?, ?, ?)", tups)
                                conn.commit()
                                print("Data inserted")
                            else:
                                pass
                else:
                    pass