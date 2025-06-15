#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023-2025 Workflows Community Initiative.

import datetime
import os
from pathlib import Path
from pprint import pprint
from string import Template
from typing import Literal

import markdown
import requests
import yaml
from pydantic import BaseModel


class SystemMetadata(BaseModel, extra="ignore"):
    name: str
    title: str
    subtitle: str
    description: str
    repository_url: str
    repository: str
    default_branch: str
    license: str
    issues: int
    forks: int
    stargazers: int
    contributors: int
    contributors_list: str
    release: str
    release_name: str
    release_date: str
    release_url: str
    year: str
    month: str
    monthn: str
    day: str
    tags: str
    topics: str
    avatar: str
    website: str
    language: str
    twitter: str
    youtube: str
    doc_general: str
    doc_installation: str
    doc_tutorial: str
    execution_environment: str
    wci_metadata: str


class SystemDefinition(BaseModel, extra="allow"):
    """Extra keys are passed to `SystemMetadata`."""

    type: str
    metadata: str = ""


class GitHubDefinition(SystemDefinition):
    type: Literal["github"] = "github"
    organization: str
    repository: str


class GitLabDefinition(SystemDefinition):
    type: Literal["gitlab"] = "gitlab"
    namespace: str
    project: str
    gitlab_url: str = "https://gitlab.com"


class PyPIDefinition(SystemDefinition):
    type: Literal["pypi"] = "pypi"
    distribution: str


def main():
    filename = Path(__file__).parent.parent / "_data" / "workflow_systems.yml"
    with open(filename) as f:
        systems = yaml.safe_load(f)

    output_dir = Path(__file__).parent.parent / "_systems"
    output_dir.mkdir(parents=True, exist_ok=True)

    for system in systems:
        print()
        print(system)

        # Get workflow system data from the sources
        if system["type"] == "github":
            definition = GitHubDefinition(**system)
            model = _process_github_system(definition)
        elif system["type"] == "gitlab":
            definition = GitLabDefinition(**system)
            model = _process_gitlab_system(definition)
        elif system["type"] == "pypi":
            definition = PyPIDefinition(**system)
            model = _process_pypi_system(definition)
        else:
            raise ValueError(f"Unknown type: {system['type']}")

        # Overwrite workflow system data
        model = model.model_copy(update=definition.model_dump(mode="json"), deep=True)

        # Finalize workflow system data
        _render_release_info(model)

        # Convert workflow system data to web page
        template_path = Path(__file__).parent / f"{definition.type}.html.in"
        output_path = output_dir / f"{model.name}.html"
        _save_system_html(model, template_path, output_path)


