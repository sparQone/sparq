def get_user_language(user):
    """Get user's language, falling back to company default if not set"""
    if user.settings and user.settings.language:
        return user.settings.language
    return get_company_settings().default_language 