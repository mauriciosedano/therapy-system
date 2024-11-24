from difflib import SequenceMatcher

def find_similar_names(name, stored_names):
    """Find similar names using fuzzy matching."""
    matches = []
    for stored_name in stored_names:
        ratio = SequenceMatcher(None, name.lower(), stored_name.lower()).ratio()
        if ratio > 0.8:
            matches.append((stored_name, ratio))
    return sorted(matches, key=lambda x: x[1], reverse=True)

def extract_therapy_details(text):
    """Extract therapy details from natural language input."""
    # Initial implementation
    return {
        'raw_text': text,
        'processed': True
    }
