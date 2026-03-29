from ultralytics import YOLO

model = YOLO("runs/detect/train6/weights/best.pt")

model.predict(source = "/Users/erwinbehpour/Documents/GitHub/Bee-Behaviour-Detection/testvid.mp4", 
              show = True, 
              save = True, 
              conf = 0.7, 
              line_width = 2, 
              save_crop = False, 
              save_txt = False, 
              show_labels = True, 
              show_conf = True, 
              classes = [0,2], 
              iou = 0.45)