# Author: Oluwadamilola Tinubu - C24344666
# routes.py - URL routing and cultural adaptation logic
# This file defines the core cultural configuration and routing for the Glow Skincare app.
# Cultural assumptions are based on Hofstede's Individualism/Collectivism dimension
# and Hall's Affective/Neutral dimension, applied to ES (high individualism, affective)
# and JA (low individualism/collectivist, neutral) cultural contexts.

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_babel import get_locale

bp = Blueprint('main', __name__)

# CULTURAL_CONFIG defines the UI behaviour for each supported locale.
# Each key maps to a set of flags that control layout, content and styling.
# This is the central mechanism for cultural adaptation - all template decisions
# trace back to this config object being passed to the Jinja template.
#
# Hypothesis 1 (Affective/Individualist - ES/EN):
#   Users from affective, individualist cultures respond better to emotional,
#   personalised layouts with lifestyle imagery and bold colours.
#   -> layout_style: 'visual', colour_scheme: 'bold', image_style: 'lifestyle'
#
# Hypothesis 2 (Neutral/Collectivist - JA):
#   Japanese users prefer structured, information-dense layouts with neutral
#   colours and product-focused imagery, avoiding emotional or personal language.
#   -> layout_style: 'structured', colour_scheme: 'soft', image_style: 'product'
#
# Hypothesis 3 (Collectivist - JA):
#   Collectivist users are influenced by social proof and community validation.
#   Detailed ingredient info and customer reviews build trust through transparency.
#   -> show_detailed_info: True, show_recommendations: False
CULTURAL_CONFIG = {
    # English (default) - Individualist/Affective (Ireland)
    'en': {
        'layout_style': 'visual',        # Large hero, emotional headline
        'show_recommendations': True,     # Personalised product suggestions
        'show_detailed_info': False,      # No clinical detail needed
        'colour_scheme': 'bold',          # High contrast pink - Affective dimension
        'image_style': 'lifestyle',       # Lifestyle imagery - Affective dimension
    },
    # Spanish - Individualist/Affective (Spain)
    'es': {
        'layout_style': 'visual',         # Same visual approach as EN
        'show_recommendations': True,     # Personal recommendations retained
        'show_detailed_info': False,      # Emotional over informational
        'colour_scheme': 'bold',          # Bold colours - Affective dimension
        'image_style': 'lifestyle',       # Expressive lifestyle imagery
    },
    # Japanese - Collectivist/Neutral (Japan)
    'ja': {
        'layout_style': 'structured',     # Grid-based, information-first layout
        'show_recommendations': False,    # No personalisation - collectivist context
        'show_detailed_info': True,       # Clinical detail builds trust - Neutral dimension
        'colour_scheme': 'soft',          # Muted teal - Neutral dimension
        'image_style': 'product',         # Clean product shots - no emotional lifestyle imagery
    },
}

@bp.route('/')
def index():
    # Get the current locale from Flask-Babel (set via session or browser preference)
    locale = str(get_locale())
    # Look up the cultural config for this locale, falling back to English if not found
    config = CULTURAL_CONFIG.get(locale, CULTURAL_CONFIG['en'])
    # Pass both config and locale to the template so it can make cultural decisions
    return render_template('product.html', config=config, locale=locale)

@bp.route('/set_lang/<lang>')
def set_lang(lang):
    # Allow user to manually switch language via the language switcher in the header
    # The selected language is stored in the session so it persists across requests
    # Only the three supported locales are accepted to prevent invalid session values
    if lang in ['en', 'ja', 'es']:
        session['lang'] = lang
    return redirect(url_for('main.index'))