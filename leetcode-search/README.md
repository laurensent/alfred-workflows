# LeetCode Search

Alfred workflow for searching LeetCode problems with local caching.

## Installation

1. Ensure Python `requests` package is installed
2. Import the workflow to Alfred
3. First run will download problem data automatically

## Usage

**Search Problems**
- `lc <query>` - Search and open on LeetCode China
- `lcm <query>` - Search and open on LeetCode International
- Leave query empty to show first 50 problems

**Cache Management**
- `lcupdate` - View cache status and manually update

**Examples**
- `lc 94` - Search by problem number
- `lc binary tree` - Search by keywords
- `lcm two sum` - Search on international site

## Configuration

Set workflow environment variables:
- `UPDATE_DAYS` - Auto-update interval in days (default: 7)
- `AUTO_UPDATE` - Enable auto-update (default: true)

## Acknowledgments

This workflow is inspired by [@JamesHopbourn](https://github.com/JamesHopbourn)'s [leetcode-alfred-workflow](https://github.com/JamesHopbourn/leetcode-alfred-workflow)