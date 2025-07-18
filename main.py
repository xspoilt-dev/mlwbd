from mlwbd import search_movie, get_download_links, get_main_link_
import streamlit as st 

st.set_page_config(page_title="MLWBD Scraper", page_icon="🎬", layout="wide")

st.title("🎬 MLWBD - Movie Scraper")
st.markdown("Search for movies and get download links easily!")

# Initialize session state
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'download_links' not in st.session_state:
    st.session_state.download_links = None
if 'direct_links' not in st.session_state:
    st.session_state.direct_links = {}

# Movie Search Section
st.header("🔍 Search Movies")
movie = st.text_input("Enter movie name:", placeholder="e.g., Avengers, Spider-Man, etc.")

if movie:
    with st.spinner("Searching for movies..."):
        try:
            results = search_movie(movie)
            
            if results:
                st.success(f"Found {len(results)} movies!")
                
                # Display results in columns
                cols = st.columns(3)
                for i, result in enumerate(results):
                    with cols[i % 3]:
                        st.subheader(result['title'])
                        if result['image']:
                            st.image(result['image'], use_container_width=True)
                        else:
                            st.info("No image available")
                        
                        if st.button(f"Get Download Links", key=f"btn_{i}"):
                            st.session_state.selected_movie = result
                            st.session_state.download_links = None
                            st.session_state.direct_links = {}
                            st.rerun()
                        
                        with st.expander("View Details"):
                            st.markdown(f"**Original Link:** [View on Site]({result['link']})")
                        st.markdown("---")
            else:
                st.warning("No movies found. Try a different search term.")
                
        except Exception as e:
            st.error(f"Error searching movies: {str(e)}")
            st.exception(e)

# Download Links Section
if st.session_state.selected_movie:
    st.header("📥 Download Links")
    
    # Movie info card
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.selected_movie['image']:
            st.image(st.session_state.selected_movie['image'], use_container_width=True)
    with col2:
        st.subheader(st.session_state.selected_movie['title'])
        st.markdown(f"**Source:** [View Original]({st.session_state.selected_movie['link']})")
        
        if st.button("🔄 Search Another Movie", type="secondary"):
            st.session_state.selected_movie = None
            st.session_state.download_links = None
            st.session_state.direct_links = {}
            st.rerun()
    
    if st.session_state.download_links is None:
        with st.spinner("Fetching download links..."):
            try:
                links = get_download_links(st.session_state.selected_movie['link'])
                st.session_state.download_links = links
                st.rerun()
            except Exception as e:
                st.error(f"Error fetching download links: {str(e)}")
                st.exception(e)
                st.session_state.download_links = []
    
    if st.session_state.download_links:
        st.success(f"Found {len(st.session_state.download_links)} download options!")
        
        # Display download links
        for i, link_group in enumerate(st.session_state.download_links):
            title = link_group.get('title', f'Download Option {i+1}')
            with st.expander(f"📁 {title}", expanded=True):
                
                # Handle different link structures
                if 'links' in link_group:
                    # Structured links with labels
                    st.markdown("**Available Downloads:**")
                    for j, link in enumerate(link_group['links']):
                        col1, col2, col3 = st.columns([3, 2, 2])
                        with col1:
                            st.markdown(f"**{link.get('label', 'Unknown')}**")
                        with col2:
                            st.markdown(f"`{link.get('type', 'Unknown')}`")
                        with col3:
                            link_key = f"direct_{i}_{j}"
                            if st.button("🔗 Get Direct Link", key=link_key):
                                with st.spinner("Getting direct download link..."):
                                    try:
                                        direct_link = get_main_link_(link['url'])
                                        st.session_state.direct_links[link_key] = direct_link
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error getting direct link: {str(e)}")
                            
                            # Show direct link if available
                            if link_key in st.session_state.direct_links:
                                st.success("✅ Direct link ready!")
                                st.code(st.session_state.direct_links[link_key])
                
                elif 'quality' in link_group:
                    # Quality-based links
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.markdown(f"**{link_group.get('quality', 'Unknown Quality')}**")
                    with col2:
                        st.markdown(f"`{link_group.get('type', 'Unknown')}`")
                    with col3:
                        link_key = f"direct_quality_{i}"
                        if st.button("🔗 Get Direct Link", key=link_key):
                            with st.spinner("Getting direct download link..."):
                                try:
                                    direct_link = get_main_link_(link_group['link'])
                                    st.session_state.direct_links[link_key] = direct_link
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error getting direct link: {str(e)}")
                        
                        # Show direct link if available
                        if link_key in st.session_state.direct_links:
                            st.success("✅ Direct link ready!")
                            st.code(st.session_state.direct_links[link_key])
                
                else:
                    # Fallback for any other structure
                    st.json(link_group)
    
    elif st.session_state.download_links == []:
        st.warning("No download links found for this movie.")
        st.info("Try searching for a different movie or check the original link manually.")

# Manual Link Input Section
st.header("🔗 Manual Link Input")
st.markdown("If you have a direct movie link, paste it here:")

manual_link = st.text_input("Enter movie link:", placeholder="https://fojik.com/movie-name")

if manual_link:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Get Download Links", type="primary"):
            with st.spinner("Fetching download links..."):
                try:
                    links = get_download_links(manual_link)
                    st.success("Links fetched successfully!")
                    
                    # Display the links in a nice format
                    for i, link_group in enumerate(links):
                        with st.expander(f"Download Option {i+1}"):
                            if isinstance(link_group, dict):
                                for key, value in link_group.items():
                                    st.markdown(f"**{key.title()}:** {value}")
                            else:
                                st.write(link_group)
                    
                    # Also show raw JSON for debugging
                    with st.expander("Raw JSON Data"):
                        st.json(links)
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.exception(e)
    
    with col2:
        if st.button("🔗 Get Direct Link", type="secondary"):
            with st.spinner("Getting direct download link..."):
                try:
                    direct_link = get_main_link_(manual_link)
                    st.success("Direct link obtained!")
                    st.code(direct_link)
                    st.info("💡 You can copy the link above by clicking on it")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.exception(e)

with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Search Movies**: Enter a movie name in the search box
    2. **Select Movie**: Click "Get Download Links" on your desired movie
    3. **Get Links**: Click "Get Direct Link" for each download option
    4. **Manual Input**: Paste direct movie links for quick access
    """)
    
    st.header("ℹ️ About")
    st.markdown("""
    This tool helps you find and extract download links from MLWBD movies.
    
    **Features:**
    - Movie search functionality
    - Multiple download options
    - Direct link extraction
    - Manual link processing
    """)
    
    st.header("⚠️ Important")
    st.warning("This tool is for educational purposes only. Please respect copyright laws and terms of service.")

# Footer
st.markdown("---")
st.markdown("**MLWBD Movie Scraper** - Made with ❤️ using Streamlit")