# CMA&F Website — Static Prototypes

Static HTML/CSS prototypes of all 15 page templates defined in the design brief
(`originalbrief.docx`). Built for **review before Elementor implementation** —
not the production WordPress build.

## Preview

```bash
python3 -m http.server 8080
# open http://localhost:8080/prototypes.html
```

The `prototypes.html` page links to every template.

## What's in here

| File | Template |
| --- | --- |
| `index.html` | 1. Homepage |
| `adult-martial-arts.html` | 2. Adult Martial Arts |
| `kids-programs.html` | 3. Kids Programs |
| `fitness-programs.html` | 4. Fitness Programs |
| `getting-started.html` | 5. Getting Started / Funnel |
| `contact.html` | 6. Contact Us |
| `timetable.html` | 7. Timetable |
| `pricing.html` | 8. Pricing |
| `about-us.html` | 9. About Us |
| `our-team.html` | 10. Our Team |
| `hapkido.html` | 11. Individual Style Page (Hapkido example) |
| `kids-birthday-parties.html` | 12. Kids Birthday Parties |
| `member-information.html` | 13. Member Information Hub |
| `privacy-policy.html`, `terms-and-conditions.html` | 14. Legal Pages |
| `blog.html`, `blog-post.html` | 15. Blog Index + Single Post |

## Design tokens

All brand colours, typography and component styles live in
`assets/css/styles.css`. The token block at the top of that file mirrors
Section 1 of the brief — change colours there and the whole site updates.

- Navy `#334477` — primary brand
- Green `#02A850` — primary CTA
- Orange `#FF6600` — secondary CTA / highlight
- Body text `#7A7A7A`
- Font: Montserrat (loaded from Google Fonts)

## Build

Pages are assembled by `build.py` from a shared shell (nav + footer) and
per-page body content. To regenerate after editing `build.py`:

```bash
python3 build.py
```

This is throwaway tooling — the production site will use Elementor templates
that re-implement these layouts inside WordPress.

## Image placeholders

No real photography is included. Card images use brand-coloured CSS gradients
so the prototype is self-contained. When the photo library is ready, swap
`.card__image--*` gradients for `background-image: url(...)`.

## What is NOT included (intentionally, per brief)

- No homepage carousel — single promo tile only
- No "Coming Soon" anywhere for Coombs — shown as equal to Woden
- No `/drop-in/` URL — contact lives at `/contact/` (`contact.html`)
- No `Spark Member` references — GymMaster throughout
- No placeholder bio text — `Bio coming soon` empty state on team cards
- No `Christmas closure` / dated seasonal content
