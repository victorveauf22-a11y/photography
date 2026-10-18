"""Generates site/index.html from src/head.html plus the content defined below.
Run:  python build_site.py
All media live under site/img/<project>/<NN>.jpg (Behance project images) and
site/vid/vN.jpg (poster frames of the Behance-hosted films)."""
import html, json, sys
sys.path.insert(0, "src")
from i18n import TR, SENT, INVALID

# ---------- Behance films (Adobe CCV embeds; they stream from Behance) ----------
FILMS = {
    5:  dict(id='8_m-nUTEz7x', t='Nissan 200SX', sub='Barcelona', dur='0:15', ar='16/9'),
    11: dict(id='DYWyU6ociRz', t='Pit lane', sub='Barcelona-Catalunya', dur='0:15', ar='16/9'),
    6:  dict(id='J3k4sAu577y', t='Paddock', sub='Race weekend', dur='0:20', ar='16/9'),
    4:  dict(id='W8T5bXQKEER', t='KIA Tasman', sub='Moroccan desert', dur='0:49', ar='9/16'),
    10: dict(id='JZobVSXor4Y', t='KIA Tasman', sub='Desert run', dur='0:15', ar='9/16'),
    7:  dict(id='BH8IggFSkJX', t='Grid walk', sub='Race day', dur='0:19', ar='16/9'),
    2:  dict(id='3dYVVcYN42o', t='Porsche GT3 Cup', sub='Detail', dur='0:14', ar='16/9'),
    3:  dict(id='QFvAxITRcsw', t='Classic detail', sub='Short film', dur='1:15', ar='16/9'),
    9:  dict(id='4cT-Z6pBVcB', t='Sri Lanka', sub='Mountain trail', dur='0:40', ar='16/9'),
}
PLAY = '<svg viewBox="0 0 10 12"><path d="M0 0l10 6-10 6z"/></svg>'

def film_card(n, cls):
    f = FILMS[n]
    return (f'<article class="film {cls}" data-embed="{f["id"]}" data-ar="{f["ar"]}" data-cap="{html.escape(f["t"])} · {html.escape(f["sub"])}" tabindex="0" role="button" aria-label="Play {html.escape(f["t"])}">'
            f'<img src="vid/v{n}.jpg" alt="{html.escape(f["t"])} film still" loading="lazy">'
            f'<div class="tag"><div><b>{html.escape(f["t"])}</b><small>{html.escape(f["sub"])} · {f["dur"]}</small></div><span class="play">{PLAY}</span></div></article>')

# ---------- Photo selections (index = position in the Behance project) ----------
KIA = [28,0,2,3,4,6,7,10,11,8,9,12,13,14,15,16,17,19,21,24,27,29,30,26,33,34,37,40]
MOTO = [0,2,3,4,5,9,15,17,20,21,26,31,32,36,37,42,43,45,46,48,51,54,56,60,62,69,70,73,74,75]
SUPER = [0,1,2,3,4,7,8,9,10,11,13,14,15,16,5]
RETRO = list(range(15))
NISSAN = list(range(18))

def kia_cap(i):
    if i in (0,2,3,4,6,7,10,11): return 'KIA EV6 · Morocco'
    if i in (8,9): return 'KIA Picanto · Morocco'
    if i in (12,13,14): return 'KIA Seltos · Morocco'
    if 15 <= i <= 25: return 'KIA Sorento · Morocco'
    return 'KIA Tasman · Morocco'
def moto_cap(i):
    if i in (15,16,17): return 'Le Mans 24 Hours · Pit stop'
    if i == 20: return 'Le Mans 24 Hours'
    if i in (45,46,50,51): return 'Formula E · Madrid'
    return 'Motorsport'
def super_cap(i):
    if i in (0,1,2,3,4,8,9,11,12): return 'Shelby GT500 · Dubai'
    if i in (13,14,15): return 'Porsche 911 GT3 RS'
    if i == 10: return 'Porsche 911 GT3'
    if i in (6,7): return 'Ferrari F8'
    if i == 16: return 'McLaren'
    return 'Dubai'
