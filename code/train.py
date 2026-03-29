from ultralytics import YOLO # note change all paths depending on the device you run it on

# Load a model
model = YOLO("yolov11l-pose.pt")

results = model.train(data="config.yaml", 
                      epochs=300, 
                      imgsz=1280, 
                      batch=-1, 
                      device=[-1,-1,-1,-1], 
                      workers=8, 
                      augment=True,
                      patience = 50)
