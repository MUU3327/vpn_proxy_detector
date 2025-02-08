# app.py
from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime
import pytz
import logging
import time

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def get_public_ip_info():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip_address = response.json()["ip"]
        
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()
        logging.debug(f"Successfully fetched IP info: {data}")
        return data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching public IP info: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return None

def is_datacenter_ip(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()
        if data.get("hosting", False):
            return "Datacenter IP"
        else:
            return "Not a Datacenter IP"
    except requests.exceptions.RequestException as e:
        print(f"Error during datacenter IP check: {e}")
        return "Error checking Datacenter IP"

def get_ip_timezone_and_time(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()
        timezone_str = data.get("timezone", None)
        if timezone_str:
            timezone = pytz.timezone(timezone_str)
            ip_time = datetime.now(timezone)
            formatted_ip_time = ip_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
            return formatted_ip_time, timezone_str
        else:
            return "Unknown", "Unknown"
    except requests.exceptions.RequestException as e:
        print(f"Error during ip timezone check: {e}")
        return "Unknown", "Unknown"


def check_proxy_headers(headers):
    proxy_headers = [
        "via",
        "x-forwarded-for",
        "proxy-connection",
        "x-real-ip",
        "forwarded",
    ]
    for header in proxy_headers:
        if header in headers:
            return "Proxy Headers Detected"
    return "No Proxy Headers Detected"


def get_latency(url):
    try:
        start_time = time.time()
        requests.get(url, timeout = 5)
        end_time = time.time()
        latency =  end_time - start_time
        return f"{latency * 1000:.2f} ms"
    except requests.exceptions.RequestException as e:
          logging.error(f"Error during latency test of {url}: {e}")
          return "Error"
    
@app.route("/", methods=["GET", "POST"])
def index():
    public_ip_info = get_public_ip_info()
    if public_ip_info:
        public_ip = public_ip_info.get('query', 'N/A')
        datacenter_result = is_datacenter_ip(public_ip)
        ip_time, ip_timezone = get_ip_timezone_and_time(public_ip)
    else:
        public_ip = "Could not fetch public IP"
        datacenter_result = "Could not fetch public IP"
        ip_time = "Unknown"
        ip_timezone = "Unknown"
    
    beijing_timezone = pytz.timezone('Asia/Shanghai')
    beijing_time = datetime.now(beijing_timezone)
    formatted_beijing_time = beijing_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    

    timezone_test_result = "Cannot Determine" #default if no timezone info available
    if ip_time != "Unknown":
        timezone_test_result = f"IP Time: {ip_time}, Timezone: {ip_timezone}\nBeijing Time: {formatted_beijing_time}"


    proxy_headers_result = check_proxy_headers(request.headers)

    google_latency = get_latency("https://google.com")
    youtube_latency = get_latency("https://youtube.com")
    cloudflare_latency = get_latency("https://cp.cloudflare.com")
    
    latency_test_result = f"Google: {google_latency}, Youtube: {youtube_latency}, Cloudflare: {cloudflare_latency}"

    return render_template(
        "index.html",
        public_ip_info=public_ip_info,
        datacenter_result=datacenter_result,
        timezone_test_result=timezone_test_result,
        proxy_headers_result=proxy_headers_result,
        latency_test_result = latency_test_result,
        public_ip=public_ip,
    )


@app.route("/webrtc", methods=["POST"])
def webrtc_test():
    local_ip = request.json.get("local_ip", None)
    public_ip = get_public_ip_info().get('query')
    if local_ip and public_ip:
      if local_ip != public_ip:
        webrtc_result = "VPN/Proxy Detected (WebRTC)"
      else:
          webrtc_result = "No VPN/Proxy Detected (WebRTC)"
    else:
        webrtc_result = "Could Not Run WebRTC Test"
    return jsonify({"result": webrtc_result})



if __name__ == "__main__":
    app.run(debug=True)