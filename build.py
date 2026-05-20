#!/usr/bin/env python3
"""
Build script — assembles each page from a shared shell (nav + footer)
and a unique body. Outputs static HTML files at the repo root.

Run:  python3 build.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent

SHELL = """<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Canberra Martial Arts &amp; Fitness</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>

<div class="proto-banner">Prototype — CMA&amp;F website redesign · <a href="prototypes.html">Index of all 15 templates</a></div>

<header class="nav">
  <div class="nav__inner">
    <a class="nav__logo" href="index.html">
      <span class="nav__logo-mark">C</span>
      <span>CMA&amp;F</span>
    </a>
    <nav>
      <ul class="nav__menu">
        <li><a href="adult-martial-arts.html">Adult MA</a></li>
        <li><a href="kids-programs.html">Kids</a></li>
        <li><a href="fitness-programs.html">Fitness</a></li>
        <li><a href="timetable.html">Timetable</a></li>
        <li><a href="pricing.html">Pricing</a></li>
        <li><a href="about-us.html">About</a></li>
        <li><a href="our-team.html">Team</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="nav__cta">
      <a href="getting-started.html" class="btn btn--primary">Come and Try a Class</a>
      <button class="nav__toggle" data-nav-toggle aria-label="Open menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <div class="nav__mobile" data-nav-mobile>
    <ul>
      <li><a href="adult-martial-arts.html">Adult Martial Arts</a></li>
      <li><a href="kids-programs.html">Kids Programs</a></li>
      <li><a href="fitness-programs.html">Fitness Programs</a></li>
      <li><a href="timetable.html">Timetable</a></li>
      <li><a href="pricing.html">Pricing</a></li>
      <li><a href="about-us.html">About Us</a></li>
      <li><a href="our-team.html">Our Team</a></li>
      <li><a href="blog.html">Blog</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
  </div>
</header>

{body}

<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <h4>Locations</h4>
        <ul>
          <li><strong style="color:#fff;">Woden Club</strong><br>U3/10 Townshend St, Phillip ACT 2606<br><a href="#">Open in Maps →</a></li>
          <li style="margin-top:12px;"><strong style="color:#fff;">Coombs Club</strong><br>Shop 1, 1 Fairhall St, Coombs ACT 2611<br><a href="#">Open in Maps →</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact &amp; Quicklinks</h4>
        <ul>
          <li><a href="tel:0488852191">0488 852 191</a></li>
          <li><a href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a></li>
          <li><a href="timetable.html">Class Timetables</a></li>
          <li><a href="contact.html">Book a Tour</a></li>
          <li><a href="member-information.html#codeofconduct">Code of Conduct</a></li>
          <li><a href="member-information.html#cancellation">Cancellation Policy</a></li>
          <li><a href="member-information.html#suspensionandinjury">Suspension &amp; Injury</a></li>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
        </ul>
      </div>
      <div>
        <h4>Get Started</h4>
        <p>Your first class is on us. Pick a time and come and try.</p>
        <a href="getting-started.html" class="btn btn--primary">Come and Try a Class</a>
        <div class="footer__socials">
          <a class="footer__social" href="#" aria-label="Facebook">f</a>
          <a class="footer__social" href="#" aria-label="Instagram">◎</a>
          <a class="footer__social" href="#" aria-label="YouTube">▶</a>
        </div>
      </div>
    </div>
    <div class="footer__bar">
      2026 © Canberra Martial Arts &amp; Fitness Pty Ltd · All Rights Reserved ·
      <a href="terms-and-conditions.html">Terms &amp; Conditions</a> ·
      <a href="privacy-policy.html">Privacy Policy</a>
    </div>
  </div>
</footer>

<script src="assets/js/main.js"></script>
</body>
</html>
"""

# ---- Shared partials ----
LOCATIONS_STRIP = """
<section class="locations">
  <div class="container">
    <h2>Two Clubs. One Community.</h2>
    <div class="locations__grid">
      <div class="location-card">
        <h3>Woden Club</h3>
        <p>U3/10 Townshend St, Phillip ACT 2606</p>
        <a class="btn btn--primary" href="contact.html">Book a Tour — Woden</a>
      </div>
      <div class="location-card">
        <h3>Coombs Club</h3>
        <p>Shop 1, 1 Fairhall St, Coombs ACT 2611</p>
        <a class="btn btn--primary" href="contact.html">Book a Tour — Coombs</a>
      </div>
    </div>
  </div>
</section>
"""

def final_cta(heading="Ready to Give It a Try?",
              sub="Your first class is on us. No experience, no commitment.",
              label="Come and Try a Class",
              href="getting-started.html"):
    return f"""
<section class="section section--orange">
  <div class="container final-cta">
    <h2>{heading}</h2>
    <p>{sub}</p>
    <a href="{href}" class="btn btn--primary btn--lg">{label}</a>
  </div>
</section>
"""

def testimonials(items):
    """items: list of (quote, name, initials) tuples."""
    cards = "\n".join(f"""
      <div class="testimonial">
        <p class="testimonial__quote">"{q}"</p>
        <div class="testimonial__author">
          <span class="testimonial__avatar">{i}</span>
          <span class="testimonial__name">{n}</span>
        </div>
      </div>""" for q, n, i in items)
    return f"""
<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>What Our Members Say</h2></div>
    <div class="grid grid--3">{cards}</div>
  </div>
</section>
"""

def timetable_block(label, kind="adult"):
    return f"""
<div class="card" style="padding:24px;">
  <h3 style="margin-bottom:12px;">{label}</h3>
  <p class="muted" style="margin-bottom:16px;">Snapshot — see the full timetable for all times and locations.</p>
  <div style="display:flex; gap:12px; flex-wrap:wrap;">
    <a class="btn btn--secondary" href="#">Download PDF</a>
    <a class="card__link" href="timetable.html">View full timetable</a>
  </div>
</div>
"""

# =========================================================
# PAGE DEFINITIONS
# =========================================================
PAGES = {}

# -------- Template 2: Adult Martial Arts --------
PAGES["adult-martial-arts.html"] = dict(
    title="Adult Martial Arts Classes in Canberra",
    description="Five adult martial arts styles at Woden and Coombs. Beginners welcome at every class. Start with our 21-Day Trial.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Adult Martial Arts</p>
    <h1>Adult Martial Arts Classes in Canberra</h1>
    <p class="hero__sub">5 styles to choose from. Beginners welcome at every class.</p>
    <div class="hero__ctas">
      <a href="getting-started.html" class="btn btn--primary btn--lg">Come and Try a Class</a>
      <a href="#trial" class="btn btn--secondary-outline btn--lg">Start a 21-Day Trial</a>
    </div>
  </div>
</section>

<section class="section" id="trial">
  <div class="container">
    <div class="trial-banner">
      <div>
        <p class="eyebrow">Trial offer</p>
        <h2>Start With a 21-Day Trial — $99, Unlimited Classes</h2>
        <ul>
          <li>Try every class across all five styles</li>
          <li>No obligation, no contract</li>
          <li>Uniform not required for your first sessions</li>
        </ul>
      </div>
      <div><a class="btn btn--secondary btn--lg btn--block" href="#">Grab Your 21-Day Trial</a></div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title">
      <h2>Six Styles. One Club.</h2>
      <p>Every style is taught by a qualified instructor and accessible to complete beginners.</p>
    </div>
    <div class="grid grid--3">
      {''.join(f'''
      <div class="card">
        <div class="card__image card__image--adult"><span class="card__image-label">{tag}</span></div>
        <div class="card__body">
          <h3 class="card__title">{name}</h3>
          <p class="card__desc">{desc}</p>
          <a class="card__link" href="hapkido.html">Learn More</a>
        </div>
      </div>''' for name, desc, tag in [
        ("Hapkido", "Korean self-defence focused on joint locks, throws and circular motion.", "Self-defence"),
        ("Taekwondo", "Olympic-style striking — speed, kicks and form. Strong family discipline.", "Striking"),
        ("Kummooyeh (Sword)", "Korean swordsmanship — tradition, precision, focus.", "Weapons"),
        ("Epic BJJ", "Brazilian Jiu-Jitsu — ground game, leverage and live rolling.", "Grappling"),
        ("Aware Krav Maga", "Reality-based self defence. Practical, direct, no nonsense.", "Self-defence"),
        ("Women's Self Defence", "A dedicated programme — confidence, awareness and applied technique.", "Women only"),
      ])}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Adult Timetables</h2></div>
    <div class="grid grid--2">
      {timetable_block('Woden — Adult Martial Arts')}
      {timetable_block('Coombs — Adult Martial Arts')}
    </div>
  </div>
</section>

{LOCATIONS_STRIP}

{testimonials([
    ("First time on the mats in my 40s. The instructors slowed it right down — I never felt out of place.", "James R. — Hapkido", "JR"),
    ("Joined for BJJ, stayed for the people. I look forward to training every week.", "Hannah T. — Epic BJJ", "HT"),
    ("Krav Maga gave me confidence I didn't know I needed. Practical and well taught.", "Andrew M. — Aware Krav Maga", "AM"),
])}

{final_cta('Find Your Style', 'Come and try a class, or jump straight to the 21-Day Trial.', 'Come and Try a Class')}
"""
)

