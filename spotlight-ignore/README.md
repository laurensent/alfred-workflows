# Spotlight Ignore

Alfred workflow for managing macOS Spotlight exclusions.

## Features

- List and manage Spotlight exclusion paths
- Add exclusions via Universal Action
- Remove exclusions with one click
- Reveal excluded paths in Finder

## Setup

Open workflow folder, run `./install_helper.sh` in Terminal (one-time setup).

## Usage

**List exclusions:** `spig`
- Enter: Remove selected path
- Cmd+Enter: Reveal in Finder

**Add exclusions:**
- Select file/folder, use Universal Action "Add to Spotlight Ignore"

## Note

Changes restart Spotlight indexing service (mds). May take a few seconds to complete.

## Requirements

- Alfred 5 with Powerpack
- macOS 10.14+

## License

MIT License - see [LICENSE](../LICENSE) file
