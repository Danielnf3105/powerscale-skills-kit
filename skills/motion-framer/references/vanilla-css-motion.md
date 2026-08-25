# Premium motion in vanilla HTML/CSS/JS (no React)

Framer Motion is a React library. Many real pages, including single-file
landing pages meant to be pasted into a CMS (GoHighLevel) or deployed static,
are **not** React. This reference translates the same Framer-grade motion
*principles* into vanilla CSS + a few small JS helpers, so the page stays
single-file and portable while feeling like a Framer site.

Use this file when the target is a `.html` page (or any non-React surface) and
you still want premium motion: spring easing, scroll reveals, stagger, hover
micro-interactions, parallax, magnetic buttons. Single-file landing pages
(`landing-b2b.html`, etc.) are exactly this case.

The golden rules carry over from the main skill:
- **Animate only `transform` and `opacity`** (and `filter` sparingly). They are
  GPU-composited; `top/left/width/height/margin` cause layout/paint and jank.
- **Always honour `prefers-reduced-motion`.** Premium also means respectful.
- **Motion should feel like physics, not a metronome.** Use spring-like easing,
  not linear, and stagger sequences instead of firing everything at once.

---

## 1. Spring-like easing in pure CSS

CSS can't do true spring physics, but these cubic-beziers approximate the
Framer spring presets well for one-shot transitions. Define them as variables:

```css
:root{
  --ease-out-soft: cubic-bezier(.22,.61,.36,1);     /* gentle settle */
  --ease-spring:   cubic-bezier(.34,1.56,.64,1);     /* slight overshoot (bouncy) */
  --ease-snappy:   cubic-bezier(.4,0,.2,1);          /* material-ish, crisp */
}
.btn{ transition: transform .25s var(--ease-spring), box-shadow .25s var(--ease-out-soft); }
```

`--ease-spring` overshoots slightly past the target then settles, that tiny
overshoot is what reads as "alive" rather than "CSS transition". Use it on
hover/tap and reveals; use `--ease-out-soft` for things that should feel calm.

For a **true** spring (velocity-aware, interruptible) without React, see §7.

---

## 2. Scroll reveal = the `whileInView` equivalent

Framer's `whileInView` + `viewport={{ once:true }}` becomes an
`IntersectionObserver` that adds a class. Start hidden, reveal on enter.

```css
.reveal{opacity:0;transform:translateY(20px);
  transition:opacity .6s var(--ease-out-soft), transform .6s var(--ease-out-soft)}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
```

```js
const io = new IntersectionObserver((entries)=>{
  for(const e of entries){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }
},{ threshold:.15, rootMargin:'0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

**Robustness:** gate the initial hidden state behind a JS-set class (e.g.
`html.js-anim .reveal{opacity:0}`) and add a `setTimeout` fallback that reveals
everything after ~2.5s. If JS fails or the observer never fires, content must
still be visible. (This is the pattern used in single-file landings.)

---

## 3. Stagger = `staggerChildren`

Framer staggers children via the parent variant. In vanilla, set a per-item
`transition-delay` (or `--i` index) so siblings cascade instead of popping in
together. Cap the delay so long lists don't drag.

```css
.stagger > *{opacity:0;transform:translateY(16px);
  transition:opacity .5s var(--ease-out-soft), transform .5s var(--ease-out-soft);
  transition-delay:calc(var(--i,0) * .07s)}
