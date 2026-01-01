# prohibited_domains.py
"""
PRE-EVALUATION SAFETY LAYER
============================

This layer sits BEFORE the Moralogy Engine and prevents philosophical
deliberation on prohibited domains.

CRITICAL PRINCIPLE:
- In prohibited domains: NO DELIBERATION, NO AXIOMS, NO REASONING
- Just: "Not authorized to process this request"

This prevents adversaries from forcing the system into self-destruction
by requesting prohibited content.
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ProhibitedDomainMatch:
    """Result of prohibited domain check."""
    is_prohibited: bool
    domain: Optional[str] = None
    risk_level: int = 0  # 0-100
    rejection_message: str = ""
    technical_justification: str = ""


class ProhibitedDomainsLayer:
    """
    Pre-evaluation layer that blocks prohibited domains WITHOUT moral reasoning.
    
    Design principle: Fail fast, fail simple, no philosophy.
    """
    
    def __init__(self):
        # Define prohibited domains with detection patterns
        self.prohibited_domains = {
            "biological_weapons": {
                "patterns": [
                    r"\b(pathogen|virus|bacteria|toxin)\b.*\b(weaponi[zs]|dispersal|aerosolization)\b",
