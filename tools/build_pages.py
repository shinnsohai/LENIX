"""Generates index.html and the product pages into the project root.

Run from anywhere:  python tools/build_pages.py
The output is plain static HTML; nothing here is needed at runtime.
Edit the copy in this file (not in the generated .html) so the header, footer
and product data stay in step across pages.
"""
import io
import os
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARW = ('<svg class="arw" viewBox="0 0 12 10" fill="none" aria-hidden="true"><path d="M0.8 5h10M7.1 1.4 10.9 5l-3.8 3.6" '
       'stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/></svg>')
SUN = ('<svg class="i-sun" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="8" cy="8" r="3"/><path d="M8 1.2v1.6M8 13.2v1.6M1.2 8h1.6M13.2 8h1.6M3.2 3.2l1.1 1.1M11.7 11.7l1.1 1.1M3.2 12.8l1.1-1.1M11.7 4.3l1.1-1.1"/></svg>')
MOON = ('<svg class="i-moon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M13.6 9.6A6 6 0 0 1 6.4 2.4a6 6 0 1 0 7.2 7.2z"/></svg>')

VIDEO = "https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260912_104036_bd6924f6-3c8e-417e-8465-6d03c8c2e9e6.mp4"
POSTER = "https://d2ol7oe51mr4n9.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/82e7eb75-c65f-490a-99b5-f3d1cad54200.webp"

NAV = [("builtsync.html", "BuiltSync"), ("ezjob.html", "EZJOB"), ("courseatlas.html", "Course Atlas"), ("smartsite.html", "Smart Site"),
       ("index.html#services", "Services"), ("index.html#contact", "Contact")]

THEME_BOOT = """<script>
(function(){var t;try{t=localStorage.getItem('lenix-theme')}catch(e){}
if(t!=='light'&&t!=='dark'){t=window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches?'light':'dark'}
document.documentElement.setAttribute('data-theme',t);})();
</script>"""

ENTRANCE = """<script>
(function(){
  var root = document.documentElement;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  root.classList.add('anim');
  var started = false, cleaned = false, bootTimer, safety;
  function clean(){ if (cleaned) return; cleaned = true; clearTimeout(safety);
    document.removeEventListener('animationend', onEnd, true);
    root.classList.remove('anim'); root.classList.remove('go'); }
  function onEnd(ev){ if (ev.animationName === 'pillIn' && ev.target.classList && ev.target.classList.contains('btn-ghost')) clean(); }
  function start(){ if (started) return; started = true; clearTimeout(bootTimer);
    document.addEventListener('animationend', onEnd, true);
    safety = setTimeout(clean, 2600); root.classList.add('go'); }
  function boot(){ bootTimer = setTimeout(start, 900);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(start, start); else start(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
</script>"""


