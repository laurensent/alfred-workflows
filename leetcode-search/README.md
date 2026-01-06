# LeetCode Search

Search LeetCode problems with fuzzy matching and smart caching.

## Features
- Fuzzy search with smart ranking
- Chinese tokenization (no spaces needed)
- Multi-term search (order-insensitive)
- Silent background cache refresh
- Support for LeetCode CN and US

## Usage
- `lc [query]` - Search LeetCode CN
- `lcm [query]` - Search LeetCode US
- `lcupdate` - Force refresh cache
- `Cmd+L` - Quick access via hotkey

## Search Examples
- `88` or `two sum` - by number or title
- `tsum` - fuzzy match "Two Sum"
- `bst` - matches "Binary Search Tree"
- `dp hard` - multi-term search

## Configuration
- Cache Update Interval: 1/3/6/12 months (default: 3)

## Acknowledgments
This workflow is inspired by [@JamesHopbourn](https://github.com/JamesHopbourn)'s [leetcode-alfred-workflow](https://github.com/JamesHopbourn/leetcode-alfred-workflow)