def _process_github_system(definition: GitHubDefinition) -> SystemMetadata:
    access_token = os.environ.get("JEKYLL_TOKEN")
    if access_token:
        headers = {
            # "Accept": "application/vnd.github.scarlet-witch-preview+json",
            "Accept": "application/vnd.github.mercy-preview+json",
            "Authorization": f"token {os.environ['JEKYLL_TOKEN']}",
        }
    else:
        headers = {
            # "Accept": "application/vnd.github.scarlet-witch-preview+json",
            "Accept": "application/vnd.github.mercy-preview+json",
        }

    url = f"https://api.github.com/repos/{definition.organization}/{definition.repository}"
    r = requests.get(url)
    r.raise_for_status()
    repo_data = r.json()

    updated_at = datetime.datetime.strptime(
        repo_data["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
    )

    topics = _parse_topics(repo_data.get("topics", []))
    tags = _parse_tags(repo_data.get("topics", []))

    # Releases
    r = requests.get(repo_data["releases_url"].replace("{/id}", ""), headers=headers)
    r.raise_for_status()
    release_data = r.json()
    if release_data:
        date = datetime.datetime.strptime(
            release_data[0]["published_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        release_name = release_data[0]["name"]
        release_date = date.strftime("%d %b %Y")
        release_url = release_data[0]["html_url"]
    else:
        release_name = ""
        release_date = ""
        release_url = ""

    # Contributors
    r = requests.get(repo_data["contributors_url"], headers=headers)
    r.raise_for_status()
    contributors_data = r.json()
    contributors = len(contributors_data)
    contributors_list = "".join(
        f'<a href="{c["html_url"]}" target="_blank">'
        f'<img src="{c["avatar_url"]}" width="48" height="48" alt="{c["login"]}" '
        f'style="margin-right: 0.5em; border-radius: 0.5em; margin-bottom: 1em"/></a>'
        for c in contributors_data
    )

    model = SystemMetadata(
        name=definition.repository,
        title=repo_data["name"],
        subtitle=repo_data["description"],
        description=repo_data["description"],
        repository_url=(
            f"https://github.com/{definition.organization}/{definition.repository}"
        ),
        repository=definition.repository,
        default_branch=repo_data["default_branch"],
        license=(
            repo_data["license"]["spdx_id"]
            if repo_data["license"]
            else "No license available"
        ),
        issues=repo_data["open_issues"],
        forks=repo_data["forks"],
        stargazers=repo_data["stargazers_count"],
        contributors=contributors,
        contributors_list=contributors_list,
        release="",
        release_name=release_name,
        release_date=release_date,
        release_url=release_url,
        year=updated_at.strftime("%Y"),
        month=updated_at.strftime("%b"),
        monthn=updated_at.strftime("%m"),
        day=updated_at.strftime("%d"),
        tags=tags,
        topics=topics,
        avatar=repo_data["owner"]["avatar_url"],
        website=repo_data["homepage"] or "",
        language=repo_data["language"] or "",
        twitter="",
        youtube="",
        doc_general="",
        doc_installation="",
        doc_tutorial="",
        execution_environment="",
        wci_metadata="false",
    )

    # Try loading WCI metadata from .wci.yml
    metadata_path = definition.metadata or ".wci.yml"
    if ".wci.yml" not in metadata_path:
        metadata_path = f"{metadata_path}/.wci.yml"
    raw_url = f"https://raw.githubusercontent.com/{definition.organization}/{definition.repository}/{model.default_branch}/{metadata_path}"
    r = requests.get(raw_url, headers=headers)
    if r.ok:
        metadata = yaml.safe_load(r.text)
        _apply_wci_metadata(metadata, model)

    return model


def _process_gitlab_system(definition: GitLabDefinition) -> SystemMetadata:
    acces_token = os.environ.get("GITLAB_TOKEN")
    if acces_token:
        headers = {"PRIVATE-TOKEN": acces_token}
    else:
        headers = {}

    project_encoded = requests.utils.quote(
        f"{definition.namespace}/{definition.project}", safe=""
    )
    gitlab_base_url = definition.gitlab_url.rstrip("/")
    gitlab_url = f"{gitlab_base_url}/api/v4/projects/{project_encoded}"
    r = requests.get(gitlab_url, headers=headers)
    r.raise_for_status()
    repo_data = r.json()

    updated_at = datetime.datetime.fromisoformat(repo_data["updated_at"])

    topics = _parse_topics(repo_data.get("topics", []))
    tags = _parse_tags(repo_data.get("tag_list", []))

    # Releases
    release_name = ""
    release_date = ""
    release_url = ""
    r = requests.get(f"{gitlab_url}/releases", headers=headers)
    if r.ok:
        releases_data = r.json() or [None]
        release_data = releases_data[0]
        if release_data:
            release_name = release_data.get("name", release_data.get("tag_name"))
            release_url = (
                release_data.get("assets", {}).get("links", [{}])[0].get("url", "")
            )
            released_at = release_data.get("released_at")
            if released_at:
                date = datetime.datetime.fromisoformat(released_at)
                release_date = date.strftime("%d %b %Y")

    # Contributors
    contributors_url = f"{gitlab_url}/repository/contributors"
    r = requests.get(contributors_url, headers=headers)
    r.raise_for_status()
    contributors_data = r.json()
    contributors = len(contributors_data)
    contributors_list = ""  # GitLab doesn't give avatar URLs

    model = SystemMetadata(
        gitlab_url=gitlab_base_url,
        name=definition.project,
        title=repo_data["name"],
        subtitle=repo_data["description"],
        description=repo_data["description"],
        repository_url=repo_data["web_url"],
        default_branch=repo_data["default_branch"],
        license=repo_data.get("license", {}).get("name", "No license available"),
        issues=repo_data["open_issues_count"],
        forks=repo_data["forks_count"],
        stargazers=repo_data["star_count"],
        contributors=contributors,
        contributors_list=contributors_list,
        release="",
        release_name=release_name,
        release_date=release_date,
        release_url=release_url,
        year=updated_at.strftime("%Y"),
        month=updated_at.strftime("%b"),
        monthn=updated_at.strftime("%m"),
        day=updated_at.strftime("%d"),
        tags=tags,
        topics=topics,
        avatar=repo_data.get("avatar_url") or f"{gitlab_base_url}/favicon.ico",
        website=repo_data["web_url"],
        language="",
        twitter="",
        youtube="",
        doc_general="",
        doc_installation="",
        doc_tutorial="",
        execution_environment="",
        wci_metadata="false",
    )

    # Try loading WCI metadata from .wci.yml
    metadata_path = definition.metadata or ".wci.yml"
    if ".wci.yml" not in metadata_path:
        metadata_path = f"{metadata_path}/.wci.yml"
    raw_url = f"{gitlab_base_url}/{definition.namespace}/{definition.project}/-/raw/{model.default_branch}/{metadata_path}"

    r = requests.get(raw_url, headers=headers)
    if r.ok:
        metadata = yaml.safe_load(r.text)
        _apply_wci_metadata(metadata, model)

    return model


def _process_pypi_system(definition: PyPIDefinition) -> SystemMetadata:
    url = f"https://pypi.org/pypi/{definition.distribution}/json"
    r = requests.get(url)
    r.raise_for_status()
    repo_data = r.json()
    info = repo_data["info"]

    release_data = repo_data["releases"][info["version"]][-1]
    upload_time = datetime.datetime.fromisoformat(release_data["upload_time_iso_8601"])
    release_date = upload_time.strftime("%d %b %Y")

    topics = _parse_topics(repo_data.get("keywords", []))
    tags = _parse_tags(repo_data.get("keywords", []))

    description = info["description"]
    description_content_type = info.get("description_content_type", "")
    if "markdown" in description_content_type:
        description = markdown.markdown(description, extensions=["fenced_code"])
    elif "html" not in description_content_type:
        description = f"<p>{description}</p>"

    model = SystemMetadata(
        name=definition.distribution,
        title=info["name"],
        subtitle=info["summary"],
        description=description,
        repository_url=info["project_urls"]["Repository"],
        repository=definition.distribution,
        default_branch="main",
        license=info["license"] or "No license available",
        issues=0,
        forks=0,
        stargazers=0,
        contributors=0,
        contributors_list="",
        release="",
        release_name=info["version"],
        release_date=release_date,
        release_url=info["release_url"],
        year=upload_time.strftime("%Y"),
        month=upload_time.strftime("%b"),
        monthn=upload_time.strftime("%m"),
        day=upload_time.strftime("%d"),
        tags=tags,
        topics=topics,
        avatar="https://pypi.org/static/images/logo-small.8998e9d1.svg",
        website=info["home_page"] or info["project_urls"]["Homepage"] or "",
        language="Python",
        twitter="",
        youtube="",
        doc_general="",
        doc_installation="",
        doc_tutorial="",
        execution_environment="",
        wci_metadata="false",
    )

    # Documentation
    doc = {"general": info["project_urls"]["Documentation"]}
    _render_doc_elements(model, doc)

    return model


def _apply_wci_metadata(data, model):
    model.wci_metadata = "true"

    # Description
    model.title = _get_string_value("name", data, model.title)
    model.subtitle = _get_string_value("headline", data, model.subtitle)
    model.description = _get_string_value("description", data, model.description)
    if "\"" in model.description:
        model.description = model.description.replace("\"", "'")
    model.website = _get_string_value("website", data, model.website)
    model.avatar = _get_string_value("icon", data, model.avatar)
    model.language = _get_string_value("language", data, model.language)

    # Social
    if "social" in data:
        if "twitter" in data["social"]:
            model.twitter = (f"{data['social']['twitter']}"
            )
        if "youtube" in data["social"]:
            model.youtube = (f"{data['social']['youtube']}")

    # Release
    if "release" in data:
        if "date" in data["release"]:
            date = data["release"]["date"]
            if isinstance(date, str):
                try:
                    parsed = datetime.datetime.fromisoformat(date)
                    model.release_date = parsed.strftime("%d %b %Y")
                except ValueError:
                    pass
        model.release_name = _get_string_value(
            "version", data["release"], model.release_name
        )
        model.release_url = _get_string_value("url", data["release"], model.release_url)

    # Documentation
    doc = data.get("documentation", {})
    _render_doc_elements(model, doc)

    # Execution Environment
    ee = data.get("execution_environment", {})
    if ee:
        model.execution_environment = (
            '<div class="row" style="text-align: left;">'
        )

        def make_column(title, items):
            return (
                f'<div class="col-lg-12"><strong>{title}</strong>'
                '<ul class="list-services">'
                + "".join(f"<li>{item}</li>" for item in items)
                + "</ul></div>"
            )

        if "interfaces" in ee:
            model.execution_environment += make_column(
                "User Interfaces", ee["interfaces"]
            )
        if "resource_managers" in ee:
            model.execution_environment += make_column(
                "Resource Managers", ee["resource_managers"]
            )
        if "transfer_protocols" in ee:
            model.execution_environment += make_column(
                "Transfer Protocols", ee["transfer_protocols"]
            )

        model.execution_environment += "</div>"


def _get_string_value(key, obj, default_value) -> str:
    if key not in obj:
        return default_value
    value = obj[key]
    if isinstance(value, list):
        return ", ".join(map(str, value))
    return str(value)


def _render_release_info(model: SystemMetadata) -> None:
    if model.release_name:
        if model.release_url:
            if model.release_date:
                model.release = f'<a href="{model.release_url}" target="_blank"><strong>{model.release_name}</strong></a> &mdash; Released on: {model.release_date}'
            else:
                model.release = f'<a href="{model.release_url}" target="_blank"><strong>{model.release_name}</strong></a>'
        else:
            if model.release_date:
                model.release = (
                    f"{model.release_name} &mdash; Released on: {model.release_date}"
                )
            else:
                model.release = model.release_name


def _parse_topics(keywords):
    if isinstance(keywords, str):
        lst = [k.strip() for k in keywords.split(",") if k.strip()]
    elif isinstance(keywords, list):
        lst = keywords
    else:
        lst = []
    if lst:
        topics = "".join(f"<span class='topic'>{t}</span>&nbsp;&nbsp;" for t in lst)
    else:
        topics = "No topics available"
    return topics


def _parse_tags(keywords):
    if isinstance(keywords, str):
        lst = [k.strip() for k in keywords.split(",") if k.strip()]
    elif isinstance(keywords, list):
        lst = keywords
    else:
        lst = []
    if lst:
        tags = " ".join(lst)
    else:
        tags = ""
    return tags


def _render_doc_elements(model: SystemMetadata, data: dict):
    model.doc_installation = _get_string_value("installation", data, model.doc_installation)
    model.doc_tutorial = _get_string_value("tutorial", data, model.doc_tutorial)
    model.doc_general = _get_string_value("general", data, model.doc_general)
    # doc_elements = {
    #     "doc_general": ("general", "fas fa-book color-2", "Docs"),
    #     "doc_installation": ("installation", "fas fa-download color-3", "Install"),
    #     "doc_tutorial": ("tutorial", "fas fa-user-cog color-1", "Tutorial"),
    # }
    # for key, (doc_key, icon_class, heading) in doc_elements.items():
    #     if doc_key in data:
    #         value = (
    #             f'<a href="{data[doc_key]}" class="col-md-6 col-lg-3 d-flex align-self-stretch ftco-animate" target="_blank">'
    #             f'<div class="media block-6 services d-block text-center">'
    #             f'<div class="d-flex justify-content-center">'
    #             f'<div class="icon d-flex justify-content-center mb-3">'
    #             f'<span class="{icon_class}"></span></div></div>'
    #             f'<div class="media-body p-2 mt-3"><h3 class="heading">{heading}</h3></div></div></a>'
    #         )
    #         setattr(model, key, value)


def _save_system_html(model: SystemMetadata, template_path, output_path):
    with open(template_path) as f:
        template = Template(f.read())
        data = model.model_dump(mode="json")
        pprint(data)
        contents = template.substitute(data)

    with open(output_path, "w") as f:
        f.write(contents)


if __name__ == "__main__":
    main()
