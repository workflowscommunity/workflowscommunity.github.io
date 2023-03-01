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
        s["contributors_list"] += f'<a href="{c["html_url"]}" target="_blank">' \
                                  f'<img src="{c["avatar_url"]}" width="48" height="48" alt="{c["login"]}" style="margin-right: 0.5em; border-radius: 0.5em; margin-bottom: 1em"/></a>'

    # metadata file
    metadata = f"{s['metadata']}" if "metadata" in s else ".wci.yml"
    if ".wci.yml" not in metadata:
        metadata = f"{metadata}/.wci.yml"
    r = requests.get(
        f"https://raw.githubusercontent.com/{s['organization']}/{s['repository']}/{s['default_branch']}/{metadata}")

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
                s["twitter"] = "" \
                    f"<a href=\"https://twitter.com/{data['social']['twitter']}\" target=\"_blank\">" \
                    f"<i class=\"fab fa-twitter\"></i> https://twitter.com/{data['social']['twitter']}</a></li>"

            if "youtube" in data["social"]:
                s["youtube"] = "" \
                    f"<a href=\"{data['social']['youtube']}\" target=\"_blank\">" \
                    f"<i class=\"fab fa-youtube\"></i> {data['social']['youtube']}</a></li>"

        # release
        if "release" in data:
            if "date" in data["release"]:
                s["release_date"] = data["release"]["date"].strftime("%d %b %Y")
            s["release_name"] = _get_value("version", data["release"], s["release_name"])
            s["release_url"] = _get_value("url", data["release"], s["release_url"])

        # documentation
        if "documentation" in data:
            s["doc_general"] = f"<a href=\"{data['documentation']['general']}\" class=\"col-md-6 col-lg-3 d-flex align-self-stretch ftco-animate\" target=\"_blank\">" \
                                    "<div class=\"media block-6 services d-block text-center\">" \
                                    "<div class=\"d-flex justify-content-center\">" \
                                    "<div class=\"icon color-2 d-flex justify-content-center mb-3\">" \
                                    "<span class=\"fas fa-book color-2\"></span></div></div>" \
                                    "<div class=\"media-body p-2 mt-3\"><h3 class=\"heading\">Docs</h3></div></div></a>" if "general" in data["documentation"] else ""
            s["doc_installation"] = f"<a href=\"{data['documentation']['installation']}\" class=\"col-md-6 col-lg-3 d-flex align-self-stretch ftco-animate\" target=\"_blank\">" \
                                    "<div class=\"media block-6 services d-block text-center\">" \
                                    "<div class=\"d-flex justify-content-center\">" \
                                    "<div class=\"icon color-3 d-flex justify-content-center mb-3\">" \
                                    "<span class=\"fas fa-download colro-3\"></span></div></div>" \
                                    "<div class=\"media-body p-2 mt-3\"><h3 class=\"heading\">Install</h3></div></div></a>" if "installation" in data["documentation"] else ""
            s["doc_tutorial"] = f"<a href=\"{data['documentation']['tutorial']}\" class=\"col-md-6 col-lg-3 d-flex align-self-stretch ftco-animate\" target=\"_blank\">" \
                                    "<div class=\"media block-6 services d-block text-center\">" \
                                    "<div class=\"d-flex justify-content-center\">" \
                                    "<div class=\"icon color-1 d-flex justify-content-center mb-3\">" \
                                    "<span class=\"fas fa-user-cog color-1\"></span></div></div>" \
                                    "<div class=\"media-body p-2 mt-3\"><h3 class=\"heading\">Tutorial</h3></div></div></a>" if "tutorial" in data["documentation"] else ""

        # execution environment
        if "execution_environment" in data:
            s["execution_environment"] = "<div class=\"row justify-content-center mt-5\">" \
                                         "<div class=\"col-md-7 text-center heading-section ftco-animate\">" \
                                         "<h3 class=\"mb-4\">Execution Environment</h3></div></div>" \
                                         "<div class=\"row\">"

            # user interfaces
            if "interfaces" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"col-md-4 ftco-animate\">" \
                                              "<ul class=\"list-services\">" \
                                              "<li><h4>User Interfaces</h4></li>"
                for i in data["execution_environment"]["interfaces"]:
                    s["execution_environment"] += f"<li>{i}</li>"
                s["execution_environment"] += "</ul></div>"

            # resource managers
            if "resource_managers" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"col-md-4 ftco-animate\">" \
                                              "<ul class=\"list-services\">" \
                                              "<li><h4>Resource Managers</h4></li>"
                for rm in data["execution_environment"]["resource_managers"]:
                    s["execution_environment"] += f"<li>{rm}</li>"
                s["execution_environment"] += "</ul></div>"

            # transfer protocols
            if "transfer_protocols" in data["execution_environment"]:
                s["execution_environment"] += "<div class=\"col-md-4 ftco-animate\">" \
                                              "<ul class=\"list-services\">" \
                                              "<li><h4>Transfer Protocols</h4></li>"
                for tp in data["execution_environment"]["transfer_protocols"]:
                    s["execution_environment"] += f"<li>{tp}</li>"
                s["execution_environment"] += "</ul></div>"
            
            s["execution_environment"] += "</div>"

    # release component
    if s["release_name"]:
        if s["release_url"]:
            s["release"] = f"<a href=\"{s['release_url']}\" target=\"_blank\"><strong>{s['release_name']}</strong> " \
                f"</a> &mdash; Released on: {s['release_date']}"
        else:
            s["release"] = f"{s['release_name']} " \
                f" &mdash; Released on: {s['release_date']}"

    # fill template
    with open('scripts/systems.html.in') as f:
        template = Template(f.read())
        contents = template.substitute(s)

        from pathlib import Path
        Path("_systems").mkdir(parents=True, exist_ok=True)

        # write workflows data
        with open(f"_systems/{s['repository']}.html", 'w') as f:
            f.write(contents)
