# BlitzSearch

Real-time fuzzy file/folder search for Alfred using fd + fzf.

## Usage

- `fs [query]` - Fuzzy search files and folders
- `fs [query] #folder` - Filter by folder name (fuzzy, AND logic for multiple)
- `fs [query] @filter` - Filter by type (@h=hidden, @f=files, @d=dirs)
- `fsh [query]` - Show recently opened files
- `Shift` - Open enclosing folder

## Type Filters (@)

| Filter | Shortcut | Description |
|--------|----------|-------------|
| `@hidden` | `@h` | Only hidden files/folders (starting with `.`) |
| `@files` | `@f` | Only files |
| `@dirs` | `@d` | Only directories |

Filters can be combined: `@hf` = hidden files only, `@hd` = hidden dirs only

## Examples

```
fs readme                  # Search for files containing "readme"
fs config #dotfiles        # Search "config" in paths containing "dotfiles"
fs test #src #utils        # Must match both "src" AND "utils" in path
fs @h zshrc                # Search hidden files for "zshrc"
fs @d #project config      # Search directories named "config" in project paths
fs @hf bashrc              # Search hidden files only for "bashrc"
```

## Features

- Real-time search using fd + fzf (no indexing required)
- Fuzzy matching with typo tolerance (Levenshtein distance)
- Smart ranking: exact > prefix > contains > fuzzy > subsequence
- Type filters: hidden only, files only, dirs only
- Folder filters with fuzzy matching (AND logic)
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
| Include Hidden Files | `off` | Include hidden files/folders in search results by default |

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
