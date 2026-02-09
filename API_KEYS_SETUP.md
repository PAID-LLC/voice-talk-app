# Free API Keys Setup Guide

## Complete Step-by-Step Instructions

This guide will help you set up FREE API keys for enhanced features. You only NEED HuggingFace - the rest are optional premium upgrades.

---

## 1. HuggingFace API Key (ESSENTIAL - START HERE)

**Why**: Improves speech recognition accuracy + conversational AI
**Cost**: FREE - 1,000 calls per day
**Time**: 5 minutes
**Difficulty**: Easy

### Step 1: Create HuggingFace Account
1. Go to: https://huggingface.co/
2. Click **"Sign Up"** (top right)
3. Fill in email and password
4. Click **"Sign Up"**
5. Verify your email (check inbox)

### Step 2: Get Your API Token
1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"** button
3. Fill in:
   - **Name**: `voice-talk-app` (or any name)
   - **Type**: `read` (for inference)
   - **Expiration**: Never (or 1 month)
4. Click **"Generate token"**
5. **COPY THE TOKEN** (starts with `hf_`)
   - It will look like: `hf_aBcDeFgHiJkLmNoPqRsT`
6. **KEEP IT SECRET** - Don't share on GitHub!

### Step 3: Add to Your .env File

In project folder, edit `.env`:

```bash
# Open with notepad or VS Code
c:\Users\MyAIE\voice-talk-app\.env
```

Add these two lines:

```env
STT_HUGGINGFACE_API_KEY=hf_your_token_here
AI_HUGGINGFACE_API_KEY=hf_your_token_here
```

Replace `hf_your_token_here` with your actual token (paste it twice).

### Step 4: Test It Works

```bash
cd c:\Users\MyAIE\voice-talk-app
python cli.py server
```

Then try:
```bash
curl -X POST http://127.0.0.1:8000/api/conversation/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, how are you?","session_id":"test"}'
```

✅ If you get a response with conversational text, it works!

---

## 2. Azure Speech Services (OPTIONAL - Better TTS)

**Why**: High-quality text-to-speech, 5 million characters free/month
**Cost**: FREE tier available
**Time**: 10 minutes
**Difficulty**: Medium

### Step 1: Create Microsoft Account (if needed)
1. Go to: https://account.microsoft.com/
2. Click **"Create one"** (or sign in if you have account)
3. Use existing email or create new Microsoft account

