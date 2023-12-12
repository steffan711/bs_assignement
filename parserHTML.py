from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

class HTMLParser:
    """
    A class for parsing HTML files and extracting specific data.
    """

    def parse_html(self, file_name):
        """
        Parses an HTML file and extracts section elements and related data.

        :param file_name: Name of the HTML file to be parsed.
        :return: A dictionary containing parsed data.
        """
        with open(file_name, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            sections = soup.find_all('section')
            file_data = {"records": []}
            element_cache = []

            for section in sections:
                for element in section.descendants:
                    # Exclude certain elements based on specified criteria
                    if not (next(element.parents, None).name == 'a' and element == "#"):
                        element_cache.append(element)
                    if element.name == 'a' and element.get_text(strip=True) == "#":
                        href = element.get('href', '')
                        new_citation_text = self.empty_elem_cache(element_cache, next(element.parents, None), file_data)
                        file_data["records"].append([href, new_citation_text])

            self.empty_elem_cache(element_cache, None, file_data)
            return file_data

    def empty_elem_cache(self, cache, a_tag_first_parent, file_data):
        """
        Empties the cache of elements and processes them into text.

        :param cache: List of elements to be processed.
        :param a_tag_first_parent: The first parent of the 'a' tag.
        :param file_data: The data dictionary to be updated.
        :return: String of processed elements.
        """
        split_index = -1 if not a_tag_first_parent else cache.index(a_tag_first_parent)
        first_part = cache[:split_index]
        if file_data["records"]:
            file_data["records"][-1][1] += ''.join([str(element) for element in first_part if element.name is None])
        second_part = cache[split_index:]
        new_citation_text = ''.join([str(element) for element in second_part if element.name is None])
        cache.clear()
        return new_citation_text

    def crawl_website(self, base_folder, website_address):
        """
        Crawls a website and extracts data from HTML files.

        :param base_folder: The base folder containing HTML files.
        :param website_address: The base URL of the website.
        :return: List of dictionaries with URL and text data.
        """
        base_path = Path(base_folder)
        data = []
        for file in base_path.rglob('*.html'):
            relat_path = str(file.relative_to(base_path))
            for record in self.parse_html(file)["records"]:
                url = urljoin(urljoin(website_address, relat_path.replace('\\', '/')), record[0])
                data.append({"url": url, "text": record[1]})

        return data
