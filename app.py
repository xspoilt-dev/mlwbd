from flask import Flask, render_template, request, jsonify, redirect, url_for
from mlwbd import search_movie, get_download_links, get_main_link_
import json
import traceback

app = Flask(__name__)
app.secret_key = 'mlwbd_scraper_secret_key_2025'

@app.route('/')
def index():
    """Home page with search functionality"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Search for movies"""
    try:
        query = request.form.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Please enter a movie name'}), 400
        
        results = search_movie(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/movie/<path:movie_url>')
def movie_details(movie_url):
    """Movie details page"""
    return render_template('movie.html', movie_url=movie_url)

@app.route('/get-links', methods=['POST'])
def get_links():
    """Get download links for a movie"""
    try:
        movie_url = request.json.get('url')
        if not movie_url:
            return jsonify({'error': 'Movie URL is required'}), 400
        
        links = get_download_links(movie_url)
        return jsonify({
            'success': True,
            'links': links,
            'count': len(links) if links else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/direct-link', methods=['POST'])
def direct_link():
    """Get direct download link"""
    try:
        link_url = request.json.get('url')
        if not link_url:
            return jsonify({'error': 'Link URL is required'}), 400
        
        direct_link = get_main_link_(link_url)
        return jsonify({
            'success': True,
            'direct_link': direct_link
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/search')
def api_search():
    """API endpoint for searching movies"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'error': 'Query parameter q is required'}), 400
        
        results = search_movie(query)
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/links')
def api_links():
    """API endpoint for getting download links"""
    try:
        movie_url = request.args.get('url')
        if not movie_url:
            return jsonify({'error': 'URL parameter is required'}), 400
        
        links = get_download_links(movie_url)
        return jsonify({
            'success': True,
            'url': movie_url,
            'links': links,
            'count': len(links) if links else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/direct')
def api_direct():
    """API endpoint for getting direct links"""
    try:
        link_url = request.args.get('url')
        if not link_url:
            return jsonify({'error': 'URL parameter is required'}), 400
        
        direct_link = get_main_link_(link_url)
        return jsonify({
            'success': True,
            'url': link_url,
            'direct_link': direct_link
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
