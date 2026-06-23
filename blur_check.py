import cv2, numpy as np, glob, os

def laplacian_var_center_crop(img_path, crop_ratio=0.6):
    img = cv2.imread(img_path)
    if img is None: return None
    h, w = img.shape[:2]
    ch, cw = int(h*crop_ratio), int(w*crop_ratio)
    y0, x0 = (h-ch)//2, (w-cw)//2
    crop = img[y0:y0+ch, x0:x0+cw]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

paths = glob.glob(r"data\raw_photos\patch\*.jpg")
vals = [laplacian_var_center_crop(p) for p in paths]
vals = [v for v in vals if v is not None]
print(f"평균: {np.mean(vals):.1f}, variance<100 비율: {sum(v<100 for v in vals)/len(vals)*100:.1f}%")