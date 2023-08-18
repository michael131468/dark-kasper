#!/usr/bin/env python3

import pathlib
import sys
import urllib.parse

import filetype

from PIL import Image
from sh import convert, exiftool, ffprobe, ffmpeg


def is_ignoreable_file(file: pathlib.Path) -> bool:
    """Helper function to check if file is ignoreable  when processing a gallery directory"""
    if str(file.name).startswith("thumbnail_"):
        return True
    elif str(file.name).endswith("_original"):
        return True
    elif not file.is_file():
        return True
    elif not filetype.is_image(file) and not filetype.is_video(file):
        return True
    return False


def get_thumbnail_path(file: pathlib.Path) -> pathlib.Path:
    """Helper function to determine the thumbnail path for a corresponding gallery file"""
    if filetype.is_video(file):
        return file.parent / f"thumbnail_{file.with_suffix('.jpg').name}"
    else:
        return file.parent / f"thumbnail_{file.name}"


def gen_gallery_item_html_image(
    file: pathlib.Path, top_dir: pathlib.Path, base_url: str
) -> str:
    """Generates html for image item in gallery in index.html file"""
    im = Image.open(file)
    width, height = im.size

    thumbnail_file = get_thumbnail_path(file)
    thumbnail_file_subdirectory = thumbnail_file.relative_to(top_dir).parents[0]
    file_subdirectory = file.relative_to(top_dir).parents[0]
    gallery_item_html = f"""
          <div class="grid-item">
            <a href="{base_url}/galleries/{urllib.parse.quote(str(file_subdirectory))}/{urllib.parse.quote(file.name)}" data-pswp-width="{width}" data-pswp-height="{height}" target="_blank">
              <img src="{base_url}/galleries/{urllib.parse.quote(str(thumbnail_file_subdirectory))}/{urllib.parse.quote(thumbnail_file.name)}" alt="" />
            </a>
          </div>
    """

    return gallery_item_html


def gen_gallery_item_html_video(
    file: pathlib.Path, top_dir: pathlib.Path, base_url: str
) -> str:
    """Generates html for video item in gallery in index.html file"""
    width = ffprobe(
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width",
        "-of",
        "csv=s=x:p=0",
        str(file),
    )
    width = int(width)
    height = ffprobe(
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=height",
        "-of",
        "csv=s=x:p=0",
        str(file),
    )
    height = int(height)

    thumbnail_file = get_thumbnail_path(file)
    thumbnail_file_subdirectory = thumbnail_file.relative_to(top_dir).parents[0]
    file_subdirectory = file.relative_to(top_dir).parents[0]
    gallery_item_html = f"""
          <div class="grid-item">
            <a href="{base_url}/galleries/{urllib.parse.quote(str(file_subdirectory))}/{urllib.parse.quote(file.name)}" data-pswp-width="{width}" data-pswp-height="{height}" data-pswp-type="video" target="_blank">
              <img src="{base_url}/galleries/{urllib.parse.quote(str(thumbnail_file_subdirectory))}/{urllib.parse.quote(thumbnail_file.name)}" alt="" />
            </a>
          </div>
    """

    return gallery_item_html


def gen_gallery_item_html(
    file: pathlib.Path, top_dir: pathlib.Path, base_url: str
) -> str:
    """Generates html for item in gallery in index.html file"""
    if filetype.is_image(file):
        return gen_gallery_item_html_image(file, top_dir, base_url)
    elif filetype.is_video(file):
        return gen_gallery_item_html_video(file, top_dir, base_url)
    else:
        return ""


def gen_gallery_html(
    gallery_dir: pathlib.Path, top_dir: pathlib.Path, base_url: str
) -> str:
    """Generates index.html for gallery directories"""
    print(f"Generating gallery html for {gallery_dir}")
    gallery_items_html = ""
    for file in gallery_dir.rglob("*"):
        if is_ignoreable_file(file):
            continue

        thumbnail_file = get_thumbnail_path(file)
        if not thumbnail_file.exists():
            continue

        gallery_items_html += gen_gallery_item_html(file, top_dir, base_url)

    html = f"""
    <html>
      <head>
        <link rel="stylesheet" href="{base_url}/assets/css/photoswipe/photoswipe.css">
        <script src="{base_url}/assets/js/imagesloaded/imagesloaded.pkgd.min.js"></script>
        <script src="{base_url}/assets/js/masonry/masonry.pkgd.min.js"></script>
        <style>
          .grid-item {{
            width: 210px;
            margin-bottom: 20px;
          }}
        </style>
      </head>
      <body>
        <div class="grid pswp-gallery" id="my-gallery">
          <!-- Copy and paste from here to your post -->
          {gallery_items_html}
          <!-- End copy and paste -->
        </div>
        <script type="module">
          import PhotoSwipeLightbox from "{base_url}/assets/js/photoswipe/photoswipe-lightbox.esm.min.js";
          import PhotoSwipeVideoPlugin from "{base_url}/assets/js/photoswipe/photoswipe-video-plugin.esm.min.js";
          import PhotoSwipe from "{base_url}/assets/js/photoswipe/photoswipe.esm.min.js";

          const lightbox = new PhotoSwipeLightbox({{
            gallery: "#my-gallery",
            children: "a",
            pswpModule: PhotoSwipe
          }});
          const videoPlugin = new PhotoSwipeVideoPlugin(lightbox, {{}});
          lightbox.init();
        </script>
        <script>
          var elem = document.querySelector(".grid");
          var msnry = new Masonry( elem, {{
            itemSelector: ".grid-item",
            columnWidth: 230
          }});

          imagesLoaded( elem ).on("progress", function() {{
            msnry.layout();
          }});
        </script>
      </body>
    </html>
    """

    index_file = gallery_dir / "index.html"
    with open(index_file, "w") as index_f:
        index_f.write(html)


def thumbnailify(file: pathlib.Path):
    thumbnail_file = get_thumbnail_path(file)
    if thumbnail_file.exists():
        print(f"Thumbnailing: Skipping {file}")
        return

    print(f"Thumbnailing: {file}")
    if filetype.is_image(file):
        convert("-strip", "-thumbnail", "210x>", str(file), str(thumbnail_file))
    elif filetype.is_video(file):
        ffmpeg(
            "-i",
            str(file),
            "-vf",
            "scale=210:-2:force_original_aspect_ratio=decrease",
            "-ss",
            "00:00:01.000",
            "-vframes",
            "1",
            str(thumbnail_file),
        )
    else:
        print("Unknown file type. Cannot generate thumbnail!")


def strip_exif(file: pathlib.Path):
    """Strip exif data from image files using exiftool"""
    if filetype.is_image(file):
        print(f"Stripping exif data: {file}")
        exiftool("-EXIF=", str(file))


def walk_dir(directory: pathlib.Path, base_url: str) -> None:
    """Process a tree of files creating thumbnails and index.html files"""
    gallery_dirs = set()
    for file in directory.rglob("*"):
        # ignore thumbnail files, directories, and unknown file types
        if is_ignoreable_file(file):
            continue
        # Strip exif data from image file for privacy reasons
        strip_exif(file)
        thumbnailify(file)
        gallery_dirs.add(file.parent)

    for gallery_dir in gallery_dirs:
        gen_gallery_html(gallery_dir, directory, base_url)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: argv[0] [directory]")
        return 1

    directory = sys.argv[1]

    if len(sys.argv) >= 2:
        base_url = sys.argv[2]
    else:
        base_url = "./"

    walk_dir(pathlib.Path(directory), base_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
