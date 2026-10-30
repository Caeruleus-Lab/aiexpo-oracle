"""Open Graph / Twitter / description / canonical tags, shared by build_index.py and every lesson's build_web.py."""
import html as H

SITE = "https://aiexpo.buildwithoracle.com"


def og_tags(*, title, description, path, image, image_alt, lang="th", kind="website"):
    """path: site-relative URL of the page ('' for the landing page, '<dir>/th' for a lesson edition)."""
    url = f"{SITE}/{path}"
    loc, alt = ("en_US", "th_TH") if lang == "en" else ("th_TH", "en_US")
    e = lambda s: H.escape(s, quote=True)
    return "\n".join([
        f'<meta name="description" content="{e(description)}">',
        f'<link rel="canonical" href="{e(url)}">',
        f'<meta property="og:type" content="{kind}">',
        '<meta property="og:site_name" content="AIExpo Oracle">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(description)}">',
        f'<meta property="og:url" content="{e(url)}">',
        f'<meta property="og:locale" content="{loc}">',
        f'<meta property="og:locale:alternate" content="{alt}">',
        f'<meta property="og:image" content="{SITE}/og/{image}">',
        f'<meta property="og:image:secure_url" content="{SITE}/og/{image}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(image_alt)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(title)}">',
        f'<meta name="twitter:description" content="{e(description)}">',
        f'<meta name="twitter:image" content="{SITE}/og/{image}">',
        f'<meta name="twitter:image:alt" content="{e(image_alt)}">',
    ])
