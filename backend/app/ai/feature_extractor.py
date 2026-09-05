import numpy as np
from PIL import Image

def extract_features_from_path(img_path: str) -> np.ndarray:
    """
    Fast feature extraction from image path using PIL JPEG draft scaling.
    """
    with Image.open(img_path) as img:
        # Fast draft resizing during JPEG decoding
        img.draft("RGB", (128, 128))
        img = img.resize((128, 128))
        if img.mode != "RGB":
            img = img.convert("RGB")
        return extract_features(img)

def extract_features(img: Image.Image) -> np.ndarray:
    """
    Extract color, texture, and lesion features from a mulberry leaf PIL image.
    Returns a 1D numpy feature vector.
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    img_resized = img.resize((128, 128))
    arr = np.array(img_resized, dtype=np.float32) / 255.0  # (128, 128, 3)
    
    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]
    
    # RGB Channel Statistics
    r_mean, r_std = np.mean(R), np.std(R)
    g_mean, g_std = np.mean(G), np.std(G)
    b_mean, b_std = np.mean(B), np.std(B)
    
    # Color ratios & differences
    # Greenness index: 2G - R - B
    exg = 2.0 * G - R - B
    exg_mean, exg_std = np.mean(exg), np.std(exg)
    
    # Red-Green contrast ratio (Rust indication)
    rg_ratio = np.mean((R + 1e-5) / (G + 1e-5))
    
    # Convert RGB to HSV manually using numpy for portability
    max_c = np.max(arr, axis=2)
    min_c = np.min(arr, axis=2)
    delta = max_c - min_c + 1e-5
    
    # Value
    V = max_c
    # Saturation
    S = np.zeros_like(max_c)
    mask_max = max_c > 0
    S[mask_max] = delta[mask_max] / max_c[mask_max]
    
    # Hue computation
    H = np.zeros_like(max_c)
    r_eq = max_c == R
    g_eq = max_c == G
    b_eq = max_c == B
    
    H[r_eq] = ((G[r_eq] - B[r_eq]) / delta[r_eq]) % 6
    H[g_eq] = ((B[g_eq] - R[g_eq]) / delta[g_eq]) + 2
    H[b_eq] = ((R[b_eq] - G[b_eq]) / delta[b_eq]) + 4
    H = H / 6.0  # Normalize Hue to [0, 1]
    
    h_mean, h_std = np.mean(H), np.std(H)
    s_mean, s_std = np.mean(S), np.std(S)
    v_mean, v_std = np.mean(V), np.std(V)
    
    # Disease-specific pixel ratios
    healthy_mask = (H >= 0.20) & (H <= 0.45) & (S > 0.15)
    healthy_ratio = np.mean(healthy_mask)
    
    rust_mask = ((H <= 0.18) | (H >= 0.92)) & (S > 0.25) & (V > 0.2)
    rust_ratio = np.mean(rust_mask)
    
    spot_mask = (V < 0.38) & (S < 0.6)
    spot_ratio = np.mean(spot_mask)
    
    # Color histograms
    h_hist, _ = np.histogram(H, bins=16, range=(0.0, 1.0), density=True)
    s_hist, _ = np.histogram(S, bins=8, range=(0.0, 1.0), density=True)
    v_hist, _ = np.histogram(V, bins=8, range=(0.0, 1.0), density=True)
    
    # Spatial 2x2 grid features for local variance
    h_split = np.array_split(H, 2, axis=0)
    grid_h_stds = []
    for row in h_split:
        for col in np.array_split(row, 2, axis=1):
            grid_h_stds.append(np.std(col))
            
    features = np.hstack([
        [r_mean, r_std, g_mean, g_std, b_mean, b_std],
        [exg_mean, exg_std, rg_ratio],
        [h_mean, h_std, s_mean, s_std, v_mean, v_std],
        [healthy_ratio, rust_ratio, spot_ratio],
        grid_h_stds,
        h_hist,
        s_hist,
        v_hist
    ])
    
    return features.astype(np.float32)