# -------- Template 3: Kids Programs --------
PAGES["kids-programs.html"] = dict(
    title="Kids Martial Arts Classes in Canberra — Ages 3 to 14",
    description="Kids martial arts at Woden and Coombs. Tiny Tigers (3–4), Tigers (5–8), Youth (9–13). Confidence, discipline and fun.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Kids Programs</p>
    <h1>Kids Martial Arts Classes in Canberra — Ages 3 to 14</h1>
    <p class="hero__sub">Confidence, discipline, and fun. Two locations: Woden and Coombs.</p>
    <div class="hero__ctas">
      <a href="#" class="btn btn--primary btn--lg">Try a Class — Woden</a>
      <a href="#" class="btn btn--primary btn--lg">Try a Class — Coombs</a>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Find Your Child's Age Group</h2></div>
    <div class="grid grid--3">
      <a href="#pre-martial-arts" class="card" style="text-decoration:none;color:inherit;">
        <div class="card__image card__image--kids"><span class="card__image-label">Ages 3–4</span></div>
        <div class="card__body">
          <h3 class="card__title">Tiny Tigers</h3>
          <p class="card__desc">First introduction to coordination, listening and play-based learning.</p>
          <span class="card__link">Jump to section</span>
        </div>
      </a>
      <a href="#pre-martial-arts" class="card" style="text-decoration:none;color:inherit;">
        <div class="card__image card__image--kids"><span class="card__image-label">Ages 5–8</span></div>
        <div class="card__body">
          <h3 class="card__title">Tigers</h3>
          <p class="card__desc">Structured martial arts foundations — discipline, focus and serious fun.</p>
          <span class="card__link">Jump to section</span>
        </div>
      </a>
      <a href="#youth" class="card" style="text-decoration:none;color:inherit;">
        <div class="card__image card__image--kids"><span class="card__image-label">Ages 9–13</span></div>
        <div class="card__body">
          <h3 class="card__title">Youth Martial Arts</h3>
          <p class="card__desc">Style-specific training across Hapkido, Taekwondo, BJJ and Kumdo (Sword).</p>
          <span class="card__link">Jump to section</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="trial-banner">
      <div>
        <p class="eyebrow">Kids trial pack</p>
        <h2>3-Week Trial Pack — From $59</h2>
        <p>Ages 5–6: $59 · Ages 7–14: $69 · 3 weeks of unlimited classes + a full uniform pack.</p>
      </div>
      <div style="display:grid; gap:10px;">
        <a class="btn btn--primary" href="#">Woden Trial</a>
        <a class="btn btn--primary" href="#">Coombs Trial</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Kids Timetables</h2></div>
    <div class="grid grid--2">
      {timetable_block('Woden — Kids Martial Arts')}
      {timetable_block('Coombs — Kids Martial Arts')}
    </div>
  </div>
</section>

<section class="section" id="pre-martial-arts">
  <div class="container">
    <div class="section-title">
      <h2>Pre-Martial Arts — Ages 3 to 8</h2>
      <p>Two distinct age bands. Different photos, different energy.</p>
    </div>
    <div class="grid grid--2">
      <div class="card">
        <div class="card__image card__image--kids"><span class="card__image-label">3–4 yrs</span></div>
        <div class="card__body">
          <h3 class="card__title">Tiny Tigers (3–4 yrs)</h3>
          <p class="card__desc">Parent-supported, play-based introduction. Listening, balance, taking turns. 30-minute classes.</p>
        </div>
      </div>
      <div class="card">
        <div class="card__image card__image--kids"><span class="card__image-label">5–8 yrs</span></div>
        <div class="card__body">
          <h3 class="card__title">Tigers (5–8 yrs)</h3>
          <p class="card__desc">Structured martial arts foundations. Belt progression, focus mitts, sparring drills with armour.</p>
        </div>
      </div>
    </div>
    <div class="center mt-4" style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
      <a class="btn btn--primary" href="#">Try a Class — Woden</a>
      <a class="btn btn--primary" href="#">Try a Class — Coombs</a>
    </div>
  </div>
</section>

<section class="section section--grey" id="youth">
  <div class="container">
    <div class="section-title"><h2>Youth Martial Arts — Ages 9 to 13</h2></div>
    <div class="grid grid--4">
      {''.join(f'''
      <div class="card">
        <div class="card__image card__image--kids"><span class="card__image-label">9–13 yrs</span></div>
        <div class="card__body">
          <h3 class="card__title">{name}</h3>
          <p class="card__desc">{desc}</p>
        </div>
      </div>''' for name, desc in [
        ("Youth Hapkido", "Self-defence focus — joint locks, throws, situational awareness."),
        ("Youth Taekwondo", "Striking, kicks and form. Olympic-style progression."),
        ("Epic Youth BJJ", "Brazilian Jiu-Jitsu for teens — leverage, control, live drilling."),
        ("Youth Kumdo (Sword)", "Korean swordsmanship — discipline, precision, focus."),
      ])}
    </div>
    <div class="center mt-4" style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
      <a class="btn btn--primary" href="#">Try a Class — Woden</a>
      <a class="btn btn--primary" href="#">Try a Class — Coombs</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title">
      <h2>Junior Leadership Programme</h2>
      <p>Teens can progress from student to paid instructor assistant. Real responsibility, real mentoring.</p>
    </div>
    <div class="center"><a class="btn btn--primary" href="contact.html">Find Out More</a></div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="grid grid--2">
      <div class="card">
        <div class="card__image card__image--kids"><span class="card__image-label">School holidays</span></div>
        <div class="card__body">
          <h3 class="card__title">Holiday Programmes</h3>
          <p class="card__desc">Full-day and half-day school holiday programmes at Woden. Martial arts, games and projects.</p>
          <a class="card__link" href="#">Book a Holiday Programme</a>
        </div>
      </div>
      <div class="card">
        <div class="card__image card__image--party"><span class="card__image-label">Tiger Parties</span></div>
        <div class="card__body">
          <h3 class="card__title">Birthday Parties</h3>
          <p class="card__desc">Ages 5–9. Two classes, cake break, board breaking finale. From $225 (10 kids).</p>
          <a class="card__link" href="kids-birthday-parties.html">Plan a Party</a>
        </div>
      </div>
    </div>
  </div>
</section>

{LOCATIONS_STRIP}

{testimonials([
    ("My 5-year-old went from clinging to my leg to leading warm-ups. The Tigers instructors are gold.", "Jen O. — Tigers parent", "JO"),
    ("Our Youth Hapkido group is the highlight of his week. He's more focused at school too.", "Daniel S. — Youth parent", "DS"),
    ("Tiny Tigers is perfect for our 3-year-old. Calm, structured, fun.", "Aisha R. — Tiny Tigers parent", "AR"),
])}

{final_cta('Ready to Get Your Child Started?', "Pick a club and we'll see you at class.", 'Try a Class — Woden', '#')}
"""
)

# -------- Template 4: Fitness Programs --------
PAGES["fitness-programs.html"] = dict(
    title="Fitness Classes in Canberra — Group Fitness With Personality",
    description="Group fitness at CMA&F. FLEXfit, POWERfit, FIGHTINGfit, HIITfit and Jerra bootcamp. Two locations.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Fitness Programs</p>
    <h1>Fitness Classes in Canberra — With People Who Actually Have Fun</h1>
    <p class="hero__sub">Group fitness that gets results without the serious vibe.</p>
    <div class="hero__ctas">
      <a href="getting-started.html" class="btn btn--primary btn--lg">Come and Try a Class</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title">
      <h2>Five Fitness Classes</h2>
      <p>Each class is led by a qualified coach. All levels welcome — modify or push, your choice.</p>
    </div>
    <div class="grid grid--3">
      {''.join(f'''
      <div class="card">
        <div class="card__image card__image--fitness"><span class="card__image-label">{tag}</span></div>
        <div class="card__body">
          <h3 class="card__title">{name}</h3>
          <p class="muted" style="margin-bottom:8px;"><strong style="color:var(--orange);">{hashtag}</strong></p>
          <p class="card__desc">{desc}</p>
        </div>
      </div>''' for name, hashtag, desc, tag in [
        ("Mobility &amp; Flexibility", "#FLEXfit", "Move better, hurt less. Active flexibility and joint range work.", "Recovery"),
        ("Strength &amp; Endurance", "#POWERfit", "Progressive strength training in a small-group format.", "Strength"),
        ("Cardio Boxing", "#FIGHTINGfit", "Cardio boxing with martial arts elements. Energy, sweat, fun.", "Cardio"),
        ("HIIT Intervals", "#HIITfit", "High-intensity intervals — efficient and effective.", "HIIT"),
        ("Outdoor Bootcamp", "#JERRAbootcamp", "6am outdoor bootcamp at Jerrabomberra. Best way to start the day.", "Outdoor"),
      ])}
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="grid grid--2" style="align-items:center;">
      <div>
        <p class="eyebrow">Personal Training</p>
        <h2>One-on-One Coaching</h2>
        <p>Tailored programming for specific goals — strength, weight loss, return from injury, sport prep. Sessions with qualified CMA&amp;F coaches at either club.</p>
        <a class="btn btn--secondary" href="contact.html">Enquire About PT</a>
      </div>
      <div class="card__image card__image--fitness" style="aspect-ratio:4/3; border-radius:var(--radius-lg);"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Fitness Timetables</h2></div>
    <div class="grid grid--2">
      {timetable_block('Woden — Fitness')}
      {timetable_block('Coombs — Fitness')}
    </div>
  </div>
</section>

{LOCATIONS_STRIP}

{testimonials([
    ("FIGHTINGfit is the most fun I've had at a gym. I actually look forward to 6am.", "Eli W. — Fitness", "EW"),
    ("The 6am Jerra bootcamp changed my mornings. Coach pushes you but it never feels like a slog.", "Chloe B. — Bootcamp", "CB"),
    ("POWERfit is structured strength without the gym-bro nonsense. Loved it.", "Sam P. — Fitness", "SP"),
])}

{final_cta('Come Sweat With Us', 'First class on us. Then decide.', 'Come and Try a Class')}
"""
)

