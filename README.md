# Dark-Kasper

This is a modified fork of the Kasper theme [Kasper](https://github.com/rosario/kasper) for Jekyll to convert it into a dark theme. Here is a live [demo](https://michael131468.github.io/dark-kasper/).

This is under active development and not finished.

The colours are picked a bit randomly and this theme is not fully tested so here be dragons.

Feel free to fork, change, modify and re-use it.

## Installation

    git clone https://github.com/rosario/kasper.git
    cd kasper
    gem install jekyll
    gem install jekyll-paginate
    
## Change _config.yml

Change the following settings in _config.yaml. Most likely you want the `baseurl: ""`

```
baseurl: ""
domain_name: "yourblog-domain.com"
```

## How to use it

Build page and start local web server

    jekyll serve

Build page into `_site` folder

    jekyll build

## Kasper theme includes

* Pagination
* Rss
* Google Analytics Tracking code
* Code Syntax Highlight
* Author's profile with picture
* Disqus comments

## Screenshots

![index page](https://raw.github.com/michael131468/dark-kasper/dark-mode/assets/images/kasper-theme-index.png)
![post page 1/2](https://raw.github.com/michael131468/dark-kasper/dark-mode/assets/images/kasper-theme-post.png)
![post page 2/2](https://raw.github.com/michael131468/dark-kasper/dark-mode/assets/images/kasper-theme-post-2.png)


## Thanks

Most of the work has been already done by the Ghost team, I've just ported Casper to Jekyll. 
I've also added few things specific to Jekyll and some minor style changes.

## Copyright & License

Copyright (C) 2013 Ghost Foundation - Released under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