def head(title, desc, extra=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
%s
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;800&display=block" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/showcase.css">
%s</head>
""" % (e(title), e(desc), THEME_BOOT, extra)


def topbar(current, home=False):
    def href(h):
        return h.replace("index.html", "") if home and h.startswith("index.html#") else h
    links = "".join('<a href="%s"%s>%s</a>' % (href(h), ' aria-current="page"' if h == current else "", e(t)) for h, t in NAV)
    return """<header class="topbar%s" id="topbar"%s>
  <div class="wrap bar">
    <a class="tb-logo" href="%s" aria-label="LENIX home">
      <img class="on-dark" src="assets/logo-on-dark.png" alt="LENIX" width="628" height="220">
      <img class="on-light" src="assets/logo-on-light.png" alt="LENIX" width="655" height="220">
    </a>
    <nav class="tb-links" aria-label="Primary">%s</nav>
    <div class="tb-actions">
      <button class="icon-btn js-theme" type="button" aria-label="Switch theme">%s%s</button>
      <a class="pill solid sm" href="%s">Talk to us %s</a>
      <button class="icon-btn tb-burger js-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="tbMenu"><span></span></button>
    </div>
  </div>
  <nav class="tb-menu wrap" id="tbMenu" aria-label="Mobile">%s</nav>
</header>
""" % (" is-hidden" if home else "", " inert" if home else "", "#top" if home else "index.html",
       links, SUN, MOON, href("index.html#contact"), ARW, links)


def footer(home=False, scripts=""):
    pre = "" if home else "index.html"
    return """<footer>
  <div class="wrap">
    <a href="%s" aria-label="LENIX home">
      <img class="on-dark" src="assets/logo-on-dark.png" alt="LENIX" width="628" height="220">
      <img class="on-light" src="assets/logo-on-light.png" alt="LENIX" width="655" height="220">
    </a>
    <nav aria-label="Footer">
      <a href="builtsync.html">BuiltSync</a><a href="ezjob.html">EZJOB</a><a href="courseatlas.html">Course Atlas</a><a href="smartsite.html">Smart Site</a>
      <a href="%s#services">Services</a><a href="%s#contact">Contact</a>
    </nav>
    <span>&copy; 2026 LENIX Pte Ltd. A Clarity Group company.</span>
  </div>
</footer>
<script src="assets/site.js"></script>
%s</body>
</html>
""" % ("#top" if home else "index.html", pre, pre, scripts)


# --------------------------------------------------------------------------
# Product data. Every claim about a LENIX product comes from its own live page.
# Comparisons are against categories of alternatives, not named competitors.
# --------------------------------------------------------------------------
PRODUCTS = [
    dict(
        slug="builtsync", name="BuiltSync", kind="Workforce OS for project sites", accent="var(--violet)",
        shot=("shot-bs-att.jpg", 1900, 671, "BuiltSync worker check-in screen beside the admin console attendance summary"),
        demo=("#demo", "Try the interactive demo"),
        second=("#p2live", "Use the Phase 2 prototype"),
        title="BuiltSync by LENIX: workforce OS for project sites",
        desc="BuiltSync connects attendance, payroll, leave, certificates and safety for project sites. What it does, how it compares with timesheets, time clocks and HR software, and where it falls short.",
        h1="Every worker, every shift, every site, in one place.",
        lede="BuiltSync is a worker app and an admin console that carry one record from the first check-in of the day to the payslip at the end of the month.",
        home_copy="A worker app and an admin console for project sites that replace paper timesheets and scattered spreadsheets. Built around Singapore work permits, CPF and MOM-issued certificates.",
        home_feats=["Geofenced, face-verified check-in and check-out", "Payslips that workers confirm or dispute in the app", "Permit and certificate expiries tracked with reminders"],
        intro=[
            "On most project sites, the facts about a working day are scattered. Attendance sits on a paper timesheet or in a photo sent to a group chat. Leave is agreed verbally. Certificate expiry dates live in a spreadsheet one person maintains. Payroll is then rebuilt from all of this at month end, and any disagreement about hours turns into an argument with nothing to check it against.",
            "BuiltSync puts those facts into one system with two faces. <strong>Workers</strong> carry an app that checks them in, shows their documents, takes leave requests and presents their payslip. <strong>Supervisors and admins</strong> use a console that shows who is on site right now, flags what looks wrong, and releases pay.",
            "It was built by LENIX for Singapore project sites, so it is designed around work permits, NRIC/FIN, CPF and MOM-issued certificates, and it runs in English and Simplified Chinese.",
        ],
        functions=[
            ("Attendance", "Geofenced and face-verified", "Check-in and check-out use the phone's GPS against the site geofence, plus face recognition. Late arrivals, early leaving, punches outside the geofence and missing punches are flagged for review automatically, so a supervisor reviews exceptions instead of reading every line. The console gives daily summary, daily detail and monthly summary views."),
            ("Payroll", "Payslips workers can check", "Payslips are generated from attendance and pay rules. A worker sees gross pay, overtime, CPF and deductions, then confirms or disputes. Admins review, adjust and release the payout, which keeps a dispute inside the system instead of on a piece of paper."),
            ("Leave", "From request to approval", "Workers apply from the app against their balance. Supervisors approve on the go, and admins see the whole workforce on a monthly leave calendar."),
            ("Certificates", "Permits that do not lapse unseen", "Work permits and trade certificates are recorded with number, issuer and expiry date. Both the worker and the admin are reminded before anything expires."),
            ("Safety", "In front of every shift", "Safety reminders sit on the worker's home screen. Admins can set a notice that appears at check-in, run site-entry quizzes and send broadcasts."),
            ("Admin console", "One place for the whole workforce", "Analytics, staff roster, projects and zones, roles and data scope, announcements and an audit log, with Excel export. Like the worker app, it is bilingual."),
            ("In the Phase 2 prototype", "Preview, not yet released", "The prototype adds expense claim review, permit to work, training booking, dormitory beds, a skill passport, site group chat, surveys, and client and subcontractor records. These are visible in the preview and may change before release."),
        ],
        audience="Main contractors, subcontractors and manpower suppliers in Singapore who run workers across several project sites, and who are tired of rebuilding attendance for payroll every month.",
        alts=["Paper timesheets and spreadsheets", "Fixed biometric time clocks", "General HR and payroll software"],
        rows=[
            ("Proof a worker was on site", "GPS against the site geofence plus a face check, on the worker's own phone", "A supervisor's signature", "Fingerprint or face at a terminal fixed to one spot", "Mobile clock-in is common; location and face checks vary by product"),
            ("Setting up a new site", "Draw the site and its zones in the console", "Nothing to set up", "Install, power and network a terminal at each gate", "Add a location; it rarely models zones inside a site"),
            ("From hours to payslip", "Verified hours flow straight into the payslip", "Re-keyed by hand at month end", "Exported, then imported into payroll", "Integrated, if you also use its payroll module"),
            ("What the worker sees", "Their hours, overtime, CPF and deductions, with a confirm or dispute button", "A paper payslip", "Nothing", "Usually a payslip view; disputes happen outside the system"),
            ("Permits and trade certificates", "Tracked with issuer and expiry, with reminders to worker and admin", "A separate spreadsheet", "Not covered", "Often document storage, not built around MOM certificates"),
            ("Safety communication", "Check-in notices, quizzes and broadcasts are built in", "Toolbox talks and paper sign-offs", "Not covered", "Not usually covered"),
            ("Languages for workers", "English and Simplified Chinese", "Whatever the supervisor speaks", "Not applicable", "Usually English first"),
            ("What it depends on", "A smartphone with camera, GPS and data for every worker", "Diligent supervisors", "Hardware at every entry point", "Office staff to run it"),
        ],
        pros=[
            ("One record, start to finish.", "The hours a worker is paid for are the hours the system verified, with no re-keying in between."),
            ("Problems surface the same day.", "Late, missing and out-of-zone punches are flagged automatically instead of being discovered at payroll."),
            ("Disputes have something to check against.", "Workers confirm or dispute inside the app, and the console keeps an audit log."),
            ("No hardware to install.", "A new site is a geofence drawn in the console, not a terminal bolted to a gate."),
            ("Built for Singapore sites.", "Work permits, NRIC/FIN, CPF and MOM-issued certificates are part of the design, not an add-on."),
        ],
        cons=[
            ("Every worker needs a capable phone.", "Check-in relies on camera, GPS and a data connection. Sites with weak signal, basements, or rules against phones need a fallback."),
            ("It collects sensitive personal data.", "Face verification and location tracking need clear consent and a data protection process that you are comfortable defending."),
            ("Two languages only, for now.", "English and Simplified Chinese do not cover every crew. Workers who read neither will need help."),
            ("It is a newer product.", "The app store releases are still listed as coming soon, and the Phase 2 features are in preview. Expect it to change."),
            ("It is not a full HR suite.", "It does not try to cover recruitment, appraisals or accounting. Those stay in your other tools."),
        ],
        fit="A fixed terminal can be the better choice where phones are not allowed on site, and a general HR suite may be all you need if your people work from one office. Paper still works for a single small crew whose supervisor knows everyone by name. BuiltSync earns its place once workers move between sites and payroll depends on what happened on each of them.",
    ),
    dict(
        slug="ezjob", name="EZJOB", kind="Skilled trades and technical talent matching", accent="var(--cyan)",
        shot=("shot-ez-jobs.jpg", 1900, 960, "EZJOB job search with filters and live listings"),
        demo=("https://lenix-ezjob.vercel.app/", "Open EZJOB"),
        second=None,
        title="EZJOB by LENIX: skilled trades and technical talent matching",
        desc="EZJOB matches skilled trades and technical workers with employers using a verified Digital Skill Passport. What it does, how it compares with job portals and agencies, and where it falls short.",
        h1="Skilled trades hiring, matched on proven skill.",
        lede="EZJOB is a recruitment and skill verification platform for construction, electrical and heavy industry. Workers show what they can do; employers get ranked candidates.",
        home_copy="A hiring platform built for construction, electrical and heavy industry. Workers carry a verified Digital Skill Passport; employers get ranked candidates instead of keyword hits.",
        home_feats=["Digital Skill Passport with video skill demonstration", "AI Job Studio drafts a job specification from a trade title", "Free for workers"],
        intro=[
            "Hiring a welder, a pipefitter or a high-voltage technician is not like hiring for a desk job. A CV says very little about whether someone can do the work, and a keyword search cannot tell a certified TIG welder from someone who once held a torch. Employers fall back on agencies and personal referrals, and workers fall back on whoever promises them a job.",
            "EZJOB is built for that gap. Each worker builds a <strong>Digital Skill Passport</strong>: a verified digital identity that holds their credentials and a video of them demonstrating their trade. Employers post roles and receive candidates ranked on those trade skills.",
            "It is free for workers and built for roles that cross borders, across Singapore, Malaysia and the wider region. EZJOB is in preview today.",
        ],
        functions=[
            ("Digital Skill Passport", "A portable, verified record", "One profile holds the worker's identity, authenticated certification records and trade credentials. It can be exported as a standardised, print-ready PDF portfolio, so the record is useful outside the platform too."),
            ("Video skill demonstration", "Show the work, not the CV", "Workers upload a video of themselves doing the job. Automated skill and credential validation checks it, and employers can view worker video portfolios directly."),
            ("Skill-based matching", "Ranked on trade skills", "Employers receive ranked candidate recommendations based on actual trade skills, in real time, instead of a list of everyone whose CV contains the right word."),
            ("AI Job Studio", "A job specification in seconds", "An employer enters a skilled trade title and the studio generates a complete, structured job specification to edit and post."),
            ("Integrity Bond System", "A transparent hiring model", "The hiring model is designed to remove the incentive for bribery and exploitation in placement, which is a known problem in cross-border blue-collar hiring."),
            ("Pricing model", "Free for workers", "The platform is free for workers and priced to be affordable for employers, so a worker does not pay to be considered for a job."),
            ("Cross-border roles", "Singapore, Malaysia and the region", "The platform is built for regional deployment across Singapore, Malaysia and APAC hubs."),
        ],
        audience="Employers hiring industrial, engineering and certified technical specialists, and skilled workers who want their ability, not their paperwork, to be what gets them hired.",
        alts=["General job portals", "Recruitment and manpower agencies", "Referrals and informal agents"],
        rows=[
            ("How skill is shown", "A video of the worker doing the job, plus credential records in one passport", "A CV or PDF upload, self-declared", "The agency's own screening; quality varies by agency", "Someone vouches for them"),
            ("How candidates are found", "Ranked on trade skills", "Keyword search", "A recruiter's judgement and contacts", "Whoever is available"),
            ("Cost to the worker", "Free", "Usually free", "Placement fees are sometimes charged to the worker", "Informal fees and favours are a risk"),
            ("Writing the job post", "Drafted by AI from a trade title, then edited", "Written by hand", "Written by the agency", "No written specification"),
            ("Transparency of the process", "Designed around a transparent hiring model", "Open listings, little verification", "Depends on the agency", "Low"),
            ("Size of the talent pool today", "Smaller: the platform is in preview", "Very large", "Limited to the agency's network", "Limited to personal networks"),
            ("Hands-on help with deployment", "A platform, not a service desk", "None", "Often handles paperwork and logistics for you", "None"),
        ],
        pros=[
            ("Skill is shown, not claimed.", "A video demonstration and verified credentials tell an employer far more than a CV does."),
            ("Built for trades.", "Matching, job templates and passports are designed around trade skills, not adapted from office recruitment."),
            ("Workers do not pay.", "Being free for workers removes one of the main routes to exploitation in this kind of hiring."),
            ("Faster job posts.", "The AI Job Studio turns a trade title into a full specification to edit, which helps employers who rarely write them."),
            ("The record is portable.", "A worker can export their passport as a PDF and use it anywhere."),
        ],
        cons=[
            ("The pool is still small.", "A matching platform is only as good as the people on it. On 11 November 2026 it listed 42 jobs from 3 employers, far fewer than an established portal."),
            ("It asks more of the worker.", "Recording and uploading a skill video needs a smartphone, data and some confidence. Some good workers will not bother."),
            ("Automated checks are not a trade test.", "AI verification can be wrong. For safety-critical work, you should still confirm certificates and test the worker yourself."),
            ("AI-drafted job posts need a human read.", "Review pay, requirements and site conditions before posting."),
            ("It is for trades only.", "It is not designed for office, retail or professional roles."),
        ],
        fit="An agency is still the easier route if you want someone else to manage the whole deployment for you, and a general job portal will reach more people if the role is not a skilled trade. EZJOB makes most sense when the hard part of the hire is knowing whether the person can really do the work.",
    ),
    dict(
        slug="courseatlas", name="Course Atlas", kind="Singapore training course calendar", accent="var(--magenta)",
        shot=("shot-courseatlas.jpg", 1510, 716, "Course Atlas month calendar with course filters and listings"),
        demo=("https://course-atlas-sg-shinn.shinnsohai.chatgpt.site/", "Open Course Atlas"),
        second=None,
        title="Course Atlas by LENIX: Singapore training course calendar",
        desc="Course Atlas is a searchable calendar of published training courses in Singapore. What it does, how it compares with provider websites and phone calls, and where it falls short.",
        h1="Find the right course. On the right date.",
        lede="Course Atlas is a searchable calendar of published training courses in Singapore. Compare dates, providers, teaching languages and fees in one view.",
        home_copy="A searchable calendar of published training courses in Singapore, for coordinators, employers and workers who need to compare dates, providers, languages and fees in one view.",
        home_feats=["Calendar, list, map and provider-coverage views", "Filter by course type, language, fee and day of week", "Export a shortlist to CSV or your calendar"],
        intro=[
            "A training coordinator's question is rarely just which course. It is which course, in which language, on a date this worker is free, before their certificate expires. Answering it today means opening each training provider's website in turn, or sending the same message to five of them and waiting.",
            "Course Atlas gathers published course dates from Singapore training providers into one searchable calendar. You can see every session of a course across providers on one month view, filter it down to the language and the days that work, and shortlist the ones worth asking about.",
            "It is deliberately honest about what it is: a <strong>snapshot of published information</strong>, with every listing linked back to its source. It does not take bookings or payment. In the November 2026 snapshot it held 2,753 listings from 14 providers.",
        ],
        functions=[
            ("Four views", "Calendar, list, map, coverage", "A month, week or agenda calendar of sessions; a sortable course list; a map of training centres; and a provider coverage view that shows which providers are included."),
            ("Filters", "Narrow to what is usable", "Filter by course type (fresh or full course against recertification), industry scope, provider, teaching language, training mode, seat availability, published fee ceiling and days of the week. Common courses have one-tap chips."),
            ("Date distribution", "See the busy and quiet days", "A chart shows how published sessions are spread across the month, which makes it easy to spot the dates with the most choice."),
            ("Shortlist and booking request", "Keep the candidates together", "Courses can be shortlisted and gathered into a booking request list, ready to take to the provider."),
            ("Export", "Take it with you", "The current selection exports to CSV, to an ICS calendar file, or to JSON."),
            ("Source-linked listings", "Check it at the source", "Each listing links to the provider's own page, shows explicit attendance dates, and labels seat counts as saved observations with the date they were seen."),
            ("Languages", "Interface in three languages", "The interface is available in English, Simplified Chinese and Traditional Chinese, and courses can be filtered by their teaching language."),
        ],
        audience="Training coordinators, employers and workers in Singapore who book safety and trade courses often and across more than one provider.",
        alts=["Each provider's own website", "Phoning or messaging providers", "A coordinator's own spreadsheet"],
        rows=[
            ("Comparing across providers", "One calendar holds every included provider", "One site at a time, each laid out differently", "One conversation at a time", "Only what someone has typed in"),
            ("Finding a date that fits", "Filter by days of the week and see the month at once", "Scroll each provider's schedule", "Ask, then wait for a reply", "Depends on how fresh the sheet is"),
            ("Teaching language", "A filter", "Sometimes listed, often per course page", "You have to ask", "If someone recorded it"),
            ("Seat availability", "A saved observation, not live", "Live, where the provider publishes it", "The most reliable answer", "Usually out of date"),
            ("Booking and payment", "Not handled; you confirm with the provider", "Direct", "Direct", "Not applicable"),
            ("Which providers are covered", "Only those included so far", "That provider, completely", "Anyone you can reach", "Whoever you already know"),
            ("Effort to keep current", "Maintained for you as snapshots", "None, but you repeat the search every time", "Repeated for every booking", "All yours"),
        ],
        pros=[
            ("One view across providers.", "The comparison that used to take several browser tabs happens on one calendar."),
            ("It starts from the date.", "It answers the question coordinators really have, which is when, not just what."),
            ("Language is a filter.", "Finding a session in the right teaching language takes one click, not five enquiries."),
            ("You can take the result away.", "CSV, calendar and JSON exports fit into whatever you already use."),
            ("It shows its working.", "Listings link to their source, and observations are labelled as observations."),
        ],
        cons=[
            ("Coverage is partial.", "It holds the providers included so far. A missing result does not mean a course is unavailable."),
            ("Seat counts are not live.", "They are saved observations, not reservations. A course can fill between the snapshot and your call."),
            ("It does not book or take payment.", "Course recognition, dates, fees and seats all still need confirming with the provider."),
            ("Snapshots can lag.", "If a provider changes a date, the listing is wrong until the next update."),
            ("Singapore only.", "It covers published training courses in Singapore."),
        ],
        fit="If you only ever book with one training provider, their own website is quicker and always current. For a single urgent booking, a phone call gives the most reliable answer on seats. Course Atlas saves the most time when you book often, across providers, and the date and the language matter as much as the course.",
    ),
]


# --------------------------------------------------------------------------
# Showcase data: the pinned chapter statement and pinned scene for each product.
# A scene step is (heading, text, stat or None, "x,y,scale" focus on the screenshot).
# --------------------------------------------------------------------------
SHOWCASE = {
    "builtsync": dict(
        chapter="From the first check-in to the last payslip.",
        steps=[
            ("One system, two faces", "A worker app and an admin console, working from the same record. These are real screens from the Phase 2 prototype, with sample data.", None, "", "shot-bs-home.jpg"),
            ("Check in on the phone", "The worker signs in from site. The app confirms the location is inside the geofence and starts counting the shift.", "The admin's daily summary updates at once: expected, normal, abnormal, on leave", "", "shot-bs-att.jpg"),
            ("A payslip the worker confirms", "Payslips are generated from attendance and pay rules. The worker sees net pay, days, overtime and deductions, and confirms or disputes.", "The admin sees which payslips are confirmed, waiting or disputed", "", "shot-bs-pay.jpg"),
            ("Leave, on a calendar", "The worker applies against their balance and tracks each request. Admins approve from a month view of the whole workforce.", None, "", "shot-bs-leave.jpg"),
            ("Certificates and skills", "Each worker carries a skill passport. Admins see every certificate with its number, expiry and status: valid, expiring soon or expired.", "Expiring certificates are flagged before they lapse", "", "shot-bs-cert.jpg"),
        ]),
    "ezjob": dict(
        chapter="Show the work. Not the CV.",
        steps=[
            ("Search by trade, pay and country", "Workers filter live roles by role, salary, country and benefits, in a list or a swipe view.", "42 jobs listed on 11 November 2026", "", "shot-ez-jobs.jpg"),
            ("Every job names its skills", "Each listing shows the employer, the openings left and the trade skills it needs, so the match is on skills and not on keywords.", None, "0.42,0.86,1.7", "shot-ez-jobs.jpg"),
            ("See who is hiring", "Employers have their own pages with open roles, so a worker can check the company before applying.", "3 companies hiring on 11 November 2026", "", "shot-ez-companies.jpg"),
        ]),
    "courseatlas": dict(
        chapter="Every provider. One calendar.",
        steps=[
            ("A month of courses on one screen", "Every published session from the included providers, laid out by date.", None, "0.5,0.5,1", None),
            ("Filter to what is usable", "Course type, industry, provider and teaching language narrow thousands of listings to the few that fit.", None, "0.07,0.42,2.4", None),
            ("See the busy and quiet days", "The date distribution shows how many sessions are published on each day of the month.", None, "0.5,0.26,1.8", None),
            ("Know what you are looking at", "The month overview counts listings and providers, and lists the first published dates with their language.", None, "0.93,0.5,2.3", None),
        ]),
    "smartsite": dict(
        chapter="One person. One ID. One tag.",
        plan=True,
        steps=[
            ("One site, six controls", "Handhelds and fixed readers cover the gate, vehicles, toolbox meetings, the store, controlled rooms and every floor.", None, "", "smartsite/helmet-tag.jpg"),
            ("Worker gate", "The guard sweeps the queue. Each worker's photo, company, pass and induction status appear on screen. Green: entry logged. Red: stop.", "Read range up to 15 m, as stated by the reader vendor", "", "smartsite/m1-gate.jpg"),
            ("Vehicle lane", "The guard scans the windscreen tag and the vehicle is checked against the register. Unknown vehicles raise an alert.", "Log book: about 60 s per vehicle. Stated RFID check: 2 s.", "", "smartsite/m2-vehicle.jpg"),
            ("Toolbox meeting", "The supervisor sweeps the crew's helmets. The roster is checked and the absentee list appears at once.", "One sweep reads the whole crew", "", "smartsite/m3-toolbox.jpg"),
            ("Store and materials", "Pick an item and sweep the store to find its tag. Withdrawals scan the worker's helmet, then the items.", "Every withdrawal is tied to a named worker", "", "smartsite/m4-store.jpg"),
            ("Controlled rooms", "A reader at the room, zone or hoist lets only trained, authorised workers pass. Refusals are logged for audits.", "Log book: about 30 s per person. Stated RFID check: 2 s.", "", "-"),
            ("Floors and mustering", "Readers at stair cores and hoists keep a live count per floor. At the assembly point, a handheld sweep lists who is missing.", "Shows the last checkpoint passed, not a live position", "", "smartsite/m6-muster.jpg"),
        ]),
}

PRODUCTS.append(dict(
    slug="smartsite", name="Smart Site", kind="RFID control for workers, vehicles and materials", accent="var(--orange)",
    shot=None, demo=("#demo", "Try the demo"), second=None,
    title="Smart Site by LENIX: RFID control for workers, vehicles and materials",
    desc="Smart Site gives every worker, vehicle and item one RFID tag, read by handhelds and fixed readers. What the six modules do, how it compares with log books, turnstiles and QR codes, and where it falls short.",
    h1="Know who is on site, and where they were last seen.",
    lede="Smart Site gives every worker, vehicle and item one RFID tag, read in seconds by handhelds and fixed readers, and checked against one register.",
    note="Smart Site is at proposal and demo stage. Figures on this page are stated reader figures or illustrative; each site's real numbers are measured in a pilot.",
    home_copy="RFID control for construction-stage sites, where thousands of workers pass gates that have no permanent access control yet. One tag per worker, vehicle and item.",
    home_feats=["Gate checks by handheld, with photo and status on screen", "Toolbox meeting headcount in one sweep", "Live count per floor, and a missing list at muster"],
    intro=[
        "During construction, before permanent turnstiles exist, a large site is controlled by people writing in books. Guards log every entry by hand. Vehicles are checked by eye. Toolbox meetings are counted by head. Store withdrawals go on slips. In an emergency, the roll call is a paper list.",
        "One cause sits behind all of it: identity and presence are written down by people, not captured by a system. Smart Site replaces that with one rule: <strong>one person, one ID, one tag</strong>. Each worker is enrolled once, with photo, company, trade, work pass, safety course and induction, and carries a combined QR and UHF sticker on their helmet. The tag itself holds a random ID and no personal data.",
        "Handheld readers do most of the work, because gates and floors move during construction. Handhelds need no civil work and are useful from day one. Fixed readers are added later at chokepoints such as stair cores and hoists, and every read flows to one platform that checks it against the register and the rules.",
    ],
    functions=[
        ("M1 Worker gate", "Handheld", "The guard sweeps the queue and the screen shows each worker's photo, name, company, pass and induction status. Green means the entry is logged; red means stop and call the supervisor. Every entry and exit is time-stamped."),
        ("M2 Vehicle control", "Handheld", "The guard scans a tamper-evident windscreen tag and the vehicle is checked against the register. Unknown vehicles raise an alert, and the site finally has a count of vehicles inside."),
        ("M3 Toolbox meeting headcount", "Handheld", "The supervisor sweeps the crew's helmets in seconds. The reads are checked against the crew roster, absentees are listed at once, and attendance is saved per meeting, crew and date."),
        ("M4 Store and materials", "Handheld", "Select an item and sweep the store to locate its tag, guided by signal strength. Withdrawals scan the worker's helmet and then the items, so every withdrawal has a name on it. Stocktakes become a walk with a reader."),
        ("M5 Controlled-area access", "Fixed reader and handheld", "A reader at the room, zone or hoist lets only trained, authorised workers pass. Refusals are logged, which gives an audit trail that a visual check never leaves."),
        ("M6 Floor headcount and mustering", "Fixed reader and handheld", "Readers at stair cores and hoists keep a live count per floor and zone. In an emergency, handhelds sweep the muster point and the platform lists who is still unaccounted for, with the last checkpoint they passed."),
        ("The platform", "Register, rules, records", "One register of workers, vehicles and materials. Rules check each read for a valid pass and the right training. Outputs are a gate screen, dashboards per gate, floor and zone, monthly reports and exports."),
    ],
    audience="Main contractors and owners running large construction-stage sites, where crews change weekly and the gates have no permanent access control yet.",
    alts=["Guard and log book", "Turnstiles with biometrics", "QR code scanning"],
    rows=[
        ("Checking one worker", "Read from a distance with no contact; the guard compares the face with the photo on screen", "A name written in a book", "The strongest identity proof, one person at a time", "Close approach and careful aiming for each person"),
        ("A whole crew or queue", "One sweep reads many tags at once", "One line at a time", "One at a time through each lane", "One at a time"),
        ("Before permanent gates exist", "Useful from day one; handhelds need no civil work", "Works anywhere", "Needs civil work, power and network, and is hard to move as gates shift", "Works anywhere there is a scanner"),
        ("Proof of who it was", "Proves which helmet passed, not who wears it; relies on the photo check and spot checks", "None", "Strongest", "Proves which code was shown"),
        ("Vehicles and materials", "The same tags and readers cover vehicles and store items", "Separate books", "People only", "Possible, one item at a time"),
        ("Where people are on site", "The last checkpoint passed, per floor or zone; not continuous tracking", "Unknown", "Known at the gate only", "Only where someone scans"),
        ("Emergency muster", "Sweep the assembly point and list who is missing", "Roll call from paper lists", "Knows who entered, not who has reached the muster point", "Scan each person in turn"),
        ("Records for an audit", "Every read is time-stamped automatically", "Handwritten and hard to search", "Automatic at the gate", "Automatic wherever a scan was made"),
    ],
    pros=[
        ("It reads crowds, not individuals.", "A queue, a crew or a shelf is read in one sweep, which is where log books and one-at-a-time scanning lose the most time."),
        ("It works before the building does.", "Handhelds need no turnstiles, power or civil work, so control starts in the construction stage."),
        ("One system for people, vehicles and materials.", "The same tags, readers and register cover all three."),
        ("It adds coverage that did not exist.", "Floor counts and mustering are usually outside any control system during construction."),
        ("The tag carries no personal data.", "It holds a random ID. Personal details stay in the register, with access by role."),
    ],
    cons=[
        ("The tag proves the helmet, not the person.", "Helmets can be swapped. The guard's photo check and random spot checks are what close that gap."),
        ("Location is by checkpoint.", "It shows the last point a worker passed, not where they are standing. Exact tracking needs BLE or UWB tags, which is an option, not the base system."),
        ("It needs approvals before it can start.", "The site owner must approve radio, ESD and IT use, and readers must run on Singapore's permitted UHF band."),
        ("It depends on enrolment and tag discipline.", "Every worker must be enrolled, and lost or damaged stickers must be replaced, or the counts drift."),
        ("The numbers are not proven on your site yet.", "It is at proposal and demo stage. Read rates near metal and in dense crowds have to be measured in a pilot."),
    ],
    fit="Where permanent turnstiles with biometrics are already installed and the workforce is small and stable, they give stronger identity proof than a helmet tag. A log book is still enough for a small site with one gate. Smart Site is for the construction stage of a large project: big, changing crews, moving gates and a need to know who is where.",
))


def plan(counts=False, uid="a"):
    """The Smart Site plot plan: an aerial site image (assets/site-aerial.jpg) with reader positions marked up on it.
    Coordinates are in the image's own pixels (1448 x 1086), so a new image needs its markup re-placed."""
    def c(z, x, y):
        return '<text class="cnt" data-z="%s" x="%d" y="%d" text-anchor="middle">0</text>' % (z, x, y) if counts else ""

    def tag(code, x, y):
        return ('<g class="tag"><rect x="%d" y="%d" width="54" height="30" rx="15"/><text x="%d" y="%d" text-anchor="middle">%s</text></g>'
                % (x, y, x + 27, y + 21, code))

    return """<svg class="plan aerial" viewBox="0 0 1448 1086" role="img" aria-label="Aerial view of a construction site with RFID reader positions marked: a worker gate on the left hoarding, a vehicle gate at the bottom, a toolbox meeting area, the building with a controlled room and two stair-core readers, a store, and a muster point">
  <image href="assets/site-aerial.jpg" width="1448" height="1086" preserveAspectRatio="xMidYMid slice"/>
  <rect class="scrim" width="1448" height="1086"/>
  <g class="m m1">
    <rect class="pl" x="136" y="546" width="26" height="60" rx="5"/><circle class="ping" cx="149" cy="576" r="64"/>
    <path class="lead" d="M162 576h70"/>%(t1)s<text x="296" y="583">Worker gate</text>%(c_gate)s
  </g>
  <g class="m m2">
    <rect class="pl" x="608" y="966" width="174" height="62" rx="8"/><circle class="ping" cx="695" cy="997" r="76"/>
    <path class="lead" d="M782 997h14"/>%(t2)s<text x="860" y="1004">Vehicle gate</text>
  </g>
  <g class="m m3">
    <circle class="pl dash-ln" cx="700" cy="262" r="54"/><circle class="ping" cx="700" cy="262" r="64"/>
    <path class="lead" d="M746 234l20-8"/>%(t3)s<text x="830" y="230">Toolbox meeting</text>%(c_yard)s
  </g>
  <g class="m m6">
    <rect class="pl" x="710" y="346" width="160" height="440" rx="4"/>
    <circle class="solid" cx="736" cy="372" r="8"/><circle class="solid" cx="844" cy="760" r="8"/>
    <circle class="ping" cx="736" cy="372" r="48"/><circle class="ping" cx="844" cy="760" r="48"/>
    <path class="lead" d="M870 640h16"/>%(t6)s<text x="950" y="647">Building, by floor</text>%(c_building)s
    <circle class="pl dash-ln" cx="1045" cy="895" r="58"/><circle class="ping" cx="1045" cy="895" r="66"/>
    <text x="1045" y="822" text-anchor="middle">Muster point</text>%(c_muster)s
  </g>
  <g class="m m5">
    <rect class="pl" x="746" y="446" width="88" height="108" rx="3"/><circle class="solid" cx="746" cy="500" r="7"/><circle class="ping" cx="746" cy="500" r="42"/>
    <path class="lead" d="M834 470h52"/>%(t5)s<text x="950" y="477">Controlled room</text>%(c_room)s
  </g>
  <g class="m m4">
    <rect class="pl" x="1144" y="924" width="164" height="82" rx="6"/><circle class="ping" cx="1226" cy="965" r="76"/>
    <path class="lead" d="M1226 924v-14"/>%(t4)s<text x="1190" y="902" text-anchor="end">Store</text>%(c_store)s
  </g>
</svg>""" % dict(t1=tag("M1", 232, 561), t2=tag("M2", 796, 982), t3=tag("M3", 766, 208), t6=tag("M6", 886, 625),
                 t5=tag("M5", 886, 455), t4=tag("M4", 1199, 880),
                 c_gate=c("gate", 205, 540), c_yard=c("yard", 700, 273), c_building=c("building", 790, 690),
                 c_muster=c("muster", 1045, 906), c_room=c("room", 790, 512), c_store=c("store", 1226, 976))


def chapter(text):
    words = text.split()
    spans = " ".join('<span style="--i:%d">%s</span>' % (i, e(w)) for i, w in enumerate(words))
    return ('<section class="chapter" data-pin style="--n:%d"><div class="chapter-pin"><p class="chapter-words">%s</p></div></section>\n'
            % (len(words), spans))


def scene(p):
    sc = SHOWCASE[p["slug"]]
    is_plan = bool(sc.get("plan"))
    files = []
    for step in sc["steps"]:
        if step[4] and step[4] != "-" and step[4] not in files:
            files.append(step[4])
    lis = ""
    for t, d, stat, focus, img in sc["steps"]:
        attrs = ' data-focus="%s"' % focus if focus else ""
        if img == "-":
            attrs += ' data-img="-1"'
        elif img:
            attrs += ' data-img="%d"' % files.index(img)
        lis += '<li%s><h3>%s</h3><p>%s</p>%s</li>' % (attrs, e(t), e(d), '<span class="stat">%s</span>' % e(stat) if stat else "")
    if is_plan:
        stage = plan() + "".join('<img class="inset%s" src="assets/%s" alt="" loading="lazy">' % (" on" if i == 0 else "", f)
                                 for i, f in enumerate(files))
    elif files:
        stage = "".join('<img%s src="assets/%s" alt="%s screen %d of %d" width="%d" height="%d">'
                        % (' class="on"' if i == 0 else "", f, e(p["name"]), i + 1, len(files), SHOT_DIMS[f][0], SHOT_DIMS[f][1])
                        for i, f in enumerate(files))
    else:
        f, w, h, alt = p["shot"]
        stage = '<img class="on" src="assets/%s" alt="%s" width="%d" height="%d">' % (f, e(alt), w, h)
    return """<section class="scene" data-pin data-scene style="--steps:%d">
  <div class="scene-pin"><div class="wrap scene-grid">
    <div><div class="scene-count" aria-hidden="true"></div><div class="scene-bar" aria-hidden="true"><i></i></div>
      <ol class="scene-steps">%s</ol></div>
    <div class="stage">%s</div>
  </div></div>
</section>
""" % (len(sc["steps"]), lis, stage)


SHOT_DIMS = {'shot-bs-home.jpg': (1900, 671), 'shot-bs-att.jpg': (1900, 671), 'shot-bs-pay.jpg': (1900, 671), 'shot-bs-leave.jpg': (1900, 671), 'shot-bs-cert.jpg': (1900, 671), 'shot-ez-home.jpg': (1900, 961), 'shot-ez-jobs.jpg': (1900, 960), 'shot-ez-companies.jpg': (1900, 960)}

SMARTSITE_EXTRA = """
    <section class="sec" id="demo">
      <h2>A shift on one screen</h2>
      <div class="prose"><p>Drag the time to watch a shift arrive, spread across the site and leave. Then start a muster drill. All figures here are illustrative: a made-up site of 1,200 workers, not a live system.</p></div>
      <div class="dash" id="dash">
        <div class="dash-top">
          <div><b data-k="on">0</b><span>On site, from entry and exit scans</span></div>
          <div><b data-k="in">0</b><span>Entries this shift</span></div>
          <div><b data-k="out">0</b><span>Exits this shift</span></div>
          <div><b data-k="muster">0</b><span data-k="await">No drill running</span></div>
        </div>
        <div class="dash-main" data-step="0">""" + plan(counts=True, uid="b") + """</div>
        <div class="dash-ctl">
          <label>Time <input type="range" min="0" max="24" step="1" value="10" aria-label="Time of day"> <output>12:00</output></label>
          <button class="pill line js-muster" type="button">Start muster drill</button>
        </div>
      </div>
      <p class="tbl-note">Numbers on the plan are workers last read in each zone. A count shows the last checkpoint passed, not a continuous position.</p>
      <h3 style="margin-top:56px;font-size:clamp(22px, 2.4vw, 28px);font-weight:500;letter-spacing:-.02em">Go deeper: the worker-movement dashboard</h3>
      <div class="prose"><p>This is the sample dashboard from a Smart Site proposal, running on 10,000 synthetic worker records. Filter by subcontractor, work package and floor, open a worker to see their day as a numbered sequence of reads, play a shift back in 30-minute steps, and run a muster drill.</p></div>
      <div class="embed tall">
        <img class="embed-poster" src="assets/smartsite/control-room.jpg" alt="" loading="lazy">
        <div class="embed-cta">
          <button type="button" class="pill solid js-embed" data-src="demo/smart-site-dashboard.html" data-title="Smart Site worker-movement dashboard">Open the dashboard here """ + ARW + """</button>
          <p>It is a 1.4 MB sample and works best on a desktop screen. All worker records, counts and scan times in it are synthetic. <a href="demo/smart-site-dashboard.html" target="_blank" rel="noopener">Open it in a new tab</a> instead.</p>
        </div>
      </div>
    </section>

    <section class="sec" id="rollout">
      <h2>Pilot first, then scale</h2>
      <div class="prose"><p>Each phase starts only when the one before it has passed its gate, and the first ask is small: one gate, one store, one contractor group.</p></div>
      <ol class="flow four stagger">
        <li><b>Survey and approvals</b>A joint site survey of gates, chokepoints, power and network, and the owner's approval for radio, ESD and IT.</li>
        <li><b>Pilot</b>One gate, one store and one contractor group, with the gate, toolbox and store modules live and a two-week baseline.</li>
        <li><b>Full roll-out</b>Every worker enrolled, all gates and the vehicle lane covered, and the handheld modules running site-wide.</li>
        <li><b>Floors and mustering</b>Fixed readers at stair cores, hoists and controlled rooms, followed by muster drills.</li>
      </ol>
      <div class="prose"><p><strong>Built to pass review.</strong> Workers are told the purpose at enrolment, the tag holds a random ID with no personal data, access to named records is by role, and retention is set before go-live. Readers are set to Singapore's UHF band of 917 to 925 MHz.</p></div>
    </section>

    <section class="sec" id="more">
      <h2>What the same backbone can carry next</h2>
      <div class="prose"><p>Once every worker, vehicle and item has an ID and the site has readers, new controls are mostly a matter of rules and screens. The first three below are options in the Smart Site proposal today. The rest are directions we can build with a site that needs them.</p></div>
      <div class="rows">
        <div><h3>Live location</h3><p>BLE or UWB tags give a continuous position where the last checkpoint is not enough, such as lone working or confined spaces. Available as an option.</p></div>
        <div><h3>Face recognition at gates</h3><p>Adds identity proof to the helmet tag where the risk justifies it. Available as an option.</p></div>
        <div><h3>Door interlocks</h3><p>A controlled room that will not open for an untrained or unauthorised tag. Available as an option.</p></div>
        <div><h3>Tools and equipment</h3><p>The store module's tags and readers extended to shared tools and plant: who has it, and when it is due back. A direction, not a product yet.</p></div>
        <div><h3>One record with BuiltSync</h3><p>A gate read that also starts the day's attendance, and an expired certificate that turns the gate screen red. A direction, not a product yet.</p></div>
        <div><h3>Training that unlocks access</h3><p>A course found in Course Atlas and completed becomes the authorisation a controlled room checks for. A direction, not a product yet.</p></div>
      </div>
    </section>
"""

SMARTSITE_DEMO, _rest = SMARTSITE_EXTRA.split('\n    <section class="sec" id="rollout">')
SMARTSITE_END = '\n    <section class="sec" id="rollout">' + _rest


BUILTSYNC_FLOW = [
    ("Check in", "The worker checks in on site. Location, time and face are verified.", "app-checkin", "adm-att-daily"),
    ("Monitor", "Admins see who is in, who is late and who is outside the geofence.", "app-geofence", "adm-att-detail"),
    ("Get paid", "Hours roll into payslips that workers confirm, or dispute, in the app.", "app-payslip", "adm-payroll"),
]
PHASE2_URL = "https://buildsync-phase2-test.shinnsohai.workers.dev/"


def builtsync_pre():
    cards = "".join(
        '<li><h3>%s</h3><p>%s</p><div class="p-links">'
        '<button type="button" class="pill line" data-demo-go="%s">See it in the app</button>'
        '<button type="button" class="pill line" data-demo-go="%s">See it in the console</button></div></li>'
        % (e(t), e(d), app, adm) for t, d, app, adm in BUILTSYNC_FLOW)
    return """<section class="blk" id="phase1">
  <div class="wrap">
    <h2>Phase 1: tap through the app and the console.</h2>
    <p class="lede">This is the same interactive demo as on the Clarity site: 22 worker app screens and 14 admin console screens, in English or Chinese. Tap the highlighted areas to move around, or play the tour.</p>
    <div class="demo" id="demo" tabindex="-1">
      <noscript><p class="note">The interactive demo needs JavaScript. You can also <a href="https://www.clarity.com.sg/our-business/lenix/builtsync">open it on the Clarity site</a>.</p></noscript>
    </div>
    <h3 style="margin-top:72px;font-size:clamp(22px, 2.4vw, 28px);font-weight:500;letter-spacing:-.02em">From check-in to payslip</h3>
    <ol class="flowcards">%s</ol>
  </div>
</section>

<section class="blk" id="phase2">
  <div class="wrap">
    <h2>Phase 2: the working prototype.</h2>
    <p class="lede">Phase 2 puts the worker app and the admin console side by side on live demo data, and adds claims, permit to work, training, dormitory beds, a skill passport and site chat. Scroll for five real screens, then use the prototype itself.</p>
  </div>
</section>
""" % cards


def builtsync_post():
    return """<section class="blk" id="p2live" style="padding-top:clamp(40px, 6vw, 80px)">
  <div class="wrap wide">
    <h2>Now use Phase 2 yourself.</h2>
    <p class="lede">The prototype runs here on demo data. Pick a module and the worker app and the admin console both jump to it; from there every button works, so carry on wherever you like.</p>
    <div class="p2" id="p2demo" data-src="demo/builtsync-phase2/index.html">
      <div class="p2-top">
        <div class="seg" role="group" aria-label="View">
          <button type="button" data-p2-view="both" aria-pressed="false">Side by side</button>
          <button type="button" data-p2-view="app" aria-pressed="false">Worker app</button>
          <button type="button" data-p2-view="admin" aria-pressed="false">Admin console</button>
        </div>
        <p class="p2-cap" aria-live="polite"></p>
      </div>
      <div class="p2-mods" role="group" aria-label="Guided tour"></div>
      <div class="embed tall p2-frame">
        <img class="embed-poster" src="assets/shot-bs-home.jpg" alt="" loading="lazy">
        <div class="embed-cta">
          <button type="button" class="pill solid" data-p2-start>Start the prototype %s</button>
          <p>Data stays in your browser and can be reset from the prototype's own top bar. The guided buttons use the English labels; you can still switch the prototype to Chinese and explore by hand.</p>
        </div>
      </div>
      <span class="note"><a href="demo/builtsync-phase2/index.html" target="_blank" rel="noopener">Open the prototype full screen</a></span>
    </div>
  </div>
</section>
""" % ARW


# Extra media per product: a logo for the page header, a photo for the "what it is" section,
# photos beside functions, and a live app that loads into the page on request.
MEDIA = {
    "builtsync": dict(logo=("builtsync/logo.png", "builtsync/logo.png", "")),
    "ezjob": dict(
        logo=("logo-ezjob-light.png", "logo-ezjob-dark.png", " band"),
        live=("https://lenix-ezjob.vercel.app/", "shot-ez-jobs.jpg", "Use EZJOB here.",
              "The live job board loads into this page. Search the open roles, open a company, or start a Skill Passport.",
              "Open EZJOB here")),
    "courseatlas": dict(
        live=("https://course-atlas-sg-shinn.shinnsohai.chatgpt.site/", "shot-courseatlas.jpg", "Use Course Atlas here.",
              "The live calendar loads into this page. Filter by course, language and day, then shortlist what fits.",
              "Open Course Atlas here")),
    "smartsite": dict(
        figure=("smartsite/gate-logbook.jpg", "Workers queue at a site gate while a guard writes each entry in a log book",
                "The gate today: every entry is written into a book by hand."),
        fn_photos={0: "m1-gate", 1: "m2-vehicle", 2: "m3-toolbox", 3: "m4-store", 5: "m6-muster", 6: "control-room"}),
}


def media_logo(p):
    m = MEDIA.get(p["slug"], {}).get("logo")
    if not m:
        return ""
    light, dark, cls = m
    return ('<img class="p-logo%s on-light" src="assets/%s" alt="%s logo"><img class="p-logo%s on-dark" src="assets/%s" alt="%s logo">'
            % (cls, light, e(p["name"]), cls, dark, e(p["name"])))


def media_figure(p):
    m = MEDIA.get(p["slug"], {}).get("figure")
    if not m:
        return ""
    return ('<figure class="figure"><span class="shot wipe"><img src="assets/%s" alt="%s" loading="lazy"></span><figcaption>%s</figcaption></figure>'
            % (m[0], e(m[1]), e(m[2])))


def media_live(p):
    m = MEDIA.get(p["slug"], {}).get("live")
    if not m:
        return ""
    url, poster, heading, text, label = m
    return """<section class="blk" id="live" style="padding-top:clamp(40px, 6vw, 80px)">
  <div class="wrap wide">
    <h2>%s</h2>
    <p class="lede">%s</p>
    <div class="embed tall" style="margin-top:40px">
      <img class="embed-poster" src="assets/%s" alt="" loading="lazy">
      <div class="embed-cta">
        <button type="button" class="pill solid js-embed" data-src="%s" data-title="%s live app">%s %s</button>
        <p>It is in preview and runs from its own test address. <a href="%s" target="_blank" rel="noopener">Open it in a new tab</a> instead.</p>
      </div>
    </div>
  </div>
</section>
""" % (e(heading), e(text), poster, url, e(p["name"]), e(label), ARW, url)


def product_page(i, p):
    nxt = PRODUCTS[(i + 1) % len(PRODUCTS)]
    smart = p["slug"] == "smartsite"
    href, label = p["demo"]
    ext = "" if href.startswith("#") else ' target="_blank" rel="noopener"'
    links = '<a class="pill solid" href="%s"%s>%s %s</a>' % (href, ext, e(label), ARW)
    if p["second"]:
        ext2 = "" if p["second"][0].startswith("#") else ' target="_blank" rel="noopener"'
        links += '<a class="pill line" href="%s"%s>%s</a>' % (p["second"][0], ext2, e(p["second"][1]))
    links += '<a class="pill line" href="index.html#contact">Talk to us</a>'
    if p.get("note"):
        note = '<p class="note" style="margin-top:14px;max-width:70ch">%s</p>' % e(p["note"])
    elif p["slug"] == "builtsync":
        note = ""
    else:
        note = '<p class="note" style="margin-top:14px">%s is in preview and opens on a test address.</p>' % e(p["name"])
    intro = "".join("<p>%s</p>" % x for x in p["intro"])
    fn_photos = MEDIA.get(p["slug"], {}).get("fn_photos")
    fns = ""
    for k, (fa, fb, fc) in enumerate(p["functions"]):
        ph = ""
        if fn_photos is not None:
            ph = ('<span class="ph"><img src="assets/smartsite/%s.jpg" alt="" loading="lazy"></span>' % fn_photos[k]) if k in fn_photos else "<span></span>"
        fns += "<div><dt>%s<small>%s</small></dt><dd>%s</dd>%s</div>" % (e(fa), e(fb), e(fc), ph)
    ths = "".join('<th scope="col">%s</th>' % e(a) for a in p["alts"])
    rows = "".join('<tr><th scope="row">%s</th><td class="us">%s</td>%s</tr>' % (e(r[0]), e(r[1]), "".join("<td>%s</td>" % e(c) for c in r[2:])) for r in p["rows"])
    pros = "".join("<li><b>%s</b> %s</li>" % (e(a), e(b)) for a, b in p["pros"])
    cons = "".join("<li><b>%s</b> %s</li>" % (e(a), e(b)) for a, b in p["cons"])
    body = """<body style="--c:%(accent)s">
<div class="progress" aria-hidden="true"></div>
%(topbar)s
<main>
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">LENIX</a> / <a href="index.html#products">Products</a> / %(name)s</nav>
    %(logo)s
    <h1>%(h1)s</h1>
    <p class="lede">%(lede)s</p>
    <div class="p-links">%(links)s</div>
    %(note)s
  </div>
</section>

%(chapter)s%(pre)s%(scene)s%(post)s
<div class="wrap doc">
  <nav class="toc" aria-label="On this page">
    <a href="#what">What it is</a>
    <a href="#functions">What it does</a>
    %(toc_mid)s<a href="#compare">How it compares</a>
    <a href="#verdict">Strengths</a>
    %(toc_end)s
  </nav>
  <div>
    <section class="sec" id="what">
      <h2>What %(name)s is, and the problem it is for</h2>
      <div class="prose">%(intro)s</div>
      %(figure)s
    </section>

    <section class="sec" id="functions">
      <h2>What it does, function by function</h2>
      <dl class="fn%(fn_cls)s">%(fns)s</dl>
      <div class="prose"><p><strong>Who it is for.</strong> %(audience)s</p></div>
    </section>
%(mid)s
    <section class="sec" id="compare">
      <h2>How it compares with the usual alternatives</h2>
      <div class="tbl-wrap" role="region" aria-label="Comparison table" tabindex="0">
        <table class="cmp">
          <thead><tr><th scope="col"><span class="sr">Criterion</span></th><th scope="col" class="us">%(name)s</th>%(ths)s</tr></thead>
          <tbody class="stagger">%(rows)s</tbody>
        </table>
      </div>
      <p class="tbl-note">The comparison is against the typical setup in each category, not a named product. Individual products and agencies differ, so check the ones you are considering.</p>
    </section>

    <section class="sec" id="verdict">
      <h2>Where %(name)s is stronger</h2>
      <div class="verdict solo">
        <div class="pro"><ul>%(pros)s</ul></div>
      </div>
    </section>
%(end)s
  </div>
</div>

<div class="wrap">
  <a class="next" href="%(nslug)s.html"><span>Next product</span><strong>%(nname)s %(arw)s</strong></a>
</div>
</main>
""" % dict(accent=p["accent"], topbar=topbar(p["slug"] + ".html"), name=e(p["name"]), h1=e(p["h1"]), lede=e(p["lede"]),
           links=links, note=note, chapter=chapter(SHOWCASE[p["slug"]]["chapter"]), scene=scene(p), intro=intro,
           pre=builtsync_pre() if p["slug"] == "builtsync" else "",
           post=builtsync_post() if p["slug"] == "builtsync" else media_live(p),
           logo=media_logo(p), figure=media_figure(p), fn_cls=" has-photos" if fn_photos is not None else "",
           fns=fns, audience=e(p["audience"]), ths=ths, rows=rows, pros=pros, cons=cons, fit=e(p["fit"]),
           toc_mid='<a href="#demo">Demo</a>\n    ' if smart else "",
           toc_end='<a href="#rollout">Roll-out</a>\n    <a href="#more">What comes next</a>' if smart else "",
           mid=SMARTSITE_DEMO if smart else "", end=SMARTSITE_END if smart else "",
           nslug=nxt["slug"], nname=e(nxt["name"]), arw=ARW)
    scripts = '<script src="assets/builtsync/demo-data.js"></script>\n<script src="assets/demo.js"></script>\n<script src="assets/p2demo.js"></script>\n' if p["slug"] == "builtsync" else ""
    return head(p["title"], p["desc"]) + body + footer(scripts=scripts)


def home_visual(p):
    if p["shot"] is None:
        return '<a class="shot wipe" href="%s.html" aria-label="%s: full breakdown" data-step="0">%s</a>' % (p["slug"], e(p["name"]), plan(uid="h"))
    f, w, h, alt = p["shot"]
    return ('<a class="shot wipe" href="%s.html" aria-label="%s: full breakdown"><img src="assets/%s" alt="%s" width="%d" height="%d" loading="lazy"></a>'
            % (p["slug"], e(p["name"]), f, e(alt), w, h))


def demo_link(p):
    href, label = p["demo"]
    if href.startswith("#"):
        return '<a class="pill line" href="%s.html%s">%s</a>' % (p["slug"], href, e(label))
    return '<a class="pill line" href="%s" target="_blank" rel="noopener">%s</a>' % (href, e(label))


# Client wall on the home page. Add a company as (name, logo file in assets/ or None, link or None).
CLIENTS = [
    ("Clarity Group", None, "https://www.clarity.com.sg"),
]
CLIENT_SLOTS = 6


def client_wall():
    cells = ""
    for name, logo, link in CLIENTS:
        inner = '<img src="assets/%s" alt="%s">' % (logo, e(name)) if logo else e(name)
        cells += "<li>%s</li>" % ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (link, inner) if link else "<span>%s</span>" % inner)
    for _ in range(max(0, CLIENT_SLOTS - len(CLIENTS))):
        cells += '<li><span class="open">Reserved for a pilot partner</span></li>'
    return '<ul class="clients">%s</ul>' % cells