# -------- Template 5: Getting Started --------
PAGES["getting-started.html"] = dict(
    title="Getting Started — Let's Get You Started",
    description="Pick a club, find a class time, and come and try. That's it.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Let's Get You Started</h1>
    <p class="hero__sub">Pick your club, find a class time, and come and try. That's it.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:840px;">

    <div class="step">
      <span class="step__num">1</span>
      <h2>Pick Your Club</h2>
      <p>Both clubs run a full schedule of adult, kids and fitness classes.</p>
      <div class="grid grid--2 mt-2">
        <div class="card" style="padding:24px;">
          <h3>Woden Club</h3>
          <p class="muted">U3/10 Townshend St, Phillip ACT 2606</p>
          <p class="muted">Mon–Fri 6:00am–9:00pm · Sat 7:00am–12:00pm</p>
          <a class="btn btn--primary btn--block" href="#">Book a Tour — Woden</a>
        </div>
        <div class="card" style="padding:24px;">
          <h3>Coombs Club</h3>
          <p class="muted">Shop 1, 1 Fairhall St, Coombs ACT 2611</p>
          <p class="muted">Mon–Fri 6:00am–8:30pm · Sat 7:00am–11:00am</p>
          <a class="btn btn--primary btn--block" href="#">Book a Tour — Coombs</a>
        </div>
      </div>
    </div>

    <div class="step">
      <span class="step__num">2</span>
      <h2>Book a Tour or Call</h2>
      <p>Pick a time that works. A coach will walk you through the club and answer questions.</p>
      <div style="aspect-ratio:16/10; background:var(--grey-50); border:1px dashed var(--grey-200); border-radius:var(--radius-lg); display:grid; place-items:center; color:var(--text);">
        GHL booking calendar embed
      </div>
      <p class="muted mt-2"><strong>Can't find a time?</strong> Call <a href="tel:0488852191">0488 852 191</a> or email <a href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a></p>
    </div>

    <div class="step">
      <span class="step__num">3</span>
      <h2>Come and Try</h2>
      <p>You'll get a confirmation with your class details. No uniform needed. No experience required. Just turn up.</p>
    </div>

    <div class="step">
      <span class="step__num">4</span>
      <h2>Grab a Trial Pack (If You Love It)</h2>
      <p class="muted">Kids from $59 · Adults $99 · 3-week unlimited access.</p>
      <div class="grid grid--2 mt-2">
        <a class="btn btn--secondary" href="#">Kids Trial — Woden</a>
        <a class="btn btn--secondary" href="#">Kids Trial — Coombs</a>
        <a class="btn btn--secondary" href="#">Adult Trial — Woden</a>
        <a class="btn btn--secondary" href="#">Adult Trial — Coombs</a>
      </div>
    </div>

  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Quick Questions</h2></div>
    <div class="faq">
      <details><summary>What should I wear?</summary><p>Comfortable activewear. No uniform needed for your first class — we'll sort that later if you join.</p></details>
      <details><summary>Can I watch a class first?</summary><p>Yes — book a tour and we'll show you around. You're also welcome to watch from the lounge before joining a class.</p></details>
      <details><summary>What if I've never done martial arts?</summary><p>Most of our members started exactly where you are. Every class is built to accommodate complete beginners.</p></details>
      <details><summary>Can my child join?</summary><p>Yes — kids from 3 years old. Pick a class time on the <a href="timetable.html">timetable</a> and book a trial.</p></details>
    </div>
  </div>
</section>
"""
)

# -------- Template 6: Contact --------
PAGES["contact.html"] = dict(
    title="Get in Touch",
    description="Contact CMA&F. Call, email, or book a tour. Two locations: Woden and Coombs.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Get in Touch</h1>
    <p class="hero__sub">We'd love to meet you. Pick an option below.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="max-width:760px; margin:0 auto;">
      <div class="card" style="padding:24px;">
        <h3>Call us</h3>
        <p class="muted">Tom or one of the team will pick up Mon–Fri 9am–6pm.</p>
        <a class="btn btn--primary btn--block" href="tel:0488852191">0488 852 191</a>
      </div>
      <div class="card" style="padding:24px;">
        <h3>Email us</h3>
        <p class="muted">We reply within one business day.</p>
        <a class="btn btn--primary btn--block" href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Booking Options</h2></div>
    <div class="grid grid--3" style="margin-bottom:32px;">
      <a class="card" style="padding:24px; text-decoration:none; color:inherit;" href="#">
        <h3>Book a Tour — Woden</h3>
        <p>Walk through the Woden club with a coach. 20 minutes.</p>
        <span class="card__link">Pick a time</span>
      </a>
      <a class="card" style="padding:24px; text-decoration:none; color:inherit;" href="#">
        <h3>Book a Tour — Coombs</h3>
        <p>Walk through the Coombs club with a coach. 20 minutes.</p>
        <span class="card__link">Pick a time</span>
      </a>
      <a class="card" style="padding:24px; text-decoration:none; color:inherit;" href="#">
        <h3>Book a Phone Call</h3>
        <p>Prefer to talk first? Pick a 15-minute slot.</p>
        <span class="card__link">Pick a time</span>
      </a>
    </div>
    <div style="aspect-ratio:16/9; background:var(--white); border:1px dashed var(--grey-200); border-radius:var(--radius-lg); display:grid; place-items:center; color:var(--text); max-width:900px; margin:0 auto;">
      GHL booking calendar embed
    </div>
    <p class="muted center mt-2">Prefer to message? Use the chat widget in the bottom right corner.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Find Us</h2></div>
    <div class="grid grid--2">
      <div class="card">
        <div style="aspect-ratio:16/10; background:linear-gradient(135deg, var(--navy), #6a7cb0); display:grid; place-items:center; color:rgba(255,255,255,.7);">Woden — embedded map</div>
        <div class="card__body">
          <h3 class="card__title">Woden Club</h3>
          <p class="card__desc">U3/10 Townshend St, Phillip ACT 2606</p>
          <p class="muted">Mon–Fri 6:00am–9:00pm · Sat 7:00am–12:00pm</p>
        </div>
      </div>
      <div class="card">
        <div style="aspect-ratio:16/10; background:linear-gradient(135deg, var(--green), #6fd28e); display:grid; place-items:center; color:rgba(255,255,255,.7);">Coombs — embedded map</div>
        <div class="card__body">
          <h3 class="card__title">Coombs Club</h3>
          <p class="card__desc">Shop 1, 1 Fairhall St, Coombs ACT 2611</p>
          <p class="muted">Mon–Fri 6:00am–8:30pm · Sat 7:00am–11:00am</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
)

# -------- Template 7: Timetable --------
PAGES["timetable.html"] = dict(
    title="Class Timetables",
    description="Class timetables for Woden and Coombs. Adults, kids and fitness.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Class Timetables</h1>
    <p class="hero__sub">Pick your club, find your time.</p>
  </div>
</section>

<section class="section--tight" style="background:var(--orange); color:#fff; text-align:center;">
  <div class="container" style="padding-top:14px; padding-bottom:14px;">
    <strong>School Holiday Schedule in Effect</strong> — modified Tiger and Tiny Tiger times. <a href="#" style="color:#fff; text-decoration:underline;">See holiday timetable →</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="tabs" data-tabs="club">
      <button class="tab active" data-tab="woden">Woden</button>
      <button class="tab" data-tab="coombs">Coombs</button>
    </div>

    <!-- WODEN PANEL -->
    <div data-panel-group="club" data-panel="woden">
      <h2>Woden Timetable</h2>

      <h3 style="margin-top:32px;">Kids Martial Arts</h3>
      <div class="timetable-wrap">
        <table class="timetable">
          <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>
          <tbody>
            <tr><td>3:30pm</td><td>Tiny Tigers</td><td></td><td>Tiny Tigers</td><td></td><td>Tiny Tigers</td><td></td></tr>
            <tr><td>4:00pm</td><td>Tigers</td><td>Tigers</td><td>Tigers</td><td>Tigers</td><td>Tigers</td><td>Tigers</td></tr>
            <tr><td>5:00pm</td><td>Youth Hapkido</td><td>Youth TKD</td><td>Youth BJJ</td><td>Youth Kumdo</td><td>Youth Hapkido</td><td></td></tr>
          </tbody>
        </table>
      </div>
      <p class="mt-2"><a class="btn btn--secondary" href="#">Download Kids PDF</a> &nbsp; <a class="card__link" href="kids-programs.html">Learn more about kids programs</a></p>

      <h3 style="margin-top:32px;">Adult Martial Arts</h3>
      <div class="timetable-wrap">
        <table class="timetable">
          <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>
          <tbody>
            <tr><td>6:00pm</td><td>Hapkido</td><td>BJJ</td><td>Taekwondo</td><td>Krav Maga</td><td>Hapkido</td><td>Open Mat</td></tr>
            <tr><td>7:30pm</td><td>BJJ</td><td>Krav Maga</td><td>Hapkido</td><td>Kummooyeh</td><td>Women's SD</td><td></td></tr>
          </tbody>
        </table>
      </div>
      <p class="mt-2"><a class="btn btn--secondary" href="#">Download Adult PDF</a> &nbsp; <a class="card__link" href="adult-martial-arts.html">Learn more about adult martial arts</a></p>

      <h3 style="margin-top:32px;">Fitness</h3>
      <div class="timetable-wrap">
        <table class="timetable">
          <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>
          <tbody>
            <tr><td>6:00am</td><td>FIGHTINGfit</td><td>POWERfit</td><td>HIITfit</td><td>POWERfit</td><td>FIGHTINGfit</td><td>FLEXfit</td></tr>
            <tr><td>12:00pm</td><td>FLEXfit</td><td></td><td>FLEXfit</td><td></td><td>FLEXfit</td><td></td></tr>
          </tbody>
        </table>
      </div>
      <p class="mt-2"><a class="btn btn--secondary" href="#">Download Fitness PDF</a> &nbsp; <a class="card__link" href="fitness-programs.html">Learn more about fitness</a></p>
    </div>

    <!-- COOMBS PANEL -->
    <div data-panel-group="club" data-panel="coombs" hidden>
      <h2>Coombs Timetable</h2>
      <p>Coombs is a combined-program club — kids, adults and fitness times below.</p>
      <div class="timetable-wrap">
        <table class="timetable">
          <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>
          <tbody>
            <tr><td>6:00am</td><td>POWERfit</td><td>FIGHTINGfit</td><td>POWERfit</td><td>HIITfit</td><td>POWERfit</td><td>FLEXfit</td></tr>
            <tr><td>3:30pm</td><td>Tiny Tigers</td><td>Tigers</td><td>Tiny Tigers</td><td>Tigers</td><td>Tigers</td><td>Tigers</td></tr>
            <tr><td>5:00pm</td><td>Youth Hapkido</td><td>Youth BJJ</td><td>Youth TKD</td><td>Youth BJJ</td><td>Youth Hapkido</td><td></td></tr>
            <tr><td>6:30pm</td><td>Hapkido</td><td>BJJ</td><td>Taekwondo</td><td>Krav Maga</td><td>Hapkido</td><td></td></tr>
          </tbody>
        </table>
      </div>
      <p class="mt-2"><a class="btn btn--secondary" href="#">Download Coombs PDF</a></p>
    </div>

  </div>
</section>

<section class="section section--grey">
  <div class="container center">
    <h2>Book Into Classes Anywhere</h2>
    <p>Use the GymMaster app to book, cancel and track your progress.</p>
    <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
      <a class="btn btn--primary" href="#">App Store</a>
      <a class="btn btn--primary" href="#">Google Play</a>
    </div>
  </div>
</section>

{final_cta()}
"""
)

