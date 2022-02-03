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


def _get_value(key, obj, default_value):
    return obj[key] if key in obj else default_value


systems = []
headers = {
    "Accept": "application/vnd.github.scarlet-witch-preview+json",
    "Accept": "application/vnd.github.mercy-preview+json",
    "Authorization": f"token {os.environ['JEKYLL_TOKEN']}"
}

# read list of workflow system repositories
with open("_data/workflow_systems.yml") as f:
    systems = yaml.safe_load(f)

for s in systems:
    print(s)
    url = f"https://api.github.com/repos/{s['organization']}/{s['repository']}"
    r = requests.get(url, headers=headers)
    response = r.json()
    # print(json.dumps(response, indent=2))

    # repo general information
    s["title"] = response["name"]
    s["default_branch"] = response["default_branch"]
    s["subtitle"] = response["description"]
    s["description"] = response["description"]
    s["license"] = response["license"]["spdx_id"] if response["license"] else "No license available"
    s["issues"] = response["open_issues"]
    s["forks"] = response["forks"]
    s["stargazers"] = response["stargazers_count"]
    s["avatar"] = response["owner"]["avatar_url"]
    s["website"] = response["homepage"]
    s["language"] = response['language']
    s["twitter"] = ""
    s["youtube"] = ""
    s["release"] = ""
    s["release_name"] = ""
    s["release_date"] = ""
    s["release_url"] = ""
    s["doc_general"] = ""
    s["doc_installation"] = ""
    s["doc_tutorial"] = ""
    s["execution_environment"] = ""
    s["wci_metadata"] = "false"

    # date
    date = datetime.datetime.strptime(
        response["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    s["year"] = date.strftime("%Y")
    s["month"] = date.strftime("%b")
    s["monthn"] = date.strftime("%m")
    s["day"] = date.strftime("%d")

    # topics
    s["topics"] = "No topics available"
    s["tags"] = ""
    topics = response["topics"]
    if len(topics) > 0:
        s["topics"] = ""
        for topic in topics:
            s["topics"] += f"<span class='topic'>{topic}</span>&nbsp;&nbsp;"
            s["tags"] += f"{topic} "

    # releases
    url = response['releases_url']
    r = requests.get(url[:-5], headers=headers)
    data = r.json()
    if len(data) > 0:
        date = datetime.datetime.strptime(
            data[0]["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        release_date = date.strftime("%d %b %Y")
        s["release_name"] = data[0]["name"]
        s["release_date"] = release_date
        s["release_url"] = data[0]["html_url"]

    # contributors
    r = requests.get(response['contributors_url'], headers=headers)
    data = r.json()
    s["contributors"] = len(data)
    s["contributors_list"] = ""
    for c in data:
        s["contributors_list"] += f'<a href="{c["html_url"]}" target="_blank"><img src="{c["avatar_url"]}" width="32" height="32" alt="{c["login"]}"/></a>'

    # metadata file
    r = requests.get(
        f"https://raw.githubusercontent.com/{s['organization']}/{s['repository']}/{s['default_branch']}/.wci.yml")

    if r.ok:
        data = yaml.safe_load(r.text)
        s["wci_metadata"] = "true"
        print(data)

        # description
        s["title"] = _get_value("name", data, s["title"])
        s["subtitle"] = _get_value("headline", data, s["subtitle"])
        s["description"] = _get_value("description", data, s["description"])
        s["website"] = _get_value("website", data, s["website"])
        s["avatar"] = _get_value("icon", data, s["avatar"])
        s["language"] = _get_value("language", data, s["language"])

        # social
        if "social" in data:
            if "twitter" in data["social"]:
                s["twitter"] = "<li>" \
                    f"<a href=\"https://twitter.com/{data['social']['twitter']}\" target=\"_blank\" class=\"fa-stack fa-2x\">" \
                    "<i class=\"fa fa-circle fa-stack-2x\" style=\"color: #fff\"></i><i class=\"fab fa-twitter fa-stack-1x\"></i></a></li>"

            if "youtube" in data["social"]:
                s["youtube"] = "<li>" \
                    f"<a href=\"{data['social']['youtube']}\" target=\"_blank\" class=\"fa-stack fa-2x\">" \
                    "<i class=\"fa fa-circle fa-stack-2x\" style=\"color: #fff\"></i><i class=\"fab fa-youtube fa-stack-1x\"></i></a></li>"

        # release
        if "release" in data:
            if "date" in data["release"]:
                s["release_date"] = data["release"]["date"].strftime("%d %b %Y")
            s["release_name"] = _get_value("version", data["release"], s["release_name"])
            s["release_url"] = _get_value("url", data["release"], s["release_url"])

        # documentation
        if "documentation" in data:
            s["doc_general"] = f"<li><a href=\"{data['documentation']['general']}\" target=\"_blank\"><i class=\"fas fa-book\"></i><br />Documentation</a></li>" if "general" in data["documentation"] else ""
            s["doc_installation"] = f"<li><a href=\"{data['documentation']['installation']}\" target=\"_blank\"><i class=\"fas fa-download\"></i><br />Installation</a></li>" if "installation" in data["documentation"] else ""
            s["doc_tutorial"] = f"<li><a href=\"{data['documentation']['tutorial']}\" target=\"_blank\"><i class=\"fas fa-user-cog\"></i><br />Tutorial</a></li>" if "tutorial" in data["documentation"] else ""

        # execution environment
        if "execution_environment" in data:
            s["execution_environment"] = "<div class=\"system-info\"><h1>Execution Environment</h1>"

            # user interfaces
            if "interfaces" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"system-info-sub\"><h2>User Interfaces</h2><ul class=\"list-tags color-2\">"
                for i in data["execution_environment"]["interfaces"]:
                    s["execution_environment"] += f"<li>{i}</li>"
                s["execution_environment"] += "</ul></div>"

            # resource managers
            if "resource_managers" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"system-info-sub\"><h2>Supported Resource Managers</h2><ul class=\"list-tags color-4\">"
                for rm in data["execution_environment"]["resource_managers"]:
                    s["execution_environment"] += f"<li>{rm}</li>"
                s["execution_environment"] += "</ul></div>"

            # transfer protocols
            if "transfer_protocols" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"system-info-sub\"><h2>Supported Transfer Protocols</h2><ul class=\"list-tags color-6\">"
                for tp in data["execution_environment"]["transfer_protocols"]:
                    s["execution_environment"] += f"<li>{tp}</li>"
                s["execution_environment"] += "</ul></div>"

            s["execution_environment"] += "</div>"

    # release component
    if s["release_name"]:
        if s["release_url"]:
            s["release"] = f"<a href=\"{s['release_url']}\" target=\"_blank\" class=\"release-button\">{s['release_name']} " \
                f"</a><br /><span class=\"light-gray\"><i class=\"far fa-clock\"></i> Released on: {s['release_date']}</span>"
        else:
            s["release"] = f"<span class=\"release-button\">{s['release_name']} " \
                f"</span><br /><span class=\"light-gray\"><i class=\"far fa-clock\"></i> Released on: {s['release_date']}</span>"

    # fill template
    with open('scripts/systems.html.in') as f:
        template = Template(f.read())
        contents = template.substitute(s)

        from pathlib import Path
        Path("_systems").mkdir(parents=True, exist_ok=True)

        # write workflows data
        with open(f"_systems/{s['repository']}.html", 'w') as f:
            f.write(contents)
