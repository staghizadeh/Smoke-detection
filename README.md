# Smoke Detection with YOLO

End-to-end, project for training and testing a YOLOv8 model to detect **smoke** (optionally `fire`).  
Includes:
- Public dataset access (Roboflow **Wildfire Smoke**, Kaggle sets, DFS, D-Fire, Boreal).
- Ready-to-run **Jupyter notebooks** for download → train → evaluate/infer.
- A **test script** to run predictions on **unseen** images.
- Clean `.gitignore`, `requirements.txt`, and a templated `data.yaml`.

> Tip: If your dataset contains both `smoke` and `fire` but you want **smoke-only**, you can either keep a 2-class model or filter/remap labels to only `smoke`.

---

## Quick Start

```bash
# 1) Create env and install deps
python -m venv .venv
# Windows PowerShell:
#   .venv\Scripts\Activate.ps1
# macOS/Linux:
#   source .venv/bin/activate
pip install -r requirements.txt

# 2) Open notebooks to download data and train
#    01_download_dataset.ipynb  -> grab a public dataset (Roboflow/Kaggle/DFS/D-Fire/Boreal)
#    02_train_yolov8.ipynb      -> train model
#    03_evaluate_and_infer.ipynb-> evaluate and run predictions on unseen images
```

### Datasets (public)
- **Roboflow: Wildfire Smoke** (YOLO-ready, class `smoke`).  
- **Kaggle** YOLO datasets (e.g., *WildFire-Smoke-Dataset-Yolo*, *Smoke-Fire-Detection-YOLO*).  
- **D-Fire** (GitHub) — YOLO labels, large dataset with `smoke`, `fire`, and non-fire images.  
- **DFS** (GitHub) — VOC labels (`fire`, `smoke`, `other`); convert to YOLO with `src/convert_voc2yolo.py`.  
- **Boreal Forest Fire (Fairdata)** — images/videos with **YOLO smoke** boxes and segmentation masks.

> **Licenses:** Always check dataset license/terms. Some are non-commercial and require attribution.

### Train (CLI alternative to the notebook)
```bash
# after editing data/data.yaml to point at your dataset
yolo task=detect mode=train model=yolov8n.pt data=data/data.yaml imgsz=640 epochs=100 batch=16
```

### Test your model on unseen images
Put a few test JPG/PNG files in `sample_images/unseen/`, then:
```bash
python tests/test_inference.py --weights runs/detect/train/weights/best.pt --source sample_images/unseen --save_dir outputs/unseen_preds
```

### Push to GitHub
```bash
git init
git add .
git commit -m "feat: smoke detection with YOLO starter"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

---

## Repo layout

```
.
├─ data/
│  └─ data.yaml                # edit paths & classes here
├─ notebooks/
│  ├─ 01_download_dataset.ipynb
│  ├─ 02_train_yolov8.ipynb
│  └─ 03_evaluate_and_infer.ipynb
├─ sample_images/
│  └─ unseen/                  # put your own images here
├─ src/
│  ├─ download_roboflow.py     # Roboflow YOLO downloader
│  ├─ convert_voc2yolo.py      # VOC XML -> YOLO .txt
│  └─ train.py                 # optional Python entrypoint
├─ scripts/
│  └─ kaggle_download.py       # Kaggle API helper
├─ tests/
│  └─ test_inference.py        # CLI for unseen images
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## Notes
- `ultralytics` supports YOLOv8+; defaults here use `yolov8n.pt`.  
- For multi-class (e.g., `smoke`,`fire`) set `nc: 2` and `names: ['smoke','fire']` in `data.yaml`.