### Step 2: Create Azure Account
1. Go to: https://portal.azure.com/
2. Click **"Start free"** (if first time)
3. Sign in with Microsoft account
4. Fill in profile info
5. Add payment method (won't charge for free tier)
6. Click **"Next"**
7. **Agree to terms**
8. Click **"Sign up"**

### Step 3: Create Speech Resource
1. In Azure Portal, search: **"Speech"**
2. Click **"Speech Services"**
3. Click **"+ Create"**
4. Fill in:
   - **Name**: `voice-talk-speech` (any name)
   - **Region**: `East US` (closest to you)
   - **Pricing tier**: **Free (F0)** ← Important!
5. Click **"Review + create"**
6. Click **"Create"**

### Step 4: Get Your Keys
1. Go to resource → **"Keys and endpoint"**
2. Copy **"Key 1"** (looks like random letters/numbers)
3. Note the **Region** (e.g., `eastus`)

### Step 5: Add to .env

```env
TTS_AZURE_API_KEY=your_key_here
TTS_AZURE_REGION=eastus
```

Replace with your actual key and region.

### Step 6: Test It

```bash
curl -X POST http://127.0.0.1:8000/api/voice/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice":"default"}'
```

✅ Should return audio data!

---

## 3. Google Cloud Speech-to-Text (OPTIONAL - Alternative STT)

**Why**: Google-quality speech recognition
**Cost**: FREE - $300 credit + 60 minutes audio/month
**Time**: 15 minutes
**Difficulty**: Medium-Hard

### Step 1: Create Google Account
- Go to: https://accounts.google.com/
- Sign up or sign in (use existing Gmail)

### Step 2: Create Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Click project dropdown (top left)
3. Click **"New Project"**
4. Enter name: `voice-talk-app`
5. Click **"Create"**
6. Wait for project to be created (1 minute)

### Step 3: Enable Speech-to-Text API
1. Search: **"Speech-to-Text API"**
2. Click **"Enable"**
3. Wait (1 minute)

### Step 4: Create Service Account
1. Go to: **"Credentials"** (left menu)
2. Click **"+ Create Credentials"** → **"Service Account"**
3. Fill in:
   - **Service account name**: `voice-talk`
4. Click **"Create and Continue"**
5. Click **"Continue"** (skip roles for now)
6. Click **"Create Key"**
7. Select **JSON**
8. Click **"Create"**
9. **File will download** - Save it safely!
   - Save as: `c:\Users\MyAIE\voice-talk-app\google-key.json`

### Step 5: Add to .env

```env
GOOGLE_APPLICATION_CREDENTIALS=c:\Users\MyAIE\voice-talk-app\google-key.json
```

### Step 6: Test It

```bash
python
>>> from google.cloud import speech
>>> print("Google Cloud configured!")
```

✅ If no error, it works!

---

## 4. Deepgram (OPTIONAL - Real-time Speech)

**Why**: Excellent real-time transcription, $200 free credit
**Cost**: FREE - $200 credit for new users
**Time**: 5 minutes
**Difficulty**: Easy

### Step 1: Sign Up
1. Go to: https://console.deepgram.com/
2. Click **"Sign Up"**
3. Enter email and password
4. Verify email

### Step 2: Get API Key
1. Go to: **"Settings"** → **"API Keys"**
2. Click **"Create a new API Key"**
3. Copy the key

### Step 3: Add to .env

```env
DEEPGRAM_API_KEY=your_key_here
```

---

## 5. ElevenLabs (OPTIONAL - Better Voices)

**Why**: Natural-sounding AI voices, 10k characters/month free
**Cost**: FREE tier available
**Time**: 5 minutes
**Difficulty**: Easy

### Step 1: Sign Up
1. Go to: https://elevenlabs.io/
2. Click **"Sign Up"**
3. Email and password
4. Verify email

### Step 2: Get API Key
1. Go to: **"Profile"** (bottom left) → **"API Key"**
2. Copy your API key

### Step 3: Add to .env

```env
ELEVENLABS_API_KEY=your_key_here
```

---

## 6. AssemblyAI (OPTIONAL - Premium STT)

**Why**: High-accuracy speech-to-text, $50 free credit
**Cost**: FREE - $50 credit for testing
**Time**: 5 minutes
**Difficulty**: Easy

### Step 1: Sign Up
1. Go to: https://www.assemblyai.com/
2. Click **"Get Started Free"**
3. Email and password
4. Verify email

### Step 2: Get API Key
1. Go to: **"Dashboard"** → **"API Tokens"**
2. Copy your API key

### Step 3: Add to .env

```env
ASSEMBLYAI_API_KEY=your_key_here
```

---

## Your Complete .env File

Here's what your final `.env` should look like:

```env
# ===== ESSENTIAL (Get these!) =====
STT_HUGGINGFACE_API_KEY=hf_YOUR_HUGGINGFACE_TOKEN
AI_HUGGINGFACE_API_KEY=hf_YOUR_HUGGINGFACE_TOKEN

# ===== OPTIONAL BUT RECOMMENDED =====
TTS_AZURE_API_KEY=YOUR_AZURE_KEY
TTS_AZURE_REGION=eastus

# ===== OPTIONAL - Advanced =====
GOOGLE_APPLICATION_CREDENTIALS=c:\Users\MyAIE\voice-talk-app\google-key.json
DEEPGRAM_API_KEY=YOUR_DEEPGRAM_KEY
ELEVENLABS_API_KEY=YOUR_ELEVENLABS_KEY
ASSEMBLYAI_API_KEY=YOUR_ASSEMBLYAI_KEY

# ===== Server Settings =====
HOST=127.0.0.1
PORT=8000
DEBUG=false

# ===== Logging =====
LOG_LEVEL=INFO
```

---

## How to Create/Edit .env File

### Option 1: Using Command Line
```bash
cd c:\Users\MyAIE\voice-talk-app
copy .env.example .env
notepad .env
```

Then paste your keys and save.

### Option 2: Using VS Code
```bash
code .env
```

Paste keys and save (Ctrl+S).

### Option 3: Using Explorer
1. Open: `c:\Users\MyAIE\voice-talk-app`
2. Right-click → **"New"** → **"Text Document"**
3. Name it: `.env` (important - the dot!)
4. Right-click → **"Open with"** → **"Notepad"**
5. Paste your keys
6. Save

---

## Safety Tips for API Keys

⚠️ **IMPORTANT - Keep Your Keys Secret!**

1. **Never commit .env to GitHub**
   - Already in `.gitignore` ✓

2. **Never share keys publicly**
   - Don't post on forums
   - Don't put in GitHub publicly

3. **Rotate keys if exposed**
   - Go to API provider
   - Delete old key
   - Create new key

4. **Use separate keys per app**
   - One key for voice-talk-app
   - Different keys for other projects

5. **Monitor usage**
   - Check dashboards regularly
   - Set up alerts for overages

---

## Testing Your API Keys

### Test HuggingFace (Most Important)
```bash
cd c:\Users\MyAIE\voice-talk-app
python cli.py server
# In another terminal:
python cli.py talk
# Try: "Hello, what's your name?"
```

### Test Azure TTS
```bash
curl -X POST http://127.0.0.1:8000/api/voice/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Testing Azure voice"}'
```

### Test Google Cloud
```bash
python
from google.cloud import speech
print("Google Cloud working!")
```

---

## Troubleshooting

### "API key not found"
- ✓ Did you create `.env` in correct folder?
- ✓ Did you copy the full key (with `hf_` prefix)?
- ✓ No extra spaces or quotes?
- ✓ Restarted the server after editing .env?

### "Invalid API key"
- ✓ Copy entire key (sometimes partially selected)
- ✓ Make sure it's not expired
- ✓ Check you're using correct key for correct service

### "Quota exceeded"
- ✓ HuggingFace: Limited to 1000 calls/day (generous!)
- ✓ Azure: 5 million characters/month
- ✓ Just wait for next day/month

### "Connection refused"
- ✓ Is your server running? `python cli.py server`
- ✓ Is port 8000 correct?
- ✓ Do you have internet connection?

---

## Recommended Priority

1. **HuggingFace** ← Start here (5 min) ⭐⭐⭐
2. **Azure TTS** ← Optional, nice to have (10 min) ⭐⭐
3. **Google Cloud** ← Advanced option (15 min) ⭐
4. Others → Only if needed

**Minimum**: Just HuggingFace is enough to get started!

---

## Usage Limits Summary

| Service | Free Tier | Limit | Resets |
|---------|-----------|-------|--------|
| HuggingFace | 1,000 calls | Per day | Every 24h |
| Azure TTS | 5M characters | Per month | Monthly |
| Google Cloud | $300 credit | ~60 min audio | Monthly |
| Deepgram | $200 credit | One-time | N/A |
| ElevenLabs | 10k chars | Per month | Monthly |
| AssemblyAI | $50 credit | One-time | N/A |

---

## Next Steps

1. ✅ Get HuggingFace API key
2. ✅ Create `.env` file
3. ✅ Add your HuggingFace key
4. ✅ Run: `python setup.py`
5. ✅ Test: `python cli.py server`
6. ✅ Visit: http://127.0.0.1:8000/docs
7. Optional: Get Azure key for better voices
8. Optional: Get Google Cloud for alternatives

---

**Questions?** See troubleshooting section above!

Now you're ready to use all premium features for FREE! 🚀