# -------- Template 8: Pricing --------
PAGES["pricing.html"] = dict(
    title="Simple, Transparent Pricing",
    description="CMA&F pricing. No lock-in contracts. No sign-up fees. Trial packs from $59.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Simple, Transparent Pricing</h1>
    <p class="hero__sub">No lock-in contracts. No sign-up fees. No surprises.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <div class="card" style="padding:24px; text-align:center;">
        <h3>No Lock-In Contracts</h3>
        <p>Cancel any time with notice. Memberships flex around your life.</p>
      </div>
      <div class="card" style="padding:24px; text-align:center;">
        <h3>No Sign-Up Fees</h3>
        <p>What you see is what you pay. No hidden joining costs.</p>
      </div>
      <div class="card" style="padding:24px; text-align:center;">
        <h3>Inclusive Community</h3>
        <p>10% off for ADF, First Responders and Students. You belong here.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Try Before You Commit</h2></div>
    <div class="grid grid--2" style="max-width:840px; margin:0 auto;">
      <div class="price-card popular">
        <h3>Kids Trial</h3>
        <p class="muted">3 weeks unlimited + uniform pack</p>
        <div class="price-card__price">$59<span> from</span></div>
        <ul>
          <li>Ages 5–6 from $59</li>
          <li>Ages 7–14 from $69</li>
          <li>Uniform pack included</li>
          <li>All classes, both clubs</li>
        </ul>
        <a class="btn btn--primary" href="#">Grab a Kids Trial</a>
      </div>
      <div class="price-card">
        <h3>Adults Trial</h3>
        <p class="muted">21 days unlimited across all 5 styles</p>
        <div class="price-card__price">$99</div>
        <ul>
          <li>Try every adult class</li>
          <li>No obligation, no contract</li>
          <li>Uniform not required</li>
          <li>Both clubs</li>
        </ul>
        <a class="btn btn--primary" href="#">Grab an Adults Trial</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="adults">
  <div class="container">
    <div class="section-title"><h2>Adult Memberships</h2></div>
    <div class="grid grid--4">
      {''.join(f'''
      <div class="price-card{' popular' if pop else ''}">
        <h3>{name}</h3>
        <div class="price-card__price">${price}<span>/wk</span></div>
        <ul>{''.join(f'<li>{f}</li>' for f in feats)}</ul>
        <a class="btn btn--primary" href="#">Get Started</a>
      </div>''' for name, price, feats, pop in [
        ("Unlimited Access", "57", ["All adult classes", "Both clubs", "All 5 styles"], False),
        ("Family of 2", "77.50", ["Two members", "All classes", "Both clubs"], False),
        ("Family of 3", "97.50", ["Three members", "All classes", "Best value"], True),
        ("Family Pass", "104.50", ["Four+ members", "All classes", "Unlimited"], False),
      ])}
    </div>
    <p class="muted center mt-4">Prices include public holidays and Christmas shutdown. No extra fees.</p>
  </div>
</section>

<section class="section section--grey" id="kids">
  <div class="container">
    <div class="section-title"><h2>Kids Memberships</h2></div>
    <div class="grid grid--3">
      <div class="price-card">
        <h3>Standard</h3>
        <div class="price-card__price">$67.50<span>/fn</span></div>
        <ul><li>1× class per week</li><li>Belt progression</li><li>Uniform included</li></ul>
        <a class="btn btn--primary" href="#">Get Started</a>
      </div>
      <div class="price-card">
        <h3>Double</h3>
        <div class="price-card__price">$87.50<span>/fn</span></div>
        <ul><li>2× classes per week</li><li>Belt progression</li><li>Uniform included</li></ul>
        <a class="btn btn--primary" href="#">Get Started</a>
      </div>
      <div class="price-card popular">
        <h3>Unlimited</h3>
        <div class="price-card__price">$105<span>/fn</span></div>
        <ul><li>Unlimited classes</li><li>All kids programs</li><li>Holiday programmes included</li></ul>
        <a class="btn btn--primary" href="#">Get Started</a>
      </div>
    </div>
    <p class="muted center mt-4">48 weeks of classes per year. Unlimited classes during school holidays.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Questions About Pricing</h2></div>
    <div class="faq">
      <details><summary>Can I pay weekly or fortnightly?</summary><p>Fortnightly direct debit is standard. Weekly is available on request.</p></details>
      <details><summary>Is there a joining fee?</summary><p>No. No joining fee, no sign-up cost, no admin fee.</p></details>
      <details><summary>What happens if I get injured?</summary><p>See our <a href="member-information.html#suspensionandinjury">suspension &amp; injury policy</a>. We pause your membership.</p></details>
      <details><summary>How do I cancel?</summary><p>Notify us in writing. See the <a href="member-information.html#cancellation">cancellation policy</a> for the full process.</p></details>
      <details><summary>Do you offer discounts?</summary><p>Yes — 10% off for ADF, First Responders and students. Just ask.</p></details>
    </div>
  </div>
</section>

{final_cta('Not Ready Yet?', "Try before you commit. Come and try a class first — it's on us.", 'Come and Try a Class First')}
"""
)

# -------- Template 9: About Us --------
PAGES["about-us.html"] = dict(
    title="About Us — More Than a Gym",
    description="Canberra Martial Arts & Fitness has been training Canberrans since 2011. Two clubs, one community.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">About CMA&amp;F</p>
    <h1>More Than a Gym. More Like a Family.</h1>
    <p class="hero__sub">CMA&amp;F has been training Canberrans since 2011. Here's our story.</p>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:900px;">
    <div class="grid grid--2">
      <div>
        <h2>Vision</h2>
        <p>To empower self-confidence through self-awareness and a passion for martial arts and fitness.</p>
      </div>
      <div>
        <h2>Mission</h2>
        <p>To provide fun, safe and engaging martial arts and fitness programs unlike anything else available.</p>
      </div>
    </div>
    <h2 class="mt-4">Our Values</h2>
    <ol style="color:var(--text); font-size:1.05rem; line-height:1.9;">
      <li>Respect — for self, for training partners, for the art.</li>
      <li>Discipline — show up, work hard, do it again.</li>
      <li>Community — every member is a contributor, not a customer.</li>
      <li>Growth — we measure progress over performance.</li>
      <li>Inclusion — three-year-olds to sixty-year-olds, all welcome.</li>
      <li>Authenticity — qualified instructors teaching real martial arts.</li>
      <li>Fun — if you're not enjoying it, we're doing it wrong.</li>
      <li>Lifetime learning — a black belt is a beginning, not an end.</li>
    </ol>
  </div>
</section>

<section class="section section--grey">
  <div class="container" style="max-width:900px;">
    <h2>How CMA&amp;F Began</h2>
    <p>Tom started CMA&amp;F in 2011 with a small Hapkido class at a community hall in Phillip. Fifteen years later, the club teaches five martial arts styles and a full fitness program across two locations.</p>
    <p>The reason hasn't changed: build a place where people who would never walk into a typical gym feel like they belong. Kids who are shy. Adults who haven't trained since school. Parents wanting something for their three-year-old. The club is built around them.</p>
    <div class="card__image card__image--adult" style="aspect-ratio:21/9; border-radius:var(--radius-lg); margin-top:24px;"></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Our Two Clubs</h2></div>
    <div class="grid grid--2">
      <div class="card">
        <div class="card__image card__image--adult"><span class="card__image-label">Woden HQ</span></div>
        <div class="card__body">
          <h3 class="card__title">Woden Club</h3>
          <p class="card__desc">Our HQ since 2014. Full mat space, weights area, lounge and shower facilities.</p>
          <p class="muted">U3/10 Townshend St, Phillip ACT 2606</p>
          <a class="card__link" href="#">Open in Maps</a>
        </div>
      </div>
      <div class="card">
        <div class="card__image card__image--fitness"><span class="card__image-label">Coombs</span></div>
        <div class="card__body">
          <h3 class="card__title">Coombs Club</h3>
          <p class="card__desc">Opened to serve Molonglo Valley. Full programming, same standards, same community.</p>
          <p class="muted">Shop 1, 1 Fairhall St, Coombs ACT 2611</p>
          <a class="card__link" href="#">Open in Maps</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Why Train With Us</h2></div>
    <div class="grid grid--4">
      {''.join(f'<div class="card" style="padding:20px; text-align:center;"><div style="width:48px;height:48px;border-radius:50%;background:var(--green);color:#fff;display:grid;place-items:center;margin:0 auto 12px;font-weight:700;">{i}</div><h3 style="font-size:1.05rem;">{f}</h3></div>'
        for i, f in [
          ("①","All Ages 3–60yrs+"),
          ("②","Qualified Instructors"),
          ("③","5 MA + 3 Fitness Programs"),
          ("④","Community &amp; Accountability"),
          ("⑤","GymMaster Member App"),
          ("⑥","Two Locations"),
          ("⑦","WiFi Lounge"),
          ("⑧","Lifetime of Learning"),
        ])}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Awards &amp; Recognition</h2></div>
    <div class="grid grid--3">
      <div class="card" style="padding:24px; text-align:center;"><h3>ThreeBestRated</h3><p>2021 · 2022 · 2023</p></div>
      <div class="card" style="padding:24px; text-align:center;"><h3>ActiveActivities</h3><p>Most Popular Kids Activity</p></div>
      <div class="card" style="padding:24px; text-align:center;"><h3>Canberra Local</h3><p>Community Club of the Year</p></div>
    </div>
  </div>
</section>

{final_cta('Come Meet Us', 'A 20-minute tour is the best way to feel the place out.')}
"""
)

