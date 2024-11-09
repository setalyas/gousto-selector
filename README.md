# Gousto meal selector

### Email scraper

- Downloaded .eml files directly from email app. - Use the `email` package to extract the text and HTML separately from the email files (text for easy copy munging, HTML for getting images)
- Cleaned up the text versions, to identify the "title-y" lines (i.e. the recipe titles).
- Weight by popularity and date, export into a JSON.

### Shiny app set-up

- For the Github Pages approach, followed the approach in https://www.appsilon.com/post/shiny-for-python-deploy-github-pages
  - N.B. had to install shinylive via pip => did in a [new environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)