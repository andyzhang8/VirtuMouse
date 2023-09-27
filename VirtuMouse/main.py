from ultralytics import YOLO
import os
os.environ["OPENCV_LOG_LEVEL"]="DEBUG"
import torch, cv2




def getAvailableCameraDevices():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


    
def main():

    model = YOLO('model/best.pt')
    if torch.cuda.is_available():
        model.to('cuda')
        print(f'[INFO] GPU detected! Running on {torch.cuda.get_device_name(torch.cuda.current_device())}')
    else:
        print('[INFO] Running on CPU')

    devices = getAvailableCameraDevices()
    camera = 0

    if len(devices) == 1:
        print("[INFO] One input device found")
    else:
        camera = input(f'[INFO] Multuple input devices detected: {devices}\nSelect one ')


    cap = cv2.VideoCapture(camera)

    

    while True:
        success, frame = cap.read()
        result = model.predict(source=frame)

        for data in result:
            result = data.plot()

        
        cv2.imshow("frame", result)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
    
        






if __name__ == '__main__':
    main()