#!/usr/bin/env python3
"""Extract feature name from description."""
import re
import sys

def kebab_case(text):
    """Convert text to kebab-case."""
    # Replace non-alphanumeric with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Split on camelCase
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    # Convert to lowercase and kebab
    return re.sub(r'\s+', '-', text.lower()).strip('-')

def extract_feature_name(description):
    """Extract concise feature name from description."""
    # Remove common words
    words = description.lower().split()
    key_words = [w for w in words if w not in ['a', 'an', 'the', 'for', 'to', 'in', 'with']]
    return kebab_case(' '.join(key_words[:3]))

if __name__ == '__main__':
    desc = ' '.join(sys.argv[1:])
    print(extract_feature_name(desc))
