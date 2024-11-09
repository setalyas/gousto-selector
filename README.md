# Gousto meal selector

### Email scraper

- Downloaded .eml files directly from email app. - Use the `email` package to extract the text and HTML separately from the email files (text for easy copy munging, HTML for getting images)
- Cleaned up the text versions, to identify the "title-y" lines (i.e. the recipe titles).
- Weight by popularity and date, export into a JSON.

### Image grabber

- Get all the images
- N.B. noticed there were fewer images than rows in the files => used to also dedupe the image list and weights JSON

### Shiny app set-up

For the Github Pages approach, followed the approach in https://www.appsilon.com/post/shiny-for-python-deploy-github-pages:

- Make updates to app. Test locally with `shiny run app.py`
- `shiny static-assets remove`
- `shinylive export src_shiny_app docs`
- Test built correctly with `python -m http.server --directory docs --bind localhost 8008`
- N.B. had to install shinylive via pip => did in a [new environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)