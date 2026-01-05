#!/usr/bin/env python3
import base64
import zlib
import numpy as np
from PIL import Image
from typing import Optional

def reverse_cyberchef_recipe(input_image_path: str, output_image_path: str = 'output.png', debug: bool = True) -> None:
    """
    Reverses the CyberChef recipe to decode the message.
    
    :param input_image_path: Path to the input encoded image.
    :param output_image_path: Path to save the decoded image.
    :param debug: Enable debug output.
    """
    # Step 1: Read the greyscale image and convert to bytes
    if debug:
        print(f"[DEBUG] Reading image from: {input_image_path}")
    
    with Image.open(input_image_path) as img:
        if debug:
            print(f"[DEBUG] Image size: {img.size}, mode: {img.mode}")
        # Convert to grayscale if not already
        img_gray = img.convert('L')
        # Get pixel data as numpy array
        img_array = np.array(img_gray)
        # Flatten to 1D array and convert to bytes
        pixel_bytes = img_array.flatten().tobytes()
    
    if debug:
        print(f"[DEBUG] Total pixel bytes: {len(pixel_bytes)}")
    
    # Remove trailing null bytes (padding) - but also check for embedded nulls
    original_len = len(pixel_bytes)
    pixel_bytes_stripped = pixel_bytes.rstrip(b'\x00')
    
    if debug:
        print(f"[DEBUG] After removing padding: {len(pixel_bytes_stripped)} bytes")
        print(f"[DEBUG] Removed {original_len - len(pixel_bytes_stripped)} null bytes")
        print(f"[DEBUG] First 100 bytes: {pixel_bytes_stripped[:100]}")
        
        # Check if data looks like ASCII text (which it should after Base32)
        try:
            test_decode = pixel_bytes_stripped[:200].decode('ascii')
            print(f"[DEBUG] Data appears to be ASCII: {test_decode[:100]}")
        except:
            print(f"[DEBUG] WARNING: Data doesn't appear to be ASCII text!")
            print(f"[DEBUG] Byte values sample: {list(pixel_bytes_stripped[:50])}")
    
    # Step 2: Interpret as UTF-8 string (reverse of encoding to UTF-8 bytes)
    try:
        merged = pixel_bytes_stripped.decode('utf-8')
        if debug:
            print(f"\n[DEBUG] Decoded UTF-8 string length: {len(merged)} characters")
            print(f"[DEBUG] String length mod 4: {len(merged) % 4} (should be 0 for valid base32)")
            print(f"[DEBUG] First 200 characters: {merged[:200]}")
            print(f"[DEBUG] Last 100 characters: {merged[-100:]}")
            # Count newlines
            newline_count = merged.count('\n')
            print(f"[DEBUG] Number of newlines: {newline_count}")
    except UnicodeDecodeError as e:
        print(f"Error decoding UTF-8: {e}")
        return
    
    # Step 3: Split on '\n' (reverse of Merge)
    segments = merged.split('\n')
    if debug:
        print(f"[DEBUG] Number of segments after split: {len(segments)}")
        print(f"[DEBUG] First segment length: {len(segments[0]) if segments else 0}")
        print(f"[DEBUG] First segment (first 100 chars): {segments[0][:100] if segments else ''}")
    
    # Step 4-6: Process each segment
    decoded_segments = []
    success_count = 0
    fail_count = 0
    error_types = {}
    
    for idx, seg in enumerate(segments):
        if not seg:
            if debug:
                print(f"[DEBUG] Segment {idx}: Empty, skipping")
            continue
        
        # Only show detailed debug for first 10 segments and last 5, plus any successful ones
        show_detail = debug and (idx < 10 or idx >= len(segments) - 5)
        
        if show_detail:
            print(f"\n[DEBUG] Processing segment {idx}: length={len(seg)}, first 50 chars: {seg[:50]}")
        
        try:
            # Step 4: From Base32 (reverse of To Base32)
            xored = base64.b32decode(seg)
            if show_detail:
                print(f"[DEBUG]   After Base32 decode: {len(xored)} bytes")
                print(f"[DEBUG]   First 20 bytes: {xored[:20]}")
            
            # Step 5: XOR with key 'h0pp3r' (XOR is its own inverse)
            key = b'h0pp3r'
            key_len = len(key)
            compressed = bytearray()
            for i, byte in enumerate(xored):
                if byte == 0:  # Null preserving
                    compressed.append(0)
                else:
                    compressed.append(byte ^ key[i % key_len])
            
            if show_detail:
                print(f"[DEBUG]   After XOR: {len(compressed)} bytes")
                print(f"[DEBUG]   First 20 bytes: {bytes(compressed[:20])}")
            
            # Step 6: Zlib Inflate (reverse of Deflate)
            decompressed = zlib.decompress(bytes(compressed))
            if show_detail or True:  # Always show successful decompressions
                print(f"[DEBUG] ✓ Segment {idx} SUCCESS: {len(decompressed)} bytes -> {decompressed[:100]}")
            
            decoded_segments.append(decompressed.decode('utf-8'))
            success_count += 1
        except Exception as e:
            # Skip segments that fail to decode
            fail_count += 1
            error_type = str(e).split(':')[0] if ':' in str(e) else str(e)
            error_types[error_type] = error_types.get(error_type, 0) + 1
            
            if show_detail:
                print(f"[DEBUG]   ✗ ERROR in segment {idx}: {type(e).__name__}: {e}")
            if not show_detail and debug:
                # Show a progress indicator
                if idx % 100 == 0:
                    print(f"[DEBUG] Progress: {idx}/{len(segments)} segments processed, {success_count} successful, {fail_count} failed")
            continue
    
    if debug:
        print(f"\n[DEBUG] Error type summary:")
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            print(f"[DEBUG]   {error_type}: {count} occurrences")
    
    if debug:
        print(f"\n[DEBUG] Successfully decoded {len(decoded_segments)} out of {len([s for s in segments if s])} segments")
        if len(decoded_segments) == 0:
            print(f"[DEBUG] ERROR: No segments were successfully decoded!")
            print(f"[DEBUG] This might mean:")
            print(f"[DEBUG]   1. The image was not created by generate.py")
            print(f"[DEBUG]   2. The encoding parameters are different")
            print(f"[DEBUG]   3. The image has been corrupted")
            return
        elif len(decoded_segments) < len([s for s in segments if s]) / 2:
            print(f"[DEBUG] WARNING: Less than half of segments decoded successfully")
            print(f"[DEBUG] The output may be incomplete or incorrect")
    
    # Step 7: Join segments (reverse of Fork/split)
    # The Fork split on '\n', so we should join with '\n' to reverse it
    data = '\n'.join(decoded_segments)
    
    if debug:
        print(f"\n[DEBUG] After joining segments: {len(data)} characters")
        print(f"[DEBUG] First 200 characters: {data[:200]}")
        print(f"[DEBUG] Newlines in joined data: {data.count(chr(10))}")
    
    # Step 8: Reverse the loop (8 iterations in reverse)
    # The forward process did: ROT13, then Split 'H0' and join with 'H0\n'
    # To reverse: Replace 'H0\n' with 'H0', then ROT13
    for iteration in range(8):
        if debug and iteration == 0:
            print(f"\n[DEBUG] Reverse iteration {iteration + 1}/8")
            print(f"[DEBUG]   Before H0\\n replacement: length={len(data)}")
            print(f"[DEBUG]   'H0\\n' count: {data.count('H0' + chr(10))}")
            print(f"[DEBUG]   'H0' count: {data.count('H0')}")
            print(f"[DEBUG]   First 200 chars: {data[:200]}")
        
        # Reverse Step 4: Replace 'H0\n' with 'H0' (reverse of split/join)
        before_len = len(data)
        data = data.replace('H0\n', 'H0')
        after_len = len(data)
        
        if debug and iteration == 0:
            print(f"[DEBUG]   After H0\\n replacement: length={len(data)}, removed {before_len - after_len} chars")
        
        # Reverse Step 3: ROT-7 (reverse of ROT7 encoding, which is ROT19 since -7 mod 26 = 19)
        # Forward encoding uses ROT7: A->H, B->I, etc.
        # To reverse, we need ROT-7 or ROT19: H->A, I->B, etc.
        rot19_table = str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'TUVWXYZABCDEFGHIJKLMNOPQRStuvwxyzabcdefghijklmnopqrs'
        )
        data = data.translate(rot19_table)
        
        if debug and iteration == 0:
            print(f"[DEBUG]   After ROT-7 (ROT19): first 200 chars: {data[:200]}")
    
    if debug:
        print(f"\n[DEBUG] After all reverse iterations: {len(data)} characters")
        print(f"[DEBUG] First 200 characters: {data[:200]}")
        print(f"[DEBUG] Newlines in data: {data.count(chr(10))}")
        # Check for 'H0' patterns
        print(f"[DEBUG] 'H0' occurrences: {data.count('H0')}")
        print(f"[DEBUG] 'U0' occurrences (ROT13 of H0): {data.count('U0')}")
    
    # The newlines are just separating the recovered segments
    # For base64 decoding, we should remove them as they're not part of the base64 data
    data_no_newlines = data.replace('\n', '').replace('\r', '')
    
    if debug:
        print(f"[DEBUG] After removing newlines for base64: {len(data_no_newlines)} characters")
        print(f"[DEBUG] Data length mod 4: {len(data_no_newlines) % 4}")
        # Save intermediate data for inspection
        with open('debug_base64_data.txt', 'w') as f:
            f.write(data_no_newlines)
        print(f"[DEBUG] Saved intermediate base64 data to debug_base64_data.txt")
        
        # Check if there are any non-base64 characters
        import string
        valid_base64_chars = set(string.ascii_letters + string.digits + '+/=')
        invalid_chars = set(data_no_newlines) - valid_base64_chars
        if invalid_chars:
            print(f"[DEBUG] WARNING: Found invalid base64 characters: {invalid_chars}")
            print(f"[DEBUG] Count of each: {[(c, data_no_newlines.count(c)) for c in invalid_chars]}")
    
    # The length being 1 mod 4 (71877) suggests we're missing 3 characters OR have 1 extra
    # Let's try removing the last character if it's suspicious
    if len(data_no_newlines) % 4 == 1:
        if debug:
            print(f"[DEBUG] Length is 1 mod 4, last few chars: {data_no_newlines[-10:]}")
            # Try removing last char
            data_trimmed = data_no_newlines[:-1]
            print(f"[DEBUG] Trying with last char removed: {len(data_trimmed)} (mod 4: {len(data_trimmed) % 4})")
            # Use the trimmed version
            data_no_newlines = data_trimmed
    
    # Fix base64 padding if needed (only if not already divisible by 4)
    if len(data_no_newlines) % 4 != 0:
        padding_needed = (4 - (len(data_no_newlines) % 4)) % 4
        if padding_needed > 0:
            if debug:
                print(f"[DEBUG] Adding {padding_needed} padding characters ('=')")
            data_no_newlines = data_no_newlines + ('=' * padding_needed)
    
    # Step 9: From Base64 (reverse of To Base64)
    try:
        decoded_bytes = base64.b64decode(data_no_newlines)
        if debug:
            print(f"\n[DEBUG] ✓ After Base64 decode: {len(decoded_bytes)} bytes")
            print(f"[DEBUG] First 100 bytes: {decoded_bytes[:100]}")
    except Exception as e:
        print(f"Error decoding Base64: {e}")
        if debug:
            print(f"[DEBUG] Trying alternate base64 decoding methods...")
        # Try without validation
        try:
            decoded_bytes = base64.b64decode(data_no_newlines, validate=False)
            if debug:
                print(f"[DEBUG] Success with validate=False: {len(decoded_bytes)} bytes")
        except Exception as e2:
            print(f"Error with alternate method: {e2}")
            return
    
    # Step 10: Save the decoded bytes as an image
    try:
        # Try to interpret as image data
        from io import BytesIO
        img = Image.open(BytesIO(decoded_bytes))
        img.save(output_image_path)
        print(f"Decoded image saved to {output_image_path}")
        if debug:
            print(f"[DEBUG] Image size: {img.size}, mode: {img.mode}")
    except Exception as e:
        # If it's not image data, save as a text file or raw bytes
        if debug:
            print(f"[DEBUG] Could not interpret as image: {type(e).__name__}: {e}")
        print(f"Could not interpret as image: {e}")
        print("Attempting to save as text...")
        
        try:
            # Try to decode as text
            text = decoded_bytes.decode('utf-8')
            output_text_path = output_image_path.replace('.png', '.txt')
            with open(output_text_path, 'w') as f:
                f.write(text)
            print(f"Decoded text saved to {output_text_path}")
            if debug:
                print(f"[DEBUG] Text length: {len(text)} characters")
                print(f"[DEBUG] Text preview: {text[:500]}")
        except:
            # Save as raw bytes
            output_bin_path = output_image_path.replace('.png', '.bin')
            with open(output_bin_path, 'wb') as f:
                f.write(decoded_bytes)
            print(f"Decoded bytes saved to {output_bin_path}")
            if debug:
                print(f"[DEBUG] Binary data length: {len(decoded_bytes)} bytes")

# Main execution
if __name__ == "__main__":
    input_image_path = 'input.png'
    output_image_path = 'output.png'
    
    # Reverse the encoding process
    reverse_cyberchef_recipe(input_image_path, output_image_path)
