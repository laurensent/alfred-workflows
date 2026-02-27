# BlitzSearch - Technical Design Document

## Overview

BlitzSearch is a high-performance fuzzy file/folder search workflow for Alfred, using `fd` with custom ranking algorithms and typo tolerance.

## Architecture

```
User Input
    |
    v
+-------------------+
| Parse @options    |  Extract @h/@f/@d options
| and #folder       |  Extract folder filters (AND logic)
+-------------------+
    |
    v
+-------------------+
| History search    |  Instant: fuzzy match against ~100 entries
| (threshold=5)     |
+-------------------+
    |
    v
+-------------------+     Tier 1: fd -i <pattern>
| fd (file finder)  |     Filters at filesystem level
| Tiered search     |     (not full scan)
+-------------------+
    |
    |  [if < 5 results AND max_score < 1500]
    v
+-------------------+     Tier 2: fd -i <subsequence>
| fd subsequence    |     e.g. "cfg" -> c.*f.*g
+-------------------+
    |
    |  [if still 0 results AND threshold >= 3]
    v
+-------------------+     Tier 3: fd . (reduced depth)
| Levenshtein       |     + Levenshtein for typo correction
| fallback          |
+-------------------+
    |
    v
+-------------------+
| Merge & rank      |  History first, then search results
+-------------------+
    |
    v
Alfred JSON Output
```

## Tiered Search Strategy

### Tier 1: fd Pattern Match (fastest)

Passes the search term directly to `fd -i` as a regex pattern, filtering at the filesystem level instead of listing all files.

- Single word: `fd -i search` (substring match)
- Multi-word: `fd -i 'blitz.*search'` (words joined with `.*`)
- Special characters are escaped with `re.escape()` for safe regex

### Tier 2: Subsequence Pattern

Triggered only when Tier 1 returns < 5 results AND max_score < 1500 (no good quality match). Generates a character-by-character subsequence regex.

- `cfg` -> `fd -i 'c.*f.*g'` (matches `config`, `CFGPT_2.js`, etc.)
- Skipped when Tier 1 already has high-quality matches (max_score >= 1500)

### Tier 3: Levenshtein Fallback

Triggered only when Tiers 1+2 return zero results AND `fuzzy_threshold >= 3`. Runs `fd .` with reduced depth (min of configured depth and 5) to keep it fast, then applies Levenshtein distance filtering.

- `serach` -> finds `search` via Levenshtein similarity

## Fuzzy Scoring Algorithm

### Score Priority (High to Low)

| Score Range | Match Type | Example |
|-------------|------------|---------|
| 10000 | Exact match | `readme` == `readme` |
| 5000 - len | Prefix match | `read` matches `readme.md` |
| 3000 - pos - len | Contains | `adme` in `readme.md` |
| 2000 - pos - len | Word boundary | `alfred workflows` matches `alfred-workflows` |
| 1000 + similarity | Levenshtein | `alfredworkflaws` ~ `alfred-workflows` |
| 500 - len | Subsequence | `rme` matches `readme` (r-e-a-d-m-e) |

### Levenshtein Similarity Calculation

```python
similarity = 100 - (distance * 100 // max_length)
```

### Threshold Control

The `fuzzy_threshold` setting (1-5) controls multiple matching parameters:

**Levenshtein Similarity** (`min_similarity = 100 - threshold * 12`):

| threshold | min_similarity | Description |
|-----------|----------------|-------------|
| 1 | 88% | Very strict |
| 2 | 76% | Strict |
| 3 | 64% | Default |
| 4 | 52% | Lenient |
| 5 | 40% | Very lenient |

**Subsequence Density** (`min_density = 0.9 - threshold * 0.12`):

Prevents false positives from sparse character matches in long filenames.

| threshold | min_density | Description |
|-----------|-------------|-------------|
| 1 | 78% | Almost continuous |
| 2 | 66% | |
| 3 | 54% | Default |
| 4 | 42% | |
| 5 | 30% | Allows sparse matches |

**Subsequence Match Examples**:

| Match | Density | t=1 | t=2 | t=3 | t=4 | t=5 |
|-------|---------|-----|-----|-----|-----|-----|
| `rme` -> `readme` | 50% | X | X | X | O | O |
| `rdme` -> `readme` | 67% | X | O | O | O | O |
| `laurensent` -> Docker book | 15% | X | X | X | X | X |

## Performance Optimizations

### 1. Filesystem-level Filtering

**Problem**: Previous approach used `fd .` to list all files, then piped everything to `fzf --filter`. For large directories this scanned 100k+ files unnecessarily.

**Solution**: Pass the search pattern directly to `fd -i <pattern>`, letting fd filter at the filesystem level. This dramatically reduces output and eliminates the fzf subprocess.

**Benchmarks** (searching `~` with depth 8):

| Query | Old (`fd .` + fzf) | New (`fd <pattern>`) | Speedup |
|-------|-------------------|---------------------|---------|
| `search` | 0.66s | 0.22s | 3.0x |
| `readme` | 0.54s | 0.33s | 1.6x |
| `serach` (typo) | 1.13s | 0.40s | 2.8x |

### 2. Length-based Pre-filtering

**Problem**: Calculating Levenshtein distance for all files is O(n * m * k) where k is file count.

**Solution**: Use mathematical property of Levenshtein distance:
```
levenshtein(a, b) >= |len(a) - len(b)|
```

**Implementation**:
```python
# For search term "alfredworkflaws" (15 chars) with threshold=5:
# min_similarity = 40%, max_allowed_dist = 15 * 60% + 1 = 10
# Only check files with name length in range [5, 25]

min_name_len = max(1, term_len - max_allowed_dist)
max_name_len = term_len + max_allowed_dist

if name_len < min_name_len or name_len > max_name_len:
    continue  # Skip expensive Levenshtein calculation
```

**Result**: Filters out ~90% of files before Levenshtein calculation.

### 3. C Extension for Levenshtein

**Problem**: Pure Python Levenshtein is slow for string comparison.

**Solution**: Use `python-Levenshtein` C extension library.

```python
try:
    from Levenshtein import distance as levenshtein
except ImportError:
    # Fallback to pure Python implementation
    def levenshtein(a, b): ...
```

**Installation**:
```bash
pip install python-Levenshtein
```

## History-based Fuzzy Search

History records are searched **before** the main fd search with maximum tolerance:

```python
# Always use threshold=5 for history (instant due to small size)
score = fuzzy_score(filename, search_term, threshold=5)
```

**Benefits**:
- History is small (~100 entries) - fuzzy matching is instant
- High-frequency files get typo tolerance at all threshold levels
- History results are prioritized (displayed first)

**Storage**: `~/Library/Application Support/Alfred/Workflow Data/com.laurenwong.blitzsearch/history.json`

## Folder Filter Syntax

Use `#folder` to filter by directory path with fuzzy matching (AND logic for multiple filters):

```
fs leetcode #inbox          # Search "leetcode" in paths containing "inbox"
fs config #dotfiles #vim    # Must match both "dotfiles" AND "vim" in path
fs algo #donwloads          # Typo tolerance: matches "Downloads" folder
```

Folder filters use the same fuzzy matching as filename search (controlled by `fuzzy_threshold`).

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `search_path` | `~` | Search directories (semicolon-separated) |
| `num_candidates` | `50` | Max results shown |
| `max_depth` | `8` | fd max directory depth (4-12) |
| `fuzzy_threshold` | `3` | 1=strict, 5=lenient (typo tolerance) |
| `max_history` | `100` | Max history entries |
| `history_expire_months` | `3` | Auto-delete old history |
| `exclude_patterns` | `Library;.Trash;...` | Patterns to exclude (glob supported) |

## File Structure

```
BlitzSearch/
├── search.py          # Main search script
├── history.py         # History display
├── record_history.py  # Record opened files
├── info.plist         # Alfred workflow config
├── README.md          # User documentation
└── DESIGN.md          # Technical design document
```

## Dependencies

- **fd**: `brew install fd` - Fast file finder
- **python-Levenshtein** (optional): `pip install python-Levenshtein` - C extension for faster fuzzy matching
