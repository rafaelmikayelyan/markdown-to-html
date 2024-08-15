# Markdown to HTML

A simple static site generator made with Python.

Supports basic Markdown syntax with additions:
* Fenced Code Block
* Strikethrough
* Highlight

## Requirements

You need [Python 3.xx](https://www.python.org/downloads/) to run the app.

## Usage

1. Put all your `.md` files into the `./content/` folder, mimicking the the structure of the website:
* `./content/index.md` is your landing page - the web page address will be `example.com/`
* `./content/secret.md` is your 'topic' related page - the web page address will be `example.com/secret.html`
* `./content/topic/index.md` is your 'topic' related page - the web page address will be `example.com/topic`
2. Put all your images into `./static/` folder
3. Run `./main.sh` script
4. Upload the contents of `./public/` folder to the hosting of your choosing