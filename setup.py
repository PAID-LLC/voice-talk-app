"""Setup Script - Download Models and Initialize Application"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def download_vosk_model():
    """Download Vosk model"""
    print("\n" + "="*60)
    print(" Downloading Vosk Model ")
    print("="*60)

    models_dir = Path("./models/vosk_models")
    model_dir = models_dir / "model"

    if model_dir.exists():
        print(f"Vosk model already exists at {model_dir}")
        response = input("Download anyway? (y/n): ").lower()
        if response != "y":
            return True

    print("\nVosk Model Options:")
    print(" 1. Small model (50MB) - English, ~20k words, RECOMMENDED")
    print(" 2. Large model (1.4GB) - English, full vocabulary")
    print(" 3. Skip download")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        # Small model
        url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        filename = "vosk-model-small.zip"
    elif choice == "2":
        # Large model
        url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
        filename = "vosk-model-large.zip"
    else:
        print("Skipped model download")
        return False

    try:
        # Create directory
        models_dir.mkdir(parents=True, exist_ok=True)

        filepath = models_dir / filename

        if not filepath.exists():
            print(f"\nDownloading {filename}...")
            print(f"URL: {url}")

            def download_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(downloaded * 100 / total_size, 100)
                print(f"\rProgress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f}MB)", end="")

            urllib.request.urlretrieve(url, filepath, download_progress)
            print("\n✓ Download complete")

        # Extract
        print(f"\nExtracting {filename}...")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(models_dir)
        print("✓ Extraction complete")

        # Rename to 'model'
        extracted = [d for d in models_dir.iterdir() if d.is_dir() and d.name != "model"]
        if extracted:
            extracted[0].rename(model_dir)
            print(f"✓ Model placed at: {model_dir}")

        return True

    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print("\n" + "="*60)
    print(" Installing Dependencies ")
    print("="*60)

    import subprocess

    try:
        # Check if Poetry is installed
        import poetry
        print("\n✓ Poetry is installed")
        print("\nRunning: poetry install")

        # Use subprocess.run instead of os.system for better security
        result = subprocess.run(["poetry", "install"], check=False)
        if result.returncode != 0:
            print("! Poetry install failed, trying pip instead")
            result = subprocess.run(["pip", "install", "-r", "requirements.txt"], check=False)
            if result.returncode != 0:
                print("! Dependency installation failed")
                return False

    except (ImportError, FileNotFoundError):
        print("\n! Poetry not found, using pip instead")
        print("\nRunning: pip install -r requirements.txt")

        # Use subprocess.run instead of os.system for better security
        result = subprocess.run(["pip", "install", "-r", "requirements.txt"], check=False)
        if result.returncode != 0:
            print("! Dependency installation failed")
            return False

    print("\n✓ Dependencies installed")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n" + "="*60)
    print(" Creating Directories ")
    print("="*60)

    dirs = [
        "models/vosk_models",
        "data/logs",
        "data/cache",
        "data/audio_uploads"
    ]

    for d in dirs:
        p = Path(d)
        p.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {d}")


def create_env_file():
    """Create .env file template"""
    print("\n" + "="*60)
    print(" Environment Configuration ")
    print("="*60)

    env_file = Path(".env")

    if env_file.exists():
        print(" .env file already exists")
        response = input("Overwrite? (y/n): ").lower()
        if response != "y":
            return

    env_content = """# Voice Talk Application Configuration
# Leave blank for default values

# API Keys (optional, for cloud features)
STT_HUGGINGFACE_API_KEY=
AI_HUGGINGFACE_API_KEY=
TTS_AZURE_API_KEY=
TTS_AZURE_REGION=eastus

# Audio Settings
AUDIO_SAMPLE_RATE=16000
AUDIO_DEVICE_INDEX=

# Logging
LOG_LEVEL=INFO

# Debug Mode
DEBUG=false
"""

    env_file.write_text(env_content)
    print("✓ Created .env file (add your API keys here)")


def main():
    """Run setup"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     Voice Talk Application - Setup & Installation       ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Create directories
    create_directories()

    # Install dependencies
    response = input("\nInstall Python dependencies? (y/n): ").lower()
    if response == "y":
        install_dependencies()

    # Download Vosk model
    response = input("\nDownload Vosk model for offline speech recognition? (y/n): ").lower()
    if response == "y":
        download_vosk_model()

    # Create .env file
    response = input("\nCreate .env configuration file? (y/n): ").lower()
    if response == "y":
        create_env_file()

    # Final instructions
    print("\n" + "="*60)
    print(" Setup Complete! ")
    print("="*60)

    print("\nNext steps:")
    print("\n1. Add API keys to .env (optional for cloud features)")
    print("   - HuggingFace: https://huggingface.co/settings/tokens")
    print("   - Azure TTS: https://portal.azure.com")

    print("\n2. Start the application:")
    print("   Option A - Interactive Mode:")
    print("     python cli.py talk")
    print("   Option B - FastAPI Server:")
    print("     python cli.py server")
    print("   Option C - Start main server:")
    print("     python main.py")

    print("\n3. API Documentation:")
    print("   http://127.0.0.1:8000/docs (when server is running)")

    print("\n4. Transcribe audio files:")
    print("   python cli.py transcribe --file audio.wav")

    print("\n5. Check application status:")
    print("   python cli.py status")

    print("\n" + "="*60)
    print(" For help, run: python cli.py --help")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)
