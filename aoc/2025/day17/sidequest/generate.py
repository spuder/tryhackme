#!/usr/bin/env python3
import base64
import zlib
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from PIL import Image
import io

def reproduce_cyberchef_recipe(input_data: bytes, output_image_path: str = 'output.png') -> None:
    """
    Reproduces the CyberChef recipe in Python.
    
    :param input_data: The input data as bytes.
    :param output_image_path: Path to save the generated greyscale image.
    """
    # Step 1: To Base64 (standard alphabet)
    data = base64.b64encode(input_data).decode('utf-8')
    
    # Steps 2-5: Label 'encoder1' and Jump (loop up to 8 times)
    # Repeat ROT13 and Split operations
    for _ in range(8):
        # Step 3: ROT13 (preserves case, non-letters unchanged)
        rot13_table = str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        )
        data = data.translate(rot13_table)
        
        # Step 4: Split on 'H0', join with 'H0\n'
        parts = data.split('H0')
        data = 'H0\n'.join(parts)
    
    # Step 6: Fork - split on '\n'
    segments = data.split('\n')
    
    processed_segments = []
    for seg in segments:
        if not seg:
            continue  # Skip empty segments
        
        try:
            # Step 7: Zlib Deflate (Dynamic Huffman Coding is default in zlib.compress)
            compressed = zlib.compress(seg.encode('utf-8'))
            
            # Step 8: XOR with key 'h0pp3r', UTF8 scheme, Standard, Null preserving
            key = b'h0pp3r'
            key_len = len(key)
            xored = bytearray()
            for i, byte in enumerate(compressed):
                if byte == 0:  # Null preserving
                    xored.append(0)
                else:
                    xored.append(byte ^ key[i % key_len])
            
            # Step 9: To Base32 (standard alphabet A-Z2-7=)
            base32_seg = base64.b32encode(xored).decode('utf-8')
            
            processed_segments.append(base32_seg)
        except Exception:
            # Ignore errors as per Fork setting
            continue
    
    # Step 10: Merge All with '\n'
    merged = '\n'.join(processed_segments)
    
    # Step 11: Generate Image - Greyscale, Pixel Scale Factor 1, Pixels per row 512
    # Interpret the merged string as UTF-8 bytes for pixel values
    final_bytes = merged.encode('utf-8')
    length = len(final_bytes)
    if length == 0:
        print("No data to generate image.")
        return
    
    # Calculate height, pad with 0x00 if needed
    width = 512
    height = (length + width - 1) // width  # Ceiling division
    padded_length = height * width
    padded_bytes = final_bytes + b'\x00' * (padded_length - length)
    
    # Create numpy array for the image
    image_array = np.frombuffer(padded_bytes, dtype=np.uint8).reshape((height, width))
    
    # Save the image using matplotlib
    plt.figure(figsize=(width / 100, height / 100))  # Approximate DPI scaling
    plt.imshow(image_array, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    print(f"Image saved to {output_image_path}")

def read_image_as_bytes(image_path: str) -> bytes:
    """
    Read an image file and convert it to bytes.
    
    :param image_path: Path to the input image file.
    :return: Image data as bytes.
    """
    with Image.open(image_path) as img:
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format or 'PNG')
        return img_byte_arr.getvalue()

# Main execution
if __name__ == "__main__":
    input_image_path = 'input.png'
    output_image_path = 'output.png'
    
    # Read input image and convert to bytes
    input_data = read_image_as_bytes(input_image_path)
    
    # Process the data and generate output image
    reproduce_cyberchef_recipe(input_data, output_image_path)
