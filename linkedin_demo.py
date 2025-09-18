"""
AI21 Labs + Bright Data LinkedIn Profile Demo Backend
Simple backend to extract LinkedIn profiles and generate funny facts using Jamba LLM
"""

import os
import json
import time
import requests
from typing import List, Dict
from llama_index.llms.ai21 import AI21
from llama_index.core.llms import ChatMessage
from dotenv import load_dotenv

load_dotenv()

class LinkedInProfileAnalyzer:
    def __init__(self, ai21_api_key: str, bright_data_token: str, dataset_id: str = "gd_l1viktl72bvl7bjuj0"):
        """Initialize the analyzer with API keys"""
        self.ai21_api_key = ai21_api_key
        self.bright_data_token = bright_data_token
        self.dataset_id = dataset_id
        self.llm = AI21(
            api_key=ai21_api_key,
            model="jamba-mini",
            temperature=0.8,  # Higher temperature for more creative/funny responses
        )
    
    def scrape_linkedin_profiles(self, linkedin_urls: List[str]) -> List[Dict]:
        """
        Real Bright Data LinkedIn scraping implementation
        """
        print(f"🔍 Scraping {len(linkedin_urls)} LinkedIn profiles with Bright Data...")
        
        # Step 1: Trigger the scraping job
        trigger_url = f"https://api.brightdata.com/datasets/v3/trigger"
        
        headers = {
            "Authorization": f"Bearer {self.bright_data_token}",
            "Content-Type": "application/json"
        }
        
        # Prepare the payload - list of LinkedIn URLs
        payload = [{"url": url} for url in linkedin_urls]
        
        params = {
            "dataset_id": self.dataset_id,
            "include_errors": "true"
        }
        
        try:
            print("📤 Triggering Bright Data scraping job...")
            trigger_response = requests.post(
                trigger_url,
                headers=headers,
                json=payload,
                params=params,
            )
            
            trigger_response.raise_for_status()
            trigger_data = trigger_response.json()
            
            if 'snapshot_id' not in trigger_data:
                raise Exception(f"No snapshot_id in response: {trigger_data}")
                
            snapshot_id = trigger_data['snapshot_id']
            print(f"✅ Scraping job triggered successfully. Snapshot ID: {snapshot_id}")
            
            # Step 2: Poll for results
            return self._poll_for_results(snapshot_id)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error triggering Bright Data job: {str(e)}")
            raise Exception(f"Failed to trigger scraping job: {str(e)}")
    
    def _poll_for_results(self, snapshot_id: str, max_attempts: int = 600) -> List[Dict]:
        """
        Poll Bright Data API for scraping results
        """
        print(f"⏳ Polling for results (max {max_attempts} attempts, 1 second intervals)...")
        
        headers = {
            "Authorization": f"Bearer {self.bright_data_token}"
        }
        
        poll_url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
        
        for attempt in range(max_attempts):
            try:
                if attempt % 10 == 0:  # Progress update every 10 attempts
                    print(f"🔄 Polling attempt {attempt + 1}/{max_attempts}...")
                
                response = requests.get(
                    poll_url,
                    headers=headers,
                    # params={"format": "json"},
                )
                
                response.raise_for_status()
                response_text = response.text.strip()
                if '\n' in response_text and response_text.startswith('{"'):
                    # This is JSONL format - parse each line as separate JSON
                    profiles = []
                    for line in response_text.split('\n'):
                        if line.strip():
                            profiles.append(json.loads(line.strip()))
                    return profiles
                else:
                    # This is regular JSON with status info
                    data = response.json()
                
                status = data.get('status', 'unknown')
                
                if status in ['running', 'building']:
                    print(status)
                    if attempt % 30 == 0:  # Less frequent status updates
                        print(f"⏱️ Job still {status}, continuing to poll...")  
                    time.sleep(1)
                    continue
                
                elif status == 'ready':
                    print(f"🎉 Data ready after {attempt + 1} attempts!")
                    return self.data
                
                elif status == 'failed':
                    error_msg = data.get('error', 'Unknown error')
                    raise Exception(f"Bright Data job failed: {error_msg}")
                
                else:
                    print(f"⚠️ Unexpected status: {status}")
                    return self.data
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Polling error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    continue
                else:
                    raise Exception(f"Polling failed after {max_attempts} attempts")
        
        raise Exception(f"Timeout after {max_attempts} seconds waiting for data")
    
    
    def generate_funny_facts(self, profile_data: Dict) -> List[str]:
        """Generate 3 funny facts about a person using AI21 Jamba LLM"""
        
        # Create a comprehensive prompt with profile information
        profile_text = profile_data
        
        prompt = f"""
        Based on the following LinkedIn profile information, generate exactly 3 funny, witty, and entertaining facts about this person. 
        Make them humorous but respectful - the kind of facts that would make an audience laugh and be amazed. 
        Think like a comedian doing a roast but in a friendly way.

        Profile Information:
        {profile_text}

        Generate 3 funny facts in this exact format:
        1. [First funny fact]
        2. [Second funny fact]  
        3. [Third funny fact]

        Make sure each fact is:
        - Genuinely funny and engaging
        - Based on their profile information
        - Appropriate for a professional audience
        - Would get laughs from a crowd
        """
        
        messages = [
            ChatMessage(role="user", content=prompt)
        ]
        
        print(f"🤖 Generating funny facts for {profile_data.get('name')}...")
        
        try:
            response = self.llm.chat(messages)
            funny_facts_text = str(response)
            print(funny_facts_text)
            # Parse the response to extract the 3 facts
            facts = []
            lines = funny_facts_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                # Handle various formatting patterns including "assistant: 1.", "1.", "**1.**", etc.
                for num in [1, 2, 3]:
                    patterns = [f'{num}.', f'assistant: {num}.', f'**{num}.**']
                    for pattern in patterns:
                        if line.startswith(pattern):
                            # Extract fact text after the pattern
                            fact = line[len(pattern):].strip()
                            
                            # Remove markdown formatting
                            if fact.startswith('**') and fact.endswith('**'):
                                fact = fact[2:-2].strip()
                            
                            # Remove quotes if present
                            if fact.startswith('"') and fact.endswith('"'):
                                fact = fact[1:-1].strip()
                            
                            facts.append(fact)
                            break
            
            # Ensure we have exactly 3 facts
            if len(facts) < 3:
                facts.extend([f"This person is so interesting, even AI needs more time to process their awesomeness!"] * (3 - len(facts)))
            
            return facts[:3]  # Only return first 3 facts
            
        except Exception as e:
            print(f"❌ Error generating funny facts: {str(e)}")
            return [
                "This person is so mysterious, even AI can't figure them out!",
                "Their LinkedIn profile broke our comedy algorithm!",
                "Apparently they're too funny for artificial intelligence!"
            ]
    
    def analyze_profiles(self, linkedin_urls: List[str]) -> Dict:
        """Main function to analyze LinkedIn profiles and generate funny facts"""
        
        if len(linkedin_urls) != 3:
            raise ValueError("Please provide exactly 3 LinkedIn URLs")
        
        print("🚀 Starting LinkedIn Profile Analysis Demo")
        print("=" * 50)
        
        # Step 1: Scrape LinkedIn profiles using Bright Data
        profiles = self.scrape_linkedin_profiles(linkedin_urls)
        
        # Step 2: Generate funny facts for each profile
        results = []
        
        for i, profile in enumerate(profiles):
            print(f"\n📝 Processing Profile {i+1}: {profile['name']}")
            print("-" * 30)
            
            funny_facts = self.generate_funny_facts(profile)
            
            result = {
            "profile_url": profile.get("url", ""),
            "name": profile.get("name", "Unknown"), 
            "headline": profile.get("headline", profile.get("about", "No headline available")[:100] if profile.get("about") else "No headline available"),
            "funny_facts": funny_facts
        }
            
            results.append(result)
            
            # Display results in real-time
            print(f"✨ Funny Facts about {profile['name']}:")
            for j, fact in enumerate(funny_facts, 1):
                print(f"   {j}. {fact}")
        
        print("\n🎉 Analysis Complete!")
        print("=" * 50)
        
        return {
            "status": "success",
            "profiles_analyzed": len(results),
            "results": results
        }


