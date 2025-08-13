import argparse, os
from ultralytics import YOLO

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--weights", required=True, help="Path to trained weights, e.g., runs/detect/train/weights/best.pt")
    p.add_argument("--source", default="sample_images/unseen", help="Image file or folder")
    p.add_argument("--save_dir", default="outputs/unseen_preds", help="Where to save predictions")
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.25)
    args = p.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)
    model = YOLO(args.weights)
    results = model.predict(source=args.source, imgsz=args.imgsz, conf=args.conf, save=True, project=args.save_dir, name="preds", exist_ok=True)
    print(f"Saved predictions under: {os.path.join(args.save_dir, 'preds')}")

if __name__ == "__main__":
    main()
