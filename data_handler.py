"""
Utility module for handling external API calls
"""

import os
import requests
import aiohttp
import asyncio
from typing import Optional, Dict, Any
import json
from datetime import datetime
import uuid

class MurfTTSHandler:
    """Handler for Murf Text-to-Speech API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MURF_API_KEY")
        self.base_url = "https://api.murf.ai/v1/speech/generate"
        
    async def generate_speech(self, text: str, voice_id: str = "en-US-1", 
                             speed: float = 1.0, pitch: int = 0) -> Optional[bytes]:
        """Generate speech from text using Murf API"""
        if not self.api_key:
            print("❌ Murf API key not configured")
            return None
        
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text[:1000],  # Limit text length
            "voice": voice_id,
            "sampleRate": 24000,
            "format": "mp3",
            "speed": speed,
            "pitch": pitch
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=15
                ) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        return audio_data
                    else:
                        error_text = await response.text()
                        print(f"❌ Murf API Error {response.status}: {error_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ Murf TTS Error: {e}")
            return None

class DeepgramASRHandler:
    """Handler for Deepgram Speech-to-Text API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
        self.base_url = "https://api.deepgram.com/v1/listen"
        
    async def transcribe_audio(self, audio_data: bytes, 
                              model: str = "nova-2") -> Optional[str]:
        """Transcribe audio to text using Deepgram API"""
        if not self.api_key:
            print("❌ Deepgram API key not configured")
            return None
        
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "audio/wav"
        }
        
        params = {
            "model": model,
            "language": "en-US",
            "smart_format": "true",
            "utterances": "true"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}?{self._build_query(params)}",
                    data=audio_data,
                    headers=headers,
                    timeout=15
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'results' in result and 'channels' in result['results']:
                            transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
                            return transcript.strip()
                    else:
                        error_text = await response.text()
                        print(f"❌ Deepgram ASR Error {response.status}: {error_text}")
                        
        except Exception as e:
            print(f"❌ Deepgram ASR Error: {e}")
        
        return None
    
    def _build_query(self, params: Dict) -> str:
        """Build URL query string from parameters"""
        return "&".join([f"{k}={v}" for k, v in params.items()])

class LLMHandler:
    """Handler for LLM APIs (OpenAI, Groq, etc.)"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        
    async def generate_response(self, prompt: str, 
                               system_prompt: str = None,
                               provider: str = "groq") -> Optional[str]:
        """Generate response using LLM"""
        
        if provider == "openai" and self.openai_key:
            return await self._query_openai(prompt, system_prompt)
        elif provider == "groq" and self.groq_key:
            return await self._query_groq(prompt, system_prompt)
        else:
            # Fallback to rule-based response
            return self._generate_rule_based_response(prompt)
    
    async def _query_openai(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """Query OpenAI GPT models"""
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=15
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API Error: {e}")
        
        return None
    
    async def _query_groq(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """Query Groq API (Llama 3 70B)"""
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=15
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq API Error: {e}")
        
        return None
    
    def _generate_rule_based_response(self, prompt: str) -> str:
        """Generate rule-based response when LLM is not available"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm MediVoice AI. I can help you with medicine information, set reminders, and check interactions."
        
        if "thank" in prompt_lower:
            return "You're welcome! Let me know if you need any more help with medicines."
        
        if any(word in prompt_lower for word in ["medicine", "drug", "pill"]):
            return "I can help you find information about medicines. Please tell me the name of the medicine you're interested in."
        
        if "remind" in prompt_lower:
            return "I can help you set reminders for taking medicines. Please tell me the time and what you'd like to be reminded about."
        
        return f"I understand you're asking: '{prompt}'. I'm your medical assistant. I can help with medicine information, reminders, and checking interactions between medicines."