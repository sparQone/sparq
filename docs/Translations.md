# Translation System in sparQ

This document explains how to make your modules multilingual using sparQ's built-in translation system.

## Overview

The translation system in sparQ is designed to be:
- Module-specific: Each module manages its own translations
- JSON-based: Simple key-value pairs stored in JSON files
- Format-aware: Supports date and number formatting based on locale
- Fallback-enabled: Falls back to core module translations, then English

## Directory Structure

Each module should have a `lang` directory containing JSON files for each supported language:

```
modules/
  your_module/
    lang/
      en.json     # English translations
      es.json     # Spanish translations
      fr.json     # French translations
```

## Translation Files

Translation files are JSON documents with two main sections:
1. `_meta`: Contains formatting patterns
2. Key-value pairs for translations

Example `es.json`:
```json
{
    "_meta": {
        "date_formats": {
            "short": "DD/MM/YYYY",
            "medium": "DD MMM YYYY",
            "long": "DD [de] MMMM [de] YYYY",
            "time": "HH:mm",
            "datetime": "DD/MM/YYYY HH:mm"
        },
        "number_formats": {
            "decimal_separator": ",",
            "thousand_separator": ".",
            "currency_symbol": "€",
            "currency_format": "{symbol}{amount}"
        }
    },
    "Welcome": "Bienvenido",
    "Save": "Guardar",
    "Cancel": "Cancelar"
}
```

## Using Translations

### In Templates

Use the `_()` function to translate strings:
```html
<h1>{{ _("Welcome") }}</h1>
<button>{{ _("Save") }}</button>
```

### Date Formatting

Use the `format_date` filter with optional format type:
```html
{{ task.created_at|format_date('short') }}   <!-- 31/01/2025 -->
{{ task.created_at|format_date('medium') }}  <!-- 31 Jan 2025 -->
{{ task.created_at|format_date('long') }}    <!-- 31 de Enero de 2025 -->
```

### Number Formatting

Use the `format_number` filter with optional decimal places:
```html
{{ amount|format_number }}      <!-- 1.234,56 -->
{{ amount|format_number(0) }}   <!-- 1.235 -->
```

## Translation Lookup Process

1. First looks for translation in current module's language file
2. If not found, looks in core module's language file
3. If still not found, returns the original text

## Format Patterns

### Date Formats
- `YYYY`: Four-digit year
- `MM`: Two-digit month
- `DD`: Two-digit day
- `HH`: Hours (24-hour)
- `mm`: Minutes

### Number Formats
- `decimal_separator`: Character used for decimal point
- `thousand_separator`: Character used for thousand separators
- `currency_symbol`: Symbol for currency
- `currency_format`: Pattern for currency display

## Adding a New Language

1. Create a new JSON file in your module's `lang` directory (e.g., `fr.json`)
2. Copy the structure from an existing language file
3. Translate all strings and adjust formatting patterns as needed

## Best Practices

1. Keep translation keys simple and descriptive
2. Use sentence case for keys: "Welcome message" not "WELCOME_MESSAGE"
3. Include all translations in the default language (usually English)
4. Test with right-to-left (RTL) languages if supporting them
5. Use format patterns consistently across your module

## Core Module Translations

The core module should contain common translations used across multiple modules. This reduces duplication and ensures consistency.

## Language Selection

The current language is determined in the following priority order:
1. URL parameter: `?lang=es`
2. User setting (stored in database for authenticated users)
3. Session storage (for temporary preferences)
4. Default language from configuration

```python
# Default language configuration in config.py
DEFAULT_LANGUAGE = 'en'
```

This translation system provides a flexible, maintainable way to support multiple languages in your sparQ modules while maintaining clean separation of concerns.
```