# -------- Template 10: Our Team --------
PAGES["our-team.html"] = dict(
    title="Meet the Team",
    description="Every instructor at CMA&F is a qualified Black Belt, a certified coach, or both.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Our Team</p>
    <h1>Meet the Team</h1>
    <p class="hero__sub">Every instructor at CMA&amp;F is a qualified Black Belt, a certified coach, or both — and every one of them genuinely loves what they do.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Founders</h2></div>
    <div class="grid grid--2">
      <div class="team-card" style="text-align:left; padding:32px;">
        <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap;">
          <div class="team-card__photo" style="flex:none; margin:0;">TA</div>
          <div style="flex:1; min-width:200px;">
            <h3>Tom Adam</h3>
            <p class="team-card__role">Founder &amp; Chief Instructor · Master Instructor Hapkido</p>
            <p><strong>Why:</strong> Built CMA&amp;F to create a club where everyone feels they belong.</p>
            <p><strong>Classes:</strong> Adult Hapkido, Senior Instructor seminars.</p>
            <p><strong>One thing:</strong> A black belt is a beginner who never quit.</p>
          </div>
        </div>
      </div>
      <div class="team-card" style="text-align:left; padding:32px;">
        <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap;">
          <div class="team-card__photo" style="flex:none; margin:0; background:linear-gradient(135deg, var(--orange), var(--green));">TC</div>
          <div style="flex:1; min-width:200px;">
            <h3>Tamara Cain</h3>
            <p class="team-card__role">Director · Head Instructor Kids · Senior Instructor Taekwondo &amp; Kummooyeh</p>
            <p><strong>Why:</strong> Wants every kid who walks in to leave taller than they came.</p>
            <p><strong>Classes:</strong> Tigers, Tiny Tigers, Youth Taekwondo, Adult Kummooyeh.</p>
            <p><strong>One thing:</strong> Discipline is showing up on the days you don't feel like it.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Senior Instructors</h2></div>
    <div class="grid grid--4">
      {''.join(f'<div class="team-card"><div class="team-card__photo">{i}</div><h3>{n}</h3><p class="team-card__role">{r}</p><p>{b}</p></div>' for n, r, i, b in [
        ("Steven Cain", "Senior Instructor Hapkido", "SC", "10+ years on the mats. Calm, technical, generous with feedback."),
        ("Danny Weir", "Senior Instructor BJJ", "DW", "Coach for Epic BJJ adult and youth programs."),
        ("Jez Margosis", "Senior Instructor Krav Maga", "JM", "Aware Krav Maga lead. Reality-based, no theatrics."),
        ("Brett Hasler", "Senior Instructor TKD", "BH", "Olympic-style Taekwondo specialist."),
        ("Cassandra Layne", "Senior Instructor Kids", "CL", "Tigers head coach. Endless patience."),
        ("Riley Diwell", "Instructor Hapkido", "RD", "Came up through the Tigers program."),
        ("Zoe Stanford", "Instructor Women's SD", "ZS", "Women's Self Defence lead."),
        ("Jake Keily", "Instructor BJJ", "JK", "Epic BJJ kids and adults."),
        ("Eric Flis", "Instructor Hapkido", "EF", "Hapkido and Kummooyeh."),
      ])}
      <div class="team-card team-card--placeholder"><div class="team-card__photo">?</div><h3>Gaby Mora</h3><p class="team-card__role">Instructor</p><p>Bio coming soon</p></div>
      <div class="team-card team-card--placeholder"><div class="team-card__photo">?</div><h3>Bryce Lightbody</h3><p class="team-card__role">Instructor</p><p>Bio coming soon</p></div>
      <div class="team-card team-card--placeholder"><div class="team-card__photo">?</div><h3>Derek Souyave</h3><p class="team-card__role">Instructor</p><p>Bio coming soon</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Junior Instructor Team</h2></div>
    <div class="grid grid--4">
      {''.join(f'<div class="team-card" style="padding:20px;"><div class="team-card__photo" style="width:72px; height:72px; font-size:1.25rem;">{i}</div><h3 style="font-size:1.1rem;">{n}</h3><p class="team-card__role">{r}</p></div>' for n, r, i in [
        ("Marie Boldeman", "Junior Instructor", "MB"),
        ("Sebastian Cain", "Junior Instructor", "SC"),
        ("Zac Keily", "Junior Instructor", "ZK"),
        ("And more", "Junior Leadership", "+"),
      ])}
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title">
      <h2>Junior Leadership Programme</h2>
      <p>Think you have what it takes? Our Junior Leadership Programme trains teens to become instructors.</p>
    </div>
    <div class="center"><a class="btn btn--primary" href="contact.html">Find Out More</a></div>
  </div>
</section>

{final_cta('Come and Try a Class — Meet the Team in Person', 'Pick a time, walk in, train with whoever is teaching.')}
"""
)

# -------- Template 11: Hapkido (style page example) --------
PAGES["hapkido.html"] = dict(
    title="Hapkido Classes in Canberra",
    description="Adult Hapkido at Woden and Coombs. Korean self-defence. Beginners welcome.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Adult Martial Arts · Hapkido</p>
    <h1>Hapkido Classes in Canberra</h1>
    <p class="hero__sub">Korean self-defence built on joint locks, throws and circular motion. Taught by a Master Instructor.</p>
    <a href="getting-started.html" class="btn btn--primary btn--lg">Come and Try a Class</a>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:840px;">
    <h2>What Is Hapkido?</h2>
    <p>Hapkido is a Korean martial art built around three core ideas: harmony of force, circular motion, and water principle. Instead of meeting force with force, you redirect it.</p>
    <p>In practice, you'll learn joint locks, throws, kicks, strikes, falls, and weapons forms. It's an effective self-defence system that's also a deep technical art with a clear belt progression.</p>
    <p>It suits people who like learning a system over time — beginners are welcome at every class.</p>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>What to Expect at CMA&amp;F</h2></div>
    <div class="grid grid--4">
      {''.join(f'<div class="card" style="padding:24px; text-align:center;"><h3 style="font-size:1.05rem;">{t}</h3><p>{d}</p></div>' for t, d in [
        ("Class size", "8–18 students with 1–2 instructors."),
        ("Experience level", "Every class accommodates complete beginners."),
        ("What to wear", "Comfortable activewear. Uniform optional for your first month."),
        ("Progression", "10-level belt system. Promotion testing every ~6 months."),
      ])}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Meet Your Instructor</h2></div>
    <div class="grid grid--2" style="max-width:860px; margin:0 auto;">
      <div class="team-card" style="text-align:left; padding:28px;">
        <div style="display:flex; gap:20px; align-items:flex-start;">
          <div class="team-card__photo" style="margin:0;">TA</div>
          <div>
            <h3>Tom Adam</h3>
            <p class="team-card__role">Master Instructor Hapkido</p>
            <p>Founded CMA&amp;F in 2011. 20+ years training, 15+ years teaching.</p>
          </div>
        </div>
      </div>
      <div class="team-card" style="text-align:left; padding:28px;">
        <div style="display:flex; gap:20px; align-items:flex-start;">
          <div class="team-card__photo" style="margin:0; background:linear-gradient(135deg, var(--orange), var(--green));">SC</div>
          <div>
            <h3>Steven Cain</h3>
            <p class="team-card__role">Senior Instructor Hapkido</p>
            <p>10+ years on the mats. Calm, technical, generous with feedback.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Sample Class Times</h2></div>
    <div class="grid grid--2">
      {timetable_block('Woden — Hapkido')}
      {timetable_block('Coombs — Hapkido')}
    </div>
  </div>
</section>

<section class="section section--orange">
  <div class="container final-cta">
    <h2>Start Your Hapkido Journey — 21-Day Trial</h2>
    <p>$99 · Unlimited classes · No obligation</p>
    <a class="btn btn--primary btn--lg" href="#">Grab Your 21-Day Trial</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>You Might Also Be Interested In</h2></div>
    <div class="grid grid--3">
      {''.join(f'''<a class="card" href="hapkido.html" style="text-decoration:none;color:inherit;">
        <div class="card__image card__image--adult"><span class="card__image-label">Related</span></div>
        <div class="card__body"><h3 class="card__title">{n}</h3><p class="card__desc">{d}</p><span class="card__link">Learn More</span></div>
      </a>''' for n, d in [
        ("Taekwondo", "Olympic-style striking and form."),
        ("Aware Krav Maga", "Reality-based self defence."),
        ("Kummooyeh (Sword)", "Korean swordsmanship."),
      ])}
    </div>
  </div>
</section>
"""
)

