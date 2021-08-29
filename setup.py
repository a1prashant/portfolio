#!python3

import yaml
import os, shutil
import fileinput


def call_fn(fn):
    print("-> " + fn.__name__)
    fn()
    print("<- " + fn.__name__)


def md_to_html():
    global md_config
    md_config = config["md-to-html"]
    global placeholder
    placeholder = md_config["placeholder"]
    dir_src_md = md_config["src-dir"]
    dir_gen_html = md_config["gen-dir"]
    cleanup_md()
    for file in os.listdir(dir_src_md):
        if file.endswith("md"):
            print("for: " + file)
            topic, f_ext = os.path.splitext(file)
            gen_html_file = topic + ".html"
            gen_fname_path = os.path.join(dir_gen_html, gen_html_file)
            cmd = "markdown " + dir_src_md + "/" + file + " > " + gen_fname_path
            run_cmd(cmd)
            template_to_full_html(topic, gen_html_file, gen_fname_path)


def read_config():
    with open("config.yaml") as file:
        try:
            global config
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)


def cleanup_md():
    file = placeholder["file"]
    if os.path.exists(file):
        os.remove(file)


def template_to_full_html(topic, filename, content_file):
    shutil.copyfile(md_config["template-techbit-html"], filename)

    placeholder_script = placeholder["script"].format(topic, content_file)

    with open(placeholder["file"], "a") as placeholder_file:
        placeholder_file.write(placeholder_script)

    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            placeholder_id = placeholder["id"]
            if placeholder_id in line:
                print(line.replace(placeholder_id, placeholder_id + topic), end="")
            else:
                print(line, end="")


def plantuml_to_png():
    global plantuml_config
    plantuml_config = config["plantuml"]
    commands = plantuml_config["commands"]
    for cmd in commands:
        run_cmd(cmd)


def run_cmd(cmd):
    print("$ " + cmd)
    ret = os.system(cmd)
    print(": returned=", ret)


call_fn(read_config)
call_fn(md_to_html)
call_fn(plantuml_to_png)
