= ploufseo

A Powerfull, Ligth, Optimal, Ubiquitious, Fancy tool for Search Engine Optimization.

This tool help extracting information from many webpages using XPath.

== Installation

python setup.py install


== Usage

Usage: ploufseo [options]

Options:
  -h, --help            show this help message and exit
  -s SITEMAP-URL, --sitemap=SITEMAP-URL
                        Get the links from the sitemap.
  -c CSV-FILES, --csv=CSV-FILES
                        Get the links form csv files.
  -u URL-LIST, --url=URL-LIST
                        Parse specific URLs
  -S, --check-status    Check the returned status code.
  -X XPATH, --check-xpath=XPATH
                        Check the XPath expressions, they must be passed as
                        XPATH1,XPATH2,...
  -o FILENAME, --output=FILENAME
                        Overwrite the given csv file
  -p, --progress        Show progress bar
  -m, --multiple        Get all the matching value of an XPath expression
                        instead of the first

== Exemples

Checking the content of the metas descritpion and keyword for all the pages included in the sitemap.

ploufseo -s http://foo/sitemap.xml -X '//meta[@name="description"]/@content,//meta[@name="keywords"]/@content'

Checking a list of url from a CSV file and checking their http status code (200 OK, 3XX redirection, ... ).

ploufseo -c url_list.csv -S

Getting all the links from a page

ploufseo -u http//foo/bar -X '//a/@href'
