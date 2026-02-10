"""
Privacy Sentinel AI - Python-based Content Detection
Phase 0: Python implementation for privacy policy detection
Integrates with web scraping and analysis backend
"""

import re
import json
import requests
import trafilatura
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class PrivacyPolicyDetector:
    """Python-based privacy policy detection and analysis"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.detection_keywords = self._load_keywords()
        self.risk_weights = self._load_risk_weights()
        
    def _load_keywords(self) -> Dict[str, List[str]]:
        """Load privacy policy detection keywords"""
        return {
            'privacy': [
                'privacy policy', 'privacy statement', 'data protection',
                'privacy notice', 'data privacy', 'personal information',
                'your privacy', 'how we collect', 'what we collect',
                'our privacy', 'protecting your privacy', 'privacy rights'
            ],
            'consent': [
                'agree', 'accept', 'consent', 'i understand', 'allow',
                'proceed', 'continue', 'yes, i accept', 'agree and continue',
                'i agree to the terms', 'terms and conditions',
                'click to accept', 'by continuing'
            ],
            'data_types': [
                'email', 'location', 'name', 'phone', 'address',
                'credit card', 'payment', 'biometric', 'voice', 'face',
                'fingerprint', 'social security', 'medical information',
                'health data', 'genetic information', 'demographic'
            ],
            'sharing': [
                'third party', 'share with', 'sell your data',
                'partners', 'advertisers', 'analytics', 'data brokers',
                'affiliates', 'service providers', 'disclose'
            ],
            'tracking': [
                'cookies', 'tracking', 'analytics', 'monitoring',
                'web beacons', 'pixel', 'fingerprinting', 'advertising',
                'personalization', 'targeting'
            ]
        }
    
    def _load_risk_weights(self) -> Dict[str, int]:
        """Load risk assessment weights"""
        return {
            'biometric': 25,
            'location': 20,
            'voice': 18,
            'camera': 18,
            'phone': 15,
            'address': 12,
            'email': 10,
            'cookies': 8,
            'analytics': 12,
            'sharing': 20
        }

    def extract_content_from_url(self, url: str) -> Dict[str, any]:
        """Extract and analyze content from a URL using Trafilatura and BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Privacy Sentinel AI 1.0 (privacy-protection@sentinel.ai)'
            }
            
            # Use trafilatura for high-quality text extraction
            downloaded = trafilatura.fetch_url(url)
            trafilatura_text = trafilatura.extract(downloaded) if downloaded else None
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant sections using existing logic
            privacy_sections = self._extract_privacy_sections(soup)
            
            return {
                'url': url,
                'title': self._extract_title(soup),
                'privacy_policies': privacy_sections,
                'full_text': (trafilatura_text or self._clean_text(soup.get_text()))[:16000],
                'detected_elements': self._detect_policy_elements(soup),
                'extraction_time': datetime.now().isoformat(),
                'method': 'trafilatura+bs4'
            }
            
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return {'error': str(e)}

    def _extract_privacy_sections(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract sections most likely to contain privacy policies"""
        sections = []
        
        # Look for privacy-related headings and their content
        privacy_selectors = [
            'h1, h2, h3',  # Headings
            "[class*='privacy']", "[class*='policy']",
            "[id*='privacy']", "[id*='policy']",
            ".legal", ".terms", ".conditions",
            "section", "article"
        ]
        
        for selector in privacy_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if self._is_privacy_related(text) and len(text) > 100:
                    sections.append({
                        'tag': element.name,
                        'text': text,
                        'score': self._calculate_privacy_score(text),
                        'classes': element.get('class', []),
                        'id': element.get('id', '')
                    })
        
        # Sort by score and take top sections
        return sorted(sections, key=lambda x: x['score'], reverse=True)[:5]

    def _is_privacy_related(self, text: str) -> bool:
        """Check if text is likely privacy-related"""
        text_lower = text.lower()
        
        # Calculate score based on keyword matches
        score = 0
        for category, keywords in self.detection_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    
        return score >= 3  # Minimum threshold

    def _calculate_privacy_score(self, text: str) -> int:
        """Calculate privacy relevance score"""
        score = 0
        text_lower = text.lower()
        
        for category, keywords in self.detection_keywords.items():
            category_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    category_score += 1
            
            # Add category bonus
            if category_score > 0:
                score += category_score
                
        # Bonus for specific phrases
        bonus_phrases = [
            'we collect', 'how we use', 'we share',
            'your personal', 'data protection', 'privacy policy',
            'third parties', 'your rights'
        ]
        
        for phrase in bonus_phrases:
            if phrase in text_lower:
                score += 2
                
        return score

    def _detect_policy_elements(self, soup: BeautifulSoup) -> List[Dict]:
        """Detect policy-related UI elements"""
        elements = []
        
        # Look for checkboxes, radio buttons, buttons
        form_elements = soup.find_all(['input', 'button', 'select', 'textarea'])
        
        for element in form_elements:
            element_info = {
                'tag': element.name,
                'type': element.get('type', ''),
                'id': element.get('id', ''),
                'class': element.get('class', []),
                'text': element.get_text().strip(),
                'is_consent_related': self._is_consent_element(element)
            }
            
            if element_info['text'] and element_info['is_consent_related']:
                elements.append(element_info)
        
        return elements

    def _is_consent_element(self, element) -> bool:
        """Check if element is likely a consent/accept mechanism"""
        text = element.get_text().lower()
        
        consent_keywords = self.detection_keywords['consent'] + self.detection_keywords['privacy']
        return any(keyword in text for keyword in consent_keywords)

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Try h1 if title not found
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
            
        return 'Unknown'

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
        return text.strip()

    async def analyze_privacy_policy(self, url: str) -> Dict[str, any]:
        """Complete privacy policy analysis workflow"""
        print(f"Analyzing privacy policy for: {url}")
        
        # Step 1: Extract content
        content = self.extract_content_from_url(url)
        if 'error' in content:
            return content
        
        # Step 2: Prepare analysis data
        policy_text = content['full_text']
        
        # Step 3: Send to API for analysis
        try:
            analysis_response = requests.post(
                f"{self.api_base_url}/api/summarize",
                json={
                    "source_url": url,
                    "snippet": policy_text,
                    "timestamp": datetime.now().isoformat()
                },
                timeout=30
            )
            
            if analysis_response.status_code == 200:
                analysis = analysis_response.json()
                
                # Enhance analysis with additional metadata
                enhanced_analysis = {
                    **analysis,
                    'url_content': content,
                    'detection_method': 'python_content_extractor',
                    'privacy_sections_found': len(content['privacy_policies']),
                    'ui_elements_detected': len(content['detected_elements']),
                    'confidence_score': self._calculate_confidence(content)
                }
                
                return enhanced_analysis
            else:
                return {
                    'error': f'API request failed: {analysis_response.status_code}',
                    'content': content  # Include extracted content for fallback
                }
                
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'content': content
            }

    def _calculate_confidence(self, content: Dict) -> float:
        """Calculate confidence score for the analysis"""
        if 'error' in content:
            return 0.0
            
        confidence = 0.0
        
        # Boost for found privacy sections
        if content['privacy_policies']:
            confidence += min(len(content['privacy_policies']) * 0.2, 0.4)
            
        # Boost for detected UI elements
        if content['detected_elements']:
            confidence += min(len(content['detected_elements']) * 0.1, 0.3)
            
        # Boost for sufficient text length
        if content['full_text'] and len(content['full_text']) > 500:
            confidence += 0.3
            
        return min(confidence, 1.0)

    def batch_analyze_urls(self, urls: List[str]) -> Dict[str, any]:
        """Analyze multiple URLs in batch"""
        results = {}
        
        for url in urls:
            try:
                print(f"Batch analyzing: {url}")
                results[url] = self.analyze_privacy_policy(url)
            except Exception as e:
                results[url] = {'error': str(e)}
                
        return results

    def generate_analysis_report(self, analysis: Dict) -> str:
        """Generate human-readable analysis report"""
        if 'error' in analysis:
            return f"Analysis failed: {analysis['error']}"
        
        report = f"""
=== PRIVACY SENTINEL ANALYSIS REPORT ===
URL: {analysis.get('source_url', 'Unknown')}
Risk Score: {analysis.get('risk_score', 0)}/100
Risk Level: {'HIGH' if analysis.get('risk_score', 0) >= 70 else 'MEDIUM' if analysis.get('risk_score', 0) >= 40 else 'LOW'}

SUMMARY:
{analysis.get('summary', 'No summary available')}

DETECTED RISKS:
{', '.join(analysis.get('risks', []))}

RECOMMENDED ACTION:
{analysis.get('recommended_action', 'No recommendation available')}

TECHNICAL DETAILS:
- Processing Time: {analysis.get('processing_time_ms', 0)}ms
- Analysis Hash: {analysis.get('hash_id', 'Unknown')}
- Confidence Score: {analysis.get('confidence_score', 0):.2f}
- Privacy Sections Found: {analysis.get('privacy_sections_found', 0)}
"""
        
        return report

# Example usage
if __name__ == "__main__":
    detector = PrivacyPolicyDetector()
    
    # Analyze single URL
    test_urls = [
        "https://example.com/privacy",
        "https://google.com/policies/privacy/"
    ]
    
    for url in test_urls:
        result = detector.analyze_privacy_policy(url)
        print(detector.generate_analysis_report(result))
        print("=" * 50)
