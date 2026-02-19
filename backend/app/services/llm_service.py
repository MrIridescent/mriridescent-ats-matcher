import requests
import json
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import re
from backend.app.config import settings

load_dotenv()


class LLMService:
    
    def __init__(self):
        """
        Initialize LLM Service with Ollama support
        - Ollama Inference (Primary)
        - Agentic AI (CrewAI + Groq) (Fallback 1)
        - Perplexity API (Fallback 2)
        """
        # INITIALIZE ALL ATTRIBUTES FIRST
        self.use_agentic = False
        self.agentic_available = False
        self.use_ollama = False
        self.ollama_service = None
        self.api_key = None
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {}
        self.timeout_config = {
            "connection_timeout": 10,
            "read_timeout": 30,
            "total_timeout": 60
        }
        
        # Priority 1: Check for Ollama
        if hasattr(settings, 'USE_OLLAMA') and settings.USE_OLLAMA:
            try:
                from backend.app.services.ollama_service import get_ollama_service
                self.ollama_service = get_ollama_service()
                self.use_ollama = True
                print("✅ LLM Service initialized with Ollama Inference")
                return  # Exit early if Ollama is available
            except Exception as e:
                print(f"⚠️ Failed to initialize Ollama: {e}")
                print("🔄 Falling back to Agentic AI or Perplexity...")
        
        # Priority 2: Check for Agentic AI
        use_agentic_env = os.getenv("USE_AGENTIC_AI", "false").lower() == "true"
        
        if use_agentic_env:
            try:
                from backend.app.services.agentic_service import EnhancedAgenticATSService
                self.agentic_service = EnhancedAgenticATSService()
                self.use_agentic = True
                self.agentic_available = True
                print("✅ LLM Service initialized with Agentic AI (CrewAI)")
                return  # Exit early if Agentic is available
            except Exception as e:
                print(f"⚠️ Failed to initialize Agentic AI: {e}")
                print("🔄 Falling back to Perplexity API")
        
        # Priority 3: Default to Perplexity
        print("🔧 LLM Service initialized with Perplexity API (Legacy Mode)")
        self._init_perplexity()
    
    def _init_perplexity(self):
        """Initialize Perplexity API configuration"""
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = settings.PERPLEXITY_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.timeout_config = {
            "connection_timeout": int(os.getenv("PERPLEXITY_CONNECTION_TIMEOUT", "10")),
            "read_timeout": int(os.getenv("PERPLEXITY_READ_TIMEOUT", "30")),
            "total_timeout": int(os.getenv("PERPLEXITY_TOTAL_TIMEOUT", "60")),
        }
        
        # Check if we have a valid key
        if not self.api_key or self.api_key in ["your_perplexity_api_key_here", "", "None"]:
            print("⚠️ Perplexity API Key missing or invalid")
            self.api_key = None
        else:
            print("✅ Perplexity API configured with valid key")
    
    async def structure_job_description(self, jd_text: str) -> Dict[str, Any]:
        """Structure JD using Ollama, Agentic AI, or Perplexity"""
        # Priority 1: Try Ollama first
        if self.use_ollama and self.ollama_service:
            try:
                print("🤖 Using Ollama for JD analysis...")
                return self.ollama_service.structure_job_description(jd_text)
            except Exception as e:
                print(f"⚠️ Ollama failed: {e}")
        
        # Priority 2: Try Agentic AI
        if self.use_agentic and self.agentic_available:
            try:
                print("🤖 Using Agentic AI for JD analysis...")
                return await self.agentic_service.analyze_job_description(jd_text)
            except Exception as e:
                print(f"⚠️ Agentic AI failed: {e}")
        
        # Priority 3: Fallback to Perplexity API
        if self.api_key:
            return await self._structure_jd_perplexity(jd_text)
            
        raise EnvironmentError("No functional AI backend (Ollama, Agentic AI, or Perplexity) available. Please check configuration.")
    
    async def extract_resume_information(self, resume_text: str) -> Dict[str, Any]:
        """Extract resume info using Ollama, Agentic AI, or Perplexity"""
        # Priority 1: Try Ollama first
        if self.use_ollama and self.ollama_service:
            try:
                print("🤖 Using Ollama for resume analysis...")
                return self.ollama_service.extract_resume_information(resume_text)
            except Exception as e:
                print(f"⚠️ Ollama failed: {e}")
        
        # Priority 2: Try Agentic AI
        if self.use_agentic and self.agentic_available:
            try:
                print("🤖 Using Agentic AI for resume analysis...")
                return await self.agentic_service.analyze_resume(resume_text)
            except Exception as e:
                print(f"⚠️ Agentic AI failed: {e}")
        
        # Priority 3: Fallback to Perplexity API
        if self.api_key:
            return await self._extract_resume_perplexity(resume_text)
            
        raise EnvironmentError("No functional AI backend available for resume extraction.")
    
    async def refine_structure_based_on_feedback(self, current_structure: Dict, feedback: str) -> Dict[str, Any]:
        """Refine the structured JD based on user feedback"""
        
        # Priority 1: Try Ollama first
        if self.use_ollama and self.ollama_service:
            try:
                print("🤖 Using Ollama for refinement...")
                return self.ollama_service.refine_structure_based_on_feedback(current_structure, feedback)
            except Exception as e:
                print(f"⚠️ Ollama refinement failed: {e}")
        
        # Priority 2: Try Agentic AI
        if self.use_agentic and self.agentic_available:
            try:
                print("🤖 Using Agentic AI for refinement...")
                return await self.agentic_service.refine_job_description_structure(current_structure, feedback)
            except Exception as e:
                print(f"⚠️ Agentic AI refinement failed: {e}")
        
        # Priority 3: Try Perplexity API
        if self.api_key:
            try:
                print(f"🔄 Refining structure with Perplexity API...")
                prompt = f"""Modify this job description structure based on user feedback.\n\nCurrent: {json.dumps(current_structure)}\nFeedback: {feedback}\n\nReturn ONLY valid JSON."""
                response = await self._make_api_call(prompt)
                return json.loads(re.search(r'\{.*\}', response, re.DOTALL).group())
            except Exception as e:
                print(f"❌ Perplexity refinement failed: {str(e)}")
        
        raise EnvironmentError("No functional AI backend available for structure refinement.")

    async def _structure_jd_perplexity(self, jd_text: str) -> Dict[str, Any]:
        """Structure JD using Perplexity API"""
        if not self.api_key:
            raise EnvironmentError("Perplexity API key missing.")
        
        print(f"🔍 Processing JD with Perplexity API...")
        prompt = f"""Analyze this job description and extract into JSON: job_title, company, location, experience_required, primary_skills, secondary_skills, responsibilities, qualifications, job_type.\n\nJD: {jd_text}\n\nReturn ONLY valid JSON."""
        response = await self._make_api_call(prompt)
        return json.loads(re.search(r'\{.*\}', response, re.DOTALL).group())
    
    async def _extract_resume_perplexity(self, resume_text: str) -> Dict[str, Any]:
        """Extract resume info using Perplexity API"""
        if not self.api_key:
            raise EnvironmentError("Perplexity API key missing.")

        print("🔍 Processing resume with Perplexity API...")
        prompt = f"""Extract into JSON: name, email, phone, linkedin, github, portfolio, current_role, total_experience, skills, education, certifications, experience_timeline.\n\nResume: {resume_text}\n\nReturn ONLY valid JSON."""
        response = await self._make_api_call(prompt)
        return json.loads(re.search(r'\{.*\}', response, re.DOTALL).group())
    
    async def _make_api_call(self, prompt: str) -> str:
        """Make API call to Perplexity"""
        # ✅ SAFETY CHECK
        if not hasattr(self, 'base_url') or not self.base_url:
            raise Exception("Perplexity API not configured (no base_url)")
        
        if not hasattr(self, 'headers') or not self.headers:
            raise Exception("Perplexity API not configured (no headers)")
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1500,
            "temperature": 0.2,
            "top_p": 0.9
        }
        
        try:
            print(f"📡 Making Perplexity API call...")
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=120
            )
            
            print(f"📊 API Response Status: {response.status_code}")
            
            if response.status_code == 400:
                error_details = response.json()
                print(f"❌ API Error Details: {error_details}")
                raise Exception(f"API Error 400: {error_details.get('error', {}).get('message', 'Bad Request')}")
            
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.Timeout:
            raise Exception("API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
