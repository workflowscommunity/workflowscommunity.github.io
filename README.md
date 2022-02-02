# Workflows Community Initiative Website
https://workflows.community

## Editing website

You can edit this website using [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

Most of the content is generated from the [_data](_data) diretory or the individual `html` pages.

If you are editing this website locally, you can try rendering it with [Docker](https://www.docker.com/), e.g.:

    docker run -it -e PAGES_REPO_NWO=workflowscommunity/workflowscommunity.github.io \
      --volume=`pwd`:/srv/jekyll -p 4000:4000 jekyll/jekyll jekyll serve
    
Note that you will also need to execute `scripts/process_systems.py` manually with Python to recreate the workflow system pages from GitHub.
