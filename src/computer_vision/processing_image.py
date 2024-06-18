from ultralytics import YOLO


class ObjectDetection:
    model = YOLO("best.pt")

    def predict(self, frame):
        results = self.model.predict(source=frame)
        for r in results:
            r.show()
        return results

