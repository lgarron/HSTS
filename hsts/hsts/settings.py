# Scrapy settings for hsts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'hsts'

SPIDER_MODULES = ['hsts.spiders']
NEWSPIDER_MODULE = 'hsts.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
CONCURRENT_REQUESTS = 20
# LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 15
RETRY_ENABLED = False
REDIRECT_ENABLED = False
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36"