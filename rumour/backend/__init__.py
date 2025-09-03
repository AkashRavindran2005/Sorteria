# backend/__init__.py (create this file)
from .fact_checker import FactChecker
from .social_monitor import SocialMonitor  
from .viral_tracker import ViralTracker
from .origin_tracer import OriginTracer

__all__ = ['FactChecker', 'SocialMonitor', 'ViralTracker', 'OriginTracer']