# -------- Template 12: Kids Birthday Parties --------
PAGES["kids-birthday-parties.html"] = dict(
    title="Kids Birthday Parties — Tiger Parties at Woden",
    description="Martial arts birthday parties for kids 5–9 at our Woden Club. Active, fun, and unforgettable.",
    body=f"""
<section class="hero">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Birthday Parties</p>
    <h1>Martial Arts Birthday Parties for Kids in Canberra</h1>
    <p class="hero__sub">Active, fun, and unforgettable. Ages 5–9. At our Woden Club.</p>
    <a class="btn btn--primary btn--lg" href="#book">Book a Tiger Party</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>How a Tiger Party Runs</h2></div>
    <div class="runsheet">
      <div class="runsheet__item"><strong>10 min</strong><span>Welcome</span></div>
      <div class="runsheet__item"><strong>40 min</strong><span>Class 1</span></div>
      <div class="runsheet__item"><strong>30 min</strong><span>Cake Break</span></div>
      <div class="runsheet__item"><strong>40 min</strong><span>Class 2 + Boards</span></div>
      <div class="runsheet__item"><strong>5 min</strong><span>Farewell</span></div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Pick a Package</h2></div>
    <div class="grid grid--3">
      <div class="price-card">
        <h3>Package 1</h3>
        <div class="price-card__price">$22.50<span>/kiddo</span></div>
        <ul><li>2 instructor-led classes</li><li>Belt &amp; certificate</li><li>Room hire (2 hrs)</li></ul>
        <a class="btn btn--primary" href="#book">Book This Package</a>
      </div>
      <div class="price-card">
        <h3>Package 2</h3>
        <div class="price-card__price">$27.50<span>/kiddo</span></div>
        <ul><li>Everything in Package 1</li><li>Board breaking finale</li><li>Party photo bundle</li></ul>
        <a class="btn btn--primary" href="#book">Book This Package</a>
      </div>
      <div class="price-card popular">
        <h3>Package 3</h3>
        <div class="price-card__price">$32.50<span>/kiddo</span></div>
        <ul><li>Everything in Package 2</li><li>Catered party food</li><li>Custom invitations</li><li>Take-home pack</li></ul>
        <a class="btn btn--primary" href="#book">Book This Package</a>
      </div>
    </div>
    <p class="muted center mt-4">Parties from $225 · Minimum 10 children</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title"><h2>Party Gallery</h2></div>
    <div class="gallery">
      <div class="gallery__item">Boards</div>
      <div class="gallery__item">Games</div>
      <div class="gallery__item">Cake</div>
      <div class="gallery__item">Belts</div>
      <div class="gallery__item">Group</div>
      <div class="gallery__item">Finale</div>
    </div>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Parent FAQs</h2></div>
    <div class="faq">
      <details><summary>Can we bring our own food?</summary><p>Yes — bring cake and party food. Package 3 includes catering if you'd rather not.</p></details>
      <details><summary>How many kids can attend?</summary><p>Minimum 10, comfortable maximum 20. Talk to us for larger groups.</p></details>
      <details><summary>Do you provide invitations?</summary><p>Package 3 includes custom printable invitations.</p></details>
      <details><summary>Can children with special needs join?</summary><p>Yes — let us know what we can do to make the party work for your child.</p></details>
      <details><summary>Is the venue accessible?</summary><p>Our Woden location requires stair access. Please contact us to discuss requirements for guests with mobility needs, including options at our Coombs location.</p></details>
    </div>
  </div>
</section>

<section class="section" id="book">
  <div class="container" style="max-width:680px;">
    <div class="section-title"><h2>Book Your Party</h2></div>
    <div style="aspect-ratio:4/3; background:var(--grey-50); border:1px dashed var(--grey-200); border-radius:var(--radius-lg); display:grid; place-items:center; color:var(--text);">
      Party booking form embed
    </div>
    <p class="muted center mt-2">Prefer to chat? Call <a href="tel:0488852191">0488 852 191</a> or email <a href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a>.</p>
  </div>
</section>
"""
)

