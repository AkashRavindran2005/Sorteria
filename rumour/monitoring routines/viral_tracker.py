import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class ViralTracker:
    def __init__(self):
        self.platforms = ['Twitter', 'Facebook', 'Instagram', 'YouTube', 'TikTok', 'Reddit']
    
    def track_viral(self, content_url):
        timeline_data = self._generate_viral_timeline()
        platform_data = self._analyze_platform_engagement()
        influencer_data = self._identify_key_influencers()
        
        return {
            'timeline': timeline_data,
            'platforms': platform_data,
            'influencers': influencer_data,
            'viral_score': self._calculate_viral_score(timeline_data)
        }
    
    def _generate_viral_timeline(self):
        hours = 48
        timeline = []
        base_shares = 100
        
        for hour in range(hours):
            if hour < 6:
                multiplier = 1 + (hour * 0.2)
            elif hour < 24:
                multiplier = 2 + random.uniform(0, 3)
            else:
                multiplier = max(1, 5 - (hour-24) * 0.1)
            
            shares = int(base_shares * multiplier * random.uniform(0.8, 1.2))
            timeline.append({
                'time': (datetime.now() - timedelta(hours=hours-hour)).strftime('%Y-%m-%d %H:%M'),
                'shares': shares,
                'engagement': shares * random.uniform(2, 5)
            })
        
        return pd.DataFrame(timeline)
    
    def _analyze_platform_engagement(self):
        platform_data = []
        
        for platform in self.platforms:
            engagement = random.randint(1000, 50000)
            platform_data.append({
                'platform': platform,
                'engagement': engagement,
                'share_rate': random.uniform(0.05, 0.25),
                'sentiment': random.choice(['Positive', 'Negative', 'Neutral'])
            })
        
        return pd.DataFrame(platform_data)
    
    def _identify_key_influencers(self):
        influencers = [
            {'username': '@techinfluencer1', 'followers': '2.3M', 'engagement_rate': '4.2%', 'shares': 1200},
            {'username': '@newsaccount', 'followers': '890K', 'engagement_rate': '2.8%', 'shares': 850},
            {'username': '@viralcontentcreator', 'followers': '1.5M', 'engagement_rate': '5.1%', 'shares': 950},
            {'username': '@breakingnews', 'followers': '3.2M', 'engagement_rate': '3.4%', 'shares': 1500},
        ]
        
        return influencers
    
    def _calculate_viral_score(self, timeline_data):
        max_shares = timeline_data['shares'].max()
        growth_rate = timeline_data['shares'].pct_change().mean()
        viral_score = min((max_shares / 1000) * (1 + growth_rate), 10.0)
        return round(viral_score, 2)