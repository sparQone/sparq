# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Translation module that provides core translation functionality including
#     preloading translations, custom translation function, and formatting functions.
#
# Copyright (c) 2025 remarQable LLC
#
# This software is released under an open-source license.
# See the LICENSE file for details.
# -----------------------------------------------------------------------------
import json
import os
from datetime import datetime

from flask import current_app
from flask import g

# Store translations in memory
TRANSLATIONS = {}


def preload_translations():
    """Load all module translations into memory at startup"""
    global TRANSLATIONS
    TRANSLATIONS = {}

    modules_path = os.path.join(current_app.root_path, "modules")

    for module_name in os.listdir(modules_path):
        module_path = os.path.join(modules_path, module_name)
        if not os.path.isdir(module_path):
            continue

        module_lang_path = os.path.join(module_path, "lang")

        if os.path.isdir(module_lang_path):
            for lang_file in os.listdir(module_lang_path):
                if lang_file.endswith(".json"):
                    lang_code = lang_file.replace(".json", "")
                    file_path = os.path.join(module_lang_path, lang_file)

                    with open(file_path, "r", encoding="utf-8") as f:
                        TRANSLATIONS.setdefault(lang_code, {}).setdefault(module_name, {}).update(
                            json.load(f)
                        )


def translate(text):
    """Custom translation function"""
    lang = g.get("lang", current_app.config.get("DEFAULT_LANGUAGE", "en"))
    current_module = g.get("current_module", {}).get("name", "core")

    # If we're not in the core module, try the module-specific translation
    if current_module != "core":
        module_trans = TRANSLATIONS.get(lang, {}).get(current_module, {}).get(text)
        # Only use module translation if it's nonempty
        if module_trans is not None and module_trans != "":
            return module_trans

    # Fallback to core translation
    core_trans = TRANSLATIONS.get(lang, {}).get("core", {}).get(text)
    if core_trans is not None and core_trans != "":
        return core_trans

    # Finally, return the original text if no translation is found.
    return text


def get_format_patterns(lang=None):
    """Get formatting patterns for the current language"""
    if not lang:
        lang = g.get("lang", current_app.config.get("DEFAULT_LANGUAGE", "en"))

    # Get patterns from core module first (defaults)
    patterns = TRANSLATIONS.get(lang, {}).get("core", {}).get("_meta", {}).copy()

    # Override with current module patterns if they exist, but only if the value is nonempty.
    current_module = g.get("current_module", {}).get("name", "core")
    module_patterns = TRANSLATIONS.get(lang, {}).get(current_module, {}).get("_meta", {})

    for key, value in module_patterns.items():
        # Only override if the module value is not empty
        if value:
            patterns[key] = value

    return patterns


def format_date(date, format_type="medium"):
    """Format a date according to the current language patterns"""
    if not date:
        return ""

    patterns = get_format_patterns()
    date_formats = patterns.get("date_formats", {})
    pattern = date_formats.get(format_type, "%Y-%m-%d")  # Default pattern in strftime format

    # Convert pattern from our format to strftime format
    pattern = (
        pattern.replace("YYYY", "%Y")
        .replace("MM", "%m")
        .replace("DD", "%d")
        .replace("HH", "%H")
        .replace("mm", "%M")
    )

    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        return date.strftime(pattern)
    except (ValueError, AttributeError) as e:
        current_app.logger.error(f"Error formatting date: {e}")
        return str(date)


def format_number(number, decimal_places=2):
    """Format a number according to the current language patterns"""
    patterns = get_format_patterns()
    formats = patterns.get("number_formats", {})
    decimal_sep = formats.get("decimal_separator", ".")
    thousand_sep = formats.get("thousand_separator", ",")

    # Format number with proper separators
    number_str = f"{number:,.{decimal_places}f}"
    if thousand_sep != ",":
        number_str = number_str.replace(",", thousand_sep)
    if decimal_sep != ".":
        number_str = number_str.replace(".", decimal_sep)

    return number_str