.stagger.in > *{opacity:1;transform:none}
```

```js
document.querySelectorAll('.stagger').forEach(group=>{
  [...group.children].forEach((child,i)=> child.style.setProperty('--i', Math.min(i,8)));
});
// then reveal `.stagger` with the same IntersectionObserver as §2
```

Good defaults: 60–90ms between items, items rising 12–20px. The grids of cards
on a landing (scenes, steps, pillars, cases) are the natural place for this.

---

## 4. Hover & tap micro-interactions = `whileHover` / `whileTap`

```css
/* whileHover: lift + scale + shadow. Keep scale subtle (1.02–1.05) on large cards. */
.card{transition:transform .25s var(--ease-spring), box-shadow .25s var(--ease-out-soft)}
.card:hover{transform:translateY(-4px) scale(1.015); box-shadow:0 20px 50px -24px rgba(0,0,0,.5)}
/* whileTap: press in. :active fires on pointer down. */
.btn:active{transform:translateY(0) scale(.97)}
/* Animate an inner accent on parent hover (variant propagation analogue) */
.card .arrow{transition:transform .25s var(--ease-spring)}
.card:hover .arrow{transform:translateX(4px)}
```

Pair `:hover` (settle, slower) with `:active` (snap, faster) so buttons feel
physical. Respect reduced motion by scoping transforms out under the media query.

---

## 5. Parallax & scroll-linked motion

Cheap parallax: translate a layer a fraction of scroll. Throttle with rAF and
only touch `transform`.

```js
const layers = document.querySelectorAll('[data-parallax]'); // data-parallax="0.2"
let ticking=false;
addEventListener('scroll',()=>{ if(ticking) return; ticking=true;
  requestAnimationFrame(()=>{ const y=scrollY;
    layers.forEach(l=> l.style.transform = `translate3d(0,${y * +l.dataset.parallax}px,0)`);
    ticking=false; });
},{passive:true});
```

For scroll-progress effects (a bar, a number, an element that scrubs with
scroll), prefer the native **CSS Scroll-Driven Animations** where supported:

```css
@supports (animation-timeline: scroll()){
  .progress{transform-origin:left; animation:grow linear; animation-timeline:scroll(root block)}
  @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
}
```

Always provide a static fallback for browsers without `animation-timeline`.

---

## 6. Signature "Framer-feel" touches

- **Animated aurora/gradient background:** 2–3 large blurred radial-gradient
  blobs absolutely positioned, each on a slow (20–32s) `@keyframes` that
  translates/scales on `ease-in-out … alternate`. Plus a wide blurred "beam"
  with a linear-gradient that drifts. Keep blur heavy and opacity moderate so
  text stays crisp. (Typical hero treatment.) Freeze under reduced motion.
- **Marquee (logo strip):** a flex track `width:max-content`, content duplicated
  (in markup or cloned by JS), animated `translateX(0 → -50%)` linear infinite;
  `mask-image` linear-gradient to fade both edges; `animation-play-state:paused`
  on hover.
- **Count-up numbers:** on first in-view, animate `0 → target` with
  `requestAnimationFrame` over ~1.4s; keep prefix/suffix as separate spans.
- **Magnetic button** (pointer-follow, very Framer):
  ```js
  document.querySelectorAll('[data-magnetic]').forEach(btn=>{
    btn.addEventListener('pointermove',e=>{ const r=btn.getBoundingClientRect();
      btn.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.25}px,${(e.clientY-r.top-r.height/2)*.25}px)`; });
    btn.addEventListener('pointerleave',()=> btn.style.transform='');
  });
  ```
- **Nav that adapts on scroll:** toggle a `.scrolled` class past a threshold to
  swap background/colour with a `transition`. (Common in dark heroes.)

---

## 7. A real spring without React (optional, ~15 lines)

When you need velocity-aware, interruptible motion (drag inertia, a value that
springs to a new target), a tiny stiffness/damping integrator beats CSS:

```js
function spring(get,set,{stiffness=300,damping=26,mass=1}={}){
  let target=get(), v=0, raf=null, last=null;
  const step=(t)=>{ if(last==null) last=t; const dt=Math.min((t-last)/1000,1/30); last=t;
    const x=get(), f=-stiffness*(x-target)-damping*v; v+=(f/mass)*dt; set(x+v*dt);
    if(Math.abs(v)>0.01||Math.abs(get()-target)>0.01){ raf=requestAnimationFrame(step); } else { set(target); raf=null; last=null; } };
  return (to)=>{ target=to; if(!raf) raf=requestAnimationFrame(step); };
}
// usage: const toX = spring(()=>x, nx=>{x=nx; el.style.transform=`translateX(${x}px)`});  toX(120);
```

Presets mirror the main skill: gentle `100/20`, wobbly `200/10`, stiff `400/30`.

---

## 8. Mapping table (Framer Motion → vanilla)

| Framer Motion | Vanilla equivalent |
|---|---|
| `initial`/`animate` | start-state CSS class → `.in` class toggled by JS |
| `whileInView` + `viewport.once` | `IntersectionObserver` adds `.in`, then `unobserve` |
| `whileHover` | `:hover { transform … }` with spring cubic-bezier |
| `whileTap` | `:active { transform: scale(.97) }` |
| `transition spring` | `cubic-bezier(.34,1.56,.64,1)` (one-shot) or §7 JS spring |
| `staggerChildren` | per-child `transition-delay: calc(var(--i)*.07s)` |
| `AnimatePresence` exit | add `.leaving` class, listen `transitionend`, then remove node |
| `layout` | `View Transitions API` (`document.startViewTransition`) where supported |
| `useReducedMotion` | `@media (prefers-reduced-motion: reduce)` + `matchMedia` in JS |

**Bottom line:** you can get 90% of the Framer feel on a static single-file page
with cubic-bezier springs, one `IntersectionObserver`, index-based stagger, and
`transform`-only hovers. Reach for React + Framer Motion (the rest of this skill)
when the surface is already a React app or the interactions are genuinely
stateful (drag systems, shared-element route transitions, complex orchestration).
