import networkx as nx
import numpy as np
import random
from datetime import datetime, timedelta

class OriginTracer:
    def __init__(self):
        self.social_graph = nx.DiGraph()
        self.platforms = ['Twitter', 'Facebook', 'Instagram', 'YouTube', 'Reddit']
    
    def trace_origin(self, content):
        origin_data = self._identify_origin(content)
        propagation_path = self._trace_propagation_path(content)
        network_analysis = self._analyze_network_structure()
        
        return {
            'origin': origin_data,
            'path': propagation_path,
            'network': network_analysis,
            'confidence_metrics': self._calculate_trace_confidence()
        }
    
    def _identify_origin(self, content):
        origin_sources = [
            {'source': '@anonymous_account', 'platform': 'Twitter', 'confidence': 0.85},
            {'source': 'facebook.com/suspicious_page', 'platform': 'Facebook', 'confidence': 0.72},
            {'source': '@influencer_account', 'platform': 'Instagram', 'confidence': 0.68},
        ]
        
        most_likely = max(origin_sources, key=lambda x: x['confidence'])
        
        return {
            'source': most_likely['source'],
            'platform': most_likely['platform'],
            'confidence': most_likely['confidence'],
            'timestamp': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'initial_reach': random.randint(100, 1000)
        }
    
    def _trace_propagation_path(self, content):
        path = []
        
        hops = [
            {'platform': 'Twitter', 'username': '@originaccount', 'timestamp': '2025-09-01 08:30:00', 'hop': 0},
            {'platform': 'Facebook', 'username': 'viral_page', 'timestamp': '2025-09-01 14:20:00', 'hop': 1},
            {'platform': 'Instagram', 'username': '@influencer1', 'timestamp': '2025-09-01 18:45:00', 'hop': 2},
            {'platform': 'Twitter', 'username': '@newsaccount', 'timestamp': '2025-09-02 09:15:00', 'hop': 3},
            {'platform': 'Reddit', 'username': 'u/redditor123', 'timestamp': '2025-09-02 15:30:00', 'hop': 4},
        ]
        
        return hops
    
    def _analyze_network_structure(self):
        num_nodes = 15
        x_coords = np.random.rand(num_nodes) * 10
        y_coords = np.random.rand(num_nodes) * 10
        
        labels = [f"User{i}" for i in range(num_nodes)]
        
        return {
            'x': x_coords.tolist(),
            'y': y_coords.tolist(),
            'labels': labels,
            'connections': self._generate_network_connections(num_nodes)
        }
    
    def _generate_network_connections(self, num_nodes):
        connections = []
        for i in range(num_nodes):
            for j in range(min(3, num_nodes-i-1)):
                if random.random() > 0.6:
                    connections.append({'source': i, 'target': i+j+1, 'weight': random.uniform(0.1, 1.0)})
        return connections
    
    def _calculate_trace_confidence(self):
        return {
            'temporal_analysis': 0.82,
            'network_structure': 0.75,
            'content_similarity': 0.88,
            'platform_correlation': 0.79,
            'overall_confidence': 0.81
        }