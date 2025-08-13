import argparse, os, subprocess, sys

def ensure_kaggle():
    try:
        import kaggle  # noqa
        return True
    except Exception:
        print("Installing kaggle...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", required=True, help="Kaggle dataset slug, e.g. 'ahemateja19bec1025/wildfiresmokedatasetyolo'")
    p.add_argument("--out", default="data/datasets/kaggle_smoke", help="Output directory")
    args = p.parse_args()

    ensure_kaggle()

    # Expect KAGGLE_USERNAME and KAGGLE_KEY env vars or ~/.kaggle/kaggle.json present
    os.makedirs(args.out, exist_ok=True)
    print(f"Downloading {args.dataset} to {args.out} ...")
    subprocess.check_call(["kaggle", "datasets", "download", "-d", args.dataset, "-p", args.out, "--force"])
    # Unzip archives if present
    for fn in os.listdir(args.out):
        if fn.endswith(".zip"):
            zip_path = os.path.join(args.out, fn)
            subprocess.check_call([sys.executable, "-m", "zipfile", "-e", zip_path, args.out])
            os.remove(zip_path)
    print("Done.")

if __name__ == "__main__":
    main()
