# Quick Setup Checklist ✓

Follow this checklist to get Voice Talk App running in 15 minutes!

## Phase 1: Preparation (2 minutes)

- [ ] Project folder is: `c:\Users\MyAIE\voice-talk-app`
- [ ] You have GitHub repository: https://github.com/ArtiIntel1955/voice-talk-app
- [ ] You have Python 3.11+ installed
- [ ] You have internet connection

## Phase 2: Clone/Update Code (1 minute)

```bash
# Option A: If cloning fresh
git clone https://github.com/ArtiIntel1955/voice-talk-app.git
cd voice-talk-app

# Option B: If already have it
cd c:\Users\MyAIE\voice-talk-app
git pull origin main
```

- [ ] Code is up to date
- [ ] All files present (check: `ls src/` shows folders)

## Phase 3: Run Setup (5 minutes)

```bash
cd c:\Users\MyAIE\voice-talk-app
python setup.py
```

Follow prompts:
- [ ] Install dependencies? **Yes**
- [ ] Download Vosk model? **Yes** → Choose option 1 (small, 50MB)
- [ ] Create .env file? **Yes**

Output should show:
```
Setting up Voice Talk Application...
✓ Dependencies installed
✓ Vosk model downloaded
✓ .env file created
```

- [ ] Setup completed successfully
- [ ] Vosk model is in: `models/vosk_models/model/`
- [ ] `.env` file was created

## Phase 4: Get API Keys (5 minutes) - CHOOSE ONE

### Option A: HuggingFace (RECOMMENDED - 3 minutes)

**Best for**: Immediate usage, no credit card needed

1. Go to: https://huggingface.co/settings/tokens
2. Sign up (2 min)
3. Create API token (1 min)
4. Copy token (looks like: `hf_xxxxxxxxxxxxx`)

- [ ] HuggingFace account created
- [ ] API token generated
- [ ] Token copied (starts with `hf_`)

### Option B: Azure (OPTIONAL - 5 minutes)

**Best for**: Premium TTS voices

1. Go to: https://portal.azure.com
2. Sign up (2 min)
3. Create Speech resource (2 min)
4. Get API key (1 min)

- [ ] Microsoft account created
- [ ] Azure resource created
- [ ] API key copied
- [ ] Region noted (e.g., `eastus`)

### Option C: Google Cloud (OPTIONAL - 7 minutes)

**Best for**: Google-quality speech recognition

1. Go to: https://console.cloud.google.com
2. Create project (1 min)
3. Enable Speech API (1 min)
4. Create service account (3 min)
5. Download JSON key (1 min)

- [ ] Google Cloud project created
- [ ] Speech API enabled
- [ ] Service account created
- [ ] `google-key.json` downloaded

## Phase 5: Configure Environment (2 minutes)

Open `.env` file:

```bash
cd c:\Users\MyAIE\voice-talk-app
notepad .env
```

Add your API keys (use whichever you got):

**HuggingFace only:**
```env
STT_HUGGINGFACE_API_KEY=hf_your_token_here
AI_HUGGINGFACE_API_KEY=hf_your_token_here
```

**HuggingFace + Azure:**
```env
STT_HUGGINGFACE_API_KEY=hf_your_token_here
AI_HUGGINGFACE_API_KEY=hf_your_token_here
TTS_AZURE_API_KEY=your_azure_key
TTS_AZURE_REGION=eastus
```

**All services:**
```env
STT_HUGGINGFACE_API_KEY=hf_your_token
AI_HUGGINGFACE_API_KEY=hf_your_token
TTS_AZURE_API_KEY=your_azure_key
TTS_AZURE_REGION=eastus
GOOGLE_APPLICATION_CREDENTIALS=c:\Users\MyAIE\voice-talk-app\google-key.json
```

- [ ] `.env` file opened
- [ ] API keys pasted correctly
- [ ] File saved (Ctrl+S)
- [ ] No extra spaces or quotes around keys

## Phase 6: Start Server (1 minute)

```bash
cd c:\Users\MyAIE\voice-talk-app
python cli.py server
```

You should see:
```
Starting Voice Talk Server...
Server: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

INFO:     Uvicorn running on http://127.0.0.1:8000
```

