# Glow Skincare – Culturally Adaptive Web Application

**Author:** Oluwadamilola Tinubu
**Student Number:** C24344666
**Module:** SDEV2004 – Software for the Global Market

---

## Setup and Execution Instructions

**Requirements:** Python 3.10+, pip

0. Navigate into the project folder: `cd "Beauty Page"`
1. Install dependencies: `pip install -r requirements.txt`
2. Compile translations: `pybabel compile -d translations`
3. Run the app: `python run.py`
4. Open `http://127.0.0.1:5000` in your browser. Use the EN, ES and 日本語 buttons in the header to switch locale.

## Project Overview

For this project I built a culturally adaptive product page for a fictional skincare brand called Glow. The website allows users to browse and discover different skincare products made for their skin. I built the application using Flask and Jinja2. It adapts its layout, content, colours, imagery, navigation and language depending on which locale the user selects. My target area is adults and teenagers interested in skincare and beauty.

---

## Cultural Scope

**Supported languages:** English (from America), Spanish (from Spain) and Japanese (from Japan)

**Cultural models applied:**

- **Hofstede's Individualism vs Collectivism** — this dimension separates cultures where people prioritise personal choice and individual identity from cultures where group consensus and community trust matters more.
- **Hall's Affective vs Neutral** — this dimension distinguishes cultures that express emotion openly in professional and commercial contexts from cultures that keep communication restrained and fact-based.

**Which cultures map to which dimensions:**

- America and Spain score high on Hofstede's Individualism index and are classified as Affective cultures under Hall's framework.
- Japan scores low on the Individualism index, placing it in the Collectivist category, and is classified as a Neutral culture.

---

## Design Rationale

### Problem Statements

When I looked at the target user groups, I noticed three problems:

1. Skincare shoppers from Spain and the US tend to make purchasing decisions independently and respond well to personalised suggestions. When a product page is cluttered with clinical detail they didn't ask for, it slows them down and feels impersonal.
2. Japanese skincare shoppers tend to be more cautious before purchasing and rely heavily on what others think. Without visible reviews and transparent ingredient information, they're less likely to trust the product.
3. Japanese users also expect a factual, structured presentation. When a page leads with emotional language like "Find Your Perfect Glow" and lifestyle photography, it can feel out of place and untrustworthy to a user who expects clear, professional information.

### Hypotheses

**Hypothesis 1 — Individualism/Affective (EN/ES):**
We believe that implementing a "Recommended for you" section with personal product suggestions for busy skincare shoppers in America and Spain will lead to faster product selection and higher satisfaction, because users from individualist cultures prefer content that feels tailored to them personally rather than generic.

**Hypothesis 2 — Collectivism (JA):**
We believe that making customer reviews and ratings visible on the product page for Japanese users will increase trust and make purchases more likely, because collectivist users rely on social proof — knowing that others have bought and approved a product reduces individual risk.

**Hypothesis 3 — Neutral (JA):**
We believe that showing a detailed product information section covering ingredients, usage instructions and results for information-focused Japanese users will improve usability and reduce purchase hesitation, because neutral cultures prioritise factual evidence over emotional appeal when evaluating products.

### How Cultural Thinking Shaped the Design

Once I had the hypotheses in place, I tried to make sure every design decision traced back to one of them rather than just looking nice:

- The hero section uses emotional language and lifestyle imagery for EN/ES because affective cultures respond to that. For JA, the hero headline is just the product name and the subtext is clinical.
- The colour scheme is bold pink for EN/ES (expressive, high contrast) and soft teal for JA (restrained, professional).
- The navigation has three items for EN/ES (Home, Shop, About) and four for JA (Home, Products, Ingredients, Reviews).
- Currency is localised: €29.99 for EN, €29,99 for ES (comma decimal is standard in Spain), and ¥3,200 for JA.

---

## Architecture and Structure

```
Beauty Page/
├── app/
│   ├── __init__.py          # App factory, Babel setup, locale selector
│   ├── routes.py            # Blueprint, CULTURAL_CONFIG, route handlers
│   └── templates/
│       ├── base.html        # Base template (header, nav, footer, lang switcher)
│       └── product.html     # Product page with all cultural adaptation logic
│   └── static/
│       ├── css/
│       │   └── style.css    # CSS variables for cultural colour schemes
│       └── images/          # Lifestyle and minimal product images
├── translations/
│   ├── en/LC_MESSAGES/      # English .po and .mo
│   ├── es/LC_MESSAGES/      # Spanish .po and .mo
│   └── ja/LC_MESSAGES/      # Japanese .po and .mo
├── babel.cfg
├── requirements.txt
├── README.md
└── run.py
```

**Template inheritance:** `base.html` defines the shared page shell. `product.html` extends it with `{% extends 'base.html' %}` and fills in the `{% block content %}` block. This means I only had to write the structural HTML once, and all cultural variation happens inside the content block.

**Dynamic behaviour:** The key to how the adaptation works is the `CULTURAL_CONFIG` dictionary in `routes.py`. It maps each locale to a set of flags — things like `layout_style`, `colour_scheme`, `show_recommendations`, and `show_detailed_info`. Those flags get passed into the Jinja template as a `config` object, and the template uses `{% if %}` blocks to decide what to show.

