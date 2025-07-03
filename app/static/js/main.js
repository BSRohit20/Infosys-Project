// AI-Driven Guest Experience System - Main JavaScript

class GuestExperienceApp {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initCharts();
        this.loadUserData();
    }

    bindEvents() {
        // Feedback form submission
        const feedbackForm = document.getElementById('feedback-form');
        if (feedbackForm) {
            feedbackForm.addEventListener('submit', this.handleFeedbackSubmission.bind(this));
        }

        // Recommendation loading
        const loadRecommendationsBtn = document.getElementById('load-recommendations');
        if (loadRecommendationsBtn) {
            loadRecommendationsBtn.addEventListener('click', this.loadRecommendations.bind(this));
        }

        // Analytics refresh
        const refreshAnalyticsBtn = document.getElementById('refresh-analytics');
        if (refreshAnalyticsBtn) {
            refreshAnalyticsBtn.addEventListener('click', this.refreshAnalytics.bind(this));
        }

        // Real-time sentiment analysis
        const feedbackTextarea = document.getElementById('comment');
        if (feedbackTextarea) {
            feedbackTextarea.addEventListener('input', this.debounce(this.analyzeSentimentRealTime.bind(this), 500));
        }
    }

    async handleFeedbackSubmission(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Convert FormData to JSON object for API
        const feedbackData = {
            category: formData.get('category'),
            rating: parseInt(formData.get('rating')),
            subject: formData.get('subject'),
            comment: formData.get('comment'),
            location: formData.get('location') || '',
            staff_member: formData.get('staff_member') || '',
            anonymous: formData.get('anonymous') === 'on'
        };

        // Client-side validation
        if (!feedbackData.category) {
            this.showAlert('danger', 'Please select a category');
            return;
        }
        
        if (!feedbackData.rating || feedbackData.rating < 1 || feedbackData.rating > 5) {
            this.showAlert('danger', 'Please select a rating between 1 and 5 stars');
            return;
        }
        
        if (!feedbackData.subject || feedbackData.subject.trim() === '') {
            this.showAlert('danger', 'Please enter a subject for your feedback');
            return;
        }
        
        if (!feedbackData.comment || feedbackData.comment.trim() === '') {
            this.showAlert('danger', 'Please enter your feedback comment');
            return;
        }

        try {
            this.setLoading(submitBtn, true);
            
            const response = await fetch('/api/feedback/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(feedbackData)
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert('success', 'Feedback submitted successfully! Thank you for your input.');
                form.reset();
                
                // Show sentiment analysis result
                if (result.sentiment) {
                    this.displaySentimentResult(result);
                }
                
                // If negative sentiment, show alert was triggered
                if (result.alert_triggered) {
                    this.showAlert('info', 'Alert has been sent to management for immediate attention.');
                }
            } else {
                this.showAlert('danger', 'Failed to submit feedback: ' + (result.detail || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
            this.showAlert('danger', 'Error submitting feedback: ' + error.message);
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    async loadRecommendations(guestId = null) {
        const container = document.getElementById('recommendations-container');
        if (!container) return;

        try {
            this.setLoading(container, true);
            
            const url = guestId ? `/api/recommendations/guest/${guestId}` : '/api/recommendations/default';
            const response = await fetch(url, {
                credentials: 'include'
            });
            const result = await response.json();

            if (response.ok && result.success) {
                this.renderRecommendations(result.data, container);
            } else {
                throw new Error('Failed to load recommendations');
            }
        } catch (error) {
            console.error('Error loading recommendations:', error);
            container.innerHTML = '<div class="alert alert-danger">Failed to load recommendations</div>';
        }
    }

    renderRecommendations(data, container) {
        const { dining, amenities, activities } = data;
        
        const html = `
            <div class="recommendations-grid">
                <div class="recommendation-section">
                    <h3 class="text-primary mb-3">
                        <i class="fas fa-utensils"></i>
                        Dining Recommendations
                    </h3>
                    <div class="grid grid-3">
                        ${dining?.map(item => this.createRecommendationCard(item, 'dining')).join('') || '<p>No dining recommendations available</p>'}
                    </div>
                </div>
                
                <div class="recommendation-section">
                    <h3 class="text-primary mb-3">
                        <i class="fas fa-spa"></i>
                        Amenities
                    </h3>
                    <div class="grid grid-3">
                        ${amenities?.map(item => this.createRecommendationCard(item, 'amenity')).join('') || '<p>No amenity recommendations available</p>'}
                    </div>
                </div>
                
                <div class="recommendation-section">
                    <h3 class="text-primary mb-3">
                        <i class="fas fa-hiking"></i>
                        Activities
                    </h3>
                    <div class="grid grid-3">
                        ${activities?.map(item => this.createRecommendationCard(item, 'activity')).join('') || '<p>No activity recommendations available</p>'}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    createRecommendationCard(item, type) {
        const rating = this.createStarRating(item.rating || 0);
        const score = item.recommendation_score ? Math.round(item.recommendation_score * 100) : 0;
        
        return `
            <div class="card recommendation-card">
                ${item.image ? `<img src="${item.image}" alt="${item.name}" class="recommendation-image" onerror="this.style.display='none'">` : ''}
                <div class="recommendation-score badge badge-info">${score}% match</div>
                <h4 class="mb-2">${item.name}</h4>
                <div class="rating mb-2">${rating}</div>
                <p class="text-muted mb-3">${item.description}</p>
                ${item.specialties ? `
                    <div class="specialties mb-3">
                        ${item.specialties.map(spec => `<span class="badge badge-success mr-1">${spec}</span>`).join('')}
                    </div>
                ` : ''}
                ${item.price_tier ? `<div class="text-sm text-muted">Price: ${this.formatPriceTier(item.price_tier)}</div>` : ''}
            </div>
        `;
    }

    createStarRating(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';
        
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                stars += '<i class="fas fa-star star filled"></i>';
            } else if (i === fullStars && hasHalfStar) {
                stars += '<i class="fas fa-star-half-alt star filled"></i>';
            } else {
                stars += '<i class="far fa-star star"></i>';
            }
        }
        
        return stars;
    }

    formatPriceTier(tier) {
        const tiers = {
            'budget': '$',
            'standard': '$$',
            'premium': '$$$'
        };
        return tiers[tier] || tier;
    }

    async analyzeSentimentRealTime(event) {
        const text = event.target.value;
        const indicator = document.getElementById('sentiment-indicator');
        
        if (!text.trim() || !indicator) return;

        try {
            const response = await fetch(`/api/feedback/analyze?text=${encodeURIComponent(text)}`, {
                credentials: 'include'
            });
            const result = await response.json();

            if (response.ok) {
                this.updateSentimentIndicator(indicator, result);
            }
        } catch (error) {
            console.error('Error analyzing sentiment:', error);
        }
    }

    updateSentimentIndicator(indicator, result) {
        const { sentiment, confidence } = result;
        const confidencePercent = Math.round(confidence * 100);
        
        indicator.className = `sentiment-indicator sentiment-${sentiment}`;
        indicator.innerHTML = `
            <i class="fas fa-${this.getSentimentIcon(sentiment)}"></i>
            ${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)} 
            (${confidencePercent}%)
        `;
    }

    getSentimentIcon(sentiment) {
        const icons = {
            'positive': 'smile',
            'negative': 'frown',
            'neutral': 'meh'
        };
        return icons[sentiment] || 'meh';
    }

    displaySentimentResult(result) {
        const container = document.getElementById('sentiment-result');
        if (!container) return;

        const { sentiment, confidence } = result;
        const confidencePercent = Math.round(confidence * 100);
        
        container.innerHTML = `
            <div class="alert alert-info">
                <strong>Sentiment Analysis:</strong>
                <span class="sentiment-${sentiment}">
                    <i class="fas fa-${this.getSentimentIcon(sentiment)}"></i>
                    ${sentiment.charAt(0).toUpperCase() + sentiment.slice(1)} (${confidencePercent}% confidence)
                </span>
            </div>
        `;
    }

    async refreshAnalytics() {
        const dashboardContainer = document.getElementById('analytics-dashboard');
        if (!dashboardContainer) return;

        try {
            this.setLoading(dashboardContainer, true);
            
            const response = await fetch('/api/analytics/dashboard', {
                credentials: 'include'
            });
            const result = await response.json();

            if (response.ok && result.success) {
                this.renderAnalyticsDashboard(result.data, dashboardContainer);
            } else {
                throw new Error('Failed to load analytics');
            }
        } catch (error) {
            console.error('Error loading analytics:', error);
            this.showAlert('danger', 'Failed to load analytics data');
        }
    }

    renderAnalyticsDashboard(data, container) {
        const { overview, sentiment_analysis, recent_alerts } = data;
        
        const html = `
            <div class="analytics-overview">
                <div class="grid grid-4 mb-4">
                    <div class="card metric-card">
                        <div class="metric-value">${overview.total_guests}</div>
                        <div class="metric-label">Total Guests</div>
                    </div>
                    <div class="card metric-card">
                        <div class="metric-value">${overview.total_feedback}</div>
                        <div class="metric-label">Feedback Received</div>
                    </div>
                    <div class="card metric-card">
                        <div class="metric-value">${overview.average_rating.toFixed(1)}</div>
                        <div class="metric-label">Average Rating</div>
                    </div>
                    <div class="card metric-card">
                        <div class="metric-value text-${overview.alert_count > 0 ? 'danger' : 'success'}">${overview.alert_count}</div>
                        <div class="metric-label">Active Alerts</div>
                    </div>
                </div>
                
                <div class="grid grid-2">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Sentiment Analysis</h3>
                        </div>
                        <div class="sentiment-breakdown">
                            <div class="sentiment-item">
                                <span class="sentiment-positive">Positive:</span>
                                <span>${sentiment_analysis.positive_percentage}%</span>
                            </div>
                            <div class="sentiment-item">
                                <span class="sentiment-neutral">Neutral:</span>
                                <span>${sentiment_analysis.neutral_percentage}%</span>
                            </div>
                            <div class="sentiment-item">
                                <span class="sentiment-negative">Negative:</span>
                                <span>${sentiment_analysis.negative_percentage}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Recent Alerts</h3>
                        </div>
                        <div class="alerts-list">
                            ${recent_alerts.length > 0 ? 
                                recent_alerts.slice(0, 5).map(alert => {
                                    // Handle both old and new alert structure
                                    const priorityClass = alert.priority === 'high' ? 'danger' : 
                                                         alert.priority === 'medium' ? 'warning' : 'info';
                                    const priorityEmoji = alert.priority_emoji || 
                                                         (alert.priority === 'high' ? '🔴' : 
                                                         alert.priority === 'medium' ? '🟡' : '🟢');
                                    const alertTitle = alert.title || `Feedback Alert`;
                                    const alertMessage = alert.message || alert.feedback_text || '';
                                    const guestName = alert.guest_name || alert.guest_id || 'Unknown';
                                    const timestamp = alert.created_at || alert.timestamp || '';
                                    
                                    return `
                                    <div class="alert-item">
                                        <div class="alert-severity badge badge-${priorityClass}">
                                            ${priorityEmoji} ${alert.priority || 'medium'}
                                        </div>
                                        <div class="alert-content">
                                            <div class="alert-title font-weight-bold">${alertTitle}</div>
                                            <div class="alert-text">${alertMessage.substring(0, 80)}${alertMessage.length > 80 ? '...' : ''}</div>
                                            <div class="alert-meta text-muted text-sm">
                                                Guest: ${guestName} | ${new Date(timestamp).toLocaleDateString()}
                                            </div>
                                        </div>
                                    </div>
                                `}).join('') : 
                                '<p class="text-muted">No recent alerts</p>'
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    initCharts() {
        // Initialize any charts if Chart.js is available
        if (typeof Chart !== 'undefined') {
            this.initSentimentChart();
            this.initTrendsChart();
        }
    }

    initSentimentChart() {
        const ctx = document.getElementById('sentiment-chart');
        if (!ctx) return;

        // This would be populated with real data
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [70, 20, 10],
                    backgroundColor: ['#10b981', '#6b7280', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    loadUserData() {
        // Load user-specific data if logged in
        const userInfo = this.getCurrentUser();
        if (userInfo) {
            this.personalizeInterface(userInfo);
        }
    }

    getCurrentUser() {
        // This would typically come from a session or JWT
        const userElement = document.getElementById('current-user-data');
        if (userElement) {
            try {
                return JSON.parse(userElement.textContent);
            } catch (e) {
                return null;
            }
        }
        return null;
    }

    personalizeInterface(user) {
        // Personalize the interface based on user role and preferences
        if (user.role === 'admin') {
            this.showAdminFeatures();
        } else {
            this.loadPersonalizedRecommendations(user.user_id);
        }
    }

    showAdminFeatures() {
        const adminElements = document.querySelectorAll('.admin-only');
        adminElements.forEach(el => el.style.display = 'block');
    }

    async loadPersonalizedRecommendations(userId) {
        await this.loadRecommendations(userId);
    }

    setLoading(element, isLoading) {
        if (isLoading) {
            element.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
        } else {
            // The calling function should handle setting the content
        }
    }

    showAlert(type, message) {
        const alertContainer = document.getElementById('alert-container') || document.body;
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()">&times;</button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Utility functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.guestApp = new GuestExperienceApp();
});

// Export for module use if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GuestExperienceApp;
}
