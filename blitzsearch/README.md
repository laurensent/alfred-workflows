# BlitzSearch

Real-time fuzzy file/folder search for Alfred using fd + fzf.

## Features

- Real-time search with no indexing required
- Fuzzy matching with typo tolerance
- Filter by type (hidden, files, directories) or folder path
- Smart ranking prioritizes exact and prefix matches
- Search history with auto-cleanup
- Alfred Fallback Search support

## Usage

| Keyword | Description |
|---------|-------------|
| `fs [query]` | Fuzzy search files and folders |
| `fs [query] #folder` | Filter by folder name (supports multiple, AND logic) |
| `fs [query] @filter` | Filter by type (see below) |
| `fsh [query]` | Show recently opened files |

**Modifier:** Hold `Shift` on selected result to open enclosing folder

### Type Filters

| Filter | Shortcut | Description |
|--------|----------|-------------|
| `@hidden` | `@h` | Only hidden files/folders |
| `@files` | `@f` | Only files |
| `@dirs` | `@d` | Only directories |

Filters can be combined: `@hf` = hidden files, `@hd` = hidden directories

### Examples

```
fs readme                  # Search for "readme"
fs config #dotfiles        # Search "config" in "dotfiles" folder
fs test #src #utils        # Match both "src" AND "utils" in path
fs @h zshrc                # Search hidden files for "zshrc"
fs @d config               # Search directories only
fs @hf bashrc              # Search hidden files only
fs plist #library          # Search in Library (overrides exclude)
```

**Tip:** Using `#folder` that matches an excluded pattern (e.g., `#library` matching `Library`) will temporarily override the exclusion, allowing you to search in normally excluded directories.

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Search Path | `~` | Directories to search (semicolon separated) |
| Max Depth | `8` | Directory depth limit (4-12) |
| Max Results | `50` | Maximum results shown |
| Max History | `100` | Maximum history entries |
| Auto-delete After | `3 months` | Auto-delete history older than this |
| Fuzzy Tolerance | `3` | Typo tolerance (1=strict, 5=lenient) |
| Exclude Patterns | (see workflow) | Patterns to exclude (semicolon separated, supports glob) |
| Include Hidden | `off` | Include hidden files by default |

## Requirements

- Alfred 5 with Powerpack
- [fd](https://github.com/sharkdp/fd) - Fast file finder
- [fzf](https://github.com/junegunn/fzf) - Fuzzy finder
- [python-Levenshtein](https://pypi.org/project/python-Levenshtein/) (optional) - Faster fuzzy matching

```bash
brew install fd fzf
pip3 install python-Levenshtein  # optional
```

## License

MIT License - see [LICENSE](../LICENSE) file
