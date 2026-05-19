import requests
import concurrent.futures
import time
import json
from urllib.parse import urljoin


class SiteScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/') + '/'
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })

    def get_iranian_names_english(self):
        """لیست جدید اسم‌های ایرانی (فقط اسم)"""
        return [
            # دخترانه
            "abnoos", "afsaneh", "afrouz", "afsana", "anahita", "anousha", "arezo", "armaghan", "ashti", "atefeh",
            "azadeh", "azita", "bahareh", "banoo", "baraneh", "delnaz", "delshad", "delsa", "diba", "dorsa",
            "ehteram", "elmira", "eshgh", "esin", "farahnaz", "farideh", "farzaneh", "ferydoon", "firouzeh", "firooze",
            "golchehreh", "golnar", "golpari", "golrokh", "golsan", "goltaj", "hana", "hananeh", "hasti", "havva",
            "helena", "hermine", "homa", "iran", "isatis", "jeylan", "khatereh", "khorshid", "kimya", "kobra",

            # پسرانه
            "abtin", "adib", "afraz", "afshin", "ahmadreza", "akbar", "alidad", "almas", "amrollah", "anoushirvan",
            "arashbod", "ardeshir", "arjang", "armanesh", "ashour", "ataollah", "bahador", "bakhtiar", "barbod",
            "behnoud",
            "behram", "bijhan", "binesh", "bizhan", "borzou", "changiz", "cyrus", "dadmehr", "dariyan", "delavar",
            "ebrahim", "eraj", "esfandiar", "faramarz", "farrokhzad", "fathollah", "fazel", "fereydoon", "firouz",
            "goudarz",
            "hamzeh", "hormoz", "iranshah", "jalil", "jahangir", "kamran", "karun", "keykhosrow", "kiumars", "lohrasb",

            # یونیسکس
            "aida", "arian", "artina", "artmis", "ashna", "avaan", "avina", "ayra", "bahar", "baran",
            "dana", "dari", "doran", "ehsan", "erfan", "farinaz", "farin", "ghazal", "hamta", "hanan",
            "hiva", "iliya", "iman", "irani", "isa", "jasmin", "kian", "lian", "mahan", "mahra",
            "maneli", "melika", "miran", "narin", "nava", "navan", "nazanin", "negar", "nika", "nil",
            "omid", "parinaz", "parnian", "payan", "ramin", "rojin", "saina", "saman", "sarin", "sepanta",
            "shadan", "shayan", "sina", "soheil", "sorena", "tina", "vahdat", "varia", "yasin", "zarin"
        ]
    def scan_path(self, path):
        """اسکن یک مسیر خاص"""
        url = urljoin(self.base_url, path)
        try:
            response = self.session.get(
                url,
                timeout=10,
                allow_redirects=True,
                verify=False  # اگر SSL دارید، این را True کنید
            )

            result = {
                'path': path,
                'url': url,
                'status': response.status_code,
                'size': len(response.content),
                'redirect': response.url if response.history else None,
                'content_type': response.headers.get('Content-Type', '')
            }

            return result

        except requests.exceptions.SSLError:
            return {'path': path, 'error': 'SSL Error', 'status': 'SSL_ERROR'}
        except requests.exceptions.Timeout:
            return {'path': path, 'error': 'Timeout', 'status': 'TIMEOUT'}
        except requests.exceptions.ConnectionError:
            return {'path': path, 'error': 'Connection Error', 'status': 'CONN_ERROR'}
        except Exception as e:
            return {'path': path, 'error': str(e), 'status': 'ERROR'}

    def run_scan(self, max_workers=10, delay=0.1):
        """اجرای اسکن اصلی"""
        names = self.get_iranian_names_english()

        print(f"🔍 شروع اسکن: {self.base_url}")
        print(f"📊 تعداد مسیرها برای تست: {len(names)}")
        print(f"⚡ تعداد کارگران موازی: {max_workers}")
        print("=" * 60)

        found_paths = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_name = {executor.submit(self.scan_path, name): name for name in names}

            for i, future in enumerate(concurrent.futures.as_completed(future_to_name), 1):
                name = future_to_name[future]
                result = future.result()

                status = result.get('status')

                if isinstance(status, int) and status != 404:
                    if status == 200:
                        print(f"✅ [200] یافت شد: {name}")
                        found_paths.append(result)
                    elif status in [301, 302, 307, 308]:
                        print(f"↪️ [{status}] ریدایرکت: {name} → {result.get('redirect', '')}")
                        found_paths.append(result)
                    elif status == 403:
                        print(f"🚫 [403] ممنوع: {name}")
                        found_paths.append(result)
                    elif status == 401:
                        print(f"🔐 [401] نیاز به احراز: {name}")
                        found_paths.append(result)
                    elif status == 500:
                        print(f"💥 [500] خطای سرور: {name}")
                        found_paths.append(result)

                # نمایش پیشرفت
                if i % 20 == 0:
                    print(f"📊 پیشرفت: {i}/{len(names)} ({i / len(names) * 100:.1f}%)")

                # تاخیر برای جلوگیری از بلاک شدن
                time.sleep(delay)

        return found_paths

    def save_results(self, results, filename="scan_results.json"):
        """ذخیره نتایج در فایل"""
        data = {
            'base_url': self.base_url,
            'scan_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tested': len(self.get_iranian_names_english()),
            'total_found': len(results),
            'results': results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 نتایج در '{filename}' ذخیره شد")
        return filename


def main():
    # تنظیمات
    TARGET_URL = "http://download.vijra.ir:2096/normalsub/"

    # ایجاد اسکنر
    scanner = SiteScanner(TARGET_URL)

    # اجرای اسکن
    print("🎯 سایت هدف:", TARGET_URL)
    print("=" * 60)

    results = scanner.run_scan(
        max_workers=15,  # تعداد درخواست‌های همزمان
        delay=0.05  # تاخیر بین درخواست‌ها (ثانیه)
    )

    # نمایش خلاصه
    print("\n" + "=" * 60)
    print("📊 خلاصه نتایج:")
    print("=" * 60)

    if results:
        # گروه‌بندی بر اساس وضعیت
        status_groups = {}
        for result in results:
            status = result['status']
            status_groups.setdefault(status, []).append(result['path'])

        for status, paths in sorted(status_groups.items()):
            print(f"\n📁 کد وضعیت {status} ({len(paths)} مورد):")
            for path in paths[:10]:  # فقط ۱۰ مورد اول هر گروه
                print(f"   • {path}")
            if len(paths) > 10:
                print(f"   ... و {len(paths) - 10} مورد دیگر")

        print(f"\n✨ مجموع {len(results)} مسیر معتبر یافت شد!")

        # ذخیره نتایج
        scanner.save_results(results)

        # ایجاد فایل txt برای مرور آسان
        with open("found_paths.txt", "w", encoding="utf-8") as f:
            f.write(f"مسیرهای یافت شده در {TARGET_URL}\n")
            f.write(f"تاریخ اسکن: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            for result in results:
                if isinstance(result['status'], int):
                    f.write(f"[{result['status']}] {result['path']}\n")
                    f.write(f"   URL: {result['url']}\n")
                    if result.get('redirect'):
                        f.write(f"   ↪️ Redirect to: {result['redirect']}\n")
                    f.write(f"   📏 Size: {result.get('size', 0)} bytes\n\n")

        print("📄 لیست ساده مسیرها در 'found_paths.txt' ذخیره شد")

    else:
        print("🚫 هیچ مسیر معتبری یافت نشد!")

    print("\n🎉 اسکن کامل شد!")


if __name__ == "__main__":
    main()
