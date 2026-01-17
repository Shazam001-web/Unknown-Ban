#!/usr/bin/env python3
"""
WhatsApp Reporting Tool v3.0 - Ultimate Pro Edition
Author: Dev Shazam 
Features: Real number verification, mass reporting, email rotation, proxy support
"""

import os
import sys
import time
import random
import json
import smtplib
import ssl
import threading
import hashlib
import re
import itertools
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

# ===== Crypto Lord Password =====

TOOL_USERNAME = "Meta"
TOOL_PASSWORD = "admin"

# ===== GMAIL ACCOUNTS =====
GMAIL_ACCOUNTS = [
    {"email": "managerhimself032@gmail.com", "password": "inagtgypnpyweleu"},
    {"email": "arsheeqarsheeqq@gmail.com", "password": "pkkqfactxwkpvzgc"},
    {"email": "unknownhimself6@gmail.com", "password": "uupfjdufriwrdgop"},
    {"email": "cryptolord25ss@gmail.com", "password": "lczszqjxovvbuxco"},
   {"email": "unknownhimself6@gmail.com", "password": "uupfjdufriwrdgop"},
   {"email": "brandhaseeb26@gmail.com", "password": "cjjyjeyqbjibdheq"},
   {"email": "jackiechanski55@gmail", "password": "epzezxtxvrkaaged"},
   {"email": "calebaboagye509@gmail.com", "password": "wwtaxbgecnvfomzd"},
   {"email": "basitgaming190k@gmail.com", "password": "myeghlgusewjzgul"},
   {"email": "ferryxmartins@gmail.com", "password": "rvcrntktvmwqmxgi"},
   {"email": "brandhaseeb26@gmail.com", "password": "cjjyjeyqbjibdheq"},
]

# ===== PROXY CONFIGURATION =====
PROXY_LIST = []
try:
    with open('proxies.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '://' not in line:
                    line = f"http://{line}"
                PROXY_LIST.append(line)
    print(Fore.GREEN + f"✅ 𝗟𝗼𝗮𝗱𝗲𝗱 {len(PROXY_LIST)} 𝗽𝗿𝗼𝘅𝗶𝗲𝘀")
except FileNotFoundError:
    print(Fore.YELLOW + "⚠️ proxies.txt 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱")

# ===== WHATSAPP SUPPORT EMAILS =====
WHATSAPP_EMAILS = [
    "support@support.whatsapp.com",
    "support@support.whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com", 
    "android@support.whatsapp.com",
    "support@support.whatsapp.com",
    "support@support.whatsapp.com", 
    "support@support.whatsapp.com"
]

# ===== WHATSAPP API CREDENTIALS =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== SMTP CONFIGURATION =====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_SSL_PORT = 465

# ===== GLOBAL VARIABLES =====
sent_counter = 0
failed_counter = 0
current_account_index = 0
current_proxy_index = 0
lock = threading.Lock()

# ===== UTILITY FUNCTIONS =====
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def get_next_account():
    """Rotate through Gmail accounts"""
    global current_account_index
    with lock:
        account = GMAIL_ACCOUNTS[current_account_index]
        current_account_index = (current_account_index + 1) % len(GMAIL_ACCOUNTS)
        return account

def get_next_proxy():
    """Rotate through proxy list"""
    global current_proxy_index
    if not PROXY_LIST:
        return None
    with lock:
        proxy = PROXY_LIST[current_proxy_index]
        current_proxy_index = (current_proxy_index + 1) % len(PROXY_LIST)
        return proxy

def validate_phone_number(phone):
    """Validate phone number format"""
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))

def test_proxy(proxy_url):
    """Test if a proxy is working"""
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        if response.status_code == 200:
            return True, response.json().get("origin", "Unknown")
        return False, "Failed"
    except Exception as e:
        return False, str(e)

