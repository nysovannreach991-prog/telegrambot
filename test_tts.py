#!/usr/bin/env python3
"""Test script to verify edge-tts is working"""

import asyncio
import edge_tts
import tempfile
import os

async def test_tts():
    print("Testing Edge TTS...")
    
    # Test 1: Simple English
    print("\n1. Testing English voice...")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()
    
    try:
        communicate = edge_tts.Communicate("Hello", "en-US-AriaNeural")
        await communicate.save(temp_file.name)
        size = os.path.getsize(temp_file.name)
        print(f"   ✅ English: {size} bytes")
        os.unlink(temp_file.name)
    except Exception as e:
        print(f"   ❌ English failed: {e}")
    
    # Test 2: Khmer
    print("\n2. Testing Khmer voice...")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()
    
    try:
        communicate = edge_tts.Communicate("សួស្តី", "km-KH-PisethNeural")
        await communicate.save(temp_file.name)
        size = os.path.getsize(temp_file.name)
        print(f"   ✅ Khmer: {size} bytes")
        os.unlink(temp_file.name)
    except Exception as e:
        print(f"   ❌ Khmer failed: {e}")
    
    # Test 3: List available voices
    print("\n3. Listing available voices...")
    try:
        voices = await edge_tts.list_voices()
        khmer_voices = [v for v in voices if 'km-KH' in v['Name']]
        print(f"   Found {len(voices)} total voices")
        print(f"   Khmer voices: {khmer_voices}")
    except Exception as e:
        print(f"   ❌ List voices failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_tts())
