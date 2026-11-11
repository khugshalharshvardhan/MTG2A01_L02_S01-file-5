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
    const sub=card.querySelector(".sg-sub");
    if(sub)sub.textContent="दो-दो, पाँच-पाँच और दस-दस की कूद";
    hero.classList.add("fc-hero");hero.innerHTML="";
    const pond=mtgEl("div","fc-pond");
    pond.style.backgroundImage='url("'+mtgImg("sc_pond_v2")+'")';
    const leaf=(x,w=100)=>{
      const im=mtgEl("img","fc-leaf");im.src="assets/Images/prop_lotus.svg";im.alt="";
      im.style.cssText="left:"+x+"px;width:"+w+"px";pond.appendChild(im);
    };
    leaf(125,120);leaf(755,130);[300,440,580].forEach(x=>leaf(x,78));
    const svg=document.createElementNS(MTG_SVG,"svg");
    svg.setAttribute("class","fc-trail");svg.setAttribute("viewBox","0 0 880 260");
    [125,300,440,580].forEach((x,i)=>mtgArc(svg,x,[300,440,580,755][i],177,60));
    pond.appendChild(svg);
    const frog=mtgEl("img","fc-frog");frog.src=mtgImg("chr_tappu");frog.alt="टप्पू";frog.style.left="125px";
    const friend=mtgEl("img","fc-friend");friend.src=mtgImg("chr_friend");friend.alt="टप्पू का दोस्त";
    pond.appendChild(frog);pond.appendChild(friend);hero.appendChild(pond);
    const btn=$("sgBtn");if(btn){btn.setAttribute("aria-label","शुरू करें");btn.textContent="शुरू करें  ▶";}
    if(matchMedia("(prefers-reduced-motion: reduce)").matches){ready();return;}
    frog.animate([{transform:"translate(-50%,0)"},{transform:"translate(-50%,-16px)"},{transform:"translate(-50%,0)"}],{duration:650,easing:"ease-in-out"}).onfinish=ready;
    setTimeout(ready,1200);
  }
  const start=Date.now();
  function wait(){if(document.body.classList.contains("loaded")||Date.now()-start>8000)build();else setTimeout(wait,100);}
  setTimeout(wait,0);
})();