RETRO_CAPS = {4:'Alfa Romeo GTV',9:'Bentley Arnage',10:'Car meet',11:'Subaru Impreza',12:'BMW E30',13:'Simca Rallye',14:'Mazda MX-5'}
def retro_cap(i): return RETRO_CAPS.get(i, 'Classic collection')

def tiles(proj, idxs, cap, alt_prefix, first_eager=0):
    out = []
    for k, i in enumerate(idxs):
        c = cap(i)
        load = '' if k < first_eager else ' loading="lazy"'
        out.append(f'<figure class="tile" data-cap="{html.escape(c)}"><img src="img/{proj}/{i:02d}.jpg" alt="{html.escape(alt_prefix)}: {html.escape(c)}"{load}></figure>')
    return '\n        '.join(out)

def rail(rail_id, label, body):
    return (f'<div class="rail" id="{rail_id}" aria-label="{label}. Drag or swipe to explore."><div class="track">\n        {body}\n      </div></div>'
            f'<div class="railbar"><i></i></div>')

BEHANCE = 'https://www.behance.net/victorveau'
LINKS = dict(kia='https://www.behance.net/gallery/240017237/KIA-Morroco', moto='https://www.behance.net/gallery/240017679/Motorsports',
             sup='https://www.behance.net/gallery/240017545/Supercars', retro='https://www.behance.net/gallery/240017351/Retro-cars',
             vid='https://www.behance.net/gallery/257279931/Videos')

def proj_head(eyebrow, title_html, lede, link, chips=()):
    ch = ''.join(f'<span>{c}</span>' for c in chips)
    return (f'<div class="wrap proj-head"><div class="head"><p class="eyebrow rv">{eyebrow}</p>'
            f'<h2 class="h2 rv" style="--d:.06s">{title_html}</h2><p class="lede rv" style="--d:.12s">{lede}</p>'
            + (f'<div class="chips rv" style="--d:.16s">{ch}</div>' if ch else '') +
            f'</div><a class="link rv" href="{link}" target="_blank" rel="noopener">View project on Behance ↗</a></div>')

