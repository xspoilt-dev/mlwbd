# 🎬 MLWBD Movie Scraper

A Flask web application for searching movies and extracting download links from MLWBD websites. Built with Python Flask, Bootstrap 5, and modern web technologies.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

- 🔍 **Movie Search**: Search for movies with intelligent filtering
- 📥 **Download Links**: Extract multiple download options
- 🔗 **Direct Links**: Generate direct download links
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🎯 **RESTful API**: Complete API endpoints for integration
- ⚡ **Fast & Efficient**: Optimized scraping with caching
- 🎨 **Modern UI**: Clean, intuitive interface with Bootstrap 5

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xspoilt-dev/mlwbd.git
   cd mlwbd
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Web Interface

1. **Search Movies**: Enter a movie name in the search box
2. **Select Movie**: Click "Get Download Links" on your desired movie
3. **Get Links**: Click "Get Direct Link" for each download option
4. **Manual Input**: Paste direct movie links for quick access

### API Endpoints

#### Search Movies
```http
GET /api/search?q=movie_name
```

#### Get Download Links
```http
GET /api/links?url=movie_url
```

#### Get Direct Link
```http
GET /api/direct?url=link_url
```

### Example API Usage

```python
import requests

# Search for movies
response = requests.get('http://localhost:5000/api/search?q=avengers')
movies = response.json()

# Get download links
response = requests.get('http://localhost:5000/api/links?url=movie_url')
links = response.json()

# Get direct link
response = requests.get('http://localhost:5000/api/direct?url=link_url')
direct_link = response.json()
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **Requests** - HTTP library for API calls
- **BeautifulSoup** - HTML parsing and scraping
- **Gunicorn** - WSGI HTTP Server (for production)

### Frontend
- **Bootstrap 5** - CSS framework
- **Font Awesome** - Icons
- **Vanilla JavaScript** - Interactive functionality

## 📁 Project Structure

```
mlwbd/
├── app.py                 # Main Flask application
├── mlwbd.py              # Core scraping module
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── script.js    # JavaScript functionality
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── about.html       # About page
    └── error.html       # Error pages
```

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
export FLASK_ENV=development  # or production
export FLASK_DEBUG=1          # Enable debug mode
export PORT=5000              # Port number
```

### Customization

- Modify `static/css/style.css` for custom styling
- Update `static/js/script.js` for additional functionality
- Edit templates in `templates/` for UI changes

## 🚀 Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 📊 API Documentation

### Response Format

All API endpoints return JSON responses in the following format:

```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

### Error Handling

Errors are returned with appropriate HTTP status codes:

```json
{
  "success": false,
  "error": "Error message",
  "traceback": "Detailed error information (in debug mode)"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python -m pytest`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is created for educational purposes only. Please respect copyright laws and the terms of service of the websites you interact with. The developers are not responsible for any misuse of this application.

## 👨‍💻 Author

**xspoilt-dev**
- GitHub: [@xspoilt-dev](https://github.com/xspoilt-dev)

## 🌟 Support

If you like this project, please give it a ⭐ on GitHub!

## 📞 Support & Issues

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/xspoilt-dev/mlwbd/issues) page
2. Create a new issue if needed
3. Provide detailed information about the problem

---

**Made with ❤️ by xspoilt-dev**
