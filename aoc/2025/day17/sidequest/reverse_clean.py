#!/usr/bin/env python3
"""
Clean implementation of CyberChef recipe reversal.
Reverses: Base64 → ROT7(x8) → Fork → Zlib → XOR → Base32 → Image
"""
import base64
import zlib
import numpy as np
from PIL import Image

def rot_n(text, n):
    """Rotates alphabetical characters in a string by n positions."""
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + n) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + n) % 26 + ord('A')))
        else:
            result.append(char)
    return "".join(result)

def reverse_cyberchef(input_image_path: str, output_path: str = 'output.png'):
    """Reverse the CyberChef encoding recipe."""
    
    # Step 1: Read image pixels as bytes
    with Image.open(input_image_path) as img:
        img_array = np.array(img.convert('L'))
        # The image was saved with 512 pixels per row. The original data was 107520 bytes.
        # 107520 / 512 = 210. So the image dimensions should be 512x210.
        # We need to extract exactly 107520 bytes.
        pixel_bytes = img_array.flatten()[:107520].tobytes()
    
    # Step 2: Convert to UTF-8 string and split on newlines
    merged = pixel_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
    segments = merged.split('\n')
    
    # Step 3: Process each segment: Base32 → XOR → Zlib Inflate
    decoded_segments = []
    key = b'h0pp3r'
    
    for seg in segments:
        if not seg:
            continue
        try:
            # Base32 decode
            xored = base64.b32decode(seg)
            
            # XOR with key (null preserving)
            compressed = bytearray()
            for i, byte in enumerate(xored):
                if byte == 0:
                    compressed.append(0)
                else:
                    compressed.append(byte ^ key[i % len(key)])
            
            # Zlib inflate
            decompressed = zlib.decompress(bytes(compressed))
            decoded_segments.append(decompressed.decode('utf-8'))
        except Exception:
            # Skip segments that fail to decompress
            continue
    
    print(f"Successfully decoded {len(decoded_segments)} out of {len([s for s in segments if s])} segments")
    
    # Step 4: Join segments
    data = '\n'.join(decoded_segments)
    
    # Step 5: Reverse the 8-iteration loop
    for i in range(8):
        # The original operation was ROT7 then Split.
        # To reverse, we must first reverse the Split, then reverse the ROT7.
        # Reverse Split: Replace 'H0\n' with 'H0'
        data = data.replace('H0\n', 'H0')
        
        # Reverse ROT7: Apply ROT19 (26 - 7)
        data = rot_n(data, 19)
    
    # Step 6: Remove newlines and fix base64 padding
    base64_string = data.replace('\n', '').replace('\r', '')
    
    # Handle base64 padding
    padding = len(base64_string) % 4
    if padding != 0:
        base64_string += '=' * (4 - padding)
    
    # Step 7: Base64 decode
    try:
        decoded_bytes = base64.b64decode(base64_string)
        print(f"Final decoded size: {len(decoded_bytes)} bytes")
        
        # Save output
        with open(output_path, 'wb') as f:
            f.write(decoded_bytes)
        print(f"Saved to {output_path}")
        
        # Try to detect file type
        if decoded_bytes[:8] == b'\x89PNG\r\n\x1a\n':
            print("✓ Detected PNG file!")
            # If the output path isn't already a png, save it as one
            if not output_path.lower().endswith('.png'):
                png_path = output_path.rsplit('.', 1)[0] + '.png'
                with open(png_path, 'wb') as f:
                    f.write(decoded_bytes)
                print(f"Also saved as {png_path}")
        elif decoded_bytes[:2] == b'\xff\xd8':
            print("✓ Detected JPEG file!")
        elif decoded_bytes[:4] == b'GIF8':
            print("✓ Detected GIF file!")
        else:
            print(f"File type unclear. First bytes: {decoded_bytes[:20].hex()}")
            
    except Exception as e:
        print(f"Error during base64 decode: {e}")

if __name__ == '__main__':
    reverse_cyberchef('downloaded_scrambled.png')
