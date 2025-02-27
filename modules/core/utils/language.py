from modules.core.models.company_setting import CompanySetting

def get_user_language(user):
    """Get user's language, falling back to default if not set"""
    if user.settings and user.settings.language:
        return user.settings.language
    return 'en'  # Default to English
