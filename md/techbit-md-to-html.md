# Markdown to HTML


## Background
For my portfolio site, it was becoming very cumbersome to write the matter in HTML. Using the converters was too not an easy solution.
Now I created a solution to convert the __markdown__ to __HTML__ and then to embed it inside my wrapper HTML which has **< head >** and _tail_ of the **< body >**.  Making good use of 'placeholder' technique to rightly place the embedded HTML.
All of what I is been said in this document is already implemented as part of the portfolio project itself. You can take a look.

----

## Installation
- markdown
- python3
- yaml

On Mac,

```
brew install markdown
```
it's man-page: [markdown](https://linux.die.net/man/1/markdown)

And I used a python based setup script, which I run after every change to **.md** files so as to convert them in HTML.

To keep things flexible, used a configuration file in yaml.

```
pip install pyyaml
```

----

## Reading YAML Configuration
My current configuration file is [here](../config.yaml).
Code for reading the yaml file is simple:


```
def read_config():
    with open("config.yaml") as file:
        try:
            global config
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
```

As I am using the config variable in many other functions made it global.

----

## Process of conversion from Markdown to HTML
There are many steps I took to make it suit my particular setup, however, in general if you have to do it there is really one basic step, as mentioned in following code-snippet:

----

### Basic command to convert markdown to HTML-Code
```
cmd = "markdown " + dir_src_md + "/" + file + " > " + gen_fname_path
run_cmd(cmd)
```

thus for one of the files, it runs and shows the command as:
```
$ markdown md/techbit-md-to-html.md > md/html/techbit-md-to-html.html
```

----

### Embed generated HTML-Code in a proper HTML file
The generated HTML-Code is not complete. It doesn't have **< HEAD >** or **< BODY >** tags.
To solve that I created a template HTML file, see [template-techbit-.html](../template-techbit-.html)

Template HTML file has:
```
<div id="placeholder-md-"></div>
```
This is replaced by the 'setup.py' with the respective 'title' of the '.md' file.
And a 'script/gen/placeholder.js' file is created automatically with the same 'id'.
With the help of 'script/gen/placeholder.js' a newly created (generated with 'markdown' command) 'md/html/?????.html' is loaded.

And thats it!

----

## Next?
I think there should have been a better solution that this. But for now this is what I can think of.
The use of this approach for my specific project is fine. I can create '.md' (markdown) files and automatically created HTML files that have my standard header and footer.