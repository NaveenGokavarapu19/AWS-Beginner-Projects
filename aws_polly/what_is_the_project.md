# ArticleToAudio: Text-to-Speech Converter with AWS Polly

A beginner-friendly Python application that converts written text into natural-sounding audio files using Amazon Polly. Perfect for creating audiobooks, accessibility tools, podcast content, or voice-overs in just 30 minutes.

## Description

ArticleToAudio is a simple yet powerful command-line tool that leverages AWS Polly's advanced text-to-speech capabilities to transform any written content into high-quality MP3 audio files. Users can input text directly, choose from multiple voice options (including different accents and genders), and generate professional-sounding audio with minimal setup.

**Key Features:**
- 🎤 Multiple voice options (US/UK accents, male/female)
- 📝 Interactive text input or file-based conversion
- 🎧 High-quality MP3 output
- 🚀 Quick setup (under 10 minutes)
- 💰 Cost-effective (AWS Free Tier eligible)
- 🔄 Batch processing support

## Prerequisites

### 1. Python Environment
- **Python 3.7 or higher** installed on your system
  - Check version: `python --version` or `python3 --version`
  - Download from: [python.org](https://www.python.org/downloads/)

### 2. AWS Account Setup
- **Active AWS Account** (free tier eligible)
  - Sign up at: [aws.amazon.com](https://aws.amazon.com/)
  - Free tier includes 5 million characters per month for 12 months

### 3. AWS Credentials Configuration
You'll need:
- AWS Access Key ID
- AWS Secret Access Key

**To create credentials:**
1. Log into AWS Console
2. Navigate to IAM (Identity and Access Management)
3. Click "Users" → "Add User"
4. Enable "Programmatic access"
5. Attach policy: `AmazonPollyFullAccess` (or `AmazonPollyReadOnlyAccess` for read-only)
6. Save your Access Key ID and Secret Access Key

### 4. Required Python Packages
```bash
pip install boto3
```

### 5. AWS CLI (Optional but Recommended)
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
```

When prompted, enter:
- AWS Access Key ID: `[Your Access Key]`
- AWS Secret Access Key: `[Your Secret Key]`
- Default region name: `us-east-1` (or your preferred region)
- Default output format: `json`

## Step-by-Step Implementation Guide

### Step 1: Install Dependencies and Configure AWS (10 minutes)

**1.1 Create a project directory:**
```bash
mkdir article-to-audio
cd article-to-audio
```

**1.2 Install required packages:**
```bash
pip install boto3
```

**1.3 Configure AWS credentials:**

**Option A: Using AWS CLI (Recommended)**
```bash
aws configure
```

**Option B: Manual configuration**

Create `~/.aws/credentials` file:
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Create `~/.aws/config` file:
```ini
[default]
region = us-east-1
output = json
```

**1.4 Test your AWS connection:**
```python
# test_connection.py
import boto3

try:
    polly = boto3.client('polly', region_name='us-east-1')
    voices = polly.describe_voices()
    print(f"✅ Connected! Found {len(voices['Voices'])} voices available.")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run: `python test_connection.py`

---

### Step 2: Create the Main Application (15 minutes)

**2.1 Create the main script:**

Create a file named `article_to_audio.py` and add the following code:

```python
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys

class ArticleToAudio:
    def __init__(self, region='us-east-1'):
        """Initialize the Polly client"""
        self.polly = boto3.client('polly', region_name=region)
        
        # Popular voice options
        self.voices = {
            '1': {'id': 'Joanna', 'name': 'Joanna (Female, US)'},
            '2': {'id': 'Matthew', 'name': 'Matthew (Male, US)'},
            '3': {'id': 'Emma', 'name': 'Emma (Female, UK)'},
            '4': {'id': 'Brian', 'name': 'Brian (Male, UK)'},
            '5': {'id': 'Amy', 'name': 'Amy (Female, UK)'},
            '6': {'id': 'Joanna', 'name': 'Joanna (Neural, Female, US)', 'engine': 'neural'}
        }
    
    def display_voices(self):
        """Display available voice options"""
        print("\n🎤 Available Voices:")
        print("-" * 40)
        for key, voice in self.voices.items():
            print(f"{key}. {voice['name']}")
        print("-" * 40)
    
    def get_user_input(self):
        """Get text input from user"""
        print("\n📝 Enter your text (or 'q' to quit):")
        print("(For multiline text, type your text and press Enter twice)\n")
        
        lines = []
        while True:
            line = input()
            if line.lower() == 'q':
                return None
            if line == '' and lines:
                break
            lines.append(line)
        
        return ' '.join(lines)
    
    def select_voice(self):
        """Let user select a voice"""
        self.display_voices()
        
        while True:
            choice = input("\nSelect voice (1-6): ").strip()
            if choice in self.voices:
                return self.voices[choice]
            print("❌ Invalid choice. Please select 1-6.")
    
    def convert_text_to_speech(self, text, voice_id, engine='standard', output_file='output.mp3'):
        """Convert text to speech using AWS Polly"""
        try:
            print(f"\n🔄 Converting text to speech using {voice_id}...")
            
            # Request speech synthesis
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine=engine
            )
            
            # Save the audio stream to a file
            if "AudioStream" in response:
                with open(output_file, 'wb') as file:
                    file.write(response['AudioStream'].read())
                
                print(f"✅ Success! Audio saved as: {output_file}")
                return True
            else:
                print("❌ Error: No audio stream in response")
                return False
                
        except (BotoCoreError, ClientError) as error:
            print(f"❌ Error: {error}")
            return False
    
    def run(self):
        """Main application loop"""
        print("=" * 50)
        print("🎧 ArticleToAudio - Text-to-Speech Converter")
        print("=" * 50)
        
        while True:
            # Get text input
            text = self.get_user_input()
            if text is None:
                print("\n👋 Goodbye!")
                break
            
            if len(text.strip()) == 0:
                print("⚠️  Please enter some text.")
                continue
            
            # Select voice
            voice = self.select_voice()
            engine = voice.get('engine', 'standard')
            
            # Generate filename
            output_file = f"audio_{voice['id']}_{len(text[:20])}.mp3"
            
            # Convert to speech
            success = self.convert_text_to_speech(
                text=text,
                voice_id=voice['id'],
                engine=engine,
                output_file=output_file
            )
            
            if success:
                print(f"\n📊 Audio Details:")
                print(f"   - Voice: {voice['name']}")
                print(f"   - Characters: {len(text)}")
                print(f"   - File: {output_file}")
            
            # Ask if user wants to convert more text
            another = input("\n🔁 Convert another text? (y/n): ").strip().lower()
            if another != 'y':
                print("\n👋 Thank you for using ArticleToAudio!")
                break

# Run the application
if __name__ == "__main__":
    app = ArticleToAudio()
    app.run()
```

**2.2 Test the basic functionality:**
```bash
python article_to_audio.py
```

---

### Step 3: Add File Processing Capability (Optional - 5 minutes)

Create a file named `file_to_audio.py` for batch processing:

```python
import boto3
import sys
import os

def convert_file_to_audio(input_file, voice_id='Joanna', output_file=None):
    """
    Convert a text file to audio
    
    Args:
        input_file (str): Path to text file
        voice_id (str): Polly voice ID
        output_file (str): Output MP3 file path
    """
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Read text from file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Set default output filename
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_audio.mp3"
    
    # Create Polly client
    polly = boto3.client('polly', region_name='us-east-1')
    
    print(f"📖 Converting {input_file} to audio...")
    print(f"📝 Text length: {len(text)} characters")
    
    # Synthesize speech
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='standard'
    )
    
    # Save audio
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())
    
    print(f"✅ Audio saved to {output_file}")

# Command-line usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_to_audio.py <text_file> [voice_id] [output_file]")
        print("Example: python file_to_audio.py story.txt Matthew story_audio.mp3")
        sys.exit(1)
    
    input_file = sys.argv[1]
    voice_id = sys.argv[2] if len(sys.argv) > 2 else 'Joanna'
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    convert_file_to_audio(input_file, voice_id, output_file)
```

**Create a sample text file for testing:**

Create `sample_story.txt`:
```text
Welcome to ArticleToAudio! This is a demonstration of AWS Polly's 
text-to-speech capabilities. You can convert any written text into 
natural-sounding audio files. This technology is perfect for creating 
audiobooks, accessibility tools, or voice-overs for your projects.
```

**Test file conversion:**
```bash
python file_to_audio.py sample_story.txt
```

---

### Step 4: Testing and Validation (5 minutes)

**4.1 Test different voices:**
```bash
# Test with different voices
python file_to_audio.py sample_story.txt Joanna output_joanna.mp3
python file_to_audio.py sample_story.txt Matthew output_matthew.mp3
python file_to_audio.py sample_story.txt Emma output_emma.mp3
```

**4.2 Test the interactive mode:**
```bash
python article_to_audio.py
```

Try entering:
- Short text (1-2 sentences)
- Longer text (paragraph)
- Different voice options

**4.3 Verify output files:**
```bash
# List generated MP3 files
ls -lh *.mp3

# Play audio (macOS)
afplay output.mp3

# Play audio (Linux)
mpg123 output.mp3

# Play audio (Windows)
start output.mp3
```

## Expected Output/Results

### Successful Execution

When you run the application successfully, you should see:

```
==================================================
🎧 ArticleToAudio - Text-to-Speech Converter
==================================================

📝 Enter your text (or 'q' to quit):
(For multiline text, type your text and press Enter twice)

Hello, this is a test of AWS Polly text-to-speech conversion.

🎤 Available Voices:
----------------------------------------
1. Joanna (Female, US)
2. Matthew (Male, US)
3. Emma (Female, UK)
4. Brian (Male, UK)
5. Amy (Female, UK)
6. Joanna (Neural, Female, US)
----------------------------------------

Select voice (1-6): 1

🔄 Converting text to speech using Joanna...
✅ Success! Audio saved as: audio_Joanna_20.mp3

📊 Audio Details:
   - Voice: Joanna (Female, US)
   - Characters: 62
   - File: audio_Joanna_20.mp3

🔁 Convert another text? (y/n): n

👋 Thank you for using ArticleToAudio!
```

### Generated Files

After running the application, you should have:
- **MP3 audio files** in your project directory
- **File size**: Approximately 10-50 KB per 100 words
- **Audio quality**: 24 kHz, mono, MP3 format

### Audio Characteristics

- **Standard voices**: Natural-sounding, clear pronunciation
- **Neural voices**: More human-like, with better intonation
- **Supported languages**: English (US/UK), plus 20+ other languages
- **Speech rate**: ~150 words per minute (adjustable with SSML)

## Troubleshooting

### Common Issues and Solutions

#### 1. **"Unable to locate credentials"**

**Error:**
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solutions:**
- Verify AWS credentials are configured:
  ```bash
  aws configure list
  ```
- Check credentials file exists:
  ```bash
  cat ~/.aws/credentials
  ```
- Manually set credentials:
  ```python
  polly = boto3.client(
      'polly',
      region_name='us-east-1',
      aws_access_key_id='YOUR_ACCESS_KEY',
      aws_secret_access_key='YOUR_SECRET_KEY'
  )
  ```

#### 2. **"Access Denied" or Permission Errors**

**Error:**
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException)
```

**Solutions:**
- Verify IAM user has Polly permissions
- Attach `AmazonPollyFullAccess` policy to your IAM user
- Check policy in AWS Console: IAM → Users → [Your User] → Permissions

#### 3. **"Invalid Voice ID"**

**Error:**
```
An error occurred (InvalidParameterValue) when calling the SynthesizeSpeech operation
```

**Solutions:**
- List available voices:
  ```python
  import boto3
  polly = boto3.client('polly', region_name='us-east-1')
  voices = polly.describe_voices()
  for voice in voices['Voices']:
      print(f"{voice['Id']} - {voice['Name']} ({voice['LanguageCode']})")
  ```
- Use correct voice ID (case-sensitive): `Joanna`, not `joanna`