# ===== REAL WHATSAPP NUMBER CHECKING =====
def check_whatsapp_number(phone):
    """Real WhatsApp number checking using Facebook Graph API"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }

    proxy = get_next_proxy()
    
    try:
        print(Fore.CYAN + f"\n🔍 Checking WhatsApp status for {phone}")
        
        if proxy:
            print(Fore.CYAN + f"   Using proxy: {proxy}")
            proxies = {"http": proxy, "https": proxy}
            response = requests.post(url, headers=headers, json=payload, timeout=15, proxies=proxies)
        else:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
    except Exception as e:
        print(Fore.RED + f"\n⚠️ Request failed: {e}")
        if proxy:
            print(Fore.YELLOW + f"   Proxy: {proxy} may be dead")
        return

    if response.status_code == 200:
        data = response.json()
        contacts = data.get("contacts", [])
        
        if contacts:
            for contact in contacts:
                status = contact.get("status", "unknown")
                wa_id = contact.get("wa_id", "N/A")
                
                if status == "valid":
                    print(Fore.GREEN + f"\n✅ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} is 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
                    print(Fore.CYAN + f"   𝗦𝘁𝗮𝘁𝘂𝘀: 𝗔𝗰𝘁𝗶𝘃𝗲 𝗮𝗻𝗱 𝘃𝗮𝗹𝗶𝗱")
                elif status == "invalid":
                    print(Fore.RED + f"\n❌ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} 𝗶𝘀 𝗡𝗢𝗧 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
                else:
                    print(Fore.YELLOW + f"\n⚠️ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} - 𝗦𝘁𝗮𝘁𝘂𝘀: {status}")
                
                # Additional info
                info = {
                    "Input": phone,
                    "WhatsApp ID": wa_id,
                    "Status": status.upper(),
                    "Checked At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Via Proxy": proxy if proxy else "Direct"
                }
                
                for key, value in info.items():
                    print(Fore.WHITE + f"   {key}: {value}")
        else:
            print(Fore.RED + f"\n❌ 𝗡𝘂𝗺𝗯𝗲𝗿 {phone} 𝗶𝘀 𝗻𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
            
    else:
        print(Fore.RED + f"\n⚠️ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿: 𝗦𝘁𝗮𝘁𝘂𝘀 {response.status_code}")
        try:
            error_data = response.json()
            print(Fore.YELLOW + f"   Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        except:
            print(Fore.YELLOW + f"   𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {response.text[:200]}")

# ===== ENHANCED EMAIL SENDING WITH ROTATION =====
def send_whatsapp_report(subject, body, target_email, report_type="ban"):
    """Send report to WhatsApp with rotation and tracking"""
    global sent_counter, failed_counter
    
    account = get_next_account()
    sender_email = account["email"]
    sender_password = account["password"]
    
    try:
        # Create message with proper headers
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"WhatsApp User <{sender_email}>"
        msg['To'] = target_email
        msg['X-Priority'] = '1'
        msg['Importance'] = 'high'
        msg['X-Mailer'] = 'Microsoft Outlook 16.0'
        
        # Generate unique message ID
        msg_id = f"{int(time.time())}.{random.randint(1000, 9999)}@gmail.com"
        msg['Message-ID'] = f"<{msg_id}>"
        
        # Create both text and HTML versions
        text_part = MIMEText(body, 'plain')
        
        # Enhanced HTML version
        html_part = MIMEText(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; background: #f5f5f5; }}
                .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px auto; }}
                .header {{ background: linear-gradient(135deg, #25D366, #128C7E); padding: 20px; border-radius: 10px 10px 0 0; color: white; text-align: center; }}
                .content {{ padding: 25px; }}
                .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; }}
                .urgent {{ color: #d32f2f; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>WhatsApp Support Request</h2>
                </div>
                <div class="content">
                    {body.replace(chr(10), '<br>')}
                    <div class="footer">
                        <p>Request ID: {random.randint(100000, 999999)}</p>
                        <p>Type: {report_type.upper()} | Sender: {sender_email}</p>
                        <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email with fallback mechanism
        try:
            # Try STARTTLS first
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            with lock:
                sent_counter += 1
            
            return True, "Success", sender_email
            
        except Exception as e:
            # Fallback to SSL
            try:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context, timeout=30)
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                with lock:
                    sent_counter += 1
                
                return True, "Success (SSL)", sender_email
            except Exception as ssl_error:
                raise ssl_error
        
    except Exception as e:
        error_msg = str(e)
        with lock:
            failed_counter += 1
        
        return False, error_msg, sender_email

def mass_report_attack(target_number, report_type, report_count=50):
    """Execute mass reporting attack with complete rotation"""
    global sent_counter, failed_counter
    sent_counter = 0
    failed_counter = 0
    
    # Validate count (10-50)
    report_count = max(10, min(50, report_count))
    
    # Calculate optimal distribution
    senders = len(GMAIL_ACCOUNTS)
    targets = len(WHATSAPP_EMAILS)
    total_pairs = senders * targets
    
    # Generate all possible sender-target combinations
    all_pairs = []
    for sender in GMAIL_ACCOUNTS:
        for target in WHATSAPP_EMAILS:
            all_pairs.append((sender, target))
    
    # Randomize the pairs and take required number
    random.shuffle(all_pairs)
    selected_pairs = all_pairs[:report_count]
    
    print(Fore.CYAN + f"\n🚀 𝗜𝗻𝗶𝘁𝗶𝗮𝗹𝗶𝘇𝗶𝗻𝗴 {report_type.upper()} 𝗮𝘁𝘁𝗮𝗰𝗸 𝗼𝗻 {target_number}")
    print(Fore.CYAN + f"📊 𝗥𝗲𝗽𝗼𝗿𝘁𝘀 𝘁𝗼 𝘀𝗲𝗻𝗱: {report_count}")
    print(Fore.CYAN + f"📧 𝗨𝘀𝗶𝗻𝗴 {senders} 𝘀𝗲𝗻𝗱𝗲𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁𝘀")
    print(Fore.CYAN + f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁𝗶𝗻𝗴 {targets} 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗲𝗺𝗮𝗶𝗹𝘀")
    print(Fore.YELLOW + "="*60)
    
    # Generate report content based on type
    if report_type == "ban":
        subject = f"URGENT BAN REQUEST: {target_number} - HARASSMENT & SPAM"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal cybercrime complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported account is actively engaging in behavior consistent with organized cybercrime operations. The activities observed are intentional, repeated, and designed to deceive, exploit, and harm users of the WhatsApp platform.
Details of Criminal Activity:
The account has sent unsolicited messages containing fraudulent content, phishing links, and malicious URLs intended to steal personal data, login credentials, verification codes, and financial information from victims. These links are structured to impersonate legitimate services and mislead users into providing sensitive information.
In addition, the account distributes explicit sexual video links as spam without user consent. This content is used as a lure to manipulate recipients into clicking malicious links or engaging further, which is a known tactic in online exploitation and account hijacking attempts.
The sender has also attempted to pressure and manipulate recipients into actions that could lead to unauthorized access to their WhatsApp accounts, including social engineering techniques commonly associated with hacking attempts.
Pattern of Abuse:
The behavior is persistent and continues even after users ignore or disengage, indicating deliberate malicious intent rather than accidental or isolated misuse. This pattern strongly suggests systematic abuse of the platform.
Risk Assessment:
This activity poses a serious risk to user safety, privacy, and financial security. It also represents a potential threat to minors and vulnerable users due to the distribution of explicit content and deceptive messaging tactics.
Request for Immediate Action:
I respectfully request an urgent manual investigation into this account by the WhatsApp Trust and Safety and Cybercrime Review teams. Given the severity, repetition, and criminal nature of these actions, I request appropriate enforcement measures, including account suspension or permanent removal, to prevent further harm.
Thank you for your attention to this serious matter.
Sincerely,
A Concerned WhatsApp User
"""
    elif report_type == "fraud":
        subject = f"FRAUD ALERT: {target_number} - FINANCIAL SCAM"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal cybercrime complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported account is actively engaging in behavior consistent with organized cybercrime operations. The activities observed are intentional, repeated, and designed to deceive, exploit, and harm users of the WhatsApp platform.
