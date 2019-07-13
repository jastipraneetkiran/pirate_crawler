from urllib.request import urlopen
from linkseekd import LinkFinder
from domain import *
from casual import *


class Pirate:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Pirate.project_name = project_name
        Pirate.base_url = base_url
        Pirate.domain_name = domain_name
        Pirate.queue_file = Pirate.project_name + '/queue.txt'
        Pirate.crawled_file = Pirate.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Pirate.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_web_dir(Pirate.project_name)
        create_webdata_files(Pirate.project_name, Pirate.base_url)
        Pirate.queue = to_set(Pirate.queue_file)
        Pirate.crawled = to_set(Pirate.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Pirate.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Pirate.queue)) + ' | Crawled  ' + str(len(Pirate.crawled)))
            Pirate.add_links_to_queue(Pirate.gather_links(page_url))
            Pirate.queue.remove(page_url)
            Pirate.crawled.add(page_url)
            Pirate.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Pirate.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Pirate.queue) or (url in Pirate.crawled):
                continue
            if Pirate.domain_name != get_domain_name(url):
                continue
            Pirate.queue.add(url)

    @staticmethod
    def update_files():
        to_file(Pirate.queue, Pirate.queue_file)
        to_file(Pirate.crawled, Pirate.crawled_file)
