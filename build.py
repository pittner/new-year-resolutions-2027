#!/usr/bin/env python3
"""Builds index.html for pittner/new-year-resolutions-2027.

A single-purpose page for the seasonal "new year's resolutions 2027" / "resolution ideas" intent
(searched by everyone in late December and the first week of January): 36 resolutions in 6 groups,
each with why it matters and a first step for this week, and a link that opens the free maker with
that resolution and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098), so it
can go on the phone lock screen. Plus 12 questions to look back at 2026, a 45-minute plan, a box for
your own resolution, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/new-year-resolutions-2027/"
SRC = "ghpages_resolutions"
CAMPAIGN = "resolutions_2027"

# (group, [(resolution, why it matters, a first step for this week)])
GROUPS = [
    ("Health and body", [
        ("Walk 8,000 steps a day", "Walking is the habit people keep when gym plans fail.", "Check your average steps this week and add one 15-minute walk a day"),
        ("Go to bed before 11 pm", "Better sleep makes every other resolution easier.", "Set a phone alarm for 10:30 pm called Start winding down"),
        ("Drink less alcohol", "Fewer drinks means better sleep, more money and clearer mornings.", "Pick two alcohol-free days a week and write them in your calendar"),
        ("Cook at home five days a week", "Home cooking is cheaper and healthier than any diet plan.", "Write five simple dinners you already know and buy for three of them"),
        ("Strength training twice a week", "Muscle protects your back, joints and energy as you age.", "Book two 30-minute slots and do squats, push-ups and rows at home"),
        ("Book the check-ups I keep postponing", "One appointment now can save a big problem later.", "List the doctor, dentist and eye visits you skipped and book the first one"),
    ]),
    ("Mind and habits", [
        ("Spend less time on my phone", "An hour a day back is 365 hours a year.", "Look at your screen time and set a daily limit on the top app"),
        ("Read 12 books in 2027", "One book a month is enough to change how you think.", "Choose the first book and put it where your phone usually lies"),
        ("Journal for five minutes a day", "Writing things down clears your head and shows patterns.", "Put a notebook next to your bed and write three lines tonight"),
        ("Meditate ten minutes a day", "Small daily calm beats one long retreat a year.", "Try one free ten-minute guided session tomorrow morning"),
        ("Stop saying yes to everything", "Every yes to others is a no to your own goals.", "Write down one thing you will say no to this month"),
        ("Finish what I start", "One finished thing beats five half-done ones.", "List your unfinished projects and pick one to finish or drop"),
    ]),
    ("Money", [
        ("Save 10% of every paycheck", "Paying yourself first makes saving automatic.", "Set up an automatic transfer on payday to a separate account"),
        ("Build a three-month emergency fund", "A cushion turns a crisis into an inconvenience.", "Add up your monthly costs and write the target number"),
        ("Pay off my credit card", "Card interest eats the money you work for.", "List every debt with its interest rate and start with the highest"),
        ("Track every expense for 30 days", "You cannot fix spending you do not see.", "Pick one app or a notebook and log today's spending"),
        ("Cancel subscriptions I do not use", "Forgotten subscriptions quietly cost hundreds a year.", "Search your bank statement for monthly payments and cancel one"),
        ("Start investing a small amount monthly", "Time in the market matters more than the amount.", "Read one beginner guide to index funds this week"),
    ]),
    ("Relationships", [
        ("Call my parents every week", "Time with family is the thing people regret not having.", "Pick a fixed day and time and put it in your calendar"),
        ("One date night a month", "Couples who plan time together stay close.", "Agree on the first date night and book it"),
        ("See friends in person twice a month", "Real meetings beat a hundred chat messages.", "Message two friends today and suggest a date"),
        ("Make one new friend", "Adults make friends through repeated contact, not luck.", "Join one club, class or group that meets every week"),
        ("Be fully present at dinner", "Phones at the table quietly push people away.", "Put a box for phones next to the table and start tonight"),
        ("Say thank you more often", "Gratitude makes both people feel better.", "Send one thank-you message to someone who helped you in 2026"),
    ]),
    ("Work and learning", [
        ("Learn a new language", "Fifteen minutes a day gets you to basic conversations in a year.", "Install one language app and do the first lesson today"),
        ("Learn one skill the market pays for", "The right skill raises your price for years.", "Look at ten job ads one level up and count the skills that repeat"),
        ("Ask for a raise", "A raise you ask for with evidence is a raise you can get.", "Write down five results from 2026 with numbers next to them"),
        ("Start a side project", "A side project can become a new income or career.", "Write down three ideas and spend one hour on the best one"),
        ("Get good at AI tools", "People who use AI well will replace people who do not.", "Pick one weekly task and try to do it with an AI assistant"),
        ("Finish one course or certificate", "A finished course beats three started ones.", "Pick one course and block two hours a week in your calendar"),
    ]),
    ("Home, travel and joy", [
        ("Declutter one room a month", "Less stuff means less cleaning and a calmer home.", "Start with one drawer today and fill one bag to give away"),
        ("Travel somewhere new", "New places give you memories that money cannot buy later.", "Pick the place and the month and open a savings pot for it"),
        ("Pick up a hobby I dropped", "Hobbies give energy that work cannot.", "Find the old guitar, brushes or shoes and use them for 20 minutes"),
        ("Spend more time outdoors", "Daylight and nature lower stress and improve sleep.", "Plan one weekend walk somewhere green"),
        ("Volunteer once a month", "Helping others is one of the surest ways to feel better.", "Find one local group that needs help and write to them"),
        ("Celebrate small wins", "Noticing progress keeps you going in February.", "Write three wins from 2026 and tell someone about one"),
    ]),
]

QUESTIONS = [
    "What am I most proud of from 2026?",
    "What drained my energy this year, and what gave it back?",
    "Which resolution from last year did I keep, and why that one?",
    "Which one did I drop, and what got in the way?",
    "What do I want to stop doing in 2027?",
    "Who do I want to spend more time with?",
    "What would make my body feel better a year from now?",
    "Where did my money go this year, and was it worth it?",
    "What did I learn this year that I did not know a year ago?",
    "What is one thing I keep postponing?",
    "What would a good ordinary weekday look like in 2027?",
    "If 2027 goes really well, what is different a year from now?",
]

PLAN = [
    ("10 minutes: look back.", "Write three good things and three hard things from 2026. Scroll your photos and calendar to remember."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough."),
    ("10 minutes: pick three resolutions.", "Not ten. One for your body, one for money or work, one for the people you love."),
    ("10 minutes: make it visible.", "Turn your most important resolution and its first step into a phone lock screen, so you see it 80 times a day."),
]

FAQ = [
    ("What are good New Year's resolutions for 2027?",
     "Good resolutions are small, specific and come with a first step: walk 8,000 steps a day, save 10% of every paycheck, read 12 books, call your parents every week. "
     "This page has 36 resolutions in 6 groups, each with a first step for this week."),
    ("Why do most New Year's resolutions fail?",
     "They are too vague, there are too many of them, and you stop seeing them after the first week. "
     "Pick three, write one first step for each and keep them where you look every day, such as your phone lock screen."),
    ("How many resolutions should I make?",
     "Three is enough: one for your health, one for money or work, one for relationships or joy. Fewer goals get more attention."),
    ("How do I keep my resolutions?",
     "Make them concrete (a number and a date), start with a step you can do this week, and keep them visible. "
     "A lock screen with your resolution reminds you every time you pick up your phone."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone or print it."),
    ("Can I make a full vision board with all my resolutions?",
     "Yes. Start from your resolutions in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>New Year's Resolutions 2027: %%COUNT%% Ideas with a First Step, %%NQ%% Questions &amp; a Free Lock Screen</title>
<meta name="description" content="%%COUNT%% New Year's resolution ideas for 2027 (health, habits, money, relationships, work, joy), each with a first step for this week, %%NQ%% questions to look back at 2026 and a 45-minute plan. Turn your resolution into a free lock screen. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="New Year's resolutions 2027 - %%COUNT%% ideas with a first step and a free lock screen">
<meta property="og:description" content="Resolutions with a first step, %%NQ%% questions to look back, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>New Year's resolutions 2027: %%COUNT%% ideas with a first step for this week</h1>
  <p class="lede">Most resolutions are forgotten by February because they are vague and invisible. Below are %%COUNT%% resolutions, each with why it matters and a first step you can do this week, plus %%NQ%% honest questions to look back at 2026. Press a resolution and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every time you pick up your phone. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% resolutions in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your resolution?</h2>
  <div class="row">
    <div><label for="ownGoal">My resolution for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Walk 8,000 steps a day" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Add one 15-minute walk a day" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your resolution filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions to look back at 2026 before you choose</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to your resolutions.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your 2027 in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my resolutions</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board with my resolutions</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/new-year-resolutions-2027">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own resolution: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your resolution first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
