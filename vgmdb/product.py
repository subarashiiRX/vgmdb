import bs4

from . import utils

def parse_product_page(html_source):
	product_info = {}
	soup = bs4.BeautifulSoup(html_source)
	soup_profile = soup.find(id='innermain')

	soup_name = soup_profile.h1
	product_info['name'] = soup_name.span.string.strip()
	soup_real_name = soup_profile.find(id='subtitle')
	if soup_real_name:
		soup_real_name = soup_real_name.span
		if len(soup_real_name.contents) == 1:
			product_info['name_real'] = soup_real_name.string
		elif len(soup_real_name.contents) > 1:
			product_info['name_real'] = soup_real_name.contents[0].string

	soup_profile = soup_profile.find(id='innercontent').find(id='innermain')
	soup_profile_sections = soup_profile.find_all('div', recursive=False)

	soup_profile_info = soup_profile_sections[1].div.dl
	product_info.update(_parse_product_info(soup_profile_info))

	soup_section_heads = soup_profile.find_all('h3', recursive=False)
	for soup_section_head in soup_section_heads:
		section_name = soup_section_head.string
		soup_section = soup_section_head.find_next_sibling('div')
		if section_name == 'Releases':
			product_info['releases'] = _parse_product_releases(soup_section.div.table)
		if section_name == 'Albums | Credits':
			product_info['albums'] = utils.parse_discography(soup_section.div.table, 'classifications')

	return product_info

def _parse_product_info(soup_profile_info):
	""" Receives a dl list from a product's info box """
	product_info = {}
	name = None
	value = None
	for soup_child in soup_profile_info:
		if not isinstance(soup_child, bs4.Tag):
			continue
		if soup_child.name == 'dt':
		   	name = soup_child.b.string
			value = None
		if soup_child.name == 'dd':
			if soup_child.div:
				value = []
				for soup_child_div in soup_child.find_all('div', recursive=False):
					for soup_child_link in soup_child_div.find_all('a', recursive=False):
						item = {}
						item['name'] = utils.parse_names(soup_child_link)
						item['link'] = soup_child_link['href']
						value.append(item)
			else:
				value = soup_child.string

			if name == 'Franchises' and isinstance(value, list):
				product_info['franchises'] = value
			if name == 'Release Date' and value != None:
				product_info['release_date'] = utils.parse_date_time(value)
			if name == 'Organizations' and value != None:
				if isinstance(value, list):
					product_info['organizations'] = value
				else:
					product_info['organizations'] = [value]
			if name == 'Description' and value != None:
				product_info['description'] = value
	return product_info

def _parse_product_releases(soup_table):
	releases = []
	if not soup_table:
		return releases
	soup_rows = soup_table.find_all('tr', recursive=False)
	if len(soup_rows) == 0:
		return releases
	for soup_row in soup_rows[1:]:
		soup_cells = soup_row.find_all('td', recursive=False)
		release = {}
		release['date'] = utils.normalize_dashed_date(soup_cells[0].span.string)
		release['name'] = utils.parse_names(soup_cells[1].span)
		release['region'] = soup_cells[2].span.string
		release['platform'] = soup_cells[3].span.string
		releases.append(release)
	releases = sorted(releases, key=lambda e:e['date'])
	return releases
