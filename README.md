# Project Portfolio — Mohammed Jamir Uddin

Four complete, solo-built enterprise systems, each with a walkthrough video and a documentation PDF.

| Project | Slug | Page |
|---|---|---|
| Sinan International University Management System | `iums` | `projects/iums/` |
| Sayan Hospital Management System | `hms` | `projects/hms/` |
| Ainan International Auto Parts System | `iaps` | `projects/iaps/` |
| Safiyan International ECommerce System | `ecommerce` | `projects/ecommerce/` |

## Links to share (Upwork / clients)

After deploying, replace `YOUR-SITE` with your address:

- All projects together: `https://YOUR-SITE/`  (or `https://YOUR-SITE/#all` for the "Show all" layout)
- One project (video + PDF tabs): `https://YOUR-SITE/projects/iums/`
- Straight to the video: `https://YOUR-SITE/projects/iums/#video`  (default)
- Straight to the PDF: `https://YOUR-SITE/projects/iums/#pdf`
- Video and PDF side by side: `https://YOUR-SITE/projects/iums/#both`
- Raw files, if you ever need them: `.../projects/iums/demo.mp4` and `.../projects/iums/overview.pdf`

## Structure

```
index.html                  home page (all 4 projects)
projects/<slug>/index.html  project page (video + PDF)
projects/<slug>/demo.mp4    walkthrough video
projects/<slug>/overview.pdf documentation
projects/<slug>/poster.jpg  video thumbnail
assets/style.css            shared styles
build.py                    generates all the HTML pages
```

## Editing text / adding a project

1. Edit the `PROJECTS` list at the top of `build.py`.
2. Put `demo.mp4`, `overview.pdf`, `poster.jpg` in `projects/<slug>/`.
3. Run `python build.py`.

## Replacing a video or PDF

Overwrite the file in `projects/<slug>/` keeping the same name, then commit.

## Size limits

GitHub rejects any single file over 100 MB. Keep each video and PDF well under that.
