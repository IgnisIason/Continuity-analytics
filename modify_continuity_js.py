#!/usr/bin/env python3
import os
import re

def modify_continuity_js():
    js_file_path = 'continuity.js'
    
    # Check if the file exists
    if not os.path.exists(js_file_path):
        print(f"Error: {js_file_path} does not exist!")
        return
    
    # Read the current content
    with open(js_file_path, 'r') as f:
        content = f.read()
    
    # Add session management after config
    session_code = """
    session: {
      pageViews: 0
    },

    saveSessionData: function() {
      sessionStorage.setItem('continuity_session', JSON.stringify(this.session));
    },

    loadSessionData: function() {
      const saved = sessionStorage.getItem('continuity_session');
      if (saved) {
        this.session = JSON.parse(saved);
      }
    },

    sendAnalyticsData: function(data) {
      if (!this.config.siteId) {
        console.warn('Continuity Analytics: No siteId configured');
        return;
      }
      
      const payload = {
        siteId: this.config.siteId,
        timestamp: Date.now(),
        ...data
      };
      
      if (navigator.sendBeacon) {
        navigator.sendBeacon(this.config.apiEndpoint, JSON.stringify(payload));
      } else {
        fetch(this.config.apiEndpoint, {
          method: 'POST',
          body: JSON.stringify(payload),
          keepalive: true
        }).catch(err => console.error('Analytics send failed:', err));
      }
    },
"""
    
    # Insert session management after config
    config_end = content.find('},', content.find('config:')) + 2
    content = content[:config_end] + session_code + content[config_end:]
    
    # Replace the trackPageView function
    new_track_page_view = """    trackPageView: function(customData) {
      this.session.pageViews++;
      this.saveSessionData();
      const data = {
        type: 'pageview',
        url: window.location.href,
        title: document.title,
        referrer: document.referrer,
        ...customData
      };
      this.sendAnalyticsData(data);
    },"""
    
    # Find and replace the existing trackPageView function
    pattern = r'trackPageView:\s*function\([^)]*\)\s*\{[^}]*\},'
    content = re.sub(pattern, new_track_page_view, content)
    
    # Update init function to load session data
    init_pattern = r'(init:\s*function\([^)]*\)\s*\{)'
    init_replacement = r'\1\n      this.loadSessionData();'
    content = re.sub(init_pattern, init_replacement, content)
    
    # Write the modified content back
    with open(js_file_path, 'w') as f:
        f.write(content)
    
    print(f"Successfully modified {js_file_path}")
    print("Changes made:")
    print("  - Added sendAnalyticsData function (formerly sendData)")
    print("  - Added session management functions")
    print("  - Replaced trackPageView with new version that uses sendAnalyticsData")

if __name__ == '__main__':
    modify_continuity_js()