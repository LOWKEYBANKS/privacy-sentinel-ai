"""
Privacy Sentinel AI - Legal Frameworks Knowledge Base
Centralized Python definitions for global privacy regulations.
"""

LEGAL_FRAMEWORKS = {
    "GDPR": {
        "full_name": "General Data Protection Regulation (EU)",
        "key_requirements": [
            "Right to be forgotten",
            "Data portability",
            "Explicit consent for sensitive data",
            "72-hour breach notification",
            "Privacy by design"
        ],
        "critical_violations": [
            "Processing data without a legal basis",
            "Lack of clear opt-out for tracking",
            "Indefinite data retention"
        ]
    },
    "CCPA": {
        "full_name": "California Consumer Privacy Act (USA)",
        "key_requirements": [
            "Right to opt-out of data sales",
            "Right to know what data is collected",
            "Non-discrimination for exercising rights",
            "Deletion rights"
        ],
        "critical_violations": [
            "Selling data without a 'Do Not Sell' link",
            "Failing to disclose third-party sharing"
        ]
    },
    "HIPAA": {
        "full_name": "Health Insurance Portability and Accountability Act (USA)",
        "key_requirements": [
            "Protection of PHI (Protected Health Information)",
            "Strict access controls",
            "Audit trails for health data access"
        ],
        "critical_violations": [
            "Unauthorized sharing of medical history",
            "Lack of encryption for health records"
        ]
    },
    "EPRIVACY": {
        "full_name": "ePrivacy Directive (EU Cookie Law)",
        "key_requirements": [
            "Informed consent before setting non-essential cookies",
            "Clear explanation of cookie purposes",
            "Right to withdraw consent at any time"
        ],
        "critical_violations": [
            "Setting tracking cookies without prior consent",
            "Pre-ticked consent boxes",
            "Lack of a 'Reject All' option for cookies"
        ]
    }
}

def get_framework_details(framework_code: str) -> dict:
    """Retrieve details for a specific legal framework."""
    return LEGAL_FRAMEWORKS.get(framework_code.upper(), {})

def get_all_frameworks() -> list:
    """Return a list of all supported framework codes."""
    return list(LEGAL_FRAMEWORKS.keys())
