---

<h1 align="center">Fomo Bot</h1>

<p align="center">Boost your productivity with Fomo Bot – your friendly automation tool that handles key tasks with ease!</p>

---

## 🚀 About the Bot

Fomo Bot is your automation buddy designed to simplify daily operations. This bot takes over the repetitive tasks so you can focus on what really matters. With Fomo Bot, you get:

- **📆 Auto Daily:**  
  Automatically claim your daily bonuses without any hassle.

- **📋 Auto Task:**  
  Schedule and execute routine tasks automatically, reducing the need for manual intervention and letting the bot handle your daily workflow.

- **🛒 Auto Order:**  
  Seamlessly place and claim orders based on market sentiment to maximize your rewards.

- **👥 Multi Account Support:**  
  Manage multiple accounts effortlessly with built-in multi account support.

- **🧵 Thread System:**  
  Run tasks concurrently with configurable threading options to improve overall performance and speed.

- **⏱️ Configurable Delays:**  
  Fine-tune delays between account switches and loop iterations to match your specific workflow needs.

- **🔌 Support Proxy:**  
  Use HTTP/HTTPS proxies to enhance your multi-account setups.

Fomo Bot is built with flexibility and efficiency in mind – it's here to help you automate your operations and boost your productivity!

---

## 🌟 Version Updates

**Current Version: v1.0.1**

### v1.0.1 - Latest Update

- Improved auto order feature

---

## 📝 Register

Before you start using Fomo Bot, make sure to register your account.  
Click the link below to get started:

[🔗 Register for Fomo Bot](https://t.me/fomo/app?startapp=ref_IR2DJ)

---

## ⚙️ Configuration

### Main Bot Configuration (`config.json`)

```json
{
  "task": true,
  "order": true,
  "daily": true,
  "thread": 1,
  "proxy": false,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

| **Setting**            | **Description**                                   | **Default Value** |
| ---------------------- | ------------------------------------------------- | ----------------- |
| `daily`                | Enable auto daily bonus claiming. 📆              | `true`            |
| `task`                 | Enable auto task functionality. 📋                | `true`            |
| `order`                | Enable auto order placement. 🛒                   | `true`            |
| `thread`               | Number of threads to run concurrently. 🧵         | `1`               |
| `proxy`                | Enable proxy usage for multi-account setups. 🔌   | `false`           |
| `delay_account_switch` | Delay (in seconds) between switching accounts. ⏱️ | `10`              |
| `delay_loop`           | Delay (in seconds) before the next loop. ⏱️       | `3000`            |

---

## 📥 Installation Steps

### Main Bot Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/livexords-nw/fomo-bot.git
   ```

2. **Navigate to the Project Folder**

   ```bash
   cd fomo-bot
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your Query**

   Create a file named `query.txt` and add your query data.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run Bot**

   ```bash
   python main.py
   ```

---

### 🔹 Want Free Proxies? You can obtain free proxies from [Webshare.io](https://www.webshare.io/).

---

## 🛠️ Contributing

This project is developed by **Livexords**. If you have ideas, questions, or want to contribute, please reach out!

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&style=for-the-badge" height="25" alt="Telegram Logo" />
  </a>
</div>

---
