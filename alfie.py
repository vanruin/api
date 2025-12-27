
import os,sys,re,time,json
import requests,bs4,string
import faker,fake_email,random
from faker import Faker
from fake_email import Email
from bs4 import BeautifulSoup

# Color codes for terminal
W = "\x1b[97m"     # White
G = "\x1b[38;5;46m" # Green
R = "\x1b[38;5;196m" # Red
Y = "\x1b[38;5;226m" # Yellow
B = "\x1b[38;5;51m"  # Blue
M = "\x1b[38;5;201m" # Magenta
C = "\x1b[38;5;123m" # Cyan
X = f"{W}<{R}•{W}>"

oks = []
cps = []

from fake_useragent import UserAgent
ua = UserAgent()

def load_proxies():
    """Load proxies from GitHub URL and cache locally[citation:4]"""
    try:
        # Fetch fresh proxy list[citation:4]
        proxy_url = "https://raw.githubusercontent.com/hookzof/socks5_list/refs/heads/master/proxy.txt"
        response = requests.get(proxy_url, timeout=10)
        proxy_list = response.text.strip().split('\n')
        
        # Filter only SOCKS5 proxies[citation:1]
        valid_proxies = [proxy.strip() for proxy in proxy_list if proxy.strip()]
        
        print(f"{X} Loaded {G}{len(valid_proxies)}{W} SOCKS5 proxies")
        return valid_proxies
    except Exception as e:
        print(f"{X} {R}Failed to load proxies: {str(e)}")
        # Try to load from cache if exists
        try:
            with open("proxy_cache.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return []

def get_proxy(proxy_list):
    """Get next proxy from list with rotation[citation:4]"""
    if not proxy_list:
        return None
    proxy = random.choice(proxy_list)
    # Format for SOCKS5[citation:1][citation:7]
    return {
        "http": f"socks5h://{proxy}",
        "https": f"socks5h://{proxy}"
    }

def ugenX():
    ualist = [ua.random for _ in range(50)]
    return str(random.choice(ualist))

def fake_name():
    first = Faker().first_name()
    last = Faker().last_name()
    return first,last

def extractor(data):
    try:
        soup = BeautifulSoup(data,"html.parser")
        data = {}
        for inputs in soup.find_all("input"):
            name = inputs.get("name")
            value = inputs.get("value")
            if name:
                data[name] = value
        return data
    except Exception as e:
        return {"error":str(e)}

def GetEmail():
    try:
        proxy_list = load_proxies()
        proxy = get_proxy(proxy_list)
        response = requests.post(
            'https://api.internal.temp-mail.io/api/v3/email/new',
            proxies=proxy,
            timeout=10
        ).json()
        return response['email']
    except:
        return Faker().email()

def GetCode(email):
    try:
        proxy_list = load_proxies()
        proxy = get_proxy(proxy_list)
        response = requests.get(
            f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages',
            proxies=proxy,
            timeout=10
        ).text
        code = re.search(r'FB-(\d+)', response).group(1)
        return code
    except:
        return None

def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"""{M}
    
                            
                            
▄████▄ ▄▄    ▄▄▄▄▄ ▄▄ ▄▄▄▄▄ 
██▄▄██ ██    ██▄▄  ██ ██▄▄  
██  ██ ██▄▄▄ ██    ██ ██▄▄▄ 
                             
             ▀                                                  
    {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {G}┌─────────────────────────────────────────────┐
    {G}│ {C}TOOL     : {W}Facebook Auto ID Creator           {G}│
    {G}│ {C}DEVELOPER: {W}Alfie Teorema                       {G}│
    {G}│ {C}FB LINK  : {B}fb.com/AlfieTeorema                {G}│
    {G}│ {C}VERSION  : {W}2.0 Premium + Proxy Rotation       {G}│
    {G}│ {C}PROXY    : {G}SOCKS5 from GitHub List            {G}│
    {G}│ {C}STATUS   : {G}Active √                           {G}│
    {G}└─────────────────────────────────────────────┘
    {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {Y}[!] {W}This tool is for educational purposes only
    {Y}[!] {W}Use at your own risk
    {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

def linex():
    print(f"{W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def main() -> None:
    print_banner()
    
    # Load proxies once at start[citation:4]
    proxy_list = load_proxies()
    if not proxy_list:
        print(f"{X} {R}No proxies loaded! Running without proxy support.")
        input(f"{X} Press ENTER to continue anyway...")
    
    total_accounts = 1000
    print(f"{X} Total accounts to create: {G}{total_accounts}")
    print(f"{X} Output file: {G}/sdcard/create/success.txt")
    print(f"{X} Proxy rotation: {G}Enabled ({len(proxy_list)} proxies)")
    input(f"\n{X} Press ENTER to start creation process...")
    linex()
    
    # Create directory if it doesn't exist
    success_dir = "/sdcard/create"
    if not os.path.exists(success_dir):
        os.makedirs(success_dir)
    
    success_count = 0
    disabled_count = 0
    checkpoint_count = 0
    
    for make in range(total_accounts):
        print(f"\n{W}[{G}{make+1}{W}/{G}{total_accounts}{W}] {C}Creating account...")
        
        # Get fresh proxy for this session[citation:4]
        proxy_config = get_proxy(proxy_list)
        current_proxy = proxy_config.get("http", "").replace("socks5h://", "") if proxy_config else "No Proxy"
        print(f"{X} Using Proxy: {G}{current_proxy}")
        
        ses = requests.Session()
        # Apply proxy to session if available[citation:2][citation:7]
        if proxy_config:
            ses.proxies.update(proxy_config)
        
        try:
            response = ses.get(
                url='https://x.facebook.com/reg',
                params={"_rdc":"1","_rdr":"","wtsid":"rdr_0t3qOXoIHbMS6isLw","refsrc":"deprecated"},
                timeout=15
            )
        except Exception as e:
            print(f"{X} {R}Proxy connection failed: {str(e)}")
            print(f"{X} {Y}Retrying with next proxy...")
            # Remove failed proxy from list
            if proxy_config and proxy_list:
                failed_proxy = current_proxy
                proxy_list = [p for p in proxy_list if p != failed_proxy]
            continue
        
        mts = ses.get("https://x.facebook.com", timeout=10).text
        m_ts = re.search(r'name="m_ts" value="(.*?)"',str(mts)).group(1)
        formula = extractor(response.text)
        email2 = GetEmail()
        firstname,lastname = fake_name()
        print(f"{X} Name  : {G}{firstname} {lastname}")
        print(f"{X} Email : {G}{email2}")
        
        payload = {
            'ccp': "2",
            'reg_instance': str(formula["reg_instance"]),
            'submission_request': "true",
            'helper': "",
            'reg_impression_id': str(formula["reg_impression_id"]),
            'ns': "1",
            'zero_header_af_client': "",
            'app_id': "103",
            'logger_id': str(formula["logger_id"]),
            'field_names[0]': "firstname",
            'firstname': firstname,
            'lastname': lastname,
            'field_names[1]': "birthday_wrapper",
            'birthday_day': str(random.randint(1,28)),
            'birthday_month': str(random.randint(1,12)),
            'birthday_year': str(random.randint(1992,2009)),
            'age_step_input': "",
            'did_use_age': "false",
            'field_names[2]': "reg_email__",
            'reg_email__': email2,
            'field_names[3]': "sex",
            'sex': "2",
            'preferred_pronoun': "",
            'custom_gender': "",
            'field_names[4]': "reg_passwd__",
            'name_suggest_elig': "false",
            'was_shown_name_suggestions': "false",
            'did_use_suggested_name': "false",
            'use_custom_gender': "false",
            'guid': "",
            'pre_form_step': "",
            'encpass': '#PWD_BROWSER:0:{}:{}'.format(str(time.time()).split('.')[0],"MrCode@123"),
            'submit': "Sign Up",
            'fb_dtsg': "NAcMC2x5X2VrJ7jhipS0eIpYv1zLRrDsb5y2wzau2bw3ipw88fbS_9A:0:0",
            'jazoest': str(formula["jazoest"]),
            'lsd': str(formula["lsd"]),
            '__dyn': "1ZaaAG1mxu1oz-l0BBBzEnxG6U4a2i5U4e0C8dEc8uwcC4o2fwcW4o3Bw4Ewk9E4W0pKq0FE6S0x81vohw5Owk8aE36wqEd8dE2YwbK0iC1qw8W0k-0jG3qaw4kwbS1Lw9C0le0ue0QU",
            '__csr': "",
            '__req': "p",
            '__fmt': "1",
            '__a': "AYkiA9jnQluJEy73F8jWiQ3NTzmH7L6RFbnJ_SMT_duZcpo2yLDpuVXfU2doLhZ-H1lSX6ucxsegViw9lLO6uRx31-SpnBlUEDawD_8U7AY4kQ",
            '__user': "0"
        }
        
        header1 = {
            "Host":"m.facebook.com",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":ugenX(),
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "dnt":"1",
            "X-Requested-With":"mark.via.gp",
            "Sec-Fetch-Site":"none",
            "Sec-Fetch-Mode":"navigate",
            "Sec-Fetch-User":"?1",
            "Sec-Fetch-Dest":"document",
            "dpr":"1.75",
            "viewport-width":"980",
            "sec-ch-ua":"\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile":"?1",
            "sec-ch-ua-platform":"\"Android\"",
            "sec-ch-ua-platform-version":"\"\"",
            "sec-ch-ua-model":"\"\"",
            "sec-ch-ua-full-version-list":"",
            "sec-ch-prefers-color-scheme":"dark",
            "Accept-Encoding":"gzip, deflate, br, zstd",
            "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8"
        }
        
        reg_url = "https://www.facebook.com/reg/submit/?privacy_mutation_token=eyJ0eXBlIjowLCJjcmVhdGlvbl90aW1lIjoxNzM0NDE0OTk2LCJjYWxsc2l0ZV9pZCI6OTA3OTI0NDAyOTQ4MDU4fQ%3D%3D&multi_step_form=1&skip_suma=0&shouldForceMTouch=1"
        try:
            py_submit = ses.post(reg_url, data=payload, headers=header1, timeout=20)
        except Exception as e:
            print(f"{X} {R}Registration failed: {str(e)}")
            continue
        
        if "c_user" in py_submit.cookies:
            first_cok = ses.cookies.get_dict()
            uid = str(first_cok["c_user"])
            header2 = {
                'authority': 'm.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'dpr': '2',
                'referer': 'https://m.facebook.com/login/save-device/',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="125", "Google Chrome";v="125"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': ugenX(),
                'viewport-width': '980',      
            }
            
            params = {
                'next': 'https://m.facebook.com/?deoia=1',
                'soft': 'hjk',
            }
            
            try:
                con_sub = ses.get('https://x.facebook.com/confirmemail.php', params=params, headers=header2, timeout=15).text
            except:
                con_sub = ""
            
            valid = GetCode(email2)
            
            if valid:
                print(f"{X} FB UID : {G}{uid}")
                print(f"{X} OTP    : {G}{valid}")
                confirm_id(email2,uid,valid,con_sub,ses, firstname, lastname, proxy_config)
                success_count += 1
            else:
                print(f"{X} Status : {M}Account Disabled")
                disabled_count += 1
                linex()
        else:
            print(f"{X} Status : {R}Checkpoint Required")
            checkpoint_count += 1
            linex()
        
        # Small delay between accounts[citation:4]
        time.sleep(random.uniform(1, 3))
    
    # Final summary
    print_banner()
    print(f"\n    {G}╔════════════════════════════════════════╗")
    print(f"    {G}║        {W}C R E A T I O N   S U M M A R Y       {G}║")
    print(f"    {G}╠════════════════════════════════════════╣")
    print(f"    {G}║ {C}Total Attempted: {W}{total_accounts:>20} {G}║")
    print(f"    {G}║ {G}Success: {W}{success_count:>29} {G}║")
    print(f"    {G}║ {R}Disabled: {W}{disabled_count:>28} {G}║")
    print(f"    {G}║ {Y}Checkpoint: {W}{checkpoint_count:>26} {G}║")
    print(f"    {G}║ {C}Proxies Used: {W}{len(proxy_list):>26} {G}║")
    print(f"    {G}╠════════════════════════════════════════╣")
    print(f"    {G}║ {C}Success File: {W}/sdcard/create/success.txt {G}║")
    print(f"    {G}╚════════════════════════════════════════╝\n")
    
    print(f"{X} Tool developed by: {B}Alfie Teorema")
    print(f"{X} Facebook: {B}https://www.facebook.com/AlfieTeorema")
    print(f"{X} Proxy Source: {B}GitHub SOCKS5 List")
    print(f"{X} Thanks for using the tool!\n")

def confirm_id(mail,uid,otp,data,ses, firstname, lastname, proxy_config):
    try:
        # Apply proxy to confirmation request[citation:2]
        if proxy_config:
            ses.proxies.update(proxy_config)
        
        url = "https://m.facebook.com/confirmation_cliff/"
        params = {
        'contact': mail,
        'type': "submit",
        'is_soft_cliff': "false",
        'medium': "email",
        'code': otp}
        
        payload = {
        'fb_dtsg': 'NAcMC2x5X2VrJ7jhipS0eIpYv1zLRrDsb5y2wzau2bw3ipw88fbS_9A:0:0',
        'jazoest': re.search(r'"\d+"', data).group().strip('"'),
        'lsd': re.search('"LSD",\[\],{"token":"([^"]+)"}',str(data)).group(1),
        '__dyn': "",
        '__csr': "",
        '__req': "4",
        '__fmt': "1",
        '__a': "",
        '__user': uid}
        
        headers = {
        'User-Agent': ugenX(),
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-full-version-list': "",
        'sec-ch-ua-platform': "\"Android\"",
        'sec-ch-ua': "\"Android WebView\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        'sec-ch-ua-model': "\"\"",
        'sec-ch-ua-mobile': "?1",
        'x-asbd-id': "129477",
        'x-fb-lsd': "KnpjLz-YdSXR3zBqds98cK",
        'sec-ch-prefers-color-scheme': "light",
        'sec-ch-ua-platform-version': "\"\"",
        'origin': "https://m.facebook.com",
        'x-requested-with': "mark.via.gp",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://m.facebook.com/confirmemail.php?next=https%3A%2F%2Fm.facebook.com%2F%3Fdeoia%3D1&soft=hjk",
        'accept-language': "en-GB,en-US;q=0.9,en;q=0.8",
        'priority': "u=1, i"}
        
        response = ses.post(url, params=params, data=payload, headers=headers, timeout=15)
        
        if "checkpoint" in str(response.url):
            print(f"{X} Status : {R}Fucked ID Disabled")
            linex()
        else:
            cookie = (";").join([ "%s=%s" % (key,value) for key,value in ses.cookies.get_dict().items()])
            account_info = f"{uid}|MrCode@123|{cookie}|{firstname} {lastname}|{mail}"
            print(f"{X} Status : {G}SUCCESS")
            print(f"{X} Saved to: {G}/sdcard/create/success.txt")
            
            # Save to file
            success_file = "/sdcard/create/success.txt"
            with open(success_file, "a") as f:
                f.write(account_info + "\n")
            
            linex()
    except Exception as e:
        print(f"{X} Error : {R}{str(e)}")
        linex()

if __name__ == "__main__":
    try:
        # Install required packages if not present
        try:
            import socks
        except ImportError:
            print(f"{X} Installing required proxy packages...")
            os.system("pip install pysocks requests[socks]")
        
        main()
    except KeyboardInterrupt:
        print(f"\n\n{X} {Y}Process interrupted by user!")
        print(f"{X} {C}Thanks for using Alfie's Facebook Auto Creator!")
    except Exception as e:
        print(f"\n{X} {R}Error: {str(e)}")
        print(f"{X} {Y}Please contact Alfie Teorema for support")
