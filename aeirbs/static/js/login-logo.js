const logo = document.querySelector('.AEIRBS');
const fire_ring = logo.querySelector('.fire_ring');
const quake_ring = logo.querySelector('.quake_ring');
const water_ring = logo.querySelector('.water_ring');

const rings = [fire_ring, quake_ring, water_ring]

const tlm = new TimelineMax({});
tl = new TimelineMax({repeat:6, repeatDelay:0.5});

//TweenMax.method(element, duration, vars)
/*tlm
    .to(fire_ring, 1, {transformOrigin: "center center", scale: 1.5})
    .to(fire_ring, 1, {scale: 1});*/

//tlm.staggerTo(rings, 1, {transformOrigin: "center center", scale: 1.5, repeat: 1}, 0.25)

tl.fromTo(fire_ring, 1, 
    {transformOrigin:"center center", autoAlpha:1, scale: 1}, 
    {transformOrigin:"center center", autoAlpha:0, scale: 50, opacity: 30, ease:Quad.easeInOut}
   )
.fromTo(quake_ring, 1, 
    {transformOrigin:"center center", autoAlpha:1, scale: 1, opacity: 0}, 
    {transformOrigin:"center center", autoAlpha:0, scale: 50, ease:Quad.easeInOut}, 1
   )
.fromTo(water_ring, 1, 
    {transformOrigin:"center center", autoAlpha:1, scale: 1, opacity: 0}, 
    {transformOrigin:"center center", autoAlpha:0, scale: 50, ease:Quad.easeInOut}, 2
   );