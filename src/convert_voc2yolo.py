import os, glob, argparse
from lxml import etree

# Convert Pascal VOC XML annotations to YOLO .txt format.
# Each image gets a .txt file with lines:
#   <class_id> x_center y_center width height
# with all coordinates normalized to [0,1].

def parse_xml(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    size = root.find("size")
    w = float(size.findtext("width"))
    h = float(size.findtext("height"))
    boxes = []
    for obj in root.findall("object"):
        name = obj.findtext("name").strip().lower()
        bnd = obj.find("bndbox")
        xmin = float(bnd.findtext("xmin"))
        ymin = float(bnd.findtext("ymin"))
        xmax = float(bnd.findtext("xmax"))
        ymax = float(bnd.findtext("ymax"))
        xc = ((xmin + xmax) / 2.0) / w
        yc = ((ymin + ymax) / 2.0) / h
        bw = (xmax - xmin) / w
        bh = (ymax - ymin) / h
        boxes.append((name, xc, yc, bw, bh))
    return boxes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xml_dir", required=True, help="Folder containing VOC XML files")
    ap.add_argument("--out_dir", required=True, help="Output folder for YOLO .txt files")
    ap.add_argument("--classes", default="smoke,fire,other", help="Comma-separated class names (desired order)")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    class_list = [c.strip().lower() for c in args.classes.split(",")]
    class_to_id = {c:i for i,c in enumerate(class_list)}
    xml_files = glob.glob(os.path.join(args.xml_dir, "*.xml"))
    if not xml_files:
        raise SystemExit(f"No XML files found in {args.xml_dir}")

    wrote = 0
    for xml in xml_files:
        boxes = parse_xml(xml)
        stem = os.path.splitext(os.path.basename(xml))[0]
        out_txt = os.path.join(args.out_dir, f"{stem}.txt")
        with open(out_txt, "w") as f:
            for name, xc, yc, bw, bh in boxes:
                if name not in class_to_id:
                    # skip unknown classes
                    continue
                cid = class_to_id[name]
                f.write(f"{cid} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")
        wrote += 1
    print(f"Converted {wrote} XML files -> {args.out_dir}")

if __name__ == "__main__":
    main()
