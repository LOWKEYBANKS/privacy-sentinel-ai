"""
Privacy Sentinel AI - Web Scanner Main
Phase 0: Main entry point for privacy policy web scanning
"""

import asyncio
import argparse
import json
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Corrected imports after directory reorganization
from scrapers.detector import WebPrivacyScanner
from scrapers.content import PrivacyPolicyDetector

async def scan_single_url(url: str, output_format: str = 'json'):
    """Scan single URL for privacy policies"""
    print(f"🔍 Scanning {url}...")
    
    async with WebPrivacyScanner() as scanner:
        result = await scanner.scan_website_privacy(url)
        
        if output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            print_scan_report(result)

def print_scan_report(result: dict):
    """Print formatted scan report"""
    print("\n" + "="*60)
    print(f"🛡️  PRIVACY SENTINEL SCAN REPORT")
    print("="*60)
    print(f"Website: {result['base_url']}")
    print(f"Scan Time: {result['scan_timestamp']}")
    
    policies = result['policies_found']
    print(f"\n📋 Privacy Policies Found: {len(policies)}")
    
    if not policies:
        print("   ❌ No privacy policies detected")
        return
    
    # Print each policy analysis
    for policy_url in policies:
        policy_result = result['scan_results'][policy_url]
        
        print(f"\n🔗 {policy_url}")
        print(f"   Content Length: {policy_result.get('content_length', 0)} chars")
        
        analysis = policy_result.get('analysis', {})
        if 'risk_score' in analysis:
            risk_level = 'HIGH' if analysis['risk_score'] >= 70 else \
                        'MEDIUM' if analysis['risk_score'] >= 40 else 'LOW'
            
            print(f"   🎯 Risk Score: {analysis['risk_score']}/100 ({risk_level})")
            print(f"   📝 Summary: {analysis['summary']}")
            print(f"   ⚠️  Risks: {', '.join(analysis['risks'])}")
            print(f"   💡 Recommendation: {analysis['recommended_action']}")
        else:
            print(f"   ❌ Analysis failed: {analysis.get('error', 'Unknown error')}")
    
    # Print overall assessment
    overall = result.get('overall_assessment', {})
    print(f"\n🎯 Overall Assessment: {overall.get('risk_level', 'Unknown')} Risk")
    print(f"📊 Risk Score: {overall.get('risk_score', 0)}/100")
    print(f"💬 {overall.get('message', 'No message')}")
    print(f"📈 Policies Analyzed: {overall.get('total_policies_analyzed', 0)}")
    print(f"🔢 Total Risks: {overall.get('total_risks_detected', 0)}")
    print(f"🏷️  Unique Risks: {len(overall.get('unique_risks', []))}")

async def batch_scan_urls(urls: list, output_file: str = None):
    """Scan multiple URLs and save results"""
    print(f"🔍 Scanning {len(urls)} websites...")
    
    results = []
    
    async with WebPrivacyScanner() as scanner:
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing {url}")
            
            try:
                result = await scanner.scan_website_privacy(url)
                result['scan_index'] = i
                results.append(result)
                
                # Quick summary
                overall = result.get('overall_assessment', {})
                print(f"✅ {overall.get('risk_level', 'Unknown')} risk - {len(result['policies_found'])} policies")
                
            except Exception as e:
                print(f"❌ Failed to scan {url}: {e}")
                results.append({
                    'base_url': url,
                    'error': str(e),
                    'scan_index': i
                })
    
    # Save results
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to {output_file}")
    
    return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Privacy Sentinel AI Web Scanner')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single URL scan
    single_parser = subparsers.add_parser('scan', help='Scan single URL')
    single_parser.add_argument('url', help='URL to scan')
    single_parser.add_argument('--format', choices=['json', 'report'], default='report',
                              help='Output format')
    
    # Batch scan
    batch_parser = subparsers.add_parser('batch', help='Scan multiple URLs')
    batch_parser.add_argument('--urls', nargs='+', required=True, help='URLs to scan')
    batch_parser.add_argument('--output', help='Output file (JSON)')
    batch_parser.add_argument('--file', help='File with URLs (one per line)')
    
    # Demo scan
    demo_parser = subparsers.add_parser('demo', help='Demo with example websites')
    demo_parser.add_argument('--output', help='Output file (JSON)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'scan':
            asyncio.run(scan_single_url(args.url, args.format))
            
        elif args.command == 'batch':
            urls = args.urls
            if args.file:
                with open(args.file, 'r') as f:
                    urls = [line.strip() for line in f if line.strip()]
            
            asyncio.run(batch_scan_urls(urls, args.output))
            
        elif args.command == 'demo':
            demo_urls = [
                "https://google.com",
                "https://github.com",
                "https://example.com"
            ]
            asyncio.run(batch_scan_urls(demo_urls, args.output))
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⏹️  Scan interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
