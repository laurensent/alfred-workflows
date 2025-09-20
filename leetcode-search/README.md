# LeetCode Search

Search LeetCode problems with fuzzy matching and smart caching.

## Features
- Smart fuzzy search (multi-term, English/Chinese, order-insensitive)
- Recent history (shows recently opened problems first)
- Silent background cache refresh
- Support for LeetCode US and CN

## Usage
- `lcs [query]` - Search LeetCode problems
  - `Enter` - Open problem description
  - `Option+Enter` - Open solutions page
- `lcsup` - Update cache (choose incremental or full)
  - Incremental: Only fetch new problems (faster)
  - Full: Refresh all problems with tags and companies
- `Option+L` - Quick access via hotkey

## Search Examples
- `88` or `two sum` - by number or title
- `tsum` - fuzzy match "Two Sum"
- `#easy` (`#e`) / `#medium` (`#m`) / `#hard` (`#h`) - filter by difficulty
- `#array`, `#dp`, `#tree` - filter by tag
- `@google`, `@amazon` - filter by company
- `#dp #hard @google` - combine filters

## Configuration

- Default Site: US or CN (default: US)
- Cache Update Interval: 1/3/6/12 months (default: 3)

## Requirements

- Alfred 5 with Powerpack

## License

MIT License - see [LICENSE](../LICENSE) file