---

## Internationalisation and Localisation Strategy

I used Flask-Babel with GNU gettext for all translations. Every user-facing string in the templates is wrapped in `{% trans %}...{% endtrans %}`, which Babel uses to extract, translate and render the correct string at runtime.

**Language switching:** There's a language switcher in the header with three buttons (EN, ES, 日本語). Clicking one calls `/set_lang/<lang>`, which saves the choice to the Flask session. The `locale_selector` function in `__init__.py` reads that session value on every request and tells Babel which language to use. If no session value is set, Babel falls back to the browser's `Accept-Language` header.

**Default and fallback:** English is the default locale. If somehow a locale ends up being something unexpected, `routes.py` falls back to the English cultural config.

**Translation files:** Each language has a `messages.po` file under `translations/<locale>/LC_MESSAGES/`. These were compiled into binary `.mo` files using `pybabel compile`.

---

## Cultural Adaptation Mechanisms

The way the page adapts comes down to four things working together.

**Colour scheme:** I defined two sets of colours in the CSS — one bold and expressive for EN/ES (hot pink, high contrast) and one soft and restrained for JA (muted teal). Whichever locale is active, the page automatically loads the right colour set. Everything from buttons to backgrounds to section headings changes with it.

**Content sections:** The recommendations grid and skin quiz only appear for EN/ES users. The ingredient grid, usage instructions and reviews only appear for JA users. This is handled server-side in the template, so the wrong content is never even sent to the browser.

**Hero:** The size, headline and imagery all change based on the locale. EN/ES gets a large, lifestyle-driven hero with emotional language. JA gets a compact, product-focused hero with a clinical headline.

**Images:** The hero background and the main product photo both swap depending on the locale. EN/ES gets lifestyle photography. JA gets clean, minimal product shots on a white background.

| UI Element | EN/ES | JA |
|---|---|---|
| Hero size | Large, full bleed | Compact |
| Hero headline | "Find Your Perfect Glow" | Product name |
| Colour scheme | Bold pink | Soft teal |
| Navigation | 3 items | 4 items |
| Hero image | Lifestyle photo | Minimal product shot |
| Main content | Recommendations + skin quiz | Ingredient grid + reviews |
| Best seller badge | Hidden | Visible |
| Currency | €29.99 / €29,99 | ¥3,200 |

---

## Features Implemented

I built one product page that changes significantly depending on which locale is active.

**EN and ES users see:**
- A large hero with an emotional headline and a "Shop Now" button
- A skin type quiz asking "What's your skin type?" with four options — Oily, Dry, Combination and Sensitive
- A "Recommended For You" section showing three related products with lifestyle imagery
- The main product card with EUR pricing

**JA users see:**
- A compact hero with the product name as the headline and a clinical description underneath
- A product information grid broken into four sections — Ingredients, How to Use, Skin Type and Results
- A customer reviews section with star ratings and two quotes from buyers
- A "Best Seller — Loved by our community" banner above the product card
- The main product card with a minimal white-background image and ¥ pricing

All text across the page is fully translated into whichever language is active.

---

## Hypotheses Implementation

**Hypothesis 1 — Recommendations and skin quiz (EN/ES only):**
The "Recommended For You" section and the skin quiz only appear when the locale is English or Spanish. They are hidden entirely for Japanese users. The skin quiz speaks directly to the user as an individual ("What's your skin type?") which reflects the individualist dimension — the idea that EN/ES users prefer content that feels personally relevant to them rather than generic.

**Hypothesis 2 — Reviews and social proof (JA only):**
Japanese users see a customer reviews section with star ratings and two buyer quotes, as well as a "Best Seller — Loved by our community" banner above the product card. Both of these are hidden for EN/ES users. The reasoning is that collectivist users are more likely to trust a product when they can see that other people have already bought and approved it.

**Hypothesis 3 — Detailed product information (JA only):**
Japanese users also see a four-column information grid covering the full ingredient list, step-by-step usage instructions, skin type suitability and a results claim backed by a statistic. This section doesn't appear for EN/ES users at all. It's there because neutral cultures place much more weight on factual evidence than emotional appeal when deciding whether to trust a product.

---

**Requirements:** Python 3.10+, pip

0. Navigate into the project folder: `cd "Beauty Page"`
1. Install dependencies: `pip install -r requirements.txt`
2. Compile translations: `pybabel compile -d translations`
3. Run the app: `python run.py`
4. Open `http://127.0.0.1:5000` in your browser. Use the EN, ES and 日本語 buttons in the header to switch locale.
---

## Limitations and Future Work

**Current limitations:**
- The skin type quiz is visual only — selecting an option does not filter recommendations.
- The best seller badge and reviews are hardcoded, not pulled from a database.
- Currency values are fixed and not connected to a live exchange rate API.
- Only one page has been built.
- Testing has been done on Chrome and Firefox only.

**Future work:**
- Connect the skin quiz to a recommendation engine that filters products by skin type.
- Add a database backend so reviews and bestseller status reflect real user behaviour.
- Extend cultural adaptation to additional pages for a consistent full shopping journey.
- Add RTL language support (e.g. Arabic) to demonstrate adaptation across more dimensions.
- Conduct usability testing with real users from each target culture to validate the hypotheses.
