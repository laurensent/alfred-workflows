# BlitzSearch

Real-time fuzzy file/folder search for Alfred using fd + fzf.

## Usage

- `fs [query]` - Fuzzy search files and folders
- `fs [query] #folder` - Filter by folder name with fuzzy matching (AND logic for multiple)
- `fsh [query]` - Show recently opened files
- `Shift` - Open enclosing folder

## Examples

```
fs readme              # Search for files containing "readme"
fs config #dotfiles    # Search "config" in paths containing "dotfiles"
fs test #src #utils    # Must match both "src" AND "utils" in path
```

## Features

- Real-time search using fd + fzf (no indexing required)
- Fuzzy matching with typo tolerance (Levenshtein distance)
- Smart ranking: exact > prefix > contains > fuzzy > subsequence
- Search history with relative timestamps
- Auto-cleanup of old history entries
- Alfred Fallback Search support

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| Search Path | `~` | Directories to search (semicolon separated) |
| Max Depth | `8` | Directory depth limit (4-12, higher = deeper but slower) |
| Max Results | `50` | Maximum number of results shown |
| Max History | `100` | Maximum history entries to keep |
| Auto-delete After | `3` | Auto-delete history older than X months |
| Fuzzy Tolerance | `3` | 1=strict, 5=lenient (controls typo tolerance) |
| Exclude Patterns | `Library;.Trash;...` | Patterns to exclude (semicolon separated, supports glob) |

## Requirements

- [fd](https://github.com/sharkdp/fd) - Fast file finder
- [fzf](https://github.com/junegunn/fzf) - Fuzzy finder
- [python-Levenshtein](https://pypi.org/project/python-Levenshtein/) (optional) - Faster fuzzy matching

### Quick Install

```bash
brew install fd fzf
pip3 install python-Levenshtein  # optional, for better performance
```

## License

MIT