# -------- Template 13: Member Information Hub --------
PAGES["member-information.html"] = dict(
    title="Member Resources",
    description="Everything you need as a CMA&F member — apps, policies, code of conduct and more.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Member Resources</h1>
    <p class="hero__sub">Everything you need as a CMA&amp;F member, in one place.</p>
  </div>
</section>

<section class="section--tight">
  <div class="container">
    <div class="quicklinks">
      <a href="#apps" class="quicklink">GymMaster App</a>
      <a href="#video" class="quicklink">Video Portal</a>
      <a href="#policies" class="quicklink">Policies</a>
      <a href="contact.html" class="quicklink">Contact Us</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="with-sidebar">
      <aside class="side-nav">
        <ul>
          <li><a href="#apps">Apps &amp; Tools</a></li>
          <li><a href="#social">Social Media</a></li>
          <li><a href="#policies">Membership Terms</a></li>
          <li><a href="#codeofconduct">Code of Conduct</a></li>
          <li><a href="#suspensionandinjury">Suspension &amp; Injury</a></li>
          <li><a href="#cancellation">Cancellation</a></li>
        </ul>
      </aside>
      <div>

        <section id="apps">
          <h2>Apps &amp; Tools</h2>
          <p>GymMaster handles your bookings and membership. Kollab is where the training videos live. Two different jobs — that's why there are two apps.</p>
          <div class="grid grid--2">
            <div class="card" style="padding:24px;">
              <h3>GymMaster</h3>
              <p>Class booking &amp; membership management.</p>
              <p><a class="card__link" href="#">Member Portal →</a></p>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <a class="btn btn--primary" href="#">App Store</a>
                <a class="btn btn--primary" href="#">Google Play</a>
              </div>
            </div>
            <div class="card" style="padding:24px;">
              <h3>Kollab (Video Portal)</h3>
              <p>Instructional videos for every style — review what you learned in class.</p>
              <p><a class="card__link" href="#">Open Kollab →</a></p>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <a class="btn btn--primary" href="#">App Store</a>
                <a class="btn btn--primary" href="#">Google Play</a>
              </div>
            </div>
          </div>
        </section>

        <section id="social" class="mt-4">
          <h2>Social Media</h2>
          <p>Class photos, member spotlights, event reminders.</p>
          <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <a class="btn btn--secondary" href="#">Facebook</a>
            <a class="btn btn--secondary" href="#">Instagram</a>
          </div>
        </section>

        <section id="policies" class="mt-4">
          <h2>Membership &amp; Payment Terms</h2>
          <p>Direct debit runs fortnightly. Memberships continue automatically until cancelled (see below). Prices include public holidays and the Christmas shutdown — there are no extra weekly fees.</p>
          <p>For the full legal terms see <a href="terms-and-conditions.html">Terms &amp; Conditions</a>.</p>
        </section>

        <section id="codeofconduct" class="mt-4">
          <h2>Code of Conduct</h2>
          <h3>Our Values</h3>
          <p>Respect, discipline, community, growth, inclusion, authenticity, fun, lifetime learning.</p>
          <h3>Member Conduct</h3>
          <p>Treat instructors, training partners, the venue and yourself with respect. Show up on time, in clean uniform where applicable. Pay attention during instruction. Train safely — control your techniques to your partner's level.</p>
          <p>Bullying, harassment or discrimination are grounds for immediate review of membership.</p>
        </section>

        <section id="suspensionandinjury" class="mt-4">
          <h2>Suspension &amp; Injury Policy</h2>
          <p>If you're injured or unable to train for an extended period, you can request a suspension of your membership. Submit the request in writing (email is fine). Suspensions are processed for the upcoming billing cycle.</p>
          <p>Minimum suspension period: 2 weeks. Maximum: 12 weeks per calendar year without medical evidence.</p>
        </section>

        <section id="cancellation" class="mt-4">
          <h2>Cancellation Policy</h2>
          <p>Memberships can be cancelled at any time with 14 days written notice. Use the cancellation form below or email <a href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a>.</p>
          <a class="btn btn--secondary" href="#">Open Cancellation Form</a>
        </section>

      </div>
    </div>
  </div>
</section>
"""
)

# -------- Template 14: Privacy Policy --------
PAGES["privacy-policy.html"] = dict(
    title="Privacy Policy",
    description="How Canberra Martial Arts & Fitness collects, uses and protects your information.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Privacy Policy</h1>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="legal">
      <p class="updated">Last updated: 20 May 2026</p>

      <p>Canberra Martial Arts &amp; Fitness Pty Ltd (CMA&amp;F, we, us, our) is committed to protecting the privacy of our members, prospective members, and website visitors. This policy explains how we collect, use, disclose and store personal information.</p>

      <h2>1. Information we collect</h2>
      <p>We collect personal information you provide directly — name, contact details, date of birth, emergency contact, payment details, medical information relevant to training, and class attendance.</p>

      <h2>2. How we use your information</h2>
      <p>To deliver classes and manage memberships, to communicate about classes and events, to process payments, to keep our members safe, and to comply with our legal obligations.</p>

      <h2>3. Disclosure</h2>
      <p>We disclose personal information only to service providers who help us operate the club (payment processors, membership platform, email tools) and only to the extent necessary. We do not sell your personal information.</p>

      <h2>4. Storage and security</h2>
      <p>Information is stored in secure systems with access controls. We retain records only as long as needed for legal, contractual and operational purposes.</p>

      <h2>5. Your rights</h2>
      <p>You can request access to or correction of your personal information at any time by contacting us.</p>

      <h2>6. Cookies</h2>
      <p>Our website uses cookies to remember preferences and to measure how visitors use the site. You can disable cookies in your browser settings.</p>

      <h2>7. Children</h2>
      <p>For members under 18, personal information is collected from a parent or guardian, who consents to its use under this policy.</p>

      <h2>8. Contact</h2>
      <p>Questions about your data? Contact our Privacy Officer at <a href="mailto:members@canberramartialarts.com.au">members@canberramartialarts.com.au</a>.</p>
    </div>
  </div>
</section>
"""
)