Details of Criminal Activity:
The account has sent unsolicited messages containing fraudulent content, phishing links, and malicious URLs intended to steal personal data, login credentials, verification codes, and financial information from victims. These links are structured to impersonate legitimate services and mislead users into providing sensitive information.
In addition, the account distributes explicit sexual video links as spam without user consent. This content is used as a lure to manipulate recipients into clicking malicious links or engaging further, which is a known tactic in online exploitation and account hijacking attempts.
The sender has also attempted to pressure and manipulate recipients into actions that could lead to unauthorized access to their WhatsApp accounts, including social engineering techniques commonly associated with hacking attempts.
Pattern of Abuse:
The behavior is persistent and continues even after users ignore or disengage, indicating deliberate malicious intent rather than accidental or isolated misuse. This pattern strongly suggests systematic abuse of the platform.
Risk Assessment:
This activity poses a serious risk to user safety, privacy, and financial security. It also represents a potential threat to minors and vulnerable users due to the distribution of explicit content and deceptive messaging tactics.
Request for Immediate Action:
I respectfully request an urgent manual investigation into this account by the WhatsApp Trust and Safety and Cybercrime Review teams. Given the severity, repetition, and criminal nature of these actions, I request appropriate enforcement measures, including account suspension or permanent removal, to prevent further harm.
Thank you for your attention to this serious matter.
Sincerely,
A Concerned WhatsApp User
"""
    elif report_type == "unban":
        subject = f"APPEAL: Wrongful Ban - {target_number}"
        body = f"""Request for Review and Reinstatement of My WhatsApp Account

Dear WhatsApp Support Team,

I am writing to respectfully request a thorough review of my WhatsApp account associated with the phone number {target_number}, which has recently been banned. I understand that WhatsApp enforces strict policies to maintain a safe and trusted platform, and I fully support these efforts.
However, I strongly believe that my account was banned in error, as I have never knowingly violated WhatsApp's Terms of Service or Community Guidelines. I use WhatsApp primarily for personal communication with family, friends, and professional contacts, and I have always acted responsibly on the platform.
If any of my recent activity was flagged unintentionally or misunderstood, I sincerely apologize. It was never my intention to misuse WhatsApp in any way. I am more than willing to cooperate fully and adjust my usage to comply strictly with all policies going forward.
I kindly request that you review my account again and consider reinstating it. Losing access has significantly affected my daily communication, and I assure you that this situation will not be repeated.
I truly regret any action—intentional or unintentional—that may have led to this situation.
If any of my behavior violated WhatsApp's policies, I take full responsibility and sincerely apologize. I now understand the importance of strictly following all guidelines to protect the integrity of the platform and the safety of its users.
WhatsApp plays a critical role in my daily life, including communication with family members, work-related coordination, and important personal matters. The loss of access has been extremely difficult for me.
I respectfully request one opportunity to correct my mistake. I assure you that I will be extremely careful moving forward and will fully comply with all WhatsApp rules without exception.
"""
    elif report_type == "nuclear":
        subject = f"EMERGENCY SECURITY THREAT: {target_number} - TERRORIST ACTIVITIES"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal cybercrime complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported account is actively engaging in behavior consistent with organized cybercrime operations. The activities observed are intentional, repeated, and designed to deceive, exploit, and harm users of the WhatsApp platform.
Details of Criminal Activity:
The account has sent unsolicited messages containing fraudulent content, phishing links, and malicious URLs intended to steal personal data, login credentials, verification codes, and financial information from victims. These links are structured to impersonate legitimate services and mislead users into providing sensitive information.
In addition, the account distributes explicit sexual video links as spam without user consent. This content is used as a lure to manipulate recipients into clicking malicious links or engaging further, which is a known tactic in online exploitation and account hijacking attempts.
The sender has also attempted to pressure and manipulate recipients into actions that could lead to unauthorized access to their WhatsApp accounts, including social engineering techniques commonly associated with hacking attempts.
Pattern of Abuse:
The behavior is persistent and continues even after users ignore or disengage, indicating deliberate malicious intent rather than accidental or isolated misuse. This pattern strongly suggests systematic abuse of the platform.
Risk Assessment:
This activity poses a serious risk to user safety, privacy, and financial security. It also represents a potential threat to minors and vulnerable users due to the distribution of explicit content and deceptive messaging tactics.
Request for Immediate Action:
I respectfully request an urgent manual investigation into this account by the WhatsApp Trust and Safety and Cybercrime Review teams. Given the severity, repetition, and criminal nature of these actions, I request appropriate enforcement measures, including account suspension or permanent removal, to prevent further harm.
Thank you for your attention to this serious matter.
Sincerely,
A Concerned WhatsApp User
"""
    
    start_time = time.time()
    
    # Send reports with threading
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        
        for i, (sender_account, target_email) in enumerate(selected_pairs):
            # Customize subject for each email
            custom_subject = f"{subject} [Report:{i+1}]"
            
            futures.append(
                executor.submit(
                    send_custom_report,
                    custom_subject,
                    body,
                    target_email,
                    report_type,
                    sender_account
                )
            )
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        
        # Process results
        completed = 0
        for future in as_completed(futures):
            completed += 1
            try:
                success, message, sender = future.result(timeout=60)
                if success:
                    print(Fore.GREEN + f"  [{completed}/{report_count}] ✓ {sender} → {target_email[:30]}...")
                else:
                    print(Fore.RED + f"  [{completed}/{report_count}] ✗ {sender}: {message[:50]}...")
            except Exception as e:
                print(Fore.RED + f"  [{completed}/{report_count}] ✗ Error: {str(e)[:50]}...")
    
    end_time = time.time()
    duration = end_time - start_time
    
    return sent_counter, failed_counter, duration