BODY = f'''<body>

<header class="nav" id="nav">
  <a class="brand" href="#top" aria-label="Victor Veau, home">Victor Veau<i>.</i></a>
  <ul>
    <li><a href="#featured">Featured</a></li>
    <li><a href="#film">Film</a></li>
    <li><a href="#kia">Automotive</a></li>
    <li><a href="#motorsport">Motorsport</a></li>
    <li><a href="#clients">Clients</a></li>
    <li><a href="#services">Services</a></li>
  </ul>
  <div class="lang" role="group" aria-label="Language"><button data-lang="en" aria-pressed="true">EN</button><button data-lang="fr" aria-pressed="false">FR</button><button data-lang="es" aria-pressed="false">ES</button><button data-lang="ca" aria-pressed="false">CA</button></div>
  <a class="pill" href="#contact">Book a shoot</a>
</header>

<main id="top">
  <section class="hero" style="padding-top:0;padding-bottom:clamp(32px,7vh,80px)">
    <div class="hero-img" id="heroImg"><img src="img/hero.jpg" alt="KIA Tasman at sunset in the Moroccan desert" fetchpriority="high"></div>
    <div>
      <p class="eyebrow rv">Photography &amp; Film · Barcelona</p>
      <h1 class="display rv" style="--d:.08s;margin-top:18px">Cars, in <span class="serif">motion.</span></h1>
      <div class="hero-row">
        <p class="lede rv" style="--d:.2s">Automotive, motorsport and brand imagery for dealerships, universities and events. From the Atlas Mountains to Le Mans, shot on location and graded with care.</p>
        <div class="cta rv" style="--d:.3s">
          <a class="btn solid" href="#featured" data-open-embed="W8T5bXQKEER">Watch the featured film</a>
          <a class="btn ghost" href="#contact">Get in touch</a>
        </div>
      </div>
    </div>
    <span class="scrollcue">Scroll</span>
  </section>

  <div class="stats" aria-label="At a glance">
    <div class="stat rv"><b data-count="2" data-suffix="+">2+</b><span>Years working professionally</span></div>
    <div class="stat rv" style="--d:.06s"><b>KIA · Geely</b><span>Dealership clients</span></div>
    <div class="stat rv" style="--d:.12s"><b>Le Mans</b><span>24 Hours, Formula E &amp; more</span></div>
    <div class="stat rv" style="--d:.18s"><b data-count="4">4</b><span>Languages: EN · FR · ES · CA</span></div>
  </div>

  <!-- FEATURED FILM -->
  <section id="featured">
    <div class="showcase">
      <div class="copy">
        <p class="eyebrow rv">Featured film · KIA</p>
        <h2 class="h2 rv" style="--d:.06s">KIA Tasman, <span class="serif">Moroccan desert.</span></h2>
        <p class="rv" style="--d:.12s">A 49-second film built around the Tasman's off-road ability: aerial tracking over the dunes, cockpit detail, driving shots and on-screen callouts, finished to a brand standard.</p>
        <div class="meta2 rv" style="--d:.16s"><span>Direction &amp; shoot</span><span>Edit &amp; grade</span><span>Aerial</span><span>0:49</span></div>
        <div class="cta rv" style="--d:.2s"><a class="btn solid" href="#featured" data-open-embed="W8T5bXQKEER">Play the film</a><a class="btn ghost" href="#kia">See the KIA stills</a></div>
      </div>
      <div class="reel rv" style="--d:.1s">
        <article class="phone" data-embed="W8T5bXQKEER" data-ar="9/16" data-cap="KIA Tasman · Moroccan desert" tabindex="0" role="button" aria-label="Play the KIA Tasman film">
          <img src="vid/v4.jpg" alt="KIA Tasman driving toward the camera in the desert">
          <span class="bigplay">{PLAY}</span><span class="dur">0:49</span>
        </article>
        <div class="strip" aria-hidden="true"><img src="vid/v4a.jpg" alt="" loading="lazy"><img src="vid/v4b.jpg" alt="" loading="lazy"><img src="vid/v4c.jpg" alt="" loading="lazy"></div>
      </div>
    </div>
  </section>

  <!-- FILM -->
  <section id="film" class="sec-sp" style="padding-top:clamp(72px,12vw,160px)">
    <div class="proj-head wrap" style="margin-bottom:clamp(28px,4vw,56px)"><div class="head"><p class="eyebrow rv">Film</p>
      <h2 class="h2 rv" style="--d:.06s">Stories, <span class="serif">in motion.</span></h2>
      <p class="lede rv" style="--d:.12s">Short films and reels from track days, car meets and desert shoots. Tap any film to play it.</p></div>
      <a class="link rv" href="{LINKS['vid']}" target="_blank" rel="noopener">All films on Behance ↗</a></div>
    <article class="feature rv" data-embed="{FILMS[5]['id']}" data-ar="16/9" data-cap="Nissan 200SX · Barcelona" tabindex="0" role="button" aria-label="Play the Nissan 200SX film">
      <img src="vid/v5.jpg" alt="Nissan 200SX driving toward the camera in Barcelona">
      <div class="cap2"><div><h3>Nissan <em>200SX</em></h3><small>Barcelona · 0:15</small></div><span class="bigplay">{PLAY}</span></div>
    </article>
    <div class="films">
      {film_card(11,'s6')}
      {film_card(6,'s6')}
      {film_card(10,'s3 v')}
      {film_card(7,'s9 st')}
      {film_card(2,'s6')}
      {film_card(3,'s6')}
      {film_card(9,'s6')}
    </div>
  </section>

  <!-- KIA -->
  <section id="kia" class="sec-sp">
    {proj_head('Automotive · KIA Morocco', 'One brand, <span class="serif">five models.</span>', 'EV6 through the Moroccan old town, Sorento in the Atlas, the new Tasman in the dunes. Product, motion and mood built around real light instead of a studio.', LINKS['kia'], ['EV6','Picanto','Seltos','Sorento','Tasman'])}
    <div style="height:clamp(28px,4vw,56px)"></div>
    {rail('rail-kia','KIA Morocco gallery', tiles('kia', KIA, kia_cap, 'KIA Morocco', 2))}
  </section>

  <!-- MOTORSPORT -->
  <section id="motorsport" class="sec-sp">
    {proj_head('Motorsport', 'Pit lane to <span class="serif">the apex.</span>', 'Endurance racing, Formula E and historic touring cars: the grid, the garage and the moments in between.', LINKS['moto'], ['Le Mans 24 Hours','Formula E Madrid','24H Series','Barcelona-Catalunya'])}
    <div style="height:clamp(28px,4vw,56px)"></div>
    {rail('rail-moto','Motorsport gallery', tiles('motorsports', MOTO, moto_cap, 'Motorsport'))}
  </section>

  <!-- SUPERCARS -->
  <section id="supercars" class="sec-sp">
    {proj_head('Supercars', 'Night, neon <span class="serif">and chrome.</span>', 'A colour-shifting Nissan 200SX around Barcelona, then Dubai after dark: a Shelby GT500, GT3 RS and Ferrari against the skyline.', LINKS['sup'], ['Nissan 200SX','Shelby GT500','Porsche GT3 RS','Ferrari F8'])}
    <div style="height:clamp(28px,4vw,56px)"></div>
    {rail('rail-sup','Supercars gallery', tiles('nissan', NISSAN, lambda i: 'Nissan 200SX · Barcelona', 'Nissan 200SX') + chr(10) + '        ' + tiles('supercars', SUPER, super_cap, 'Supercars'))}
  </section>

  <!-- RETRO -->
  <section id="retro" class="sec-sp">
    {proj_head('Retro cars', 'Classics, <span class="serif">warm light.</span>', 'Collector garages, car meets and the cars that made people fall in love with driving.', LINKS['retro'])}
    <div style="height:clamp(28px,4vw,56px)"></div>
    {rail('rail-retro','Retro cars gallery', tiles('retro', RETRO, retro_cap, 'Retro cars'))}
  </section>

  <!-- CLIENTS -->
  <section id="clients" class="sec-sp">
    <div class="wrap head"><p class="eyebrow rv">Clients &amp; events</p>
      <h2 class="h2 rv" style="--d:.06s">Trusted on <span class="serif">location.</span></h2></div>
    <div class="wall">
      <div class="rv"><h3>Clients</h3><ul><li>KIA</li><li>Geely</li><li>Universities</li><li>Oak House School</li></ul></div>
      <div class="rv" style="--d:.08s"><h3>Events shot</h3><ul><li class="s">Le Mans 24 Hours</li><li class="s">Formula E · Madrid</li><li class="s">24H Series</li><li class="s">Barcelona Grand Tour</li></ul></div>
    </div>
  </section>

  <!-- SERVICES -->
  <section id="services" class="sec-sp">
    <div class="wrap head">
      <p class="eyebrow rv">What I do</p>
      <h2 class="h2 rv" style="--d:.06s">One shooter. <span class="serif">Stills and motion.</span></h2>
    </div>
    <div class="cards">
      <article class="card rv"><span class="n">01</span><h3>Automotive</h3><p>Launches, dealership content, details and lifestyle imagery for new and used stock.</p><ul><li>Car launches</li><li>Dealerships</li><li>Detail</li></ul></article>
      <article class="card rv" style="--d:.07s"><span class="n">02</span><h3>Motorsport &amp; events</h3><p>Race weekends, corporate events, conferences, sports and ceremonies, covered end to end.</p><ul><li>Racing</li><li>Corporate</li><li>Sports</li></ul></article>
      <article class="card rv" style="--d:.14s"><span class="n">03</span><h3>Commercial</h3><p>Product and brand content built for social, web and print, delivered in the formats you need.</p><ul><li>Product</li><li>Social assets</li><li>Brand</li></ul></article>
      <article class="card rv" style="--d:.21s"><span class="n">04</span><h3>Video &amp; aerial</h3><p>Videography, editing and colour grading, plus licensed drone work for the shots a tripod can't reach.</p><ul><li>Edit &amp; grade</li><li>Drone</li><li>Promo clips</li></ul></article>
    </div>
  </section>

  <!-- PROCESS -->
  <section id="process" class="sec-sp">
    <div class="wrap head"><p class="eyebrow rv">How it works</p>
      <h2 class="h2 rv" style="--d:.06s">From brief <span class="serif">to delivery.</span></h2></div>
    <div class="steps">
      <div class="step rv"><span class="n">1</span><h3>Brief</h3><p>Tell me the goal, the platforms and the deadline.</p></div>
      <div class="step rv" style="--d:.07s"><span class="n">2</span><h3>Plan</h3><p>Location, light and shot list agreed before the day.</p></div>
      <div class="step rv" style="--d:.14s"><span class="n">3</span><h3>Shoot</h3><p>On location, with drone and video added when the story needs it.</p></div>
      <div class="step rv" style="--d:.21s"><span class="n">4</span><h3>Edit &amp; deliver</h3><p>Retouched, graded and delivered in the formats you need.</p></div>
    </div>
  </section>

  <!-- PACKAGES -->
  <section id="packages" class="sec-sp">
    <div class="wrap head"><p class="eyebrow rv">Packages</p>
      <h2 class="h2 rv" style="--d:.06s">Choose a <span class="serif">starting point.</span></h2>
      <p class="lede rv" style="--d:.12s">Every project is quoted to fit. These are the three ways most clients begin.</p></div>
    <div class="pkgs">
      <article class="pkg rv"><h3>Essential</h3><p>A focused shoot for one car, one product or a small event.</p><ul><li>Edited, colour-graded photos</li><li>Web and social crops</li><li>Quick delivery</li></ul><span class="q">Custom quote</span></article>
      <article class="pkg hot rv" style="--d:.07s"><h3>Campaign</h3><p>Photo and film together for a launch or a dealership campaign.</p><ul><li>Photo and short film</li><li>Aerial footage</li><li>Cuts for every social format</li></ul><span class="q">Custom quote</span></article>
      <article class="pkg rv" style="--d:.14s"><h3>Event &amp; race weekend</h3><p>Full coverage of an event, from setup to the final lap.</p><ul><li>Full edited gallery</li><li>Fast highlights for social</li><li>Video recap</li></ul><span class="q">Custom quote</span></article>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about" class="sec-sp">
    <div class="about">
      <figure class="rv"><img src="img/kia/34.jpg" alt="KIA Tasman parked under an acacia tree in the desert" loading="lazy"></figure>
      <div>
        <p class="eyebrow rv">About</p>
        <h2 class="h2 rv" style="--d:.06s;margin:16px 0 22px">Barcelona-based, <span class="serif">on location.</span></h2>
        <p class="rv" style="--d:.1s">I'm Victor, a photographer and videographer shooting professionally for over two years. My work covers <strong>automotive</strong>, <strong>motorsport</strong> and <strong>commercial</strong> content, from dealership shoots to international events.</p>
        <p class="rv" style="--d:.14s">I work in four languages, fly licensed drones, and handle the edit and colour grade myself, so what you brief is what you get back, quickly.</p>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <section class="contact" id="contact">
    <div class="wrap">
      <p class="eyebrow rv">Let's work together</p>
      <h2 class="display rv" style="--d:.06s">Have a shoot <span class="serif" style="color:var(--accent)">in mind?</span></h2>
      <form class="book rv" id="book" style="--d:.12s" action="https://formspree.io/f/xljgvoeo" method="POST" novalidate>
        <input type="hidden" name="_subject" value="New shoot enquiry from the website">
        <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
        <label><span>Name</span><input name="name" required autocomplete="name" data-ph="Your name" placeholder="Your name"></label>
        <label><span>Email</span><input name="email" type="email" required autocomplete="email" data-ph="you@company.com" placeholder="you@company.com"></label>
        <label><span>Type of shoot</span><select name="type"><option value="Automotive">Automotive</option><option value="Motorsport / event">Motorsport / event</option><option value="Commercial">Commercial</option><option value="Video / aerial">Video / aerial</option><option value="Other">Other</option></select></label>
        <label><span>Date</span><input name="date" data-ph="Date or timeframe" placeholder="Date or timeframe"></label>
        <label class="full"><span>Details</span><textarea name="msg" required data-ph="Tell me about the project: location, goal, where it will be used." placeholder="Tell me about the project: location, goal, where it will be used."></textarea></label>
        <button class="btn solid go" type="submit">Send enquiry</button>
        <span class="note">Your details are only used to reply to your enquiry.</span>
        <p class="sent" id="sent" role="status"></p>
      </form>
      <div class="row rv" style="--d:.18s"><a class="btn ghost" href="{BEHANCE}" target="_blank" rel="noopener">Full portfolio on Behance ↗</a></div>
      <p class="meta rv" style="--d:.22s">Based in Barcelona · Available for travel</p>
    </div>
  </section>
</main>

<footer>
  <span>© <span id="yr">2026</span> Victor Veau</span>
  <span><a href="{BEHANCE}" target="_blank" rel="noopener">Behance</a></span>
</footer>

<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Media viewer">
  <div class="scrim" data-close></div>
  <div class="stage" id="stage"></div>
  <button class="x" data-close aria-label="Close"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <button class="pv" id="pv" aria-label="Previous"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
  <button class="nx" id="nx" aria-label="Next"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
  <div class="cap" id="cap"></div>
</div>
'''