def main():
    """Demo function to test the LinkedIn analyzer"""
    
    # Set your API keys here or in environment variables
    AI21_API_KEY = os.getenv("AI21_API_KEY", "your-ai21-api-key-here")
    BRIGHT_DATA_TOKEN = os.getenv("BRIGHT_DATA_TOKEN", "your-bright-data-token-here")
    DATASET_ID = os.getenv("DATASET_ID", "gd_l1viktl72bvl7bjuj0")  # Default from your example
    
    if AI21_API_KEY == "your-ai21-api-key-here":
        print("⚠️ Please set your AI21_API_KEY environment variable or update the code with your actual API key")
        return
    
    if BRIGHT_DATA_TOKEN == "your-bright-data-token-here":
        print("⚠️ Please set your BRIGHT_DATA_TOKEN environment variable or update the code with your actual token")
        return
    
    # Initialize the analyzer
    analyzer = LinkedInProfileAnalyzer(
        ai21_api_key=AI21_API_KEY,
        bright_data_token=BRIGHT_DATA_TOKEN,
        dataset_id=DATASET_ID
    )
    
    # Sample LinkedIn URLs (replace with actual URLs)
    sample_urls = [
        "https://www.linkedin.com/in/elad-moshe-05a90413/",
        "https://www.linkedin.com/in/jonathan-myrvik-3baa01109",
        "https://www.linkedin.com/in/aviv-tal-75b81/"
    ]

    try:
        # Run the analysis
        results = analyzer.analyze_profiles(sample_urls)
        # scrape_results=analyzer.scrape_linkedin_profiles(sample_urls)
        # Pretty print final results
        print("\n📊 FINAL RESULTS:")
        # print(json.dumps(results, indent=2, ensure_ascii=False))
        print(json.dumps(results, indent=2, ensure_ascii=False))

        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()