- [ ] Server started successfully
- [ ] No errors in console
- [ ] URL shown: http://127.0.0.1:8000

## Phase 7: Test the Application (1 minute)

### Test in Browser
1. Open browser
2. Go to: http://127.0.0.1:8000/docs
3. You should see Swagger UI with all API endpoints

- [ ] Swagger UI loaded
- [ ] All endpoints visible (conversation, speech, voice, audio, commands)

### Test in CLI (Optional Terminal)

Open NEW terminal (keep server running in first one):

```bash
cd c:\Users\MyAIE\voice-talk-app
python cli.py talk
```

Try:
```
You: Hello, how are you?
```

Wait for response...

- [ ] Response received from AI
- [ ] Text displayed in terminal
- [ ] (Optional) Audio played from speakers

### Test Transcription (Optional)

```bash
python cli.py transcribe --file test_audio.wav
```

- [ ] Transcription completed
- [ ] Output file created

---

## Quick Commands Reference

```bash
# Start interactive chat
python cli.py talk

# Start API server
python cli.py server

# Check status
python cli.py status

# List audio devices
python cli.py list-devices

# Transcribe file
python cli.py transcribe --file audio.wav
```

---

## Troubleshooting Checklist

### Server won't start
- [ ] Did you run `python setup.py` first?
- [ ] Is port 8000 free? (no other app using it)
- [ ] Is Python 3.11+ installed? (`python --version`)
- [ ] Do you have dependencies? (`pip list | grep fastapi`)

### API key not working
- [ ] Did you add it to `.env` file?
- [ ] Did you save `.env` file?
- [ ] Did you restart server after editing `.env`?
- [ ] Is key pasted completely (check for missing chars)?
- [ ] Does it have the right prefix? (`hf_` for HuggingFace)

### Vosk model not found
- [ ] Is model at: `models/vosk_models/model/`?
- [ ] Did setup.py complete successfully?
- [ ] Is folder named exactly `model` (not `vosk-model-xxx`)?
- [ ] Re-run setup: `python setup.py`

### No sound output
- [ ] Are speakers enabled in Windows?
- [ ] Check Volume in taskbar (bottom right)
- [ ] Does your microphone work? (test in Windows)
- [ ] Run: `python cli.py list-devices` to verify

### Errors in terminal?
- [ ] Copy full error message
- [ ] Google the error (usually helpful)
- [ ] Check: `DEVELOPMENT_PROGRESS.md` for solutions
- [ ] Check: `QUICKSTART.md` troubleshooting section

---

## What You Now Have

After completing this checklist:

✅ Voice Talk App installed and running
✅ Speech recognition working (Vosk offline)
✅ Text-to-speech working (Pyttsx3)
✅ Conversational AI configured (HuggingFace API)
✅ REST API accessible (http://127.0.0.1:8000/docs)
✅ CLI tools ready to use
✅ Ready for production or further development

---

## Next Steps (Optional Improvements)

1. **Build GUI** - Create PyQt6 graphical interface
2. **Add Wake Word** - Listen for "Hey Voice" automatically
3. **Deploy to Cloud** - Put on AWS/Google Cloud/Azure
4. **Create Mobile App** - Companion app for phone
5. **Add More Commands** - Create custom voice commands

---

## Documentation Files

Reference these files for more info:

- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute quick start
- **API_KEYS_SETUP.md** - Detailed API key instructions
- **GITHUB_SETUP.md** - Git and GitHub guide
- **DEVELOPMENT_PROGRESS.md** - What's already built

---

## Success Indicators ✓

If you see these, you're done!

- [ ] `python setup.py` completed without errors
- [ ] `python cli.py server` shows "Uvicorn running"
- [ ] http://127.0.0.1:8000/docs loads in browser
- [ ] Swagger UI shows 20+ API endpoints
- [ ] `python cli.py talk` gets AI responses
- [ ] (Optional) `.env` file has your API keys

---

## Emergency Help

**Everything broken?**

1. Check error message carefully
2. Google the error (usually has answer)
3. Delete and re-download: `git pull origin main`
4. Restart everything: Close terminals, reopen, run `python setup.py` again
5. Check file permissions: Make sure you can write to folder

---

**Estimated Total Time: 15 minutes**

You're ready to go! Start with **Phase 1** above. 🚀
