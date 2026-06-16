import sys
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def test_youtube_fetch(video_id):
    print(f"--- Testing Transcript Fetch for Video ID: {video_id} ---")
    try:
        # 1. Initialize the API instance
        api = YouTubeTranscriptApi()
        
        # 2. Get the list of available transcripts
        print("[1/3] Checking available transcripts...")
        transcript_list = api.list(video_id)
        
        # 3. Find the English transcript
        print("[2/3] Finding English transcript...")
        transcript = transcript_list.find_transcript(['en'])
        
        # 4. Download captions
        print("[3/3] Downloading captions...")
        raw_data = transcript.fetch()
        
        # 5. FIX: Access .text attribute instead of ["text"] dictionary key
        full_text = " ".join(segment.text for segment in raw_data)
        
        # FIX: Removed emojis to prevent Windows encoding crashes
        print("\nSUCCESS!")
        print(f"Total Character Count: {len(full_text)}")
        print("\nFirst 300 characters of transcript sample:")
        print("-" * 40)
        print(full_text[:300] + "...")
        print("-" * 40)
        return True

    except TranscriptsDisabled:
        print("\nFAILED: Captions/Transcripts are disabled for this video.")
        return False
    except Exception as e:
        print(f"\nERROR ENCOUNTERED: {str(e)}")
        return False

if __name__ == "__main__":
    test_id = "jzD_yyEcp0M" 
    test_youtube_fetch(test_id)