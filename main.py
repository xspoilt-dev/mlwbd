# Main entry point for MLWBD Movie Scraper
# Use app.py for the Flask application

from mlwbd import search_movie, get_download_links, get_main_link_

if __name__ == "__main__":
    print("🎬 MLWBD Movie Scraper")
    print("Run 'python app.py' to start the Flask web application")
    print("Or use the run.bat/run.sh scripts for easy setup")