# Terms & Conditions (sibling legal template)
PAGES["terms-and-conditions.html"] = dict(
    title="Terms and Conditions",
    description="Terms and conditions for membership at Canberra Martial Arts & Fitness.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>Terms and Conditions</h1>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="legal">
      <p class="updated">Last updated: 20 May 2026</p>
      <p>These terms govern membership and use of the services provided by Canberra Martial Arts &amp; Fitness Pty Ltd.</p>
      <h2>1. Membership</h2>
      <p>Memberships are ongoing until cancelled in accordance with our Cancellation Policy. See <a href="member-information.html#cancellation">Cancellation Policy</a>.</p>
      <h2>2. Payment</h2>
      <p>Direct debit runs fortnightly. Failed payments may incur fees passed on by our payment provider.</p>
      <h2>3. Conduct</h2>
      <p>Members must follow our <a href="member-information.html#codeofconduct">Code of Conduct</a>. CMA&amp;F reserves the right to suspend or terminate membership for conduct breaches.</p>
      <h2>4. Risk and injury</h2>
      <p>Martial arts and fitness carry inherent risks. Members participate at their own risk and must disclose relevant medical conditions to instructors.</p>
      <h2>5. Liability</h2>
      <p>CMA&amp;F's liability is limited to the maximum extent permitted by Australian Consumer Law.</p>
      <h2>6. Changes</h2>
      <p>We may update these terms from time to time. Material changes will be communicated to members by email.</p>
    </div>
  </div>
</section>
"""
)

# -------- Template 15: Blog Index --------
PAGES["blog.html"] = dict(
    title="The CMA&F Blog",
    description="Tips, updates and stories from the mat at Canberra Martial Arts & Fitness.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>The CMA&amp;F Blog</h1>
    <p class="hero__sub">Tips, updates, and stories from the mat.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="blog-filters">
      <button class="blog-filter active">All</button>
      <button class="blog-filter">Martial Arts</button>
      <button class="blog-filter">Fitness</button>
      <button class="blog-filter">Kids</button>
      <button class="blog-filter">Club News</button>
      <button class="blog-filter">Events</button>
    </div>

    <div class="blog-layout">
      <div class="grid grid--2">
        {''.join(f'''
        <a class="card" href="blog-post.html" style="text-decoration:none; color:inherit;">
          <div class="card__image card__image--{img}"></div>
          <div class="card__body">
            <div class="blog-card__meta"><span class="blog-card__tag">{tag}</span><span>{date}</span></div>
            <h3 class="card__title">{title}</h3>
            <p class="card__desc">{ex}</p>
            <span class="card__link">Read More</span>
          </div>
        </a>''' for title, tag, date, ex, img in [
          ("How to Pick the Right Martial Art For You", "Martial Arts", "12 May 2026", "Five styles, five very different paths. Here's how to choose without overthinking it.", "adult"),
          ("Why Your 4-Year-Old Should Learn to Fall", "Kids", "28 April 2026", "Falling well is the most underrated kids skill — and Tiny Tigers teach it from day one.", "kids"),
          ("Coombs Club is Open — Here's What's New", "Club News", "10 April 2026", "Full schedule of adult, kids and fitness classes. Same standards, new community.", "fitness"),
          ("6 Things You'll Notice in Your First Hapkido Class", "Martial Arts", "28 March 2026", "Heads up: the first thing you'll learn isn't a strike. It's how to fall safely.", "adult"),
          ("Bootcamp at 6am — Worth It?", "Fitness", "14 March 2026", "We surveyed regulars at #JERRAbootcamp. Here's what they said.", "fitness"),
          ("Tiger Parties — A Parent's Guide", "Kids", "1 March 2026", "Everything you need to know before booking a Tiger Party for your kid.", "kids"),
        ])}
      </div>

      <aside class="sidebar">
        <div class="sidebar__block">
          <h4>Recent Posts</h4>
          <ul style="list-style:none; padding:0; margin:0;">
            <li style="margin-bottom:10px;"><a href="blog-post.html">How to Pick the Right Martial Art For You</a></li>
            <li style="margin-bottom:10px;"><a href="blog-post.html">Why Your 4-Year-Old Should Learn to Fall</a></li>
            <li style="margin-bottom:10px;"><a href="blog-post.html">Coombs Club is Open</a></li>
            <li style="margin-bottom:10px;"><a href="blog-post.html">6 Things You'll Notice in Your First Hapkido Class</a></li>
            <li><a href="blog-post.html">Bootcamp at 6am — Worth It?</a></li>
          </ul>
        </div>
        <div class="sidebar__block">
          <h4>Categories</h4>
          <ul style="list-style:none; padding:0; margin:0;">
            <li style="margin-bottom:6px;"><a href="#">Martial Arts</a></li>
            <li style="margin-bottom:6px;"><a href="#">Fitness</a></li>
            <li style="margin-bottom:6px;"><a href="#">Kids</a></li>
            <li style="margin-bottom:6px;"><a href="#">Club News</a></li>
            <li><a href="#">Events</a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>

{final_cta("Interested in What You've Read?", "Come and try a class.", "Come and Try a Class")}
"""
)

# Single blog post
PAGES["blog-post.html"] = dict(
    title="How to Pick the Right Martial Art For You — Blog",
    description="Five styles, five very different paths. Here's how to choose without overthinking it.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <p class="eyebrow" style="color:#fff;">Martial Arts</p>
    <h1>How to Pick the Right Martial Art For You</h1>
  </div>
</section>

<section class="section">
  <div class="container">
    <article class="article">
      <div class="article__hero"></div>
      <div class="article__meta">
        <span>By Tom Adam</span>
        <span>· 12 May 2026</span>
        <span>· 6 min read</span>
        <span>· <strong style="color:var(--green);">Martial Arts</strong></span>
      </div>
      <div class="article__body">
        <p>The most common question we get from new visitors is: "Which style should I do?" Here's the honest answer — it depends on what you want, not what's "best".</p>
        <h2>Start with the why</h2>
        <p>If you want self-defence, look at Hapkido or Krav Maga. If you want competition and structured progression, Taekwondo. If you want grappling and live problem-solving, BJJ. If you want tradition and weapons, Kummooyeh.</p>
        <h2>Try before you decide</h2>
        <p>Reading about a style only gets you so far. The 21-Day Trial exists for this reason — you can sample every class and see which one clicks.</p>
        <h2>It's OK to switch</h2>
        <p>Half our long-term members started in a different style than the one they ended up loving. The point is to start.</p>
      </div>
      <div style="display:flex; gap:8px; margin-top:32px;">
        <a class="btn btn--secondary" href="#">Share on Facebook</a>
        <a class="btn btn--secondary" href="#">Share on Instagram</a>
      </div>
    </article>
  </div>
</section>

<section class="section section--navy">
  <div class="container final-cta">
    <h2>Ready to Try It Yourself?</h2>
    <p>21-Day Trial · $99 · Unlimited classes.</p>
    <a class="btn btn--primary btn--lg" href="getting-started.html">Come and Try a Class</a>
  </div>
</section>

<section class="section section--grey">
  <div class="container">
    <div class="section-title"><h2>Related Posts</h2></div>
    <div class="grid grid--3">
      {''.join(f'''
      <a class="card" href="blog-post.html" style="text-decoration:none; color:inherit;">
        <div class="card__image card__image--{img}"></div>
        <div class="card__body">
          <div class="blog-card__meta"><span class="blog-card__tag">{tag}</span></div>
          <h3 class="card__title">{title}</h3>
          <span class="card__link">Read More</span>
        </div>
      </a>''' for title, tag, img in [
        ("6 Things You'll Notice in Your First Hapkido Class", "Martial Arts", "adult"),
        ("Why Your 4-Year-Old Should Learn to Fall", "Kids", "kids"),
        ("Bootcamp at 6am — Worth It?", "Fitness", "fitness"),
      ])}
    </div>
  </div>
</section>
"""
)

# -------- Index of prototypes (helper page, not part of brief) --------
PAGES["prototypes.html"] = dict(
    title="Prototype Index",
    description="Index of all 15 page prototype templates.",
    body=f"""
<section class="hero hero--compact">
  <div class="container hero__inner">
    <h1>CMA&amp;F Prototype Templates</h1>
    <p class="hero__sub">15 page templates per the design brief. Click any to preview.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--3">
      {''.join(f'''
      <a class="card" href="{href}" style="text-decoration:none; color:inherit;">
        <div class="card__body">
          <p class="muted" style="margin-bottom:4px;">Template {n}</p>
          <h3 class="card__title">{title}</h3>
          <p class="card__desc">{desc}</p>
          <span class="card__link">Open</span>
        </div>
      </a>''' for n, href, title, desc in [
        ("1", "index.html", "Homepage", "Hero, promo, programs, community, locations, testimonials, video, final CTA."),
        ("2", "adult-martial-arts.html", "Adult Martial Arts", "Six styles, 21-Day Trial, dual-club timetables."),
        ("3", "kids-programs.html", "Kids Programs", "Ages 3–14, Tigers and Youth, dual-club trial CTAs."),
        ("4", "fitness-programs.html", "Fitness Programs", "Five fitness classes, PT, dual-club timetables."),
        ("5", "getting-started.html", "Getting Started", "Step-by-step conversion flow with booking calendar."),
        ("6", "contact.html", "Contact", "Phone + email visible in body. Booking options and maps."),
        ("7", "timetable.html", "Timetable", "Tabbed Woden/Coombs. Responsive HTML grids."),
        ("8", "pricing.html", "Pricing", "Trial packs first, then memberships. FAQs."),
        ("9", "about-us.html", "About Us", "Vision, mission, values, founding story, awards."),
        ("10", "our-team.html", "Our Team", "Founders, senior, junior team. 'Bio coming soon' state."),
        ("11", "hapkido.html", "Style Page (Hapkido)", "Template for each individual martial arts style page."),
        ("12", "kids-birthday-parties.html", "Kids Birthday Parties", "Run-sheet, packages, gallery, FAQs."),
        ("13", "member-information.html", "Member Resources", "Sticky sidebar nav. Apps, policies, code of conduct."),
        ("14", "privacy-policy.html", "Legal (Privacy Policy)", "Plus Terms & Conditions sibling page."),
        ("15", "blog.html", "Blog Index + Post", "Index with filters and sidebar. Single post template."),
      ])}
    </div>
    <p class="center mt-4"><a href="index.html" class="btn btn--primary">Open Homepage →</a></p>
  </div>
</section>
"""
)

# =========================================================
# BUILD
# =========================================================
def build():
    for filename, page in PAGES.items():
        html = SHELL.format(**page)
        (ROOT / filename).write_text(html, encoding="utf-8")
        print(f"  ✓ {filename}")
    print(f"\nBuilt {len(PAGES)} pages.")

if __name__ == "__main__":
    build()
