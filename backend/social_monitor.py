import os
import requests
import praw
from datetime import datetime
from dotenv import load_dotenv
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

load_dotenv()

class RealSocialMonitor:
    def __init__(self):
        self.reddit = None
        self.driver = None
        self.setup_apis()

    def setup_apis(self):
        try:
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT', 'MisinfoDetector/1.0')
            
            if client_id and client_secret:
                self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                print("✅ Reddit API connected")
        except Exception as e:
            print(f"❌ Reddit setup failed: {e}")

    def _setup_selenium(self):
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not installed. Install with: pip install selenium webdriver-manager")
            return False
        
        try:
            options = Options()
            options.headless = True
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            return True
        except Exception as e:
            print(f"❌ Selenium setup failed: {e}")
            return False

    def get_real_vip_content(self, vip_accounts, max_results=100):
        all_posts = []
        
        for vip in vip_accounts:
            twitter_posts = self._scrape_twitter_selenium(vip, max_results // 2)
            all_posts.extend(twitter_posts)
            
            reddit_posts = self._scrape_reddit(vip, max_results // 2)
            all_posts.extend(reddit_posts)
        
        if self.driver:
            self.driver.quit()
        
        return sorted(all_posts, key=lambda x: x.get('timestamp', datetime.now()), reverse=True)

    def _scrape_twitter_selenium(self, query, limit):
        results = []
        
        if not self._setup_selenium():
            print("❌ Cannot scrape Twitter - Selenium not available")
            return results
        
        try:
            username = query.replace('@', '').strip()
            
            search_url = f"https://twitter.com/search?q={username}&src=typed_query&f=live"
            print(f"Scraping Twitter search: {search_url}")
            
            self.driver.get(search_url)
            
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
            
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article')
            
            for i, tweet_elem in enumerate(tweet_elements[:limit]):
                try:
                    tweet_text_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    tweet_text = tweet_text_elem.text
                    
                    user_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"] a')
                    tweet_user = user_elem.get_attribute('href').split('/')[-1]
                    
                    engagement = 0
                    try:
                        like_elem = tweet_elem.find_element(By.CSS_SELECTOR, '[data-testid="like"] span')
                        engagement += int(like_elem.text.replace(',', '')) if like_elem.text.isdigit() else 0
                    except:
                        pass
                    
                    tweet_url = ""
                    try:
                        time_elem = tweet_elem.find_element(By.CSS_SELECTOR, 'time')
                        tweet_url = time_elem.find_element(By.XPATH, './..').get_attribute('href')
                    except:
                        pass
                    
                    if tweet_text and len(tweet_text) > 10:  
                        results.append({
                            'id': f'selenium_twitter_{i}',
                            'username': f'@{tweet_user}',
                            'platform': 'Twitter',
                            'content': tweet_text,
                            'timestamp': datetime.now(),
                            'engagement': engagement,
                            'url': tweet_url,
                            'source': 'Selenium WebDriver'
                        })
                        
                except Exception as e:
                    continue  
            
            print(f"✅ Found {len(results)} real Twitter posts")
            
        except Exception as e:
            print(f"❌ Twitter scraping failed: {e}")
        
        return results

    def _scrape_reddit(self, query, limit):
        results = []
        if not self.reddit:
            print("❌ Reddit API not available")
            return results
            
        try:
            query_clean = query.replace('@', '').strip()
            submissions = self.reddit.subreddit('all').search(
                query_clean, limit=limit, sort='new'
            )
            
            for s in submissions:
                content = s.selftext or s.title
                if len(content.strip()) > 10: 
                    results.append({
                        'id': s.id,
                        'username': f'u/{s.author.name if s.author else "deleted"}',
                        'platform': 'Reddit',
                        'subreddit': s.subreddit.display_name,
                        'title': s.title,
                        'content': content,
                        'timestamp': datetime.fromtimestamp(s.created_utc),
                        'engagement': s.score + s.num_comments,
                        'url': f"https://reddit.com{s.permalink}",
                        'source': 'Reddit API'
                    })
            
            print(f"✅ Found {len(results)} real Reddit posts")
                    
        except Exception as e:
            print(f"❌ Reddit search failed: {e}")
        
        return results
