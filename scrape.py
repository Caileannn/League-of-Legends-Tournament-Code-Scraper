from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
import sys

def navigate_to_tournament_page(page, username, password, tournament_name):
    # Login to Organiser Account
	page.goto('https://organizer.toornament.com/en_GB/login/')
	try:
		page.fill('input#_username', str(username))
		page.fill('input#_password', str(password))
		page.click('button[type=submit]')
		try:
			page.locator(tournament_name).click()
			page.get_by_alt_text('League Of Legends').click()
			# Create match list URL string
			current_url = page.url
			current_url = current_url + "matches"
			return current_url
		except:
			print("No tournament found.")
			return
	except:
		print("Username & Password is incorrect!")
		return
	

def fetch_urls(url_current, pagination_num, page):
    # For each page, fecth match URLs
	bar = IncrementalBar('✨ Fetching URLs', max=pagination_num)
	list_of_final_urls = []
	while pagination_num > 0:
		new_url = url_current + "/?page=" + str(pagination_num)
		page.goto(new_url)
		html = page.inner_html('section.content')
		soup = BeautifulSoup(html, 'html.parser')
		# Find <a> and their hrefs, append to list and exclude page links
		for x in soup.find_all('div', class_='size-content'):
			for a in x.find_all('a'):
				list_of_final_urls.append(a['href'].strip(""))
		pagination_num = pagination_num - 1
		bar.next()
	bar.finish()
	return list_of_final_urls

def fetch_codes(url_list, page):
    list_of_codes = []
    bar = IncrementalBar('✨ Fetching Codes', max=len(url_list))
    for url in url_list:
        try:
            if(len(url) > 80 ):
                page.goto("https://organizer.toornament.com" + str(url))
                page.click('button[type=button]')
                page.get_by_role("link", name="Tournament Codes").click()
                html = page.inner_html('table.table.hover.rows')
                soup = BeautifulSoup(html, 'html.parser')
                res = soup.find_all('td', class_="data")
                list_of_codes.append(res[1].text)
            else:
                pass
        except:
            pass
        bar.next()
    bar.finish()
    return list_of_codes

def write_codes_to_file(codes, name):
    new_code_list = []
    with open(str(name), 'w') as f:
        for code in codes:
            if code != 'No code':
                new_code_list.append(code)
                newer_list = list(filter(None, new_code_list))
                for code in newer_list:
                    f.write(f"{code},")
    
def fetch(file_name, pagination_number, headless, username, password, tournament_name):
    # Create Async Loop
	with sync_playwright() as p:
		# Launch Browser
		browser = p.chromium.launch(headless=headless)
		page = browser.new_page()
		try:
			print("🗺️  Navigating to tournament page..")
			tournament_url = navigate_to_tournament_page(page, username, password, tournament_name)
			try:
				list_of_match_urls = fetch_urls(tournament_url, pagination_number, page)
			except:
				print("Error fetching inital URLs. Please make sure your pagenation number is correct.")
				return
			try:
				list_of_codes = fetch_codes(list_of_match_urls, page)
			except:
				print("Error fetching tournament codes.")
				return
			try:
				print("✍️  Writing codes to .csv file")
				write_codes_to_file(list_of_codes, file_name)
				print("✅ Done!")
			except:
				print("Error writing codes to file")
				return
		except:
			print("Error, ending routine.")
			return

		
def main():
    file_name = 'tournament_code_list.csv'
    username = str(sys.argv[1])
    password = str(sys.argv[2])
    tournament_name = "'" + str(sys.argv[3]) + "'"
    pag_num = int(sys.argv[4])
    headerless_boolean = sys.argv[5]
    headerless = None
    if headerless_boolean == "False":
        headerless = False
    else:
        headerless = True
    fetch(file_name, pag_num, headerless, username, password, tournament_name)
		
       

if __name__ == "__main__":
    main()