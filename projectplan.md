# Plan: Restructure Directory & Dynamic Loading

## Goal
Restructure the deeplooking file hierarchy to match architecture.md (image → segment → lens), create rich markdown files for all segments, move masks into image dirs, and make index.html dynamically load from the markdown files.

## Steps

- [x] **1. Restructure marsh directories** (image → segment → lens)
  - Current: `images/marsh/poetry/boardwalk/{boardwalk.md, marsh_boardwalk.png}`
  - Target:  `images/marsh/boardwalk/poetry/{boardwalk.md, marsh_boardwalk.png}`
  - Move all 4 segments (boardwalk, marsh, sky, water) from `marsh/poetry/<segment>/` to `marsh/<segment>/poetry/`
  - Remove the now-empty `marsh/poetry/` directory

- [x] **2. Move segmentation masks into image directories**
  - `outputs/marsh/segmentation_mask.png` → `images/marsh/segmentation_mask.png`
  - `outputs/lourmarin/segmentation_mask_v3.png` → `images/lourmarin/segmentation_mask.png`

- [x] **3. Enrich marsh markdown files** with URL, image path, and consistent format
  - Add `url:` and `image:` fields so all popup data lives in the markdown
  - Format:
    ```
    title: Boardwalk
    poet: Herbert Morris
    url: https://newcriterion.com/article/boardwalk/
    image: marsh_boardwalk.png
    keyword: boardwalk

    My breath, turned smoke, is rising on the air.
    ...
    ```

- [x] **4. Create lourmarin segment directories and markdown files**
  - Create 6 segment dirs: sky, trees, cliffs, meadow, river, figures
  - Each gets a `poetry/` subdirectory with a `.md` file and the corresponding image
  - Move images from `images/lourmarin/poetry/images/` into the correct segment dirs
  - Move `artwork.WEBP` to `images/lourmarin/artwork.WEBP` (already there)
  - Remove the now-empty `images/lourmarin/poetry/images/` directory
  - Data extracted from the current index.html hardcoded galleryItems

- [x] **5. Update index.html to dynamically load from markdown files**
  - Replace hardcoded `galleryItems` poemData with fetch-based loading
  - On viewer open, fetch a manifest or scan segment directories
  - Parse the markdown front-matter to get title, poet, url, image, keyword, text
  - Keep getLabel functions (color→label mapping) in a small config since they're code, not content
  - Ensure it works via GitHub Pages (no server-side code — all client-side fetch)

- [x] **6. Update mask paths in index.html**
  - Change mask references from `outputs/` to `images/` paths

- [x] **7. Test everything works**
  - Open index.html in browser, verify both marsh and lourmarin work
  - Verify hover, click-to-pin, close, back-to-gallery all function

## File Structure After Restructuring

```
images/
  marsh/
    marsh.jpeg                    (root image)
    segmentation_mask.png         (moved from outputs/)
    boardwalk/
      poetry/
        boardwalk.md              (enriched)
        marsh_boardwalk.png
    marsh/
      poetry/
        marsh.md                  (enriched)
        marsh_marsh.png
    sky/
      poetry/
        sky.md                    (enriched)
        marsh_sky.png
    water/
      poetry/
        water.md                  (enriched)
        marsh_water.png
  lourmarin/
    artwork.WEBP                  (root image)
    segmentation_mask.png         (moved from outputs/)
    sky/
      poetry/
        sky.md                    (new)
        lourmarin_sky.png
    trees/
      poetry/
        trees.md                  (new)
        lourmarin_trees.png
    cliffs/
      poetry/
        cliffs.md                 (new)
        lourmarin_cliffs.png
    meadow/
      poetry/
        meadow.md                 (new)
        lourmarin_meadow.png
    river/
      poetry/
        river.md                  (new)
        lourmarin_river.png
    figures/
      poetry/
        figures.md                (new)
        lourmarin_travelers.png
```

## Key Design Decisions

- **Markdown front-matter format**: Simple `key: value` lines followed by a blank line, then poem text body. Not YAML `---` fenced — keeps it minimal.
- **GitHub Pages compatible**: All loading via client-side `fetch()` of known paths. We'll use a small JSON manifest per image (e.g., `images/marsh/manifest.json`) listing segments, labels, and color rules, so no directory listing is needed.
- **getLabel stays in config**: Color→label mapping is code logic, stored in manifest.json per image rather than in markdown.

## Review

### Changes made:
1. **Marsh restructured**: Flipped from `marsh/poetry/segment/` to `marsh/segment/poetry/` for all 4 segments (boardwalk, marsh, sky, water)
2. **Masks moved**: Copied segmentation masks from `outputs/` into `images/marsh/` and `images/lourmarin/` (lourmarin uses v3 as canonical)
3. **Marsh markdown enriched**: All 4 `.md` files now include `title`, `poet`, `url`, `image`, and `keyword` front-matter fields
4. **Lourmarin restructured**: Created 6 segment directories (sky, trees, cliffs, meadow, river, figures) each with `poetry/` subdirs containing `.md` and image files. Data extracted from hardcoded index.html. Unused images (bird, waterfall) moved to `images/lourmarin/unused/`
5. **Dynamic loading**: index.html now fetches `images/gallery.json` → per-image `manifest.json` → per-segment `.md` files at runtime. No hardcoded poem data remains in HTML. Color rules stored in manifest.json. GitHub Pages compatible (all client-side fetch).
6. **Title changed**: "POETRY DEEP LOOKING" → "DEEP LOOKING" (poetry is just one lens)
7. **Security improvement**: Replaced `innerHTML` with safe DOM-based `setHighlightedText()` function

### New files:
- `images/gallery.json` — list of image IDs
- `images/marsh/manifest.json` — marsh config (segments, color rules)
- `images/lourmarin/manifest.json` — lourmarin config
- 6 lourmarin `.md` files (sky, trees, cliffs, meadow, river, figures)

### Testing:
- Gallery loads both images correctly
- Marsh: hover shows popup, click pins with hyperlink, close button works, back to gallery works
- Lourmarin: hover shows popup with keyword highlighting, click pins with hyperlink, all segments load from markdown
