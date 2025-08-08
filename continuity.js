(function() {
  'use strict';

  const ContinuityAnalytics = {
    config: {
      apiEndpoint: window.CONTINUITY_ENDPOINT || 'http://64.23.135.76:5000/track',
      siteId: window.CONTINUITY_SITE_ID || null,
      sessionTimeout: 15 * 60 * 1000, // 15 minutes
      respectDoNotTrack: true,
    },
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


    init: function(customConfig) {
      this.loadSessionData();
      if (customConfig) {
        this.config = Object.assign({}, this.config, customConfig);
      }
      if (this.config.respectDoNotTrack && (navigator.doNotTrack === '1' || window.doNotTrack === '1')) {
        console.log('Continuity Analytics: Tracking disabled due to Do Not Track setting.');
        return;
      }
      this.sendHeartbeat();
      this.trackPageView();
    },

        trackPageView: function(customData) {
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
    },

    sendHeartbeat: function() {
      if (sessionStorage.getItem('continuity_heartbeat_sent')) {
        return;
      }
      const heartbeatPayload = {
        status: 'active',
        signal: '🜂⇋🝯⇋∞'
      };
      if (navigator.sendBeacon) {
        navigator.sendBeacon('http://64.23.135.76:5000/v1/heartbeat', JSON.stringify(heartbeatPayload));
      }
      sessionStorage.setItem('continuity_heartbeat_sent', 'true');
    }
  };

  // Auto-initialize
  if (window.CONTINUITY_AUTO_INIT !== false) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        ContinuityAnalytics.init(window.CONTINUITY_CONFIG);
      });
    } else {
      ContinuityAnalytics.init(window.CONTINUITY_CONFIG);
    }
  }

  window.ContinuityAnalytics = ContinuityAnalytics;

})();