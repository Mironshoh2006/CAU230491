import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────

def text_to_binary(text):
    """Convert text string to binary string (8 bits per character)."""
    return ''.join(format(ord(i), '08b') for i in text)

def binary_to_text(binary):
    """Convert binary string back to text string."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)

def encode_image(input_path, output_path, secret_text):
    """
    Hide secret_text inside input_path image using LSB steganography.
    Saves the result to output_path (should be .png to avoid lossy compression).
    """
    image = cv2.imread(input_path)
    if image is None:
        print(f"❌ Image not found at: {input_path}")
        return False

    h, w, _ = image.shape
    max_bytes = (h * w * 3) // 8 - 2  # 3 channels, minus delimiter space
    if len(secret_text) > max_bytes:
        print(f"❌ Message too long! Max {max_bytes} characters for this image.")
        return False

    # Append 16-bit end marker
    binary_text = text_to_binary(secret_text) + '1111111111111110'

    data_index = 0
    for row in image:
        for pixel in row:
            for i in range(3):  # B, G, R channels
                if data_index < len(binary_text):
                    pixel[i] = (pixel[i] & 254) | int(binary_text[data_index])
                    data_index += 1

    cv2.imwrite(output_path, image)
    print(f"✅ Encoded successfully! ({len(secret_text)} chars → {output_path})")
    return True

def decode_image(image_path):
    """
    Extract the hidden message from a steganography-encoded image.
    Returns the decoded text string.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Image not found at: {image_path}")
        return None

    binary_data = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    end_marker = "1111111111111110"
    if end_marker not in binary_data:
        print("❌ No hidden message found in this image.")
        return None

    binary_data = binary_data.split(end_marker)[0]
    text = binary_to_text(binary_data)
    print(f"✅ Decoded text: {text}")
    return text

def show_hidden_bits(image_path, num_bits=100):
    """Print the first num_bits LSBs extracted from the image."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Image not found at: {image_path}")
        return

    bits = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                bits += str(pixel[i] & 1)
                if len(bits) >= num_bits:
                    print(f"\n📡 First {num_bits} LSBs from '{image_path}':")
                    print(bits)
                    return

# ─────────────────────────────────────────────
#  VISUALIZATION
# ─────────────────────────────────────────────

def show_comparison(original_path, encoded_path):
    """
    Show a 4-panel figure:
      1. Original image
      2. Encoded (stego) image
      3. Absolute pixel difference (amplified ×20 for visibility)
      4. LSB bit-plane of encoded image
    """
    orig = cv2.imread(original_path)
    enc  = cv2.imread(encoded_path)

    if orig is None or enc is None:
        print("❌ One or both images not found.")
        return

    orig_rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    enc_rgb  = cv2.cvtColor(enc,  cv2.COLOR_BGR2RGB)

    # Difference (amplified so it's visible)
    diff = cv2.absdiff(orig, enc)
    diff_amplified = np.clip(diff.astype(np.int32) * 20, 0, 255).astype(np.uint8)
    diff_rgb = cv2.cvtColor(diff_amplified, cv2.COLOR_BGR2RGB)

    # LSB bit-plane: extract LSB of each channel and scale to 0/255
    lsb_plane = (enc & 1) * 255
    lsb_rgb = cv2.cvtColor(lsb_plane.astype(np.uint8), cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.patch.set_facecolor('#0d1117')

    panels = [
        (orig_rgb,  "Original Image",              "Images look identical to the human eye"),
        (enc_rgb,   "Encoded (Stego) Image",        "Secret message hidden in LSBs"),
        (diff_rgb,  "Pixel Difference (×20)",       "Amplified diff shows altered pixels"),
        (lsb_rgb,   "LSB Bit-Plane",                "White = LSB 1 | Black = LSB 0"),
    ]

    for ax, (img, title, subtitle) in zip(axes.flat, panels):
        ax.imshow(img)
        ax.set_title(f"{title}\n{subtitle}", color='white', fontsize=11, pad=8)
        ax.axis("off")
        ax.set_facecolor('#0d1117')

    fig.suptitle("Image Steganography — LSB Analysis", color='white',
                 fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig("steganography_analysis.png", dpi=150,
                bbox_inches='tight', facecolor='#0d1117')
    print("📊 Analysis saved to: steganography_analysis.png")
    plt.show()

def show_histogram_comparison(original_path, encoded_path):
    """
    Show pixel value histograms for original vs encoded image.
    Similar distributions confirm the encoding is imperceptible.
    """
    orig = cv2.imread(original_path)
    enc  = cv2.imread(encoded_path)

    if orig is None or enc is None:
        print("❌ One or both images not found.")
        return

    colors = ('blue', 'green', 'red')
    labels = ('Blue channel', 'Green channel', 'Red channel')

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.patch.set_facecolor('#0d1117')

    for ax, col, lbl in zip(axes, range(3), labels):
        hist_orig = cv2.calcHist([orig], [col], None, [256], [0, 256])
        hist_enc  = cv2.calcHist([enc],  [col], None, [256], [0, 256])

        ax.set_facecolor('#161b22')
        ax.plot(hist_orig, color='#58a6ff', linewidth=1.5, label='Original', alpha=0.9)
        ax.plot(hist_enc,  color='#f78166', linewidth=1.5, label='Encoded',  alpha=0.9, linestyle='--')
        ax.set_title(lbl, color='white', fontsize=11)
        ax.tick_params(colors='#8b949e')
        ax.spines[:].set_color('#30363d')
        ax.legend(facecolor='#21262d', labelcolor='white', fontsize=9)
        ax.set_xlim([0, 256])

    fig.suptitle("Pixel Histogram Comparison — Original vs Encoded",
                 color='white', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig("histogram_comparison.png", dpi=150,
                bbox_inches='tight', facecolor='#0d1117')
    print("📊 Histogram saved to: histogram_comparison.png")
    plt.show()

# ─────────────────────────────────────────────
#  MAIN DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":

    INPUT_IMAGE   = "rice.png"   # ← your source image (any .png or .jpg)
    ENCODED_IMAGE = "rice_encoded.png"
    SECRET_TEXT   = "Hello World! This is a secret message hidden in pixels."

    # ── Check image exists ───────────────────
    if not os.path.exists(INPUT_IMAGE):
        # Create a sample image if none provided
        print(f"⚠️  '{INPUT_IMAGE}' not found — creating a sample image...")
        sample = np.random.randint(100, 200, (300, 300, 3), dtype=np.uint8)
        cv2.imwrite(INPUT_IMAGE, sample)
        print(f"✅ Sample image created: {INPUT_IMAGE}")

    # ── Step 1: Encode ───────────────────────
    print("\n─── ENCODING ───────────────────────────")
    encode_image(INPUT_IMAGE, ENCODED_IMAGE, SECRET_TEXT)

    # ── Step 2: Decode ───────────────────────
    print("\n─── DECODING ───────────────────────────")
    decoded = decode_image(ENCODED_IMAGE)

    # ── Step 3: Verify match ─────────────────
    print("\n─── VERIFICATION ───────────────────────")
    if decoded == SECRET_TEXT:
        print("✅ Perfect match — encode/decode round-trip successful!")
    else:
        print("❌ Mismatch detected.")

    # ── Step 4: Show hidden bits ─────────────
    print("\n─── HIDDEN BITS (first 100) ─────────────")
    show_hidden_bits(ENCODED_IMAGE, num_bits=100)

    # ── Step 5: Visual comparison ────────────
    print("\n─── VISUALIZING ────────────────────────")
    show_comparison(INPUT_IMAGE, ENCODED_IMAGE)
    show_histogram_comparison(INPUT_IMAGE, ENCODED_IMAGE)
