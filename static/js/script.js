// JavaScript for MLWBD Movie Scraper

class MLWBDScraper {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupTooltips();
    }

    bindEvents() {
        // Search form
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', this.handleSearch.bind(this));
        }

        // Manual link buttons
        const getLinksBtn = document.getElementById('getLinksBtn');
        const getDirectBtn = document.getElementById('getDirectBtn');

        if (getLinksBtn) {
            getLinksBtn.addEventListener('click', this.handleManualLinks.bind(this));
        }

        if (getDirectBtn) {
            getDirectBtn.addEventListener('click', this.handleManualDirect.bind(this));
        }

        // Copy to clipboard functionality
        this.setupCopyButtons();
    }

    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    setupCopyButtons() {
        // Add copy functionality to code blocks and input fields
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('copy-btn') || e.target.closest('.copy-btn')) {
                const btn = e.target.classList.contains('copy-btn') ? e.target : e.target.closest('.copy-btn');
                const target = btn.getAttribute('data-target');
                const element = document.querySelector(target);
                
                if (element) {
                    const text = element.value || element.textContent;
                    navigator.clipboard.writeText(text).then(() => {
                        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        setTimeout(() => {
                            btn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                        }, 2000);
                    });
                }
            }
        });
    }

    async handleSearch(e) {
        e.preventDefault();
        
        const query = document.getElementById('movieQuery').value.trim();
        if (!query) {
            this.showAlert('Please enter a movie name', 'warning');
            return;
        }

        this.showLoading('Searching for movies...');
        this.hideAlert();

        try {
            const formData = new FormData();
            formData.append('query', query);

            const response = await fetch('/search', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.displaySearchResults(data.results);
                if (data.results.length > 0) {
                    this.showAlert(`Found ${data.results.length} movies!`, 'success');
                } else {
                    this.showAlert('No movies found. Try a different search term.', 'info');
                }
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('Failed to search movies: ' + error.message, 'danger');
        } finally {
            this.hideLoading();
        }
    }

    async handleManualLinks() {
        const url = document.getElementById('manualLink').value.trim();
        if (!url) {
            this.showAlert('Please enter a valid URL', 'warning');
            return;
        }

        await this.getMovieLinks(url, 'manualResults');
    }

    async handleManualDirect() {
        const url = document.getElementById('manualLink').value.trim();
        if (!url) {
            this.showAlert('Please enter a valid URL', 'warning');
            return;
        }

        await this.getDirectLink(url, 'manualResults');
    }

    showLoading(message = 'Loading...') {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.style.display = 'block';
            const messageEl = spinner.querySelector('p');
            if (messageEl) {
                messageEl.textContent = message;
            }
        }
    }

    hideLoading() {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            spinner.style.display = 'none';
        }
    }

    showAlert(message, type = 'info') {
        let alertEl = document.getElementById('globalAlert');
        
        if (!alertEl) {
            alertEl = document.createElement('div');
            alertEl.id = 'globalAlert';
            alertEl.className = 'alert alert-dismissible fade show';
            alertEl.innerHTML = `
                <span id="globalAlertMessage"></span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Insert after search form or at top of main content
            const searchResults = document.getElementById('searchResults');
            if (searchResults && searchResults.parentNode) {
                searchResults.parentNode.insertBefore(alertEl, searchResults);
            }
        }

        alertEl.className = `alert alert-${type} alert-dismissible fade show`;
        document.getElementById('globalAlertMessage').textContent = message;
        
        // Auto-hide success and info alerts
        if (type === 'success' || type === 'info') {
            setTimeout(() => {
                this.hideAlert();
            }, 5000);
        }
    }

    hideAlert() {
        const alertEl = document.getElementById('globalAlert');
        if (alertEl) {
            alertEl.style.display = 'none';
        }
    }

    displaySearchResults(results) {
        const container = document.getElementById('searchResults');
        if (!container) return;

        if (results.length === 0) {
            container.innerHTML = '<div class="alert alert-info">No movies found. Try a different search term.</div>';
            return;
        }

        let html = '<div class="row">';
        results.forEach((movie, index) => {
            html += this.createMovieCard(movie, index);
        });
        html += '</div>';
        
        container.innerHTML = html;
        
        // Add smooth scroll to results
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    createMovieCard(movie, index) {
        const imageHtml = movie.image ? 
            `<img src="${movie.image}" class="card-img-top" style="height: 300px; object-fit: cover;" alt="${movie.title}" loading="lazy">` :
            `<div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 300px;">
                <i class="fas fa-film text-muted" style="font-size: 4rem;"></i>
            </div>`;

        return `
            <div class="col-md-4 mb-4">
                <div class="card h-100 shadow-sm movie-card">
                    ${imageHtml}
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title text-truncate-2">${this.escapeHtml(movie.title)}</h5>
                        <div class="mt-auto">
                            <button class="btn btn-primary btn-sm me-2" onclick="mlwbd.openMovieModal('${this.escapeHtml(movie.link)}', '${this.escapeHtml(movie.title)}')">
                                <i class="fas fa-download me-1"></i>Get Links
                            </button>
                            <a href="${movie.link}" target="_blank" class="btn btn-outline-secondary btn-sm" rel="noopener">
                                <i class="fas fa-external-link-alt me-1"></i>View
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    openMovieModal(movieUrl, movieTitle) {
        const modal = new bootstrap.Modal(document.getElementById('movieModal'));
        const titleEl = document.querySelector('#movieModal .modal-title');
        const contentEl = document.getElementById('movieModalContent');

        titleEl.innerHTML = `<i class="fas fa-download me-2"></i>${this.escapeHtml(movieTitle)}`;
        contentEl.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Fetching download links...</p>
            </div>
        `;
        
        modal.show();
        this.getMovieLinks(movieUrl, 'movieModalContent');
    }

    async getMovieLinks(url, targetId) {
        try {
            const response = await fetch('/get-links', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();
            const target = document.getElementById(targetId);

            if (data.success) {
                this.displayDownloadLinks(data.links, targetId);
            } else {
                target.innerHTML = `<div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>Error: ${this.escapeHtml(data.error)}
                </div>`;
            }
        } catch (error) {
            document.getElementById(targetId).innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>Error: ${this.escapeHtml(error.message)}
                </div>
            `;
        }
    }

    displayDownloadLinks(links, targetId) {
        const target = document.getElementById(targetId);
        
        if (!links || links.length === 0) {
            target.innerHTML = '<div class="alert alert-warning"><i class="fas fa-info-circle me-2"></i>No download links found.</div>';
            return;
        }

        let html = '';
        links.forEach((linkGroup, index) => {
            html += this.createLinkGroup(linkGroup, index);
        });

        target.innerHTML = html;
    }

    createLinkGroup(linkGroup, index) {
        const title = linkGroup.title || `Download Option ${index + 1}`;
        
        let html = `
            <div class="card mb-3">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-folder me-2"></i>${this.escapeHtml(title)}</h6>
                </div>
                <div class="card-body">
        `;

        if (linkGroup.links && Array.isArray(linkGroup.links)) {
            linkGroup.links.forEach((link, linkIndex) => {
                const linkId = `direct-${index}-${linkIndex}`;
                html += `
                    <div class="row align-items-center mb-2">
                        <div class="col-md-4">
                            <strong>${this.escapeHtml(link.label || 'Unknown')}</strong>
                        </div>
                        <div class="col-md-4">
                            <code>${this.escapeHtml(link.type || 'Unknown')}</code>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-sm btn-outline-primary" onclick="mlwbd.getDirectLink('${this.escapeHtml(link.url)}', '${linkId}')">
                                <i class="fas fa-link me-1"></i>Get Direct
                            </button>
                            <div id="${linkId}" class="mt-2"></div>
                        </div>
                    </div>
                `;
            });
        } else if (linkGroup.quality) {
            const linkId = `direct-quality-${index}`;
            html += `
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <strong>${this.escapeHtml(linkGroup.quality)}</strong>
                    </div>
                    <div class="col-md-4">
                        <code>${this.escapeHtml(linkGroup.type || 'Unknown')}</code>
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-sm btn-outline-primary" onclick="mlwbd.getDirectLink('${this.escapeHtml(linkGroup.link)}', '${linkId}')">
                            <i class="fas fa-link me-1"></i>Get Direct
                        </button>
                        <div id="${linkId}" class="mt-2"></div>
                    </div>
                </div>
            `;
        }

        html += '</div></div>';
        return html;
    }

    async getDirectLink(url, targetId) {
        const target = document.getElementById(targetId);
        if (!target) return;

        target.innerHTML = '<div class="spinner-border spinner-border-sm text-primary" role="status"></div>';

        try {
            const response = await fetch('/direct-link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (data.success) {
                const linkId = `link-${Date.now()}`;
                target.innerHTML = `
                    <div class="alert alert-success alert-sm mb-0">
                        <i class="fas fa-check me-2"></i>Direct link ready!
                        <div class="mt-2 input-group input-group-sm">
                            <input type="text" id="${linkId}" class="form-control" value="${this.escapeHtml(data.direct_link)}" readonly>
                            <button class="btn btn-outline-secondary copy-btn" data-target="#${linkId}" type="button">
                                <i class="fas fa-copy"></i> Copy
                            </button>
                        </div>
                    </div>
                `;
            } else {
                target.innerHTML = `
                    <div class="alert alert-danger alert-sm mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>Error: ${this.escapeHtml(data.error)}
                    </div>
                `;
            }
        } catch (error) {
            target.innerHTML = `
                <div class="alert alert-danger alert-sm mb-0">
                    <i class="fas fa-exclamation-triangle me-2"></i>Error: ${this.escapeHtml(error.message)}
                </div>
            `;
        }
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Utility methods
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.mlwbd = new MLWBDScraper();
});

// Global functions for inline event handlers
window.openMovieModal = function(movieUrl, movieTitle) {
    if (window.mlwbd) {
        window.mlwbd.openMovieModal(movieUrl, movieTitle);
    }
};

window.getDirectLink = function(url, targetId) {
    if (window.mlwbd) {
        window.mlwbd.getDirectLink(url, targetId);
    }
};
