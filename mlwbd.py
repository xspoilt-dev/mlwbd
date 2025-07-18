import requests, re, ast, json
from bs4 import BeautifulSoup as bsx
from bs4 import BeautifulSoup

def extract_all_links(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # ========== STRATEGY 1: Structured list with headers ==========
    for tag in soup.find_all(["h2", "p", "strong", "em", "span"]):
        text = tag.get_text(strip=True)
        if any(keyword in text.lower() for keyword in ["epi", "batch", "part"]) or tag.name == "h2":
            title = text
            links = []
            next_sibling = tag.find_next_sibling()
            while next_sibling:
                if next_sibling.name in ["h2", "p"] and any(kw in next_sibling.get_text().lower() for kw in ["epi", "batch", "part"]):
                    break
                if next_sibling.name == "ul":
                    for li in next_sibling.find_all("li"):
                        label = li.get_text(strip=True).split(":")[0]
                        for a in li.find_all("a"):
                            links.append({
                                "label": label,
                                "type": a.get_text(strip=True),
                                "url": a["href"]
                            })
                next_sibling = next_sibling.find_next_sibling()
            if links:
                results.append({"title": title, "links": links})

    # ========== STRATEGY 2: Fallback center-aligned quality/type links ==========
    if not results:
        fallback = []
        quality_blocks = soup.find_all('p', style=re.compile("text-align: center;"))
        for block in quality_blocks:
            text = block.get_text(separator=' ', strip=True)
            links = block.find_all('a')
            hrefs = [(a.text.strip(), a['href']) for a in links if a.get('href')]

            if hrefs and any(ext in text for ext in ['480p', '720p', '1080p']):
                match = re.search(r"([\d.]+(?:MB|GB).*?(480p|720p|1080p))", text, re.IGNORECASE)
                quality = match.group(1).strip() if match else "Unknown"
                for link_text, link_url in hrefs:
                    fallback.append({
                        "quality": quality,
                        "type": link_text,
                        "link": link_url
                    })
        return fallback 

    return results

def search_movie(text):
    cookies = {
        'starstruck_c64520dd9f1cfb797aa415c1816a487c': '17056c72fb574b1051c60a2706bd4d07',
        'cf_clearance': 'NunVbXqcDNvo09Xs5c63zOt0K4K4GclzRsLXDDQWv2E-1745647886-1.2.1.1-gVDTFu3OhRXXm0YTtWRHth_XWJEZcuXSItfxvnWqfBUm4kG9FI5HJOWEeIDBZ2_Ob8q4x.VwB_oxJh59ut_FQUSZio1Y4sBh5WHjtxsVL0c2yftAU5lVqEGQKStDNj8i.pQG3aZ4bcAdakso5XXHTeuV2ZIPhUsm8xbVKPRyVZkM4.3paqJeCDY7EoDxHA_8gg2h7Cc.anyPtfN0JuX9Mvs6gg7SYP5fMVL02XyinNpmdfOOWAxIswRtLmih6o_Kbr4vU.oz4DdeL9p0fg2gP8RNLwtoQeDT7k4RCcP45pTkRWei1P4yfOoBJf5RGMdoqaeEgh5RVptJlvO32RifsIJ4MMatkc35b_UVwVa91so',
        'aiADB': 'cfcdbee',
        'prefetchAd_7970848': 'true',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.6',
        'priority': 'u=0, i',
        'referer': 'https://fojik.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    }
    params = {'s': text}
    resp = requests.get('https://fojik.com/', params=params, cookies=cookies, headers=headers)
    soup = bsx(resp.text, 'html.parser')
    movies_div = soup.find_all('div', class_='result-item')
    results = []
    for movie_div in movies_div:
        a_tag = movie_div.find('a', href=True)
        img_tag = movie_div.find('img', src=True)
        title_tag = movie_div.find('div', class_='title')
        if title_tag and title_tag.a:
            title = title_tag.a.get_text(strip=True)
        elif img_tag and img_tag.get('alt'):
            title = img_tag['alt']
        else:
            title = ''
        link = a_tag['href'] if a_tag else ''
        image = img_tag['src'] if img_tag else ''
        results.append({
            'title': title,
            'image': image,
            'link': link
        })
    return results

def get_download_links(url):
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=default_headers)
    soup = bsx(response.text, 'html.parser')
    FU = soup.find('input', {'type': 'hidden', 'name': 'FU'})['value']
    FN = soup.find('input', {'type': 'hidden', 'name': 'FN'})['value']

    response = requests.post("https://search.technews24.site/blog.php", headers=default_headers, data={'FU': FU, 'FN': FN})
    soup = bsx(response.text, 'html.parser')
    FU2 = soup.find('input', {'type': 'hidden', 'name': 'FU2'})['value']

    response = requests.post("https://freethemesy.com/dld.php", headers=default_headers, data={'FU2': FU2})
    ss = re.search(r"var sss = '(.*?)'; var", response.text).group(1)
    fetch_str_list = re.search(r"_0x12fb2a=(.*?);_0x3073", response.text).group(1)
    fetch_str_list = ast.literal_eval(fetch_str_list)
    v = fetch_str_list[18]

    final_url = "https://freethemesy.com/new/l/api/m"
    payload = {'s': ss, 'v': v}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://freethemesy.com/dld.php",
        "Origin": "https://freethemesy.com",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    final_response_down_page = requests.post(final_url, data=payload, headers=headers).text.strip()
    response = requests.get(final_response_down_page, headers=default_headers)
    soup = bsx(response.text, 'html.parser')
    links = extract_all_links(str(soup))
    if isinstance(links, list):
        filtered_links = []
        for item in links:
            if isinstance(item, dict) and 'links' in item:
                item['links'] = [l for l in item['links'] if '.me' not in l.get('url', '')]
                if item['links']:
                    filtered_links.append(item)
            elif isinstance(item, dict) and 'link' in item:
                if '.me' not in item['link']:
                    filtered_links.append(item)
            elif isinstance(item, dict) and 'url' in item:
                if '.me' not in item['url']:
                    filtered_links.append(item)
        links = filtered_links
    return links

def get_main_link_(url):
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=default_headers)
    FU5 = bsx(response.text, 'html.parser').find('input', {'type': 'hidden', 'name': 'FU5'})['value']
    response = requests.post("https://sharelink-3.site/dld.php", headers=default_headers, data={'FU5': FU5})
    FU7 = bsx(response.text, 'html.parser').find('input', {'type': 'hidden', 'name': 'FU7'})['value']
    response = requests.post("https://sharelink-3.site/blog/", headers=default_headers, data={'FU7': FU7})
    sss = re.search(r"var sss = '(.*?)';", response.text).group(1)
    __v = re.search(r"v: '(.*?)'", response.text).group(1)

    url_api = "https://sharelink-3.site/l/api/m"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = {
        "s": sss,
        "v": __v
    }
    response = requests.post(url_api, headers=headers, data=json.dumps(payload))
    return response.text
