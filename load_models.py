import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import snapshot_download, login

# Optional: Enable better logging for debugging
# from transformers.utils import logging
# logging.set_verbosity_info()

# Hugging Face login with environment variable
token = os.getenv("HF_TOKEN")
if token:
    try:
        login(token=token)
        print("🔐 Hugging Face login successful.")
    except Exception as e:
        print(f"❌ Login failed: {e}")
else:
    print("⚠️ Hugging Face token not found. Set HF_TOKEN environment variable.")

# Models to use
MODELS = {
    "starcoder": "bigcode/starcoder",
    "codellama": "codellama/CodeLlama-7b-hf"
}

MODEL_DIR = Path("models")
tokenizers = {}
model_instances = {}

# Ensure model directory exists
MODEL_DIR.mkdir(exist_ok=True)

def ensure_model_downloaded(model_name, hf_repo_id):
    local_model_path = MODEL_DIR / model_name
    if not local_model_path.exists() or not list(local_model_path.glob("**/*")):
        print(f"⬇️ Downloading {model_name} from {hf_repo_id} ...")
        snapshot_download(
            repo_id=hf_repo_id,
            local_dir=local_model_path,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        print(f"✅ {model_name} downloaded.")
    else:
        print(f"✅ Found local model: {model_name}")
    return str(local_model_path)

def load_all_models():
    for name, repo in MODELS.items():
        local_path = ensure_model_downloaded(name, repo)
        print(f"📦 Loading model: {name} ...")
        tokenizer = AutoTokenizer.from_pretrained(local_path)
        model = AutoModelForCausalLM.from_pretrained(
            local_path,
            device_map="auto",  # Automatically selects GPU/CPU
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        tokenizers[name] = tokenizer
        model_instances[name] = model
        print(f"✅ Model loaded: {name}")
    print("\n🚀 All models are loaded and ready!")

def generate_code(prompt):
    results = {}
    for name, model in model_instances.items():
        tokenizer = tokenizers[name]
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        output = model.generate(
            **inputs,
            max_length=200,
            do_sample=True,
            top_k=50,
            temperature=0.7
        )
        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
        results[name] = decoded
    return results

if __name__ == "__main__":
    load_all_models()
    
    # 🧪 Test prompt
    prompt = "Write a Python function to check if a number is prime."
    print(f"\n💡 Prompt: {prompt}")
    
    responses = generate_code(prompt)
    for name, output in responses.items():
        print(f"\n🔧 {name.upper()} Response:\n{output}\n")
