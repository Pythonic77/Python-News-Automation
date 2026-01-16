import requests
import time
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rss_config import OLLAMA_MODELS, OLLAMA_TIMEOUT

def test_ollama_hardening():
    print("\n🔬 TESTING OLLAMA HARDENING\n" + "="*40)
    
    test_prompt = "Summarize this in one sentence: US Senate passes a bill"
    
    # Try the ones in config first, then try the existing one as a backup test
    models_to_test = OLLAMA_MODELS + ["llama3.2:latest"]
    
    for model in models_to_test:
        print(f"\n🤖 Testing model: {model} (Timeout: {OLLAMA_TIMEOUT}s)...")
        start_time = time.time()
        
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model, 
                    "prompt": test_prompt, 
                    "stream": False
                },
                timeout=OLLAMA_TIMEOUT
            )
            
            duration = time.time() - start_time
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS in {duration:.1f}s")
                print(f"   📝 Response: {result['response'].strip()}")
                return # Exit on first success
            else:
                print(f"   ❌ FAILED with status: {response.status_code}")
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"   ❌ ERROR after {duration:.1f}s: {e}")
    
    print("\n" + "="*40 + "\n⚠️ VERIFICATION INCOMPLETE - ALL MODELS FAILED")
    sys.exit(1)

if __name__ == "__main__":
    test_ollama_hardening()
