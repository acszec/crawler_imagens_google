START_URLS?=start_urls.txt
URLS?=./links

install:
	pip install -r requirements.txt -U

ifndef START_URLS
$(error START_URLS is not set)
endif

export START_URLS
start:
	python main.py ${START_URLS}

ifndef URLS
$(error The URLS variable is not set)
endif

download:
	python download_images.py ${URLS}