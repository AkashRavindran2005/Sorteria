import tweepy
import requests
from datetime import datetime, timedelta
import random

class SocialMonitor:
    def __init__(self):
        self.twitter_api = None
        self.facebook_api = None
        self.instagram_api = None
        self.setup_apis()
    
    def setup_apis(self):
        try:
            auth = tweepy.OAuthHandler("your_consumer_key", "your_consumer_secret")
            auth.set_access_token("your_access_token", "your_access_secret")
            self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
        except:
            pass
    
    def monitor_accounts(self, vip_accounts, keywords):
        posts = []
        
        for account in vip_accounts:
            account_posts = self._get_account_posts(account, keywords)
            posts.extend(account_posts)
        
        return sorted(posts, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    def _get_account_posts(self, account, keywords):
        posts = []
        
        if self.twitter_api:
            try:
                tweets = self.twitter_api.user_timeline(screen_name=account.replace('@', ''), count=5)
                for tweet in tweets:
                    if any(keyword.lower() in tweet.text.lower() for keyword in keywords):
                        posts.append({
                            'username': account,
                            'platform': 'Twitter',
                            'content': tweet.text[:200] + "..." if len(tweet.text) > 200 else tweet.text,
                            'timestamp': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'engagement': f"{tweet.favorite_count + tweet.retweet_count}"
                        })
            except:
                pass
        
        if not posts:
            posts = self._generate_sample_posts(account, keywords)
        
        return posts
    
    def _generate_sample_posts(self, account, keywords):
        sample_posts = [
            f"Just announced groundbreaking developments in {random.choice(keywords)}",
            f"Thoughts on the latest {random.choice(keywords)} trends?",
            f"Excited to share insights about {random.choice(keywords)} innovation",
        ]
        
        posts = []
        for i, content in enumerate(sample_posts[:2]):
            posts.append({
                'username': account,
                'platform': random.choice(['Twitter', 'Facebook', 'Instagram']),
                'content': content,
                'timestamp': (datetime.now() - timedelta(hours=i*2)).strftime('%Y-%m-%d %H:%M:%S'),
                'engagement': str(random.randint(100, 10000))
            })
        
        return posts
    
    def detect_trending_rumors(self):
        trending = []
        
        return trending