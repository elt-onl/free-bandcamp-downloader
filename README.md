# free-bandcamp-downloader

This is a self-maintained fork of [7x11x13/free-bandcamp-downloader](https://github.com/7x11x13/free-bandcamp-downloader).

Download free and $0 minimum name-your-price albums and tracks from Bandcamp (including ones that are sent to email),
and tag them with data from the Bandcamp page. Also able to download items in your collection, if login cookies are
supplied using the `--cookies` or `--identity` argument.

## Installation

With [uv](https://docs.astral.sh/uv/getting-started/installation/):

```
$ uv tool install git+https://github.com/elt-onl/free-bandcamp-downloader
$ bcdl-free
```

With pip:

```
$ pip install git+https://github.com/elt-onl/free-bandcamp-downloader
$ bcdl-free
```

## Note on email downloads

Releases that are only sent by email are received through a disposable inbox from [mail.tm](https://mail.tm),
unless `--email` is set to your own address. In that case the download links are sent to you and nothing is
downloaded for those releases.

## Note on passing cookies

Only one cookie is needed to login, which has the name "identity". You can pass this cookie to `bcdl-free` using the
`--cookies` argument which you must supply a path to a Netscape cookies.txt formatted file, or using the `--identity`
argument which you must supply the value of your "identity" cookie.

## Tagging

Downloaded FLAC and Ogg files are always tagged with:

- `website`: the release's Bandcamp URL
- `genre`: the release's Bandcamp tags
- `comment`: the release's description and credits
- `date`: the full release date

Other formats are not tagged. These options add more:

- `--release-tags` writes release tags. A track URL (`/track/`) is tagged as a single, even if the track is part of
  an album. An album URL (`/album/`) is tagged as an album, with the track count filled in automatically.

  | Tag | Track URL | Album URL |
  |---|---|---|
  | `album` | the track title | the album title |
  | `albumartist`, `albumartistsort` | the artist | the album artist |
  | `artists` | the artist | the track's artist |
  | `artistsort` | the artist | the track's artist |
  | `tracknumber` | `1` | the track's number |
  | `totaltracks`, `tracktotal` | `1` | the number of tracks on the album |
  | `discnumber`, `totaldiscs`, `disctotal` | `1` | `1` |
  | `releasetype` | `single` | `album` |

- `--split-artists` makes the `artists` tag from `--release-tags` hold each artist separately, e.g.
  `Daft Punk feat. Pharrell Williams & Nile Rodgers` becomes `Daft Punk`, `Pharrell Williams` and `Nile Rodgers`.
  `artist` keeps the name as Bandcamp writes it. Without this option, `artists` holds the whole name. It has no
  effect without `--release-tags`.
- `--artist-separators "<separators>"` sets what `--split-artists` splits on, separated by spaces. The default is
  `feat. , & x and`. Words like `x` and `and` only split when there are spaces on both sides, so `Malcolm X` stays
  one artist, while `,` and `&` split anywhere. Leave out `and` to keep names like `Simon and Garfunkel` together.
- `--cover-original` replaces Bandcamp's 700x700 embedded cover with the cover at its original resolution (FLAC only).
- `--tag key=value` sets a fixed tag, e.g. `--tag "media=Digital Media"`. Repeat it for each tag. Fixed tags are
  written last, so they override tags written by the other options.

## Usage

```
Usage:
    bcdl-free defaults
    bcdl-free clear
    bcdl-free -h | --help | --version
    bcdl-free [--debug] [--force] [--no-unzip] [-al]
        [-d <dir>] [-e <email>] [-z <zipcode>] [-c <country>] [-f <format>]
        [--cookies <file>] [--identity <value>] [--download-history-file <file>]
        [--release-tags] [--split-artists] [--artist-separators <separators>]
        [--cover-original] [--tag <tag>]...
        (setdefault | URL...)

Arguments:
    URL            URL to download. Can be a link to a label or release page

Subcommands:
    setdefault     save the given options as defaults for later downloads
    defaults       list default configuration options
    clear          clear default configuration options

Options:
    -h --help                            Show this screen
    --version                            Show version
    --force                              Download even if album has been downloaded before
    --no-unzip                           Don't unzip downloaded albums
    --debug                              Set loglevel to debug
    -a -l                                Dummy options, for backwards compatibility
    -d <dir> --dir <dir>                 Set download directory
    -c <country> --country <country>     Set country
    -z <zipcode> --zipcode <zipcode>     Set zipcode
    -e <email> --email <email>           Set email (set to 'auto' to automatically download from a disposable email)
    -f <format> --format <format>        Set format
    --cookies <file>                     Path to cookies.txt file so albums in your collection can be downloaded
    --identity <value>                   Value of identity cookie so albums in your collection can be downloaded
    --download-history-file <file>       Path to history file containing downloaded albums

Tagging options:
    --release-tags                       Tag album, albumartist(sort), artists, artistsort, track and disc numbers
                                         with totals, and releasetype: single for track URLs, album for album URLs
    --split-artists                      With --release-tags, split the artists tag on the separators
    --artist-separators <separators>     Space separated; words need spaces around them, symbols don't
                                         (default: "feat. , & x and")
    --cover-original                     Embed the original-resolution cover instead of Bandcamp's 700px one (FLAC)
    --tag <tag>                          Set a fixed tag as key=value, e.g. --tag "media=Digital Media".
                                         Repeatable; applied last, so it overrides other tags

Formats:
    - FLAC
    - V0MP3
    - 320MP3
    - AAC
    - Ogg
    - ALAC
    - WAV
    - AIFF
```
