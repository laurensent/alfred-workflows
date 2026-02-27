# Browser Search

Fast fuzzy search for bookmarks, history and tabs.

## Features

- Fuzzy search bookmarks, history and tabs with adjustable tolerance
- Multi-word search: words match independently across title and URL (order-independent)
- Support for multiple Chromium-based browsers
- Filter bookmarks by folder with `#folder` syntax
- Multi-profile support with quick switching
- Activate existing tabs instead of opening duplicates
- Open links in incognito/private mode

## Browser Compatibility

| Browser | Bookmarks | History | Tabs | Incognito |
|---------|:---------:|:-------:|:----:|:---------:|
| Chrome (incl. Beta/Canary/Dev) | Y | Y | Y | Y |
| Brave | Y | Y | Y | Y |
| Vivaldi | Y | Y | Y | Y |
| Helium | Y | Y | Y | Y |
| Dia | Y | Y | Y | Y |
| ChatGPT Atlas | Y | Y | Partial | - |

**Notes:**
- **Partial**: Tab listing only, no tab switching via AppleScript

**Not Supported:** Safari, Firefox, Zen, Arc, Edge (different data formats or APIs, no plan to support)

## Usage

```
bm [query]              # Search bookmarks
bm #folder [query]      # Filter by folder
bh [query]              # Search history
bt [query]              # Search open tabs
bpf                     # List/switch profiles
bbr                     # List/switch browsers
```

## Shortcuts

| Key | Action |
|-----|--------|
| Enter | Open (activate tab if searching tabs) |
| Cmd+Enter | Open in Incognito |
| Cmd+B | Bookmarks |
| Cmd+H | History |
| Option+T | Tabs |

**bpf (Profiles):**
| Key | Action |
|-----|--------|
| Enter | Switch to profile |
| Cmd+Enter | Copy profile name |

## Configuration

| Option | Description |
|--------|-------------|
| Browser | Select browser (or use `bbr` to switch) |
| Profiles | Profiles to search, comma-separated for multi-profile (or use `bpf` to switch/copy) |
| Fuzzy | Search tolerance (1-5) |
| Cache TTL | How long to keep cached bookmarks (1-5 weeks) |

## Requirements

- Alfred 5 with Powerpack

## License

MIT License - see [LICENSE](../LICENSE) file
