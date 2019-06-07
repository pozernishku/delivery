# delivery
Grab from PDF.

Parameters:
start=int
end=int
verbose=true/false

Run script:
scrapy crawl del_sp -s LOG_FILE=grab.log -a start=456880 -a end=456900 -a verbose=true -t csv -o - > delivery.csv