# BlitzSearch - Technical Design Document

## Overview

BlitzSearch is a high-performance fuzzy file/folder search workflow for Alfred, using `fd` + `fzf` with custom ranking algorithms and typo tolerance.

## Architecture

```
User Input
    |
    v
+-------------------+
| Parse #folder     |  Extract folder filters (AND logic)
| filters           |
+-------------------+
    |
    v
+-------------------+
| fd (file finder)  |  Scan directories, exclude Library/.git/etc
+-------------------+
    |
    v
+-------------------+
| Folder filtering  |  Apply #folder filters (case-insensitive)
+-------------------+
    |
    v
+-------------------+
| fzf --filter      |  Initial fuzzy filtering on filenames
+-------------------+
    |
    v
+-------------------+
| Python ranking    |  Re-rank with custom fuzzy_score()
+-------------------+
    |
    v
+-------------------+
| Fuzzy fallback    |  Typo tolerance (when threshold > 3)
| (Levenshtein)     |
+-------------------+
    |
    v
Alfred JSON Output
```

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

**Typo Fallback**: Only enabled at threshold > 3 (to maintain speed at lower thresholds).

## Performance Optimizations

### 1. Length-based Pre-filtering

**Problem**: Calculating Levenshtein distance for 50,000+ files is O(n * m * k) where k is file count.

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

### 2. C Extension for Levenshtein

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

### 3. Two-stage Filtering

**Stage 1**: fzf for initial filtering
- Fast C implementation
- Reduces candidate set from 50,000 to ~1,000

**Stage 2**: Python for precise ranking
- Custom scoring algorithm
- Better relevance than fzf alone

### Performance Benchmarks

| Optimization | Time | Improvement |
|--------------|------|-------------|
| No optimization | 4-5s | - |
| Length pre-filtering | 0.39s | ~10x |
| + C extension | 0.15s | ~25x |

## History-based Fuzzy Search

History records are searched **before** the main fd+fzf search with maximum tolerance:

```python
# Always use threshold=5 for history (instant due to small size)
score = fuzzy_score(filename, search_term, threshold=5)
```

**Benefits**:
- History is small (~100 entries) - fuzzy matching is instant
- High-frequency files get typo tolerance at all threshold levels
- History results are prioritized (displayed first)

**Storage**: `~/Library/Application Support/Alfred/Workflow Data/com.laurenwong.blitzsearch/history.json`

## Fallback Strategy

Typo-tolerant fallback is triggered when:
1. `max_score < 1500` (no exact/prefix/contains match)
2. `fuzzy_threshold > 3` (user wants typo tolerance)

```python
if max_score < 1500 and fuzzy_threshold > 3:
    fallback_results = fuzzy_fallback(fd_results, search_term, ...)
    # Merge with existing results, avoiding duplicates
```

**Design rationale**: History provides typo tolerance for frequently used files at all threshold levels. Full typo fallback is only enabled at high tolerance settings to avoid slowing down searches.

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
- **fzf**: `brew install fzf` - Fuzzy finder
- **python-Levenshtein** (optional): `pip install python-Levenshtein` - C extension for faster fuzzy matching
