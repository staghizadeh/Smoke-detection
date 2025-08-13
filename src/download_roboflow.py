import os
import argparse
from roboflow import Roboflow

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Roboflow project slug, e.g. 'wildfire-smoke'")
    ap.add_argument("--workspace", required=True, help="Roboflow workspace slug, e.g. 'public-datasets'")
    ap.add_argument("--version", type=int, required=True, help="Dataset version number")
    ap.add_argument("--out", default="data/datasets/roboflow_smoke", help="Output dataset directory")
    args = ap.parse_args()

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("Missing ROBOFLOW_API_KEY env var. See: https://docs.roboflow.com/api-reference/authentication")

    rf = Roboflow(api_key=api_key)
    ds = rf.workspace(args.workspace).project(args.project).version(args.version).download("yolov8", location=args.out)
    print(f"Downloaded to: {ds.location}")

if __name__ == "__main__":
    main()