def send_custom_report(subject, body, target_email, report_type, sender_account):
    """Send report with specific sender account"""
    global sent_counter, failed_counter
    
    sender_email = sender_account["email"]
    sender_password = sender_account["password"]
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"WhatsApp Report <{sender_email}>"
        msg['To'] = target_email
        msg['X-Priority'] = '1'
        
        # Add text and HTML parts
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Send email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        except:
            # SSL fallback
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context, timeout=30)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
        
        with lock:
            sent_counter += 1
        
        return True, "Success", sender_email
        
    except Exception as e:
        with lock:
            failed_counter += 1
        return False, str(e), sender_email

# ===== LOGIN SYSTEM =====
def authenticate():
    """User authentication with style"""
    while True:
        clear()
        
        # Display banner
        banner_color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA])
        print(banner_color + "📲 Meta Ban Tool")
        
        print(banner_color + r'''
⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟
''')

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(Fore.YELLOW + f"📧 𝗔𝗰𝗰𝗼𝘂𝗻𝘁𝘀: {len(GMAIL_ACCOUNTS)}")
        print(Fore.YELLOW + f"🔄 𝗣𝗿𝗼𝘅𝗶𝗲𝘀 𝗟𝗼𝗮𝗱𝗲𝗱: {len(PROXY_LIST)}")
        print(Fore.YELLOW + f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁 𝗘𝗺𝗮𝗶𝗹𝘀: {len(WHATSAPP_EMAILS)}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        username = input("👤 𝗘𝗻𝘁𝗲𝗿 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: ")
        password = input("🔒 𝗘𝗻𝘁𝗲𝗿 𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱: ")

        if username == TOOL_USERNAME and password == TOOL_PASSWORD:
            print(Fore.GREEN + "\n✅ 𝗔𝘂𝘁𝗵𝗲𝗻𝘁𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!")
            print(Fore.CYAN + "⚡𝗠𝗼𝗱𝗲 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱")
            print(Fore.YELLOW + "⚠️ 𝗘𝗻𝘀𝘂𝗿𝗲 '𝗟𝗲𝘀𝘀 𝘀𝗲𝗰𝘂𝗿𝗲 𝗮𝗽𝗽 𝗮𝗰𝗰𝗲𝘀𝘀' 𝗶𝘀 𝗢𝗡")
            time.sleep(2)
            return True
        else:
            print(Fore.RED + "\n❌ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗱𝗲𝗻𝗶𝗲𝗱!")
            time.sleep(2)

# ===== MAIN MENU =====
def main_menu():
    """Display main menu"""
    while True:
        clear()
        
        menu_color = random.choice([Fore.BLUE, Fore.YELLOW, Fore.CYAN])
        print(menu_color + "🛠️ Meta Ban Tool")
        
        print(menu_color + r'''
⠀⠀⠀    ⣠⣶⣶⣶⣶
⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣧
⠀⠀⠀⠀⣼⣿⣿⣿⡿⣿⣿⣆⠀⠀⠀⠀⠀⠀⣠⣴⣶⣤⡀⠀
⠀⠀⠀⢰⣿⣿⣿⣿⠃⠈⢻⣿⣦⠀⠀⠀⠀⣸⣿⣿⣿⣿⣷⠀
⠀⠀⠀⠘⣿⣿⣿⡏⣴⣿⣷⣝⢿⣷⢀⠀⢀⣿⣿⣿⣿⡿⠋⠀
⠀⠀⠀⠀⢿⣿⣿⡇⢻⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣇⢸⣿⣿⡟⠙⠛⠻⣿⣿⣿⣿⡇⠀⠀⠀⠀
⣴⣿⣿⣿⣿⣿⣿⣿⣠⣿⣿⡇⠀⠀⠀⠉⠛⣽⣿⣇⣀⣀⣀⠀
⠙⠻⠿⠿⠿⠿⠿⠟⠿⠿⠿⠇⠀⠀⠀⠀⠀⠻⠿⠿⠛⠛⠛
''')
        
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(Fore.CYAN + " [𝟭] 📩 𝗧𝗲𝗺𝗽𝗼𝗿𝗮𝗿𝘆 𝗨𝗻𝗯𝗮𝗻 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 (𝟭𝟬-𝟱𝟬)")
        print(Fore.CYAN + " [𝟮] 🚫 𝗣𝗲𝗿𝗺𝗮𝗻𝗲𝗻𝘁 𝗨𝗻𝗯𝗮𝗻 𝗕𝗹𝗮𝘀𝘁 (𝟭𝟬-𝟱𝟬)")
        print(Fore.CYAN + " [𝟯] 🔍 𝗖𝗵𝗲𝗰𝗸 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝗡𝘂𝗺𝗯𝗲𝗿 (𝗥𝗘𝗔𝗟)")
        print(Fore.CYAN + " [𝟰] ⚠️  𝗠𝗮𝘀𝘀 𝗙𝗿𝗮𝘂𝗱 𝗥𝗲𝗽𝗼𝗿𝘁 (𝟭𝟬-𝟱𝟬)")
        print(Fore.CYAN + " [𝟱] 💀 𝗡𝘂𝗰𝗹𝗲𝗮𝗿 𝗠𝗮𝘀𝘀 𝗥𝗲𝗽𝗼𝗿𝘁 (𝟭𝟬-𝟱𝟬)")
        print(Fore.CYAN + " [𝟲] ⚙️  𝗧𝗲𝘀𝘁 𝗦𝘆𝘀𝘁𝗲𝗺")
        print(Fore.CYAN + " [𝟬] ❌ 𝗘𝘅𝗶𝘁 𝗦𝘆𝘀𝘁𝗲𝗺")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        choice = input(Fore.CYAN + "\n🎯 𝗦𝗲𝗹𝗲𝗰𝘁 𝗮𝗻 𝗼𝗽𝘁𝗶𝗼𝗻 𝗧𝗼 𝘀𝘁𝗿𝗶𝗸𝗲::: ").strip()

        if choice == "1":
            ban_unban_menu("Temporary", "unban")
        elif choice == "2":
            ban_unban_menu("Permanent", "unban")
        elif choice == "3":
            check_number_menu()
        elif choice == "4":
            fraud_menu()
        elif choice == "5":
            nuclear_menu()
        elif choice == "6":
            system_test_menu()
        elif choice == "0":
            exit_tool()
        else:
            print(Fore.RED + "\n❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗼𝗽𝘁𝗶𝗼𝗻")
            time.sleep(1)

def ban_unban_menu(action_type, report_type):
    """Handle ban/unban operations"""
    clear()
    print(Fore.GREEN + f"\n📨 {action_type.upper()} {report_type.upper()} 𝗥𝗘𝗤𝗨𝗘𝗦𝗧\n")
    
    # Get target number
    while True:
        phone = input(Fore.CYAN + "📞 𝗧𝗮𝗿𝗴𝗲𝘁 𝗻𝘂𝗺𝗯𝗲𝗿 (+𝟮𝟯𝟰𝘅𝘅𝘅𝘅...): " + Fore.WHITE).strip()
        if validate_phone_number(phone):
            break
        print(Fore.RED + "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗳𝗼𝗿𝗺𝗮𝘁. 𝗨𝘀𝗲 \n\n+𝟮𝟯𝟰𝘅𝘅𝘅𝘅𝘅𝘅")
    
    # Get report count (10-50)
    while True:
        try:
            count_input = input(Fore.CYAN + "💣 𝗡𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝗿𝗲𝗽𝗼𝗿𝘁𝘀 (𝟭𝟬-𝟱𝟬): " + Fore.WHITE).strip()
            if count_input:
                count = int(count_input)
                if 10 <= count <= 50:
                    break
                else:
                    print(Fore.RED + "❌ 𝗠𝘂𝘀𝘁 𝗯𝗲 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝟭𝟬 𝗮𝗻𝗱 𝟱𝟬")
            else:
                count = 30
                print(Fore.YELLOW + f"   𝗨𝘀𝗶𝗻𝗴 𝗱𝗲𝗳𝗮𝘂𝗹𝘁: {count}")
                break
        except ValueError:
            print(Fore.RED + "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗻𝘂𝗺𝗯𝗲𝗿")
    
    # Confirm
    print(Fore.YELLOW + f"\n⚠️  𝗧𝗮𝗿𝗴𝗲𝘁: {phone}")
    print(Fore.YELLOW + f"⚠️  𝗥𝗲𝗽𝗼𝗿𝘁𝘀: {count}")
    print(Fore.YELLOW + f"⚠️  𝗧𝘆𝗽𝗲: {action_type} {report_type}")
    
    confirm = input(Fore.RED + f"\n🚀 𝗟𝗔𝗨𝗡𝗖𝗛 {action_type.upper()} {report_type.upper()} 𝗔𝗧𝗧𝗔𝗖𝗞? (𝘆/𝗻): " + Fore.WHITE).lower()
    
    if confirm == 'y':
        print(Fore.RED + f"\n🚀 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗜𝗡𝗚 {action_type.upper()} {report_type.upper()} 𝗥𝗘𝗤𝗨𝗘𝗦𝗧...\n")
        
        success, failed, duration = mass_report_attack(phone, report_type, count)
        
        print(Fore.GREEN + f"\n✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗!")
        print(Fore.GREEN + f"📨 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹: {success}")
        print(Fore.RED + f"📭 𝗙𝗮𝗶𝗹𝗲𝗱: {failed}")
        print(Fore.CYAN + f"⏱️  𝗧𝗶𝗺𝗲: {duration:.2f} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀")
        
        if success > 0:
            print(Fore.YELLOW + f"\n🎯 𝗧𝗮𝗿𝗴𝗲𝘁 {phone} 𝘀𝗵𝗼𝘂𝗹𝗱 𝗿𝗲𝗰𝗲𝗶𝘃𝗲 𝗮𝘁𝘁𝗲𝗻𝘁𝗶𝗼𝗻 𝘄𝗶𝘁𝗵𝗶𝗻 24-48 𝗵𝗼𝘂𝗿𝘀")
            print(Fore.YELLOW + "📧 𝗥𝗲𝗽𝗼𝗿𝘁𝘀 𝘀𝗲𝗻𝘁 𝗳𝗿𝗼𝗺 𝗮𝗹𝗹 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗮𝗰𝗰𝗼𝘂𝗻𝘁𝘀 𝘁𝗼 𝗮𝗹𝗹 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗲𝗺𝗮𝗶𝗹𝘀")
    
    input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")

def check_number_menu():
    """Number checking menu"""
    clear()
    print(Fore.BLUE + "\n🔍 𝗥𝗘𝗔𝗟 𝗪𝗛𝗔𝗧𝗦𝗔𝗣𝗣 𝗡𝗨𝗠𝗕𝗘𝗥 𝗖𝗛𝗘𝗖𝗞\n")
    
    phone = input(Fore.CYAN + "📞 𝗘𝗻𝘁𝗲𝗿 𝗻𝘂𝗺𝗯𝗲𝗿 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 \n 𝗘𝘅𝗮𝗺𝗽𝗹𝗲 +𝟮𝟯𝟰𝘅𝘅𝘅𝘅𝘅): " + Fore.WHITE).strip()
    
    if validate_phone_number(phone):
        check_whatsapp_number(phone)
    else:
        print(Fore.RED + "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗽𝗵𝗼𝗻𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝗳𝗼𝗿𝗺𝗮𝘁")
    
    input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")

def fraud_menu():
    """Fraud reporting menu"""
    clear()
    print(Fore.RED + "\n🚨 𝗠𝗔𝗦𝗦 𝗙𝗥𝗔𝗨𝗗 𝗥𝗘𝗣𝗢𝗥𝗧\n")
    
    target = input(Fore.CYAN + "🎯 𝗘𝗻𝘁𝗲𝗿 𝗳𝗿𝗮𝘂𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝘁𝗼 𝗿𝗲𝗽𝗼𝗿𝘁: " + Fore.WHITE).strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗽𝗵𝗼𝗻𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝗳𝗼𝗿𝗺𝗮𝘁")
        input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")
        return
    
    # Get report count
    while True:
        try:
            count = int(input(Fore.CYAN + "💣 𝗥𝗲𝗽𝗼𝗿𝘁𝘀 𝘁𝗼 𝘀𝗲𝗻𝗱 (𝟭𝟬-𝟱𝟬): " + Fore.WHITE).strip())
            if 10 <= count <= 50:
                break
            print(Fore.RED + "❌ 𝗠𝘂𝘀𝘁 𝗯𝗲 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝟭𝟬 𝗮𝗻𝗱 𝟱𝟬")
        except:
            count = 30
            print(Fore.YELLOW + f"   𝗨𝘀𝗶𝗻𝗴 𝗱𝗲𝗳𝗮𝘂𝗹𝘁: {count}")
            break
    
    print(Fore.YELLOW + f"\n⚠️  𝗥𝗲𝗽𝗼𝗿𝘁𝗶𝗻𝗴 {target} 𝗳𝗼𝗿 𝗳𝗿𝗮𝘂𝗱 𝗩𝗶𝗼𝗹𝗲𝗻𝗰𝗲")
    confirm = input(Fore.RED + f"\n🚨 𝗟𝗔𝗨𝗡𝗖𝗛 {count} 𝗙𝗥𝗔𝗨𝗗 𝗥𝗘𝗣𝗢𝗥𝗧𝗦? (𝘆/𝗻): " + Fore.WHITE).lower()
    
    if confirm == 'y':
        success, failed, duration = mass_report_attack(target, "fraud", count)
        
        print(Fore.GREEN + f"\n✅ 𝗙𝗥𝗔𝗨𝗗 𝗥𝗘𝗣𝗢𝗥𝗧𝗦 𝗦𝗘𝗡𝗧!")
        print(Fore.GREEN + f"📨 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹: {success}")
        print(Fore.YELLOW + f"⚠️  𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝘄𝗶𝗹𝗹 𝗶𝗻𝘃𝗲𝘀𝘁𝗶𝗴𝗮𝘁𝗲 𝘄𝗶𝘁𝗵𝗶𝗻 𝟭𝟮 - 𝟰𝟴 𝗵𝗼𝘂𝗿𝘀")
    
    input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")

def nuclear_menu():
    """Nuclear mass report menu"""
    clear()
    print(Fore.RED + "☢️  𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗠𝗔𝗦𝗦 𝗥𝗘𝗣𝗢𝗥𝗧 𝗠𝗢𝗗𝗘 ☢️\n")
    
    target = input(Fore.CYAN + "🎯 𝗘𝗻𝘁𝗲𝗿 𝘁𝗮𝗿𝗴𝗲𝘁 𝗻𝘂𝗺𝗯𝗲𝗿 𝗳𝗼𝗿 𝗻𝘂𝗰𝗹𝗲𝗮𝗿 𝘀𝘁𝗿𝗶𝗸𝗲: " + Fore.WHITE).strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗽𝗵𝗼𝗻𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝗳𝗼𝗿𝗺𝗮𝘁")
        input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")
        return
    
    # Get report count
    while True:
        try:
            count = int(input(Fore.CYAN + "💣 𝗡𝘂𝗰𝗹𝗲𝗮𝗿 𝘆𝗶𝗲𝗹𝗱 (𝟭𝟬-𝟱𝟬 𝗿𝗲𝗽𝗼𝗿𝘁𝘀): " + Fore.WHITE).strip())
            if 10 <= count <= 50:
                break
            print(Fore.RED + "❌ 𝗠𝘂𝘀𝘁 𝗯𝗲 𝗯𝗲𝘁𝘄𝗲𝗲𝗻 𝟭𝟬 𝗮𝗻𝗱 𝟱𝟬")
        except:
            count = 40
            print(Fore.YELLOW + f"   𝗨𝘀𝗶𝗻𝗴 𝗱𝗲𝗳𝗮𝘂𝗹𝘁: {count}")
            break
    
    print(Fore.RED + f"\n⚠️  𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗟𝗔𝗨𝗡𝗖𝗛 𝗗𝗘𝗧𝗘𝗖𝗧𝗘𝗗")
    print(Fore.RED + f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁: {target}")
    print(Fore.RED + f"💣 𝗬𝗶𝗲𝗹𝗱: {count} reports")
    
    confirm = input(Fore.RED + "\n🔴 𝗖𝗢𝗡𝗙𝗜𝗥𝗠 𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗦𝗧𝗥𝗜𝗞𝗘? (𝘁𝘆𝗽𝗲 '𝗡𝗨𝗞𝗘' 𝘁𝗼 𝗰𝗼𝗻𝗳𝗶𝗿𝗺): " + Fore.WHITE)
    
    if confirm.upper() == 'NUKE':
        print(Fore.RED + "\n🚀 𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗟𝗔𝗨𝗡𝗖𝗛 𝗜𝗡 𝗣𝗥𝗢𝗚𝗥𝗘𝗦𝗦...\n")
        
        success, failed, duration = mass_report_attack(target, "nuclear", count)
        
        print(Fore.RED + "\n☢️  𝗡𝗨𝗖𝗟𝗘𝗔𝗥 𝗦𝗧𝗥𝗜𝗞𝗘 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗!")
        print(Fore.GREEN + f"✅ 𝗧𝗼𝘁𝗮𝗹 𝗵𝗶𝘁𝘀: {success}")
        print(Fore.RED + f"❌ 𝗠𝗶𝘀𝘀𝗲𝘀: {failed}")
        print(Fore.YELLOW + f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁 {target} 𝘀𝗵𝗼𝘂𝗹𝗱 𝗯𝗲 𝗲𝗹𝗶𝗺𝗶𝗻𝗮𝘁𝗲𝗱 𝘄𝗶𝘁𝗵𝗶𝗻 𝗵𝗼𝘂𝗿𝘀⌛")
    
    input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")

def system_test_menu():
    """System testing menu"""
    clear()
    print(Fore.CYAN + "\n⚙️  𝗦𝗬𝗦𝗧𝗘𝗠 𝗖𝗢𝗡𝗙𝗜𝗚𝗨𝗥𝗔𝗧𝗜𝗢𝗡 & 𝗧𝗘𝗦𝗧𝗜𝗡𝗚\n")
    
    print("1. 𝗧𝗲𝘀𝘁 𝗚𝗺𝗮𝗶𝗹 𝗔𝗰𝗰𝗼𝘂𝗻𝘁𝘀")
    print("2. 𝗧𝗲𝘀𝘁 𝗣𝗿𝗼𝘅𝗶𝗲𝘀")
    print("3. 𝗩𝗶𝗲𝘄 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀")
    print("4. 𝗕𝗮𝗰𝗸 𝘁𝗼 𝗺𝗮𝗶𝗻 𝗺𝗲𝗻𝘂")
    
    config_choice = input(Fore.CYAN + "\n𝗦𝗲𝗹𝗲𝗰𝘁 𝗼𝗽𝘁𝗶𝗼𝗻: " + Fore.WHITE).strip()
    
    if config_choice == "1":
        print(Fore.CYAN + "\n=== 𝗧𝗘𝗦𝗧𝗜𝗡𝗚 𝗚𝗠𝗔𝗜𝗟 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 ===\n")
        working = 0
        for i, acc in enumerate(GMAIL_ACCOUNTS):
            print(Fore.YELLOW + f"𝗧𝗲𝘀𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝗼𝘂𝗻𝘁 {i+1}: {acc['email']}")
            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
                server.starttls()
                server.login(acc['email'], acc['password'])
                server.quit()
                print(Fore.GREEN + f"  ✅ 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝘄𝗼𝗿𝗸𝗶𝗻𝗴")
                working += 1
            except Exception as e:
                print(Fore.RED + f"  ❌ 𝗙𝗮𝗶𝗹𝗲𝗱: {str(e)}")
            time.sleep(1)
        print(Fore.CYAN + f"\n𝗥𝗲𝘀𝘂𝗹𝘁: {working}/{len(GMAIL_ACCOUNTS)} 𝗮𝗰𝗰𝗼𝘂𝗻𝘁𝘀 𝘄𝗼𝗿𝗸𝗶𝗻𝗴")
        
    elif config_choice == "2":
        print(Fore.CYAN + "\n=== 𝗧𝗘𝗦𝗧𝗜𝗡𝗚 𝗣𝗥𝗢𝗫𝗜𝗘𝗦 ===\n")
        working = 0
        for i, proxy in enumerate(PROXY_LIST):
            print(Fore.YELLOW + f"𝗧𝗲𝘀𝘁𝗶𝗻𝗴 𝗽𝗿𝗼𝘅𝘆 {i+1}: {proxy}")
            status, info = test_proxy(proxy)
            if status:
                print(Fore.GREEN + f"  ✅ 𝗪𝗼𝗿𝗸𝗶𝗻𝗴👨‍💻 - 𝗜𝗣: {info}")
                working += 1
            else:
                print(Fore.RED + f"  ❌ 𝗙𝗮𝗶𝗹𝗲𝗱: {info}")
            time.sleep(0.5)
        print(Fore.CYAN + f"\n𝗥𝗲𝘀𝘂𝗹𝘁: {working}/{len(PROXY_LIST)} 𝗽𝗿𝗼𝘅𝗶𝗲𝘀 𝘄𝗼𝗿𝗸𝗶𝗻𝗴👨‍💻")
        
    elif config_choice == "3":
        print(Fore.CYAN + "\n=== 𝗦𝗬𝗦𝗧𝗘𝗠 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 ===")
        print(Fore.YELLOW + f"𝗔𝗰𝗰𝗼𝘂𝗻𝘁𝘀 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲: {len(GMAIL_ACCOUNTS)}")
        print(Fore.YELLOW + f"𝗣𝗿𝗼𝘅𝗶𝗲𝘀 𝗟𝗼𝗮𝗱𝗲𝗱: {len(PROXY_LIST)}")
        print(Fore.YELLOW + f"𝗧𝗮𝗿𝗴𝗲𝘁 𝗘𝗺𝗮𝗶𝗹𝘀: {len(WHATSAPP_EMAILS)}")
        print(Fore.YELLOW + f"𝗠𝗮𝘅 𝗥𝗲𝗽𝗼𝗿𝘁𝘀: 𝟱𝟬")
        print(Fore.YELLOW + f"𝗠𝗶𝗻 𝗥𝗲𝗽𝗼𝗿𝘁𝘀: 𝟭𝟬")
        print(Fore.YELLOW + f"𝗖𝗼𝗻𝗰𝘂𝗿𝗿𝗲𝗻𝘁 𝗧𝗵𝗿𝗲𝗮𝗱𝘀: 3")
        print(Fore.YELLOW + f"𝗩𝗲𝗿𝘀𝗶𝗼𝗻: 𝟱.𝟬 Pro")
        print(Fore.GREEN + "\n✅ 𝗔𝗹𝗹 𝘀𝘆𝘀𝘁𝗲𝗺𝘀 𝗼𝗽𝗲𝗿𝗮𝘁𝗶𝗼𝗻𝗮𝗹")
        
    input(Fore.CYAN + "\n↵ 𝗣𝗿𝗲𝘀𝘀 𝗘𝗻𝘁𝗲𝗿 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲...")

def exit_tool():
    """Exit the tool"""
    print(Fore.YELLOW + "\n👋 𝗦𝗵𝘂𝘁𝘁𝗶𝗻𝗴 𝗱𝗼𝘄𝗻 𝘀𝘆𝘀𝘁𝗲𝗺...")
    print(Fore.RED + "⚠️  𝗖𝗹𝗲𝗮𝗿𝗶𝗻𝗴 𝗹𝗼𝗴𝘀...")
    time.sleep(2)
    sys.exit(0)

# ===== MAIN EXECUTION =====
def main():
    """Main execution function"""
    try:
        # Authenticate user
        if not authenticate():
            return
        
        # Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  𝗜𝗻𝘁𝗲𝗿𝗿𝘂𝗽𝘁𝗲𝗱 𝗯𝘆 𝘂𝘀𝗲𝗿")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ 𝗖𝗿𝗶𝘁𝗶𝗰𝗮𝗹 𝗲𝗿𝗿𝗼𝗿: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()