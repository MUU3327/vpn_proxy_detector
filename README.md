IP 信息显示： 显示用户的公网 IP 地址、国家、地区、城市、ISP 和时区。

数据中心 IP 检测： 检测用户的 IP 地址是否属于数据中心。

WebRTC 测试： 检测是否存在 WebRTC 泄露，这可能指示 VPN 或代理的使用。

延迟测试： 测试访问 google.com, youtube.com 和 cp.cloudflare.com 的延迟速度。

IP 时区与浏览器时区比较： 比较 IP 时区和浏览器时区，检查是否存在时区不匹配的情况。

HTTP 代理头检测： 检查请求头中是否存在常见的代理服务器添加的 HTTP 头。



# VPN/Proxy Detector

## 项目介绍 | Project Introduction

这是一个基于Flask的网页应用，用于检测用户是否正在使用VPN或代理服务。该应用通过多种技术手段检测可能的VPN/代理使用情况，并以直观的界面展示结果。

This is a Flask-based web application designed to detect if a user is using a VPN or proxy service. The application employs multiple detection techniques and displays the results in an intuitive interface.

## 功能特点 | Features

- **公共IP信息检测** | **Public IP Information**: 显示用户的公共IP地址、国家、地区、城市、ISP和时区信息。
- **数据中心IP检测** | **Datacenter IP Detection**: 检查IP地址是否来自数据中心(通常由VPN服务使用)。
- **WebRTC检测** | **WebRTC Leak Test**: 检测本地IP和公共IP是否一致。
- **延迟测试** | **Latency Testing**: 测量到Google、YouTube和Cloudflare的连接延迟。
- **时区比较** | **Timezone Comparison**: 比较IP时区与浏览器时区是否匹配。
- **代理HTTP头检测** | **Proxy Header Detection**: 检查HTTP请求头中是否存在代理相关标记。
- **地图可视化** | **Map Visualization**: 在地图上显示IP地址的地理位置。

## 安装说明 | Installation

1. 克隆此项目 | Clone this repository:
```
git clone <repository-url>
cd vpn_proxy_detector
```

2. 安装所需依赖 | Install required dependencies:
```
pip install -r requirements.txt
```

## 运行方法 | Usage

1. 启动Flask应用 | Start the Flask application:
```
python app.py
```

2. 在浏览器中访问 | Visit in your browser:
```
http://127.0.0.1:5000
```

3. 查看检测结果 | View the detection results displayed on the page.

## 技术栈 | Technology Stack

- **后端** | **Backend**: Python (Flask)
- **前端** | **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **地图** | **Mapping**: Leaflet.js
- **API调用** | **API Calls**: ip-api.com

## 注意事项 | Notes

- 此应用仅用于教育目的，展示了VPN/代理检测的常见技术。
- 检测结果不保证100%准确，因为高级VPN可能采取措施规避这些检测。
- 需要互联网连接才能获取IP信息和进行测试。

This application is for educational purposes only, demonstrating common techniques for VPN/proxy detection. Results are not 100% guaranteed as sophisticated VPNs may employ measures to evade detection. Internet connection is required to fetch IP information and perform tests.

