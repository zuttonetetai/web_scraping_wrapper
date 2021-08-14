# web_scraping_wrapper

Web scraping wrapper functions.

## Requirements

- bs4
- requests
- urllib
- selenium
- ast
- tqdm
- chromedriver_binary



## Functions

- ### get_source_text_with_selenium

  Web scraping with selenium module and chromedriver_binary. return source code(str)

  ```python
  get_source_text_with_selenium(url, timeout=None, wait=0, os="windows", headless=True, proxy=None, proxy_id=None, proxy_pass=None)
  ```

  

- ### get_source_text

  web scraping. return source code(str)

  ```python
  get_source_text(url)
  ```

  

- ### search_tag

  return source code(str)

  ```python
  search_tag(txt, tag, search_type='all', class_name=None, id_name=None, output_type='all')
  ```

  - text: str, str(source_code), not bs4 tag type
  - tag: str or list, html-tag (exp. 'a', 'div')
  - search_type: str, 'all' or 'one'
  - class_name: str or list, html-class
  - id_name: str or list, html-id
  - output_type: str, 'all' or 'text' or 'href'

  

- ### download_img

  download image file. no return

  ```python
  download_img(img_url, path, process_name=None, log=True, file_extension='jpg', dl_on_exist_dir=False)
  ```

  - img_url: str or list, image urls

  - path: str, download directly path

  - process_name: str, show process_name on process bar when log=True

  - log: bool, show process bar on terminal

  - file_extension: str, 'jpg', 'png' and so on.

  - dl_on_exist_dir: bool, True is dl on a already exist directly
