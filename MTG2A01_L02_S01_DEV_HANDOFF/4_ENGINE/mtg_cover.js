/* Pond adventure: resting leaves, counting trail, existing start and audio gates. */
(function frogCover(){
  if(!CARD.landing_hero||CARD.landing_hero.kind!=="frog_cover")return;
  window.__ltReady=false;window.__ltWaiters=[];
  const ready=()=>{
    if(window.__ltReady)return;window.__ltReady=true;
    window.__ltWaiters.splice(0).forEach(fn=>{try{fn();}catch(e){}});
  };
  window.landingTrainReady=fn=>window.__ltReady?fn():window.__ltWaiters.push(fn);
  function build(){
    const card=document.querySelector("#startGate .sg-card"),title=$("sgTitle"),hero=$("sgHero");
    if(!card||!title||!hero){ready();return;}
    card.classList.add("fc-card");title.classList.add("fc-title");
    title.setAttribute("aria-label",CARD.title.hi);title.replaceChildren();
    title.appendChild(mtgEl("span","fc-title-line",CARD.title.hi));
    const sub=card.querySelector(".sg-sub");
    if(sub)sub.remove();
    hero.classList.add("fc-hero");hero.innerHTML="";
    const pond=mtgEl("div","fc-pond");
    pond.style.backgroundImage='url("'+mtgImg("sc_pond_v4")+'")';
    const W=card.clientWidth,H=card.clientHeight,feet=Math.round(H*.63);
    const leaf=(x,w=100)=>{
      const im=mtgEl("img","fc-leaf");im.src="assets/Images/prop_lotus.svg";im.alt="";
      im.style.cssText="left:"+x+"px;top:"+(feet-14)+"px;width:"+w+"px";pond.appendChild(im);
    };
    const positions=[W*.16,W*.34,W*.5,W*.66,W*.84];
    leaf(positions[0],190);leaf(positions[4],190);positions.slice(1,4).forEach(x=>leaf(x,96));
    const svg=document.createElementNS(MTG_SVG,"svg");
    svg.setAttribute("class","fc-trail");svg.setAttribute("viewBox","0 0 "+W+" "+H);
    positions.slice(0,4).forEach((x,i)=>mtgArc(svg,x,positions[i+1],feet,52).style.setProperty("--trail-delay",(.4+i*.22)+"s"));
    pond.appendChild(svg);
    const frog=mtgEl("img","fc-frog");frog.src=mtgImg("lesson_frog");frog.alt="टप्पू";frog.style.left=positions[0]+"px";frog.style.top=(feet-110)+"px";
    const friend=mtgEl("img","fc-friend");friend.src=mtgImg("lesson_friend_gold");friend.alt="टप्पू का दोस्त";friend.style.left=positions[4]+"px";friend.style.top=(feet-110)+"px";
    pond.appendChild(frog);pond.appendChild(friend);hero.appendChild(pond);
    [positions[0],positions[4]].forEach((x,i)=>{const splash=mtgEl("i","fc-cover-splash"+(i?" friend":""));splash.style.left=x+"px";splash.style.top=(feet+8)+"px";splash.setAttribute("aria-hidden","true");pond.appendChild(splash);});
    [positions[0],positions[4]].forEach(x=>{
      [false,true].forEach(late=>{const ring=mtgEl("i","fc-water-ring"+(late?" late":""));ring.style.left=x+"px";ring.style.top=(feet+22)+"px";pond.appendChild(ring);});
    });
    for(let i=0;i<5;i++){const mote=mtgEl("i","fc-mote");mote.style.cssText="left:"+(W*(.25+i*.12))+"px;top:"+(feet+25+(i%2)*30)+"px;--mote-delay:"+(-i*.9)+"s";mote.setAttribute("aria-hidden","true");pond.appendChild(mote);}
    const btn=$("sgBtn");if(btn){
      btn.setAttribute("aria-label","शुरू करें");btn.innerHTML='<img class="fc-play-ready" src="assets/Images/btn-play-round.svg" alt="" draggable="false"><img class="fc-play-waiting" src="assets/Images/btn-play-round-waiting.svg" alt="" draggable="false">';
      let wasReady=false;
      new MutationObserver(()=>{
        const isReady=!btn.disabled&&!btn.classList.contains("sg-waiting");
        if(isReady&&!wasReady){btn.classList.add("fc-play-pop");setTimeout(()=>btn.classList.remove("fc-play-pop"),900);}
        wasReady=isReady;
      }).observe(btn,{attributes:true,attributeFilter:["class","disabled"]});
    }
    // The ready signal follows the actual sprites, so a fast tap cannot outrun the pads.
    const font=document.fonts.load('64px "Yatra One"').catch(()=>{});
    Promise.all([font,...pond.querySelectorAll("img")].map(im=>im instanceof HTMLImageElement?im.decode().catch(()=>{}):im)).then(()=>{
      card.classList.add("fc-ready");setTimeout(ready,matchMedia("(prefers-reduced-motion: reduce)").matches?0:1000);
    });
    setTimeout(()=>{card.classList.add("fc-ready");ready();},6000);
  }
  const start=Date.now();
  function wait(){if(document.body.classList.contains("loaded")||Date.now()-start>8000)build();else setTimeout(wait,100);}
  setTimeout(wait,0);
})();
