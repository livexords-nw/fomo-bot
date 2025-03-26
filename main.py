from datetime import datetime
import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style
import random
from fake_useragent import UserAgent
import asyncio


class fomo:
    BASE_URL = "https://api.miniapp.dropstab.com/api/"
    HEADERS = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "app-version": "1.0.0",
        "content-type": "application/json",
        "origin": "https://mdkefjwsfepf.dropstab.com",
        "priority": "u=1, i",
        "referer": "https://mdkefjwsfepf.dropstab.com/",
        "sec-ch-ua": '"Microsoft Edge";v="134", "Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge WebView2";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.query_raw = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Fomo Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        # Prepare login request to auth/login with header "x-tg-data" and payload "webAppData"
        login_url = f"{self.BASE_URL}auth/login"
        headers = {**self.HEADERS, "x-tg-data": token}
        payload = {"webAppData": token}

        self.log("📡 Sending login request to auth/login...", Fore.CYAN)
        try:
            login_response = requests.post(login_url, headers=headers, json=payload)
            login_response.raise_for_status()
            data = login_response.json()

            # Retrieve access token from jwt data
            jwt_data = data.get("jwt", {})
            access_data = jwt_data.get("access", {})
            self.token = access_data.get("token")
            self.query_raw = token
            if not self.token:
                self.log("❌ Failed to retrieve access token.", Fore.RED)
                return

            self.log("✅ Login successful! Access token retrieved.", Fore.GREEN)

            # Display important user data without revealing the full token
            user_data = data.get("user", {})
            balance = user_data.get("balance", "N/A")
            used_ref_link_code = user_data.get("usedRefLinkCode", "N/A")

            self.log("🔎 User Data:", Fore.CYAN)
            self.log(f"    • Balance: {balance}", Fore.CYAN)
            self.log(f"    • Referral Code Used: {used_ref_link_code}", Fore.CYAN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {login_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during login: {e}", Fore.RED)
            return

    def daily(self) -> None:
        self.log("⏰ Starting daily bonus...", Fore.GREEN)

        bonus_url = f"{self.BASE_URL}bonus/dailyBonus"
        headers = {
            **self.HEADERS,
            "x-tg-data": self.query_raw,
            "Authorization": f"Bearer {self.token}",
        }

        self.log("📡 Sending daily bonus request...", Fore.CYAN)
        try:
            daily_response = requests.post(bonus_url, headers=headers)
            daily_response.raise_for_status()
            data = daily_response.json()

            result = data.get("result", False)
            bonus = data.get("bonus", "N/A")
            streaks = data.get("streaks", "N/A")

            if result:
                self.log("✅ Daily bonus claimed successfully!", Fore.GREEN)
                self.log(f"💰 Bonus: {bonus}", Fore.CYAN)
                self.log(f"🔥 Streaks: {streaks}", Fore.CYAN)
            else:
                self.log("❌ Daily bonus claim failed.", Fore.RED)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to claim daily bonus: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {daily_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error during daily bonus claim: {e}", Fore.RED)
            return

    def task(self) -> None:
        self.log("📋 Fetching quest tasks...", Fore.CYAN)
        quest_url = f"{self.BASE_URL}quest"
        headers = {
            **self.HEADERS,
            "x-tg-data": self.query_raw,
            "Authorization": f"Bearer {self.token}",
        }

        try:
            quest_response = requests.get(quest_url, headers=headers)
            quest_response.raise_for_status()
            quest_groups = quest_response.json()
            self.log("✅ Quests retrieved successfully!", Fore.GREEN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch quests: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {quest_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching quests: {e}", Fore.RED)
            return

        # List to store quests that were started successfully
        quests_to_claim = []

        # Step 1: Start all quests with status "NEW" or "VERIFICATION"
        for group in quest_groups:
            group_name = group.get("name", "Unknown Group")
            quests = group.get("quests", [])
            self.log(f"🔎 Processing quest group: {group_name}", Fore.CYAN)

            for quest in quests:
                quest_id = quest.get("id")
                quest_name = quest.get("name", "Unknown Quest")
                quest_status = quest.get("status", "N/A")

                # Process quests with status "NEW" or "VERIFICATION"
                if quest_status in ["NEW", "VERIFICATION"]:
                    self.log(
                        f"🚀 Starting quest: {quest_name} (ID: {quest_id}) with status {quest_status}",
                        Fore.CYAN,
                    )
                    start_url = f"{self.BASE_URL}quest/{quest_id}/verify"
                    try:
                        start_response = requests.put(start_url, headers=headers)
                        start_response.raise_for_status()
                        start_data = start_response.json()
                        if start_data.get("status") == "OK":
                            self.log(
                                f"✅ Quest '{quest_name}' started successfully.",
                                Fore.GREEN,
                            )
                            quests_to_claim.append({"id": quest_id, "name": quest_name})
                        else:
                            self.log(
                                f"❌ Failed to start quest '{quest_name}'. Response: {start_data}",
                                Fore.RED,
                            )
                    except requests.exceptions.RequestException as e:
                        self.log(
                            f"❌ Error starting quest '{quest_name}': {e}", Fore.RED
                        )
                    except Exception as e:
                        self.log(
                            f"❌ Unexpected error starting quest '{quest_name}': {e}",
                            Fore.RED,
                        )
                else:
                    self.log(
                        f"ℹ️ Skipping quest: {quest_name} (Status: {quest_status})",
                        Fore.YELLOW,
                    )

        # Step 2: Wait 30 seconds before claiming all started quests
        if quests_to_claim:
            self.log(
                "⏳ Waiting 30 seconds before claiming all started quests...", Fore.CYAN
            )
            time.sleep(30)
        else:
            self.log("ℹ️ No quests were started; nothing to claim.", Fore.YELLOW)
            return

        # Step 3: Claim all quests that were started
        for quest in quests_to_claim:
            quest_id = quest["id"]
            quest_name = quest["name"]
            self.log(f"🎯 Claiming quest: {quest_name} (ID: {quest_id})", Fore.CYAN)
            claim_url = f"{self.BASE_URL}quest/{quest_id}/claim"
            try:
                claim_response = requests.put(claim_url, headers=headers)
                claim_response.raise_for_status()
                claim_data = claim_response.json()
                if claim_data.get("status") == "OK":
                    self.log(
                        f"✅ Quest '{quest_name}' claimed successfully.", Fore.GREEN
                    )
                else:
                    self.log(
                        f"❌ Failed to claim quest '{quest_name}'. Response: {claim_data}",
                        Fore.RED,
                    )
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Error claiming quest '{quest_name}': {e}", Fore.RED)
                try:
                    self.log(f"📄 Response content: {claim_response.text}", Fore.RED)
                except Exception:
                    pass
            except Exception as e:
                self.log(
                    f"❌ Unexpected error claiming quest '{quest_name}': {e}", Fore.RED
                )

    def order(self) -> None:
        self.log("📋 Checking current orders...", Fore.CYAN)
        orders_url = f"{self.BASE_URL}order"
        headers = {
            **self.HEADERS,
            "x-tg-data": self.query_raw,
            "Authorization": f"Bearer {self.token}",
        }

        # Step 1: Retrieve current order info
        try:
            orders_response = requests.get(orders_url, headers=headers)
            orders_response.raise_for_status()
            orders_data = orders_response.json()
            periods = orders_data.get("periods", [])
            self.log("✅ Order info retrieved successfully!", Fore.GREEN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch order info: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {orders_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching orders: {e}", Fore.RED)
            return

        # Step 2: Retrieve coin list
        coins_url = f"{self.BASE_URL}order/coins"
        try:
            coins_response = requests.get(coins_url, headers=headers)
            coins_response.raise_for_status()
            coins = coins_response.json()  # list of coins
            self.log("✅ Coin list retrieved successfully!", Fore.GREEN)
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch coin list: {e}", Fore.RED)
            try:
                self.log(f"📄 Response content: {coins_response.text}", Fore.RED)
            except Exception:
                pass
            return
        except Exception as e:
            self.log(f"❌ Unexpected error while fetching coins: {e}", Fore.RED)
            return

        # Mapping period IDs to corresponding sentiment keys
        period_sentiment_key = {1: "1H", 2: "4H", 3: "24H"}

        # Step 3: For each period, if order is missing, place an order using a random coin among eligible candidates
        for period_item in periods:
            period_info = period_item.get("period", {})
            period_id = period_info.get("id")
            if "order" in period_item:
                self.log(
                    f"ℹ️ Period {period_id} already has an order. Skipping.", Fore.YELLOW
                )
                continue

            sentiment_key = period_sentiment_key.get(period_id)
            if not sentiment_key:
                self.log(f"❌ Unknown period id {period_id}. Skipping.", Fore.RED)
                continue

            # Gather candidates with available smartSentiment for this period
            candidates = []
            for coin in coins:
                smart = coin.get("smartSentiment", {})
                if sentiment_key in smart:
                    candidates.append(coin)

            if not candidates:
                self.log(
                    f"❌ No suitable coin found for period {period_id} based on sentiment.",
                    Fore.RED,
                )
                continue

            # Randomly select one candidate
            selected_coin = random.choice(candidates)
            smart = selected_coin.get("smartSentiment", {}).get(sentiment_key, {})
            long_sent = smart.get("long", 0)
            short_sent = smart.get("short", 0)
            # Determine direction based on sentiment values
            best_direction = False if long_sent >= short_sent else True

            coin_id = selected_coin.get("id")
            coin_name = selected_coin.get("name", "Unknown Coin")
            sentiment_value = long_sent if not best_direction else short_sent
            direction_str = "Short" if best_direction else "Long"
            self.log(
                f"🚀 Placing order for period {period_id} with coin {coin_name} (ID: {coin_id}), direction: {direction_str}, sentiment: {sentiment_value}%",
                Fore.CYAN,
            )

            order_payload = {
                "coinId": coin_id,
                "short": best_direction,
                "periodId": period_id,
            }
            try:
                place_response = requests.post(
                    orders_url, headers=headers, json=order_payload
                )
                place_response.raise_for_status()
                order_result = place_response.json()
                self.log(
                    f"✅ Order placed successfully for period {period_id}: {order_result}",
                    Fore.GREEN,
                )
            except requests.exceptions.RequestException as e:
                self.log(
                    f"❌ Failed to place order for period {period_id}: {e}", Fore.RED
                )
                try:
                    self.log(f"📄 Response content: {place_response.text}", Fore.RED)
                except Exception:
                    pass
                continue
            except Exception as e:
                self.log(
                    f"❌ Unexpected error while placing order for period {period_id}: {e}",
                    Fore.RED,
                )
                continue

        # Step 4: Claim orders that are ready (status "CLAIM_AVAILABLE")
        # Re-fetch the order info to get the latest order status
        try:
            orders_response = requests.get(orders_url, headers=headers)
            orders_response.raise_for_status()
            orders_data = orders_response.json()
            periods = orders_data.get("periods", [])
        except Exception as e:
            self.log(f"❌ Error re-fetching orders for claim: {e}", Fore.RED)
            return

        for period_item in periods:
            if "order" in period_item:
                order_info = period_item["order"]
                order_status = order_info.get("status")
                order_id = order_info.get("id")
                period_id = order_info.get("period", {}).get("id")
                
                if order_status == "NOT_WIN":
                    upload_url = f"{self.BASE_URL}order/{order_id}/markUserChecked"
                    self.log(
                        f"🎯 Uploading result image for order ID {order_id} for period {period_id} (LOSE)",
                        Fore.CYAN,
                    )
                    try:
                        upload_response = requests.put(upload_url, headers=headers)
                        upload_response.raise_for_status()
                        upload_result = upload_response.json()
                        self.log(
                            f"✅ Order result image uploaded successfully: {upload_result}",
                            Fore.GREEN,
                        )
                    except requests.exceptions.RequestException as e:
                        self.log(
                            f"❌ Failed to upload result image for order ID {order_id}: {e}",
                            Fore.RED,
                        )
                        try:
                            self.log(
                                f"📄 Response content: {upload_response.text}", Fore.RED
                            )
                        except Exception:
                            pass
                    except Exception as e:
                        self.log(
                            f"❌ Unexpected error while uploading result image for order ID {order_id}: {e}",
                            Fore.RED,
                        )
                elif order_status == "CLAIM_AVAILABLE":
                    claim_url = f"{self.BASE_URL}order/{order_id}/claim"
                    self.log(
                        f"🎯 Claiming order ID {order_id} for period {period_id}",
                        Fore.CYAN,
                    )
                    try:
                        claim_response = requests.put(claim_url, headers=headers)
                        claim_response.raise_for_status()
                        claim_result = claim_response.json()
                        self.log(
                            f"✅ Order claimed successfully: {claim_result}", Fore.GREEN
                        )
                    except requests.exceptions.RequestException as e:
                        self.log(
                            f"❌ Failed to claim order ID {order_id}: {e}", Fore.RED
                        )
                        try:
                            self.log(
                                f"📄 Response content: {claim_response.text}", Fore.RED
                            )
                        except Exception:
                            pass
                    except Exception as e:
                        self.log(
                            f"❌ Unexpected error while claiming order ID {order_id}: {e}",
                            Fore.RED,
                        )

        # Step 5: Restart order placement for any empty slots after claiming
        self.log("🔄 Restarting order placement for empty slots...", Fore.CYAN)
        try:
            orders_response = requests.get(orders_url, headers=headers)
            orders_response.raise_for_status()
            orders_data = orders_response.json()
            periods = orders_data.get("periods", [])
        except Exception as e:
            self.log(f"❌ Error re-fetching orders for restart: {e}", Fore.RED)
            return

        for period_item in periods:
            period_info = period_item.get("period", {})
            period_id = period_info.get("id")
            if "order" in period_item:
                self.log(
                    f"ℹ️ Period {period_id} already has an order. Skipping restart.",
                    Fore.YELLOW,
                )
                continue

            sentiment_key = period_sentiment_key.get(period_id)
            if not sentiment_key:
                self.log(
                    f"❌ Unknown period id {period_id} during restart. Skipping.",
                    Fore.RED,
                )
                continue

            # Gather candidates again for restart
            candidates = []
            for coin in coins:
                smart = coin.get("smartSentiment", {})
                if sentiment_key in smart:
                    candidates.append(coin)

            if not candidates:
                self.log(
                    f"❌ No suitable coin found for period {period_id} during restart.",
                    Fore.RED,
                )
                continue

            selected_coin = random.choice(candidates)
            smart = selected_coin.get("smartSentiment", {}).get(sentiment_key, {})
            long_sent = smart.get("long", 0)
            short_sent = smart.get("short", 0)
            best_direction = False if long_sent >= short_sent else True

            coin_id = selected_coin.get("id")
            coin_name = selected_coin.get("name", "Unknown Coin")
            sentiment_value = long_sent if not best_direction else short_sent
            direction_str = "Short" if best_direction else "Long"
            self.log(
                f"🚀 Restarting order for period {period_id} with coin {coin_name} (ID: {coin_id}), direction: {direction_str}, sentiment: {sentiment_value}%",
                Fore.CYAN,
            )

            order_payload = {
                "coinId": coin_id,
                "short": best_direction,
                "periodId": period_id,
            }
            try:
                place_response = requests.post(
                    orders_url, headers=headers, json=order_payload
                )
                place_response.raise_for_status()
                order_result = place_response.json()
                self.log(
                    f"✅ Order restarted successfully for period {period_id}: {order_result}",
                    Fore.GREEN,
                )
            except requests.exceptions.RequestException as e:
                self.log(
                    f"❌ Failed to restart order for period {period_id}: {e}", Fore.RED
                )
                try:
                    self.log(f"📄 Response content: {place_response.text}", Fore.RED)
                except Exception:
                    pass
                continue
            except Exception as e:
                self.log(
                    f"❌ Unexpected error while restarting order for period {period_id}: {e}",
                    Fore.RED,
                )
                continue

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        import random

        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


async def process_account(account, original_index, account_label, fom, config):
    # Set a random fake User-Agent for this account
    ua = UserAgent()
    fom.HEADERS["User-Agent"] = ua.random

    display_account = account[:10] + "..." if len(account) > 10 else account
    fom.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)

    # Override proxy if enabled
    if config.get("proxy", False):
        fom.override_requests()
    else:
        fom.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

    # Login (blocking call executed in a thread) using the account's index
    await asyncio.to_thread(fom.login, original_index)

    fom.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "daily": "auto claim daily",
        "task": "Automatically solving tasks 🤖",
        "order": "Auto order",
    }

    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        fom.log(
            f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
            color,
        )
        if task_status:
            fom.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(fom, task_key))

    delay_switch = config.get("delay_account_switch", 10)
    fom.log(
        f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.",
        Fore.CYAN,
    )
    await asyncio.sleep(delay_switch)


async def worker(worker_id, fom, config, queue):
    """
    Each worker takes one account from the queue and processes it sequentially.
    A worker will not take a new account until the current one is finished.
    """
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, fom, config)
        queue.task_done()
    fom.log(f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN)


async def main():
    fom = fomo()  # Initialize your fomo instance
    config = fom.load_config()
    all_accounts = fom.query_list
    num_workers = config.get("thread", 1)  # Number of concurrent workers (threads)

    fom.log(
        "🎉 [LIVEXORDS] === Welcome to Fomo Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    fom.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)

    if config.get("proxy", False):
        proxies = fom.load_proxies()

    while True:
        # Create a new asyncio Queue and add all accounts (with their original index)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))

        # Create worker tasks according to the number of threads specified
        workers = [
            asyncio.create_task(worker(i + 1, fom, config, queue))
            for i in range(num_workers)
        ]

        # Wait until all accounts in the queue are processed
        await queue.join()

        # Cancel workers to avoid overlapping in the next loop
        for w in workers:
            w.cancel()

        fom.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        fom.log(
            f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.",
            Fore.CYAN,
        )
        await asyncio.sleep(delay_loop)


if __name__ == "__main__":
    asyncio.run(main())
