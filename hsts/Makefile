all:
	scrapy crawl hsts \
		-t json \
		-o data/items.json \
		-a url_file="../data/alexa-top-100k-2013-09-24.csv" \
		-a num=10 \
		-a start=1