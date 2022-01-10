#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Workflows Community Initiative.

import datetime
import os
import requests
import yaml
import json

from string import Template


systems = []
headers = {
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": f"token {os.environ['JEKYLL_TOKEN']}"
}

# read list of workflow system repositories
with open("_data/workflow_systems.yml") as f:
    systems = yaml.safe_load(f)

for w in systems:
    print(w)
    url = f"https://api.github.com/repos/{w['organization']}/{w['repository']}"
    r = requests.get(url, headers=headers)
    response = r.json()

    # repo general information
    w["title"] = response["name"]
    w["default_branch"] = response["default_branch"]
    w["subtitle"] = response["description"]
    w["description"] = response["description"]
    w["license"] = response["license"]["spdx_id"] if response["license"] else "No license available"
    w["issues"] = response["open_issues"]
    w["forks"] = response["forks"]
    w["stargazers"] = response["stargazers_count"]
    w["avatar"] = response["owner"]["avatar_url"]
    w["website"] = response["homepage"]
    w["twitter"] = ""
    w["youtube"] = ""
    w["doc_general"] = ""
    w["doc_installation"] = ""
    w["doc_tutorial"] = ""

    # date
    date = datetime.datetime.strptime(
        response["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    w["year"] = date.strftime("%Y")
    w["month"] = date.strftime("%b")
    w["monthn"] = date.strftime("%m")
    w["day"] = date.strftime("%d")

    # topics
    w["topics"] = "No topics available"
    w["tags"] = ""
    topics = response["topics"]
    if len(topics) > 0:
        w["topics"] = ""
        for topic in topics:
            w["topics"] += f"<span class='topic'>{topic}</span>&nbsp;&nbsp;"
            w["tags"] += f"{topic} "

    # releases
    url = response['releases_url']
    r = requests.get(url[:-5], headers=headers)
    data = r.json()
    w["release"] = ""
    w["releases"] = len(data)
    if len(data) > 0:
        date = datetime.datetime.strptime(data[0]["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        release_date = date.strftime("%d %b %Y")
        w["release"] = f"<a href=\"{data[0]['html_url']}\" target=\"_blank\" class=\"release-button\">{data[0]['name']} " \
            f"<span class=\"light-gray\">({release_date})</span></a>"

    # contributors
    r = requests.get(response['contributors_url'], headers=headers)
    data = r.json()
    w['contributors'] = len(data)
    w['contributors_list'] = ""
    for c in data:
        w["contributors_list"] += f'<a href="{c["html_url"]}" target="_blank"><img src="{c["avatar_url"]}" width="32" height="32" alt="{c["login"]}"/></a>'

    # metadata file
    r = requests.get(
        f"https://raw.githubusercontent.com/{w['organization']}/{w['repository']}/{w['default_branch']}/.wci.yml")

    if r.ok:
        data = yaml.safe_load(r.text)
        print(data)

        if "name" in data:
            w["title"] = data["name"]

        # description
        if "headline" in data:
            w["subtitle"] = data["headline"]
        if "description" in data:
            w["description"] = data["description"]
        if "website" in data:
            w["website"] = data["website"]

        # social
        if "social" in data:
            if "twitter" in data["social"]:
                w["twitter"] = "<li>" \
                    f"<a href=\"https://twitter.com/{data['social']['twitter']}\" target=\"_blank\" class=\"fa-stack fa-2x\">" \
                    "<i class=\"fa fa-circle fa-stack-2x\" style=\"color: #fff\"></i><i class=\"fab fa-twitter fa-stack-1x\"></i></a></li>"

            if "youtube" in data["social"]:
                w["youtube"] = "<li>" \
                    f"<a href=\"{data['social']['youtube']}\" target=\"_blank\" class=\"fa-stack fa-2x\">" \
                    "<i class=\"fa fa-circle fa-stack-2x\" style=\"color: #fff\"></i><i class=\"fab fa-youtube fa-stack-1x\"></i></a></li>"

        # documentation
        if "documentation" in data:
            w["doc_general"] = f"<li><a href=\"{data['documentation']['general']}\" target=\"_blank\"><i class=\"fas fa-book\"></i>Documentation</a></li>" if "general" in data["documentation"] else ""
            w["doc_installation"] = f"<li><a href=\"{data['documentation']['installation']}\" target=\"_blank\"><i class=\"fas fa-download\"></i>Installation</a></li>" if "installation" in data["documentation"] else ""
            w["doc_tutorial"] = f"<li><a href=\"{data['documentation']['tutorial']}\" target=\"_blank\"><i class=\"fas fa-user-cog\"></i>Tutorial</a></li>" if "tutorial" in data["documentation"] else ""

    # fill template
    with open('scripts/systems.html.in') as f:
        template = Template(f.read())
        contents = template.substitute(w)

        from pathlib import Path
        Path("_systems").mkdir(parents=True, exist_ok=True)

        # write workflows data
        with open(f"_systems/{w['repository']}.html", 'w') as f:
            f.write(contents)