def home():
    nav_links = ('<a href="builtsync.html">BuiltSync</a><a href="ezjob.html">EZJOB</a><a href="courseatlas.html">Course Atlas</a>'
                 '<a href="smartsite.html">Smart Site</a><a href="#services">Services</a><a href="#about">About</a>')
    prows = ""
    for i, p in enumerate(PRODUCTS):
        prows += """
    <article class="prow%s" id="%s" style="--c:%s">
      <div class="p-copy">
        <h3>%s</h3>
        <span class="kind">%s</span>
        <p>%s</p>
        <ul class="feats">%s</ul>
        <div class="p-links">
          <a class="pill solid" href="%s.html">How %s works %s</a>
          %s
        </div>
      </div>
      %s
    </article>""" % (" flip" if i % 2 else "", p["slug"], p["accent"], e(p["name"]), e(p["kind"]), e(p["home_copy"]),
                     "".join("<li>%s</li>" % e(x) for x in p["home_feats"]), p["slug"], e(p["name"]), ARW,
                     demo_link(p), home_visual(p))

    body = """<body>
%(topbar)s
<main class="hero" id="top">
  <div class="bg" role="img" aria-label="Stylised globe of Earth rendered as a violet dot matrix against a starfield, slowly rotating">
    <video class="bg-video is-active" id="bgVideoA" autoplay muted loop playsinline preload="auto" disablepictureinpicture aria-hidden="true" poster="%(poster)s">
      <source src="%(video)s" type="video/mp4">
    </video>
    <video class="bg-video" id="bgVideoB" muted loop playsinline preload="auto" disablepictureinpicture aria-hidden="true" poster="%(poster)s">
      <source src="%(video)s" type="video/mp4">
    </video>
  </div>

  <header class="nav">
    <a class="logo" href="#top" aria-label="LENIX home"><img src="assets/logo-on-dark.png" alt="LENIX" width="628" height="220"></a>
    <nav class="nav-links" aria-label="Primary">%(nav_links)s</nav>
    <div class="nav-actions">
      <button class="btn btn-login js-theme" type="button" aria-label="Switch theme">%(sun)s%(moon)s</button>
      <a class="btn btn-nav-start" href="#contact">Talk to us %(arw)s</a>
    </div>
    <button class="burger js-burger" id="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </header>

  <nav class="menu" id="menu" aria-label="Mobile">
    %(nav_links)s
    <div class="divider"></div>
    <button class="m-theme js-theme" type="button"><span class="js-theme-label">Light theme</span></button>
    <a class="m-start" href="#contact">Talk to us %(arw)s</a>
  </nav>

  <div class="hero-inner">
    <h1><span class="ln"><span class="ln-i">Every workforce,</span></span>
        <span class="ln"><span class="ln-i grad-text">connected.</span></span></h1>
    <p class="sub">Hire skilled talent, train and certify your people,<br>
      and run every site from check-in to payslip,<br>
      on technology built to work together.</p>
    <div class="ctas">
      <a class="btn btn-lg btn-primary" href="#products">Explore products %(arw)s</a>
      <a class="btn btn-lg btn-ghost" href="#contact">Contact us %(arw)s</a>
    </div>
  </div>
</main>

<section class="blk thread" id="loop">
  <div class="wrap">
    <h2>One line from the first hire to the final payslip.</h2>
    <p class="lede">Workforce data usually lives in job boards, training providers' inboxes, paper timesheets and payroll spreadsheets. LENIX builds the products that join those steps up.</p>
    <ol data-scroll data-steps>
      <li><span class="n">01</span><h3>Hire</h3><p>Match verified skilled-trades and technical talent with the employers who need them.</p><a href="ezjob.html">EZJOB %(arw)s</a></li>
      <li><span class="n">02</span><h3>Train</h3><p>Find the right course on the right date, across Singapore's training providers.</p><a href="courseatlas.html">Course Atlas %(arw)s</a></li>
      <li><span class="n">03</span><h3>Deploy</h3><p>Check workers in on site with location and face verification, and see attendance live.</p><a href="builtsync.html">BuiltSync %(arw)s</a></li>
      <li><span class="n">04</span><h3>Pay</h3><p>Turn verified hours into payslips that workers can confirm or dispute in the app.</p><a href="builtsync.html#functions">BuiltSync payroll %(arw)s</a></li>
    </ol>
  </div>
</section>

<section class="blk" id="products">
  <div class="wrap">
    <h2>Four products under one umbrella.</h2>
    <p class="lede">Each one has its own page with what it does, how it compares with the usual alternatives, and where it is stronger.</p>%(prows)s
  </div>
</section>

<section class="blk" id="services" style="padding-top:clamp(24px, 4vw, 48px)">
  <div class="wrap">
    <h2>The team behind the products.</h2>
    <p class="lede">Beyond its own platforms, LENIX builds, pilots and maintains the digital backbone between site and strategy.</p>
    <div class="rows">
      <div><h3>Venture Lab</h3><p>Incubates and tests new operational tools before they scale.</p></div>
      <div><h3>Pilot Data</h3><p>Runs data pilots that turn raw field signals into operational forecasts.</p></div>
      <div><h3>Digital Transformation</h3><p>Re-engineers legacy workflows into connected, data-driven systems.</p></div>
      <div><h3>IT Solutions</h3><p>Deploys and maintains the hardware, network and infrastructure that keep teams online.</p></div>
    </div>
  </div>
</section>

<section class="blk" id="about">
  <div class="wrap split">
    <div>
      <h2>A technology company built from the project site up.</h2>
      <p class="lede">LENIX Pte Ltd is the digital products, data and IT arm of Clarity Group, a Singapore engineering, construction and industrial manpower group. Our products start from problems we see on real sites, and are tested there before anyone else uses them.</p>
    </div>
    <dl class="facts">
      <div><dt>Company</dt><dd>LENIX Pte Ltd</dd></div>
      <div><dt>Group</dt><dd><a href="https://www.clarity.com.sg/our-business/lenix" target="_blank" rel="noopener">Clarity Group</a></dd></div>
      <div><dt>Based in</dt><dd>Singapore</dd></div>
      <div><dt>Focus</dt><dd>Workforce technology, data and IT</dd></div>
    </dl>
  </div>
</section>

<section class="blk" id="clients">
  <div class="wrap">
    <h2>Reserved for the companies that build what comes next.</h2>
    <p class="lede">LENIX is the technology arm of Clarity Group. We are taking on pilot partners now, and this wall is kept for the companies that run on our products.</p>
    %(clients)s
    <div class="p-links"><a class="pill solid" href="#contact">Run a pilot with us %(arw)s</a></div>
  </div>
</section>

<section class="blk" id="contact">
  <div class="wrap contact">
    <div>
      <h2>Want a walkthrough or a pilot?</h2>
      <p class="lede">Tell us about your sites and your workforce. We will show you the products on your own use case.</p>
    </div>
    <div class="contact-links">
      <a href="mailto:lenix@clarity.com.sg">lenix@clarity.com.sg</a>
      <a href="tel:+6589948015">+65 8994 8015</a>
    </div>
  </div>
</section>
""" % dict(topbar=topbar("index.html", home=True), poster=POSTER, video=VIDEO, nav_links=nav_links, sun=SUN, moon=MOON, arw=ARW,
           prows=prows, clients=client_wall())
    return head("LENIX — Connecting every workforce",
                "LENIX builds the technology that links the workforce together: EZJOB for hiring, Course Atlas for training and BuiltSync for running every project site.",
                ENTRANCE) + body + footer(home=True)


def write(name, text):
    with io.open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote", name, len(text))


if __name__ == "__main__":
    # The pages are now built by build_site.py (the 3D redesign); this file supplies the product data and demo blocks.
    import runpy
    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_site.py"), run_name="__main__")
