"""
Privacy Sentinel AI - Web Content Scanner
Phase 0: Automated privacy policy detection from websites
"""

import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class WebPrivacyScanner:
    """Automated web privacy policy scanner"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_url = api_base_url
        self.session = None
        self.scanned_urls = {}  # Cache scanned results
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Privacy Sentinel AI Scanner 1.0 (privacy-protection@sentinel.ai)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def scan_website_privacy(self, base_url: str) -> Dict[str, any]:
        """Comprehensive privacy policy scan of a website"""
        result = {
            'base_url': base_url,
            'scan_timestamp': datetime.now().isoformat(),
            'policies_found': [],
            'scan_results': {},
            'errors': []
        }
        
        try:
            # Normalize URL
            normalized_url = self._normalize_url(base_url)
            
            # Step 1: Discover privacy policy URLs
            policy_urls = await self._discover_privacy_policies(normalized_url)
            result['policies_discovered'] = policy_urls
            
            # Step 2: Analyze each discovered policy
            for policy_url in policy_urls:
                try:
                    policy_result = await self._analyze_policy_page(policy_url)
                    result['scan_results'][policy_url] = policy_result
                    result['policies_found'].append(policy_url)
                    
                except Exception as e:
                    result['errors'].append(f"Failed to analyze {policy_url}: {str(e)}")
                    continue
            
            # Step 3: Generate overall risk assessment
            if result['policies_found']:
                result['overall_assessment'] = await self._generate_overall_assessment(result['scan_results'])
            else:
                result['overall_assessment'] = {
                    'risk_level': 'Low',
                    'message': 'No privacy policies found - this site may not collect personal data'
                }
        
        except Exception as e:
            result['errors'].append(f"Scan failed: {str(e)}")
        
        return result

    async def _discover_privacy_policies(self, base_url: str) -> List[str]:
        """Discover privacy policy URLs on a website"""
        policy_urls = set()
        
        try:
            # Fetch main page
            async with self.session.get(base_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find links to privacy policies
                    privacy_links = soup.find_all('a', href=True)
                    
                    for link in privacy_links:
                        href = link['href']
                        text = link.get_text().strip().lower()
                        title = link.get('title', '').lower()
                        
                        if self._is_privacy_link(text, href, title):
                            full_url = urljoin(base_url, href)
                            policy_urls.add(full_url)
            
            # Additional common privacy policy paths to try
            common_paths = [
                '/privacy', '/privacy-policy', '/privacy.html',
                '/privacy.htm', '/privacy.php', '/policies/privacy',
                '/legal/privacy', '/terms/privacy', '/privacy-statement',
                '/privacy-notice', '/data-privacy', '/privacy-policy-center'
            ]
            
            for path in common_paths:
                test_url = urljoin(base_url, path)
                if await self._url_exists(test_url):
                    policy_urls.add(test_url)
        
        except Exception as e:
            print(f"Error discovering policies for {base_url}: {e}")
        
        return list(policy_urls)

    async def _analyze_policy_page(self, policy_url: str) -> Dict[str, any]:
        """Analyze individual privacy policy page"""
        try:
            # Check cache first
            cache_key = f"policy_{policy_url}"
            if cache_key in self.scanned_urls:
                cached_result = self.scanned_urls[cache_key]
                if datetime.fromisoformat(cached_result['timestamp']) > datetime.now() - timedelta(hours=24):
                    return cached_result
            
            # Fetch policy page
            async with self.session.get(policy_url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract main content
                content_text = self._extract_main_content(soup)
                
                # Send to analysis API
                analysis_result = await self._send_to_analysis_api(policy_url, content_text)
                
                # Cache result
                result = {
                    'url': policy_url,
                    'content_length': len(content_text),
                    'last_modified': self._get_last_modified(response),
                    'analysis': analysis_result,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.scanned_urls[cache_key] = result
                return result
        
        except Exception as e:
            return {
                'url': policy_url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _send_to_analysis_api(self, url: str, content: str) -> Dict[str, any]:
        """Send content to analysis API"""
        try:
            async with self.session.post(
                f"{self.api_url}/api/summarize",
                json={
                    "source_url": url,
                    "snippet": content[:16000],  # Limit to API max
                    "timestamp": datetime.now().isoformat()
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        'error': f'API returned {response.status}',
                        'response_text': await response.text()
                    }
        
        except Exception as e:
            return {'error': f'API request failed: {str(e)}'}

    async def _generate_overall_assessment(self, scan_results: Dict) -> Dict[str, any]:
        """Generate overall risk assessment from all scanned policies"""
        if not scan_results:
            return {'risk_level': 'Low', 'message': 'No policies analyzed'}
        
        # Aggregate risks from all policies
        all_risks = set()
        risk_scores = []
        total_risks = 0
        
        for policy_url, result in scan_results.items():
            if 'analysis' in result:
                analysis = result['analysis']
                risk_scores.append(analysis.get('risk_score', 0))
                all_risks.update(analysis.get('risks', []))
                total_risks += len(analysis.get('risks', []))
        
        # Calculate overall risk
        avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        overall_risks = list(all_risks)
        
        if avg_risk_score >= 70:
            risk_level = 'High'
            message = "This website has high privacy concerns across multiple policies"
        elif avg_risk_score >= 40:
            risk_level = 'Medium'
            message = "This website has moderate privacy practices"
        else:
            risk_level = 'Low'
            message = "This website appears to have good privacy practices"
        
        return {
            'risk_level': risk_level,
            'risk_score': round(avg_risk_score, 1),
            'message': message,
            'total_policies_analyzed': len(scan_results),
            'total_risks_detected': total_risks,
            'unique_risks': overall_risks,
            'risk_distribution': self._calculate_risk_distribution(risk_scores)
        }

    def _calculate_risk_distribution(self, risk_scores: List[int]) -> Dict[str, int]:
        """Calculate distribution of risk levels"""
        distribution = {
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for score in risk_scores:
            if score >= 70:
                distribution['High'] += 1
            elif score >= 40:
                distribution['Medium'] += 1
            else:
                distribution['Low'] += 1
        
        return distribution

    def _is_privacy_link(self, text: str, href: str, title: str) -> bool:
        """Check if a link is likely to privacy policy"""
        privacy_indicators = [
            'privacy', 'policy', 'terms', 'conditions',
            'legal', 'agreement', 'notice', 'statement'
        ]
        
        combined_text = f"{text} {href} {title}".lower()
        
        return any(indicator in combined_text for indicator in privacy_indicators)

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from webpage"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Get content from main areas
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content'))
        
        if main_content:
            return self._clean_text(main_content.get_text())
        else:
            # Fallback to body
            return self._clean_text(soup.get_text())[:10000]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]\n', ' ', text)
        return text.strip()

    def _normalize_url(self, url: str) -> str:
        """Normalize URL format"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    async def _url_exists(self, url: str) -> bool:
        """Check if URL exists and is accessible"""
        try:
            async with self.session.head(url, allow_redirects=True) as response:
                return response.status in [200, 301, 302]
        except:
            return False

    def _get_last_modified(self, response) -> Optional[str]:
        """Get last modified date from response headers"""
        return response.headers.get('last-modified', response.headers.get('date'))

# Example usage
async def main():
    """Example usage of WebPrivacyScanner"""
    websites_to_scan = [
        "https://google.com",
        "https://facebook.com",
        "https://github.com"
    ]
    
    async with WebPrivacyScanner() as scanner:
        for website in websites_to_scan:
            print(f"\nScanning {website}...")
            result = await scanner.scan_website_privacy(website)
            
            print(f"Found {len(result['policies_found'])} privacy policies")
            for policy_url in result['policies_found']:
                analysis = result['scan_results'][policy_url].get('analysis', {})
                print(f"  - {policy_url}: Risk {analysis.get('risk_score', 0)}/100")
            
            print(f"Overall assessment: {result['overall_assessment']['risk_level']} level risk")

if __name__ == "__main__":
    asyncio.run(main())