SCRIPT = r'''
<script>
(()=>{
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
document.getElementById('yr').textContent = new Date().getFullYear();

const io = new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));

const nav = document.getElementById('nav'); let ly = scrollY;
addEventListener('scroll',()=>{const y=scrollY; nav.classList.toggle('hide', y>ly && y>240); ly=y; hero()},{passive:true});

const hi = document.getElementById('heroImg');
function hero(){ if(RM) return; const y=Math.min(scrollY,innerHeight); hi.style.transform=`translate3d(0,${y*.18}px,0) scale(${1+y/innerHeight*.06})` }
hero();

document.querySelectorAll('[data-count]').forEach(el=>{
  const end=+el.dataset.count, suf=el.dataset.suffix||''; if(RM){el.textContent=end+suf;return}
  el.textContent='0'+suf;
  new IntersectionObserver(([e],o)=>{ if(!e.isIntersecting) return; o.disconnect(); const t0=performance.now();
    (function f(t){const p=Math.min((t-t0)/1100,1), v=1-Math.pow(1-p,3); el.textContent=Math.round(end*v)+suf; if(p<1) requestAnimationFrame(f)})(t0) },{threshold:.6}).observe(el);
});

/* Draggable rail: 1:1 tracking, momentum projection, rubber-banding, spring settle that inherits release velocity */
function rail(root){
  const bar = root.nextElementSibling.querySelector('i'), track = root.querySelector('.track');
  let x=0, min=0, v=0, drag=false, moved=0, sx=0, ox=0, last=0, lt=0, raf=0, raw=0;
  const rb=(o,d=innerWidth)=>(o*d*.55)/(d+.55*Math.abs(o));
  const measure=()=>{min=Math.min(0,root.clientWidth-track.scrollWidth)};
  const paint=()=>{ track.style.transform=`translate3d(${x}px,0,0)`;
    const tw=track.scrollWidth, cw=root.clientWidth, frac=Math.min(1,cw/tw), span=tw-cw;
    bar.style.width=(frac*100)+'%'; bar.style.transform=`translateX(${span>0? (-Math.max(min,Math.min(0,x))/span)*(1/frac-1)*100 : 0}%)` };
  root.addEventListener('pointerdown',e=>{ if(e.pointerType==='mouse'&&e.button!==0) return; cancelAnimationFrame(raf); drag=true; moved=0; sx=e.clientX; ox=x; raw=x; last=e.clientX; lt=e.timeStamp; v=0; root.classList.add('drag'); root.setPointerCapture(e.pointerId) });
  root.addEventListener('pointermove',e=>{ if(!drag) return; const dx=e.clientX-sx; moved=Math.max(moved,Math.abs(dx)); raw=ox+dx;
    const dt=e.timeStamp-lt; if(dt>0){v=.8*v+.2*((e.clientX-last)/dt*1000)} last=e.clientX; lt=e.timeStamp;
    x=raw>0? rb(raw): raw<min? min+rb(raw-min): raw; paint() });
  const end=()=>{ if(!drag) return; drag=false; root.classList.remove('drag');
    const proj=(v/1000)*.998/(1-.998)*.35, target=Math.max(min,Math.min(0,x+proj)); let p=x, vel=v, t0=performance.now();
    const k=170, c=2*Math.sqrt(k)*.9;
    const step=t=>{const dt=Math.min((t-t0)/1000,.032); t0=t; vel+=(-k*(p-target)-c*vel)*dt; p+=vel*dt; x=p; paint();
      if(Math.abs(vel)>.5||Math.abs(p-target)>.3) raf=requestAnimationFrame(step); else {x=target;paint()}};
    raf=requestAnimationFrame(step) };
  root.addEventListener('pointerup',end); root.addEventListener('pointercancel',end);
  root.addEventListener('wheel',e=>{ if(Math.abs(e.deltaX)>Math.abs(e.deltaY)){ e.preventDefault(); x=Math.max(min,Math.min(0,x-e.deltaX)); paint() } },{passive:false});
  root.addEventListener('click',e=>{ if(moved>6){e.stopPropagation();e.preventDefault()} },true);
  const re=()=>{measure(); x=Math.max(min,Math.min(0,x)); paint()};
  addEventListener('resize',re); addEventListener('load',re);
  root.querySelectorAll('img').forEach(i=>i.addEventListener('load',re));
  re();
}
document.querySelectorAll('.rail').forEach(rail);

/* Lightbox: photos and Behance-hosted film embeds */
const items=[...document.querySelectorAll('.tile, [data-embed]')];
const lb=document.getElementById('lb'), stage=document.getElementById('stage'), cap=document.getElementById('cap'); let cur=0, lastFocus=null;
function show(i){ cur=(i+items.length)%items.length; const el=items[cur]; stage.innerHTML='';
  if(el.dataset.embed){ const [a,b]=el.dataset.ar.split('/').map(Number); const w=document.createElement('div'); w.className='frame'+(a<b?' vert':''); w.style.setProperty('--ar',a/b);
    const f=document.createElement('iframe'); f.src=`https://www-ccv.adobe.io/v1/player/ccv/${el.dataset.embed}/embed?api_key=behance1&bgcolor=%23000000`;
    f.allow='autoplay; fullscreen; picture-in-picture'; f.allowFullscreen=true; f.title=el.dataset.cap; w.appendChild(f); stage.appendChild(w) }
  else { const s=el.querySelector('img'); const im=new Image(); im.src=s.currentSrc||s.src; im.alt=s.alt; stage.appendChild(im) }
  cap.textContent=el.dataset.cap||'' }
function open(i){ lastFocus=document.activeElement; show(i); lb.classList.add('open'); document.body.style.overflow='hidden'; lb.querySelector('.x').focus() }
function close(){ lb.classList.remove('open'); document.body.style.overflow=''; stage.innerHTML=''; lastFocus&&lastFocus.focus&&lastFocus.focus() }
document.querySelectorAll('[data-open-embed]').forEach(btn=>btn.addEventListener('click',e=>{ e.preventDefault(); const i=items.findIndex(x=>x.dataset.embed===btn.dataset.openEmbed); if(i>=0) open(i) }));
items.forEach((el,i)=>{ el.addEventListener('click',()=>open(i)); el.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();open(i)} }) });
lb.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',close));
document.getElementById('pv').addEventListener('click',()=>show(cur-1));
document.getElementById('nx').addEventListener('click',()=>show(cur+1));
addEventListener('keydown',e=>{ if(!lb.classList.contains('open')) return; if(e.key==='Escape') close(); if(e.key==='ArrowLeft') show(cur-1); if(e.key==='ArrowRight') show(cur+1) });

/* ---------- Language ---------- */
const TR = __TR__, SENT = __SENT__, INVALID = __INVALID__;
const LANGS=['en','fr','es','ca']; const tpl=document.createElement('template');
const canon=s=>{tpl.innerHTML=s; return tpl.innerHTML.replace(/\s+/g,' ').trim()};
const MAP=new Map(Object.entries(TR).map(([k,v])=>[canon(k),v]));
const targets=[];
document.querySelectorAll('header *, main *, footer *').forEach(el=>{ if(['SCRIPT','STYLE','IFRAME','IMG','INPUT','TEXTAREA','SELECT'].includes(el.tagName)) return;
  const k=el.innerHTML.replace(/\s+/g,' ').trim(); if(MAP.has(k)){ el.dataset.en=el.innerHTML; targets.push([el,MAP.get(k)]) } });
const phs=[...document.querySelectorAll('[data-ph]')].map(el=>[el,TR[el.dataset.ph]]).filter(x=>x[1]);
let lang='en';
function setLang(l,save){ if(!LANGS.includes(l)) l='en'; lang=l; const i=LANGS.indexOf(l)-1;
  targets.forEach(([el,t])=>{ el.innerHTML = i<0? el.dataset.en : t[i] });
  phs.forEach(([el,t])=>{ el.placeholder = i<0? el.dataset.ph : t[i] });
  document.documentElement.lang=l; if(typeof renderSent==='function') renderSent();
  document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lang===l)));
  if(save){ try{localStorage.setItem('lang',l)}catch(e){} } }
document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>setLang(b.dataset.lang,true)));
let stored=null; try{stored=localStorage.getItem('lang')}catch(e){}
const nl=(navigator.language||'en').slice(0,2).toLowerCase();

/* ---------- Booking form (opens the visitor's email app; no server needed) ---------- */
const form=document.getElementById('book'), sent=document.getElementById('sent'); let sentState=null;
const TO=['victor.veauf22','gmail.com'].join('@');
function renderSent(){ if(!sentState){ sent.classList.remove('show'); return } sent.innerHTML = (sentState==='invalid'? INVALID : SENT[sentState])[lang].replace('{a}',`<a href="mailto:${TO}">${TO}</a>`); sent.classList.add('show') }
form.addEventListener('submit',async e=>{ e.preventDefault(); const d=new FormData(form);
  const bad=[...form.elements].filter(f=>f.name&&(f.name==='name'||f.name==='msg'?!f.value.trim():f.name==='email'?!/^\S+@\S+\.\S+$/.test(f.value.trim()):false));
  form.querySelectorAll('[aria-invalid]').forEach(f=>f.removeAttribute('aria-invalid'));
  if(bad.length){ bad.forEach(f=>f.setAttribute('aria-invalid','true')); sentState='invalid'; renderSent(); bad[0].focus(); return }
  const btn=form.querySelector('.go'); btn.disabled=true; sentState='sending'; renderSent();
  try{
    const r=await fetch(form.action,{method:'POST',headers:{Accept:'application/json'},body:d});
    if(!r.ok) throw new Error(r.status);
    sentState='ok'; form.reset();
  }catch(err){
    const body=`Name: ${d.get('name')}
Email: ${d.get('email')}
Type: ${d.get('type')}
Date: ${d.get('date')||'-'}

${d.get('msg')}`;
    location.href='mailto:'+TO+'?subject='+encodeURIComponent(`Shoot enquiry: ${d.get('type')} (${d.get('name')})`)+'&body='+encodeURIComponent(body);
    sentState='fallback';
  }
  btn.disabled=false; renderSent() });
setLang(stored || (LANGS.includes(nl)?nl:'en'), false);
})();
</script>
</body>
</html>
'''

head = open('src/head.html', encoding='utf8').read()
script = SCRIPT.replace('__TR__', json.dumps(TR, ensure_ascii=False)).replace('__SENT__', json.dumps(SENT, ensure_ascii=False)).replace('__INVALID__', json.dumps(INVALID, ensure_ascii=False))
open('site/index.html', 'w', encoding='utf8').write(head + BODY + script)
print('built site/index.html')
