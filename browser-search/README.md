# Browser Search

Fast fuzzy search for bookmarks, history and tabs.

## Features

- Fuzzy search bookmarks and history with adjustable tolerance
- Search and switch between open browser tabs
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
| ChatGPT Atlas | Y | Y | Partial | - |
| Dia | Y | Y | Partial | - |

**Notes:**
- **Partial**: Tabs search only, no switching; no Incognito support

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
| Cmd+Enter | Incognito |
| Cmd+B | Bookmarks |
| Cmd+H | History |
| Option+T | Tabs |

## Configuration

| Option | Description |
|--------|-------------|
| Browser | Select browser (or use `bbr` to switch) |
| Profiles | Profiles to search (or use `bpf` to switch) |
| Fuzzy | Search tolerance (1-5) |

## Requirements

- Alfred 5 with Powerpack

## License

MIT License - see [LICENSE](../LICENSE) file
