#!/usr/bin/env python3
"""
Translate text from English to Chinese (Simplified) using Google Translate
Uses deep-translator library (not LLM)
"""

import sys
from deep_translator import GoogleTranslator

def translate_text(text, max_chunk=4500):
    """Translate text to Chinese (Simplified)"""
    if not text or not text.strip():
        return text
    
    translator = GoogleTranslator(source='en', target='chinese (simplified)')
    
    # Split into chunks if text is too long
    chunks = []
    current_chunk = []
    current_length = 0
    
    lines = text.split('\n')
    for line in lines:
        if current_length + len(line) > max_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += len(line)
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    # Translate each chunk
    translated_chunks = []
    for chunk in chunks:
        if chunk.strip():
            try:
                translated = translator.translate(chunk)
                translated_chunks.append(translated)
            except Exception as e:
                print(f"⚠️ Translation error: {e}", file=sys.stderr)
                translated_chunks.append(chunk)  # Keep original on error
        else:
            translated_chunks.append(chunk)
    
    return '\n'.join(translated_chunks)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Read from stdin
        text = sys.stdin.read()
    
    translated = translate_text(text)
    print(translated)
