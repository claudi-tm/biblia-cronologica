// ---------- DIAGRAMAS (época 3 e partilhados) ----------
// Cada função devolve o HTML de um cartão. Cores só por tokens do tema.
const C2M = 0.45; // côvado ≈ 45 cm
const m = c => (c*C2M).toLocaleString("pt-PT",{maximumFractionDigits:1});
function cartao(titulo, legenda, corpo){ return `<div class="card vis"><h3>${titulo}</h3><div class="cap">${legenda}</div>${corpo}</div>`; }
function svgT(x,y,t,o={}){ return `<text class="${o.cls||"svg-t"}" x="${x}" y="${y}" text-anchor="${o.a||"start"}"${o.w?` font-weight="${o.w}"`:""}${o.fill?` style="fill:${o.fill}"`:""}>${t}</text>`; }
function num(x,y,n){ return `<circle cx="${x}" cy="${y}" r="7" fill="var(--fg)"/><text x="${x}" y="${y+3.5}" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--bg)" font-family="var(--f-ui)">${n}</text>`; }

const DG = {};

// 1. Planta do tabernáculo (Êx 26–27, 30). Escala: 3 px por côvado.
DG["planta-tabernaculo"] = () => {
  const X=20, Y=36, s=3;
  let g = `<rect x="${X}" y="${Y}" width="${100*s}" height="${50*s}" fill="var(--land)" stroke="var(--muted)" stroke-width="1.2"/>
  <line x1="${X+100*s}" y1="${Y+15*s}" x2="${X+100*s}" y2="${Y+35*s}" stroke="var(--at)" stroke-width="4"/>
  <rect x="${X+20*s}" y="${Y+20*s}" width="${30*s}" height="${10*s}" fill="var(--surface)" stroke="var(--fg)" stroke-width="1.2"/>
  <line x1="${X+30*s}" y1="${Y+20*s}" x2="${X+30*s}" y2="${Y+30*s}" stroke="var(--red)" stroke-width="2.5"/>
  <rect x="${X+25*s-6}" y="${Y+25*s-4}" width="12" height="8" fill="var(--at)"/>
  <rect x="${X+38*s-5}" y="${Y+21.5*s}" width="10" height="5" fill="var(--at)"/>
  <rect x="${X+38*s-2}" y="${Y+28.5*s-5}" width="4" height="5" fill="var(--at)"/>
  <rect x="${X+31.5*s}" y="${Y+25*s-3}" width="6" height="6" fill="var(--at)"/>
  <circle cx="${X+62*s}" cy="${Y+25*s}" r="5" fill="var(--sea)" stroke="var(--muted)"/>
  <rect x="${X+75*s-7.5}" y="${Y+25*s-7.5}" width="15" height="15" fill="var(--muted)"/>`;
  g += num(X+25*s, Y+20*s-10, 1) + num(X+42*s, Y+20*s-10, 2) + num(X+38*s, Y+30*s+10, 3) + num(X+31*s, Y+20*s-10, 4)
     + num(X+62*s, Y+25*s-14, 5) + num(X+75*s, Y+25*s-17, 6) + num(X+100*s-12, Y+25*s, 7);
  g += `<line x1="${X}" y1="${Y-12}" x2="${X+100*s}" y2="${Y-12}" stroke="var(--muted)" stroke-width="1"/>` + svgT(X+50*s,Y-16,`100 côvados ≈ ${m(100)} m`,{a:"middle",cls:"svg-m"});
  g += svgT(X+100*s, Y+50*s+14, "NASCENTE →", {a:"end",cls:"svg-m"}) + svgT(X, Y+50*s+14, "↑ NORTE", {cls:"svg-m"});
  g += svgT(X+30*s-3, Y+30*s+28, "SANTÍSSIMO", {a:"end",cls:"svg-m"}) + svgT(X+30*s+3, Y+30*s+28, "LUGAR SANTO", {cls:"svg-m"});
  const leg = [["Arca da aliança, no Santíssimo","25:10"],["Mesa do pão da proposição, a norte","26:35"],["Candelabro, a sul","26:35"],["Altar do incenso, junto ao véu (linha vermelha)","30:1–6"],["Pia de bronze, para os sacerdotes se lavarem","30:18"],["Altar do holocausto, 5 × 5 côvados","27:1"],["Entrada, 20 côvados ≈ 9 m","27:16"]];
  return cartao("Planta do tabernáculo", `Vista de cima, à escala. O átrio mede 100 × 50 côvados (cerca de ${m(100)} × ${m(50)} m). A posição exata da tenda dentro do átrio é uma reconstrução comum; o texto não a dá.`,
    `<div class="scroll"><svg viewBox="0 0 340 222" role="img" aria-label="Planta do tabernáculo vista de cima">${g}</svg></div>
     <ol class="leg">${leg.map(([t,r])=>`<li>${t} <span>Êxodo ${r}</span></li>`).join("")}</ol>`);
};

// 2. Vestes do sumo sacerdote (Êx 28)
DG["vestes-sumo-sacerdote"] = () => {
  let g = `<path d="M90 64 L150 64 L162 288 L78 288 Z" fill="var(--blue)"/>
  <rect x="82" y="286" width="76" height="20" fill="var(--surface)" stroke="var(--line)"/>
  <path d="M90 66 L70 160 L80 162 L96 90 Z M150 66 L170 160 L160 162 L144 90 Z" fill="var(--blue)"/>
  <circle cx="120" cy="42" r="15" fill="var(--line)"/>
  <rect x="103" y="16" width="34" height="20" rx="7" fill="var(--surface)" stroke="var(--muted)"/>
  <rect x="109" y="27" width="22" height="6" fill="var(--at)"/>
  <rect x="94" y="64" width="52" height="88" rx="3" fill="var(--at-soft)" stroke="var(--at)" stroke-width="1.5"/>
  <circle cx="99" cy="69" r="5" fill="var(--fg)"/><circle cx="141" cy="69" r="5" fill="var(--fg)"/>
  <rect x="94" y="148" width="52" height="8" fill="var(--at)"/>
  <rect x="104" y="80" width="32" height="40" fill="var(--surface)" stroke="var(--at)" stroke-width="1.5"/>`;
  const cores=["var(--red)","var(--nt)","var(--at)","var(--blue)"];
  for(let r=0;r<4;r++) for(let c=0;c<3;c++) g+=`<rect x="${108+c*9}" y="${84+r*9}" width="6" height="6" rx="1" fill="${cores[(r+c)%4]}"/>`;
  for(let i=0;i<8;i++){ const x=84+i*10; g+= i%2 ? `<circle cx="${x}" cy="284" r="3.2" fill="var(--at)"/>` : `<circle cx="${x}" cy="284" r="3.6" fill="var(--red)"/>`; }
  const L=[["Mitra e placa de ouro","28:36–39",131,30,30],["Ónix nos ombros","28:9–12",146,69,64],["Peitoral, 12 pedras","28:15–21",136,96,100],["Urim e Tumim","28:30",136,112,136],["Éfode","28:6–7",146,138,172],["Cinto do éfode","28:8",146,152,204],["Manto azul","28:31",156,230,240],["Romãs e campainhas","28:33–35",158,284,274],["Túnica de linho","28:39",158,300,306]];
  L.forEach(([t,r,x,y,ly])=>{ g+=`<polyline points="${x},${y} 196,${ly-4} 202,${ly-4}" fill="none" stroke="var(--muted)" stroke-width=".8"/>`+svgT(205,ly-1,t)+svgT(205,ly+10,"Êxodo "+r,{cls:"svg-m"}); });
  return cartao("Vestes do sumo sacerdote", "Representação simplificada. Os nomes das 12 tribos iam nos ombros e sobre o coração. Por baixo de tudo, calções de linho (28:42).",
    `<svg viewBox="0 0 340 318" role="img" aria-label="Vestes do sumo sacerdote com as partes identificadas">${g}</svg>`);
};

// 3. Conversor de medidas
const UNID = {
  comp:[["côvado",0.45,"m"],["côvado longo",0.52,"m"],["palmo (meio côvado)",0.225,"m"],["palmo menor",0.075,"m"],["dedo",0.019,"m"]],
  peso:[["gera",0.57,"g"],["beca (meio siclo)",5.7,"g"],["siclo",11.4,"g"],["mina (50 siclos)",0.57,"kg"],["talento (3000 siclos)",34,"kg"]],
  vol:[["ômer",2.2,"L"],["efa (10 ômeres)",22,"L"],["hómer (10 efas)",220,"L"],["him (líquidos)",3.7,"L"],["bato (líquidos)",22,"L"]]
};
function converter(el){
  const box=el.closest(".conv"); const q=parseFloat(box.querySelector("[data-q]").value.replace(",","."))||0;
  const [k,i]=box.querySelector("[data-u]").value.split(":"); const [n,f,u]=UNID[k][+i];
  box.querySelector("[data-out]").textContent = `${q.toLocaleString("pt-PT")} ${n} ≈ ${(q*f).toLocaleString("pt-PT",{maximumFractionDigits:2})} ${u}`;
}
DG["conversor-medidas"] = () => {
  const opts = Object.entries({comp:"Comprimento",peso:"Peso",vol:"Volume"}).map(([k,l])=>`<optgroup label="${l}">${UNID[k].map(([n],i)=>`<option value="${k}:${i}">${n}</option>`).join("")}</optgroup>`).join("");
  const ex = [["Arca da aliança",2.5],["Tenda do tabernáculo",30],["Átrio",100],["Arca de Noé",300]];
  const tab = k => UNID[k].map(([n,f,u])=>`<tr><td>${n}</td><td class="num">≈ ${f.toLocaleString("pt-PT")} ${u}</td></tr>`).join("");
  return cartao("Medidas da Bíblia", "Valores aproximados. Os estudiosos propõem números um pouco diferentes, sobretudo para os volumes.",
    `<div class="conv">
      <div class="conv-row"><input type="text" inputmode="decimal" data-q value="2,5" aria-label="Quantidade">
      <select data-u aria-label="Unidade">${opts}</select></div>
      <div class="conv-out" data-out>2,5 côvado ≈ 1,13 m</div>
      <div class="conv-ex">${ex.map(([t,v])=>`<button type="button" data-conv-ex="${v}">${t}: ${String(v).replace(".",",")} côvados</button>`).join("")}</div>
      <div class="conv-tabs"><table><caption>Comprimento</caption>${tab("comp")}</table><table><caption>Peso</caption>${tab("peso")}</table><table><caption>Volume</caption>${tab("vol")}</table></div>
    </div>`);
};

// 4. Arca da aliança (Êx 25:10–22), vista de lado. 70 px por côvado.
DG["arca-da-alianca"] = () => {
  const s=70, X=82, Y=118, W=2.5*s, H=1.5*s;
  let g = `<rect x="${X}" y="${Y}" width="${W}" height="${H}" fill="var(--at)" rx="2"/>
  <line x1="${X}" y1="${Y+8}" x2="${X+W}" y2="${Y+8}" stroke="var(--at-soft)" stroke-width="2"/>
  <rect x="${X-2}" y="${Y-7}" width="${W+4}" height="7" fill="var(--at)" stroke="var(--at-soft)" stroke-width=".8"/>
  <line x1="${X-40}" y1="${Y+H-22}" x2="${X+W+40}" y2="${Y+H-22}" stroke="var(--muted)" stroke-width="5" stroke-linecap="round"/>
  <circle cx="${X+14}" cy="${Y+H-22}" r="5" fill="none" stroke="var(--at-soft)" stroke-width="2"/><circle cx="${X+W-14}" cy="${Y+H-22}" r="5" fill="none" stroke="var(--at-soft)" stroke-width="2"/>`;
  [[X+22,1],[X+W-22,-1]].forEach(([cx,d])=>{
    g += `<path d="M${cx-9} ${Y-7} L${cx-7} ${Y-40} Q${cx} ${Y-48} ${cx+7} ${Y-40} L${cx+9} ${Y-7} Z" fill="var(--at)"/>
    <circle cx="${cx+2*d}" cy="${Y-50}" r="7" fill="var(--at)"/>
    <path d="M${cx} ${Y-38} Q${cx+d*30} ${Y-90} ${X+W/2} ${Y-62}" fill="none" stroke="var(--at)" stroke-width="5" stroke-linecap="round"/>`;
  });
  g += `<line x1="${X}" y1="${Y+H+16}" x2="${X+W}" y2="${Y+H+16}" stroke="var(--muted)"/>` + svgT(X+W/2,Y+H+30,`2,5 côvados ≈ ${m(2.5)} m`,{a:"middle",cls:"svg-m"});
  g += `<line x1="${X+W+16}" y1="${Y}" x2="${X+W+16}" y2="${Y+H}" stroke="var(--muted)"/>` + svgT(X+W+22,Y+H/2+4,`1,5 côv.`,{cls:"svg-m"}) + svgT(X+W+22,Y+H/2+16,`≈ ${m(1.5)} m`,{cls:"svg-m"});
  g += svgT(X+W/2,14,"querubins com as asas estendidas",{a:"middle",cls:"svg-m"}) + svgT(X-6,Y-1,"coberta",{a:"end",cls:"svg-m"}) + svgT(X+W/2,Y+H/2-6,"acácia coberta de ouro",{a:"middle",cls:"svg-m",fill:"var(--on-accent)"});
  g += svgT(X-38,Y+H-30,"vara",{cls:"svg-m"});
  return cartao("Arca da aliança", "Vista de lado. As varas passavam por quatro argolas e nunca se tiravam (25:15).",
    `<svg viewBox="0 0 340 270" role="img" aria-label="Arca da aliança vista de lado, com medidas">${g}</svg>
     <ul class="leg plain"><li><b>Dentro:</b> as tábuas da Lei (25:16). Mais tarde, junto delas, um vaso com maná e a vara de Arão (Êxodo 16:33–34; Números 17:10).</li><li><b>Por cima:</b> a coberta de ouro, onde se aspergia o sangue no Dia da Expiação (Levítico 16:14).</li></ul>`);
};

// 5. Rota do Êxodo
DG["rota-exodo"] = () => VIS["rota-exodo"]();

// 6. Tabela dos sacrifícios (Lv 1–7)
DG["tabela-sacrificios"] = () => {
  const L=[["Holocausto","1","Macho sem defeito: boi, carneiro, bode ou aves","Tudo","Ninguém (a pele ia para o sacerdote)","Entrega total a Deus"],
    ["Oferta de grãos","2","Flor de farinha, azeite e incenso, sem fermento","Um punhado","Os sacerdotes","Gratidão e reconhecimento"],
    ["Sacrifício pacífico","3; 7:11–34","Boi, ovelha ou cabra, macho ou fêmea","A gordura","Sacerdote (peito e coxa) e a família de quem oferecia","Comunhão, agradecimento, votos"],
    ["Expiação (pelo pecado)","4:1–5:13","Depende de quem pecou: bezerro, bode, cabra, rolinhas ou farinha","A gordura","Os sacerdotes, em geral","Purificar pecados cometidos sem intenção"],
    ["Oferta pela culpa","5:14–6:7","Carneiro, mais a devolução do dano e um quinto","A gordura","Os sacerdotes","Reparar um dano a Deus ou ao próximo"]];
  return cartao("Os cinco tipos de oferta","Levítico 1 a 7, com os nomes usados nesta tradução.",
    `<div class="scroll"><table class="dtab"><thead><tr><th>Oferta</th><th>O que se oferecia</th><th>Queimado</th><th>Quem comia</th><th>Para quê</th></tr></thead><tbody>
    ${L.map(r=>`<tr><td><b>${r[0]}</b><span class="ref-s">Levítico ${r[1]}</span></td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td><td>${r[5]}</td></tr>`).join("")}</tbody></table></div>`);
};

// 7. Calendário das festas (Lv 23)
DG["calendario-festas"] = () => {
  const cx=170, cy=150, R=92;
  const meses=["Nisã","Iyar","Sivã","Tamuz","Ab","Elul","Tisri","Hesvã","Quisleu","Tebete","Sebate","Adar"];
  const ang=(mm,d)=>(-90+((mm-1)+(d-1)/30)/12*360)*Math.PI/180;
  const P=(mm,d,r)=>[cx+r*Math.cos(ang(mm,d)), cy+r*Math.sin(ang(mm,d))];
  let g=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="var(--line)" stroke-width="18"/>`;
  meses.forEach((n,i)=>{ const [x1,y1]=P(i+1,1,R-9),[x2,y2]=P(i+1,1,R+9); g+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="var(--bg)" stroke-width="2"/>`;
    const [tx,ty]=P(i+1,16,R-26); g+=svgT(tx,ty+3,`${i+1}`,{a:"middle",cls:"svg-m"}); });
  const arco=(m1,d1,m2,d2,cor)=>{ const [x1,y1]=P(m1,d1,R),[x2,y2]=P(m2,d2,R); return `<path d="M${x1} ${y1} A${R} ${R} 0 0 1 ${x2} ${y2}" fill="none" stroke="${cor}" stroke-width="18"/>`; };
  g+=arco(1,14,1,22,"var(--at)")+arco(3,5,3,8,"var(--nt)")+arco(7,1,7,23,"var(--red)");
  const lab=(mm,d,t1,t2,a,dx)=>{ const [x,y]=P(mm,d,R+12),[lx,ly]=P(mm,d,R+30); return `<line x1="${x}" y1="${y}" x2="${lx+dx}" y2="${ly}" stroke="var(--muted)" stroke-width=".8"/>`+svgT(lx+dx+(a==="start"?3:-3),ly-2,t1,{a,w:600})+svgT(lx+dx+(a==="start"?3:-3),ly+10,t2,{a,cls:"svg-m"}); };
  g+=lab(1,18,"Páscoa · Ázimos","mês 1","start",6)+lab(3,6,"Semanas","mês 3","start",0)+lab(7,12,"Trombetas · Expiação · Cabanas","mês 7","middle",0);
  g+=svgT(cx,cy-4,"ano religioso",{a:"middle",cls:"svg-m"})+svgT(cx,cy+10,"começa na primavera",{a:"middle",cls:"svg-m"});
  const L=[["Páscoa","mês 1, dia 14","23:5","Libertação do Egito"],["Pães Ázimos","mês 1, dias 15–21","23:6","Saída apressada, sem tempo para levedar"],["Primícias","no dia a seguir ao sábado","23:10–11","Primeira colheita oferecida a Deus"],["Semanas","50 dias depois","23:15–16","Fim da colheita do trigo"],["Trombetas","mês 7, dia 1","23:24","Toque de trombetas, início do outono"],["Dia das Expiações","mês 7, dia 10","23:27","Purificação do povo e do santuário"],["Cabanas","mês 7, dias 15–21","23:34","Vida em cabanas no deserto; fim das colheitas"]];
  return cartao("Calendário das festas", "Os meses começavam com a lua nova, por isso as datas variam no nosso calendário.",
    `<svg viewBox="0 0 340 300" role="img" aria-label="Ano religioso de Israel com as festas">${g}</svg>
    <div class="scroll"><table class="dtab"><thead><tr><th>Festa</th><th>Quando</th><th>O que lembrava</th></tr></thead><tbody>
    ${L.map(r=>`<tr><td><b>${r[0]}</b><span class="ref-s">Levítico ${r[2]}</span></td><td>${r[1]}</td><td>${r[3]}</td></tr>`).join("")}</tbody></table></div>`);
};

// Mapa-base de Canaã (esquemático)
function baseCanaa(){
  return `<rect x="0" y="0" width="300" height="380" fill="var(--land)"/>
  <path d="M0 0 H96 L88 40 L80 82 L72 130 L62 180 L50 230 L38 280 L25 330 L14 380 H0 Z" fill="var(--sea)"/>
  <path d="M186 26 Q190 60 189 92" fill="none" stroke="var(--sea)" stroke-width="2.5"/>
  <ellipse cx="190" cy="105" rx="8" ry="13" fill="var(--sea)"/>
  <path d="M190 118 Q196 140 189 165 Q184 190 192 215 Q197 235 194 250" fill="none" stroke="var(--sea)" stroke-width="3"/>
  <ellipse cx="196" cy="285" rx="10" ry="35" fill="var(--sea)"/>
  <text class="svg-m" x="12" y="150" transform="rotate(-78 12 150)">MAR MEDITERRÂNEO</text>
  <text class="svg-m" x="204" y="126">MAR DA GALILEIA</text><text class="svg-m" x="210" y="292">MAR MORTO</text>
  <text class="svg-m" x="200" y="200" transform="rotate(80 200 200)">JORDÃO</text>`;
}
const pin=(x,y,n,o={})=>`<circle cx="${x}" cy="${y}" r="${o.r||4}" fill="${o.c||"var(--fg)"}" stroke="var(--surface)" stroke-width="1.5"/>`+svgT(x+(o.a==="end"?-7:7),y+4,n,{a:o.a||"start",w:o.w});

// 8. Tribos em Canaã (Josué 13–19)
DG["mapa-tribos-canaa"] = () => {
  const T=[["Dã (depois)",180,22,"a"],["Aser",110,62,"a"],["Naftali",158,70,"a"],["Zebulom",140,104,"a"],["Issacar",158,136,"a"],["Manassés",118,168,"a"],["Efraim",118,205,"a"],["Benjamim",150,234,"a"],["Dã",70,222,"a"],["Judá",120,288,"a"],["Simeão",80,340,"a"],["Manassés",240,76,"b"],["Gade",238,172,"b"],["Rúben",238,262,"b"]];
  let g=baseCanaa();
  T.forEach(([n,x,y,l])=>{ const w=n.length*5.6+14; g+=`<rect x="${x-w/2}" y="${y-10}" width="${w}" height="16" rx="8" fill="${l==="a"?"var(--at-soft)":"var(--nt-soft)"}"/>`+svgT(x,y+2,n,{a:"middle",w:600}); });
  g+=pin(160,252,"Jerusalém",{r:3,c:"var(--muted)",a:"end"});
  return cartao("As tribos em Canaã", "Esquema aproximado, sem fronteiras exatas. Rúben, Gade e metade de Manassés ficaram a leste do Jordão (Números 32). Levi não recebeu território, só cidades. Dã começou junto à costa e mais tarde mudou-se para norte (Juízes 18).",
    `<div class="scroll"><svg viewBox="0 0 300 380" role="img" aria-label="Mapa esquemático das tribos de Israel em Canaã" style="max-width:420px;margin:auto">${g}</svg></div>`);
};

// 9. Acampamento das tribos (Números 2–3)
DG["acampamento-tribos"] = () => {
  const box=(x,y,w,h,titulo,linhas,cor)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="${cor}"/>`+svgT(x+w/2,y+14,titulo,{a:"middle",cls:"svg-m"})+linhas.map((l,i)=>svgT(x+w/2,y+30+i*14,l,{a:"middle"})).join("");
  let g = `<rect x="150" y="158" width="40" height="24" fill="var(--surface)" stroke="var(--fg)"/>`+svgT(170,198,"tabernáculo",{a:"middle",cls:"svg-m"})
   +`<rect x="80" y="112" width="180" height="116" rx="12" fill="none" stroke="var(--line)" stroke-dasharray="4 3"/>`
   +svgT(170,128,"Meraritas",{a:"middle"})+svgT(170,218,"Coatitas",{a:"middle"})+svgT(110,174,"Gersonitas",{a:"middle"})+svgT(228,166,"Moisés, Arão",{a:"middle",cls:"svg-m"})+svgT(228,178,"e sacerdotes",{a:"middle",cls:"svg-m"});
  g += box(267,108,70,124,"NASCENTE",["Judá","Issacar","Zebulom","186 400"],"var(--at-soft)")
     + box(3,108,70,124,"POENTE",["Efraim","Manassés","Benjamim","108 100"],"var(--at-soft)")
     + box(100,18,140,80,"NORTE",["Dã · Aser · Naftali","157 600"],"var(--at-soft)")
     + box(100,242,140,80,"SUL",["Rúben · Simeão · Gade","151 450"],"var(--at-soft)");
  g += ``;
  return cartao("O acampamento à volta do tabernáculo", "Números 2 e 3. Os números são os homens contados em cada grupo, num total de 603 550 (Números 2:32). A entrada do tabernáculo ficava a nascente, do lado de Judá.",
    `<svg viewBox="0 0 340 330" role="img" aria-label="Disposição das tribos e dos levitas à volta do tabernáculo">${g}</svg>`);
};

// 10. Candelabro (Êx 25:31–40)
DG["candelabro"] = () => {
  const cx=170, top=70;
  let g=`<line x1="${cx}" y1="${top}" x2="${cx}" y2="230" stroke="var(--at)" stroke-width="7" stroke-linecap="round"/>`;
  [30,60,90].forEach(r=>{ g+=`<path d="M${cx-r} ${top} A${r} ${r} 0 0 0 ${cx+r} ${top}" fill="none" stroke="var(--at)" stroke-width="6"/>`; });
  [-90,-60,-30,0,30,60,90].forEach(dx=>{ g+=`<rect x="${cx+dx-7}" y="${top-8}" width="14" height="8" rx="3" fill="var(--at)"/><path d="M${cx+dx} ${top-26} Q${cx+dx+5} ${top-16} ${cx+dx} ${top-10} Q${cx+dx-5} ${top-16} ${cx+dx} ${top-26} Z" fill="var(--red)"/>`; });
  g+=`<path d="M${cx-40} 250 L${cx-20} 230 L${cx+20} 230 L${cx+40} 250 Z" fill="var(--at)"/>`;
  g+=svgT(cx,top-34,"7 lâmpadas de azeite (25:37)",{a:"middle",cls:"svg-m"})+svgT(cx,272,"um talento de ouro ≈ 34 kg (25:39)",{a:"middle",cls:"svg-m"});
  return cartao("O candelabro de ouro", "Um tronco central e seis braços, três de cada lado, feitos de uma só peça de ouro batido, com copos em forma de flor de amendoeira (25:33). A Bíblia não dá a altura nem diz se os braços eram curvos ou retos; esta forma segue representações antigas.",
    `<svg viewBox="0 0 340 285" role="img" aria-label="Candelabro de sete lâmpadas">${g}</svg>`);
};

// 11. Animais puros e impuros (Lv 11)
DG["tabela-animais"] = () => {
  const L=[["Da terra","Unha fendida e ruminar (11:3)","boi, ovelha, cabra, veado","camelo, coelho, lebre (11:4–6), porco (11:7)"],
    ["Das águas","Barbatanas e escamas (11:9)","a maioria dos peixes","os que não têm escamas ou barbatanas, como enguias e mariscos"],
    ["Das aves","Lista de proibidas (11:13–19)","as que não estão na lista (pombas, rolinhas)","aves de rapina, abutres, corvos, avestruz, corujas, garças, morcego"],
    ["Insetos com asas","Pernas para saltar (11:21)","gafanhotos e grilos (11:22)","todos os outros"]];
  return cartao("Animais puros e impuros","Levítico 11 e Deuteronómio 14. A razão dada no texto é a santidade de Israel (11:44–45).",
    `<div class="scroll"><table class="dtab"><thead><tr><th>Grupo</th><th>Regra</th><th>Puros (exemplos)</th><th>Impuros (exemplos)</th></tr></thead><tbody>
    ${L.map(r=>`<tr><td><b>${r[0]}</b></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join("")}</tbody></table></div>`);
};

// 12. As dez pragas (Êx 7–12)
DG["tabela-dez-pragas"] = () => {
  const L=[["Água em sangue","7:14–25","Hápi, deus do Nilo",""],["Rãs","8:1–15","Heket, deusa com cabeça de rã",""],["Piolhos","8:16–19","Geb, deus da terra (o pó)",""],["Moscas","8:20–32","—","Gósen poupada (8:22)"],["Peste no gado","9:1–7","Ápis e Hator, touro e vaca sagrados","Gado de Israel poupado (9:4)"],["Sarna com úlceras","9:8–12","Sekhmet, deusa das doenças",""],["Granizo","9:13–35","Nut, deusa do céu","Gósen poupada (9:26)"],["Gafanhotos","10:1–20","deuses das colheitas",""],["Trevas","10:21–29","Rá, deus do sol","Luz nas casas de Israel (10:23)"],["Morte dos primogénitos","11:1–12:30","o próprio faraó, visto como deus","Casas com sangue poupadas"]];
  return cartao("As dez pragas", "Êxodo 12:12 diz que Deus faria juízos \"em todos os deuses do Egito\". As ligações a deuses concretos são propostas de estudiosos, não estão no texto.",
    `<div class="scroll"><table class="dtab"><thead><tr><th>#</th><th>Praga</th><th>Possível alvo</th><th>Israel</th></tr></thead><tbody>
    ${L.map((r,i)=>`<tr><td class="num">${i+1}</td><td><b>${r[0]}</b><span class="ref-s">Êxodo ${r[1]}</span></td><td>${r[2]}</td><td>${r[3]||"—"}</td></tr>`).join("")}</tbody></table></div>`);
};

// 13. Cidades de refúgio (Números 35, Josué 20)
DG["mapa-cidades-refugio"] = () => {
  let g=baseCanaa();
  [["Quedes",176,58,"start"],["Siquém",146,186,"end"],["Hebrom",140,290,"end"],["Golã",226,96,"start"],["Ramote-Gileade",238,162,"end"],["Bezer",234,252,"start"]].forEach(([n,x,y,a])=>{ g+=pin(x,y,n,{c:"var(--red)",r:5,a,w:600}); });
  g+=pin(160,252,"Jerusalém",{r:3,c:"var(--muted)",a:"end"});
  return cartao("As seis cidades de refúgio", "Três de cada lado do Jordão, espalhadas de norte a sul, para que nenhuma ficasse longe demais (Deuteronómio 19:2–3). Posições aproximadas.",
    `<div class="scroll"><svg viewBox="0 0 300 380" role="img" aria-label="Mapa das seis cidades de refúgio" style="max-width:420px;margin:auto">${g}</svg></div>`);
};

// 14. Delta do Egito (Êx 1:11; 12:37)
DG["mapa-egito-delta"] = () => {
  let g=`<rect x="0" y="0" width="340" height="260" fill="var(--land)"/>
  <path d="M0 0 H340 V30 Q300 40 260 36 Q220 46 170 44 Q120 50 80 42 Q40 48 0 40 Z" fill="var(--sea)"/>
  <path d="M150 260 L150 170 Q148 150 140 140 Q110 100 70 44 M150 170 Q170 120 200 46 M150 170 Q152 120 140 46" fill="none" stroke="var(--sea)" stroke-width="3"/>
  <path d="M250 150 Q270 170 280 200 L300 260 L340 260 L340 200 Q300 180 290 150 Z" fill="var(--sea)"/>
  <ellipse cx="262" cy="140" rx="12" ry="7" fill="var(--sea)"/>
  <path d="M185 70 Q220 75 245 115 Q235 140 205 135 Q180 120 178 95 Z" fill="var(--at-soft)" stroke="var(--at)" stroke-dasharray="3 3"/>`;
  g+=svgT(212,102,"GÓSEN",{a:"middle",cls:"svg-m"})+svgT(110,22,"MAR MEDITERRÂNEO",{cls:"svg-m"})+svgT(30,150,"EGITO",{cls:"svg-m"})+svgT(296,236,"Golfo",{a:"middle",cls:"svg-m"})+svgT(296,248,"de Suez",{a:"middle",cls:"svg-m"})+svgT(262,162,"Lagos Amargos",{a:"middle",cls:"svg-m"});
  g+=pin(205,82,"Ramessés",{c:"var(--red)"})+pin(220,124,"Pitom",{c:"var(--red)",a:"end"})+pin(240,124,"Sucote")+pin(150,190,"Om (Heliópolis)",{a:"end"})+pin(150,232,"Mênfis",{a:"end"})+svgT(158,252,"Nilo ↑",{cls:"svg-m"});
  return cartao("O delta do Nilo", "Esquema da região onde Israel viveu. Ramessés e Pitom são as cidades-armazém de Êxodo 1:11. A identificação exata dos lugares é debatida.",
    `<div class="scroll"><svg viewBox="0 0 340 260" role="img" aria-label="Mapa esquemático do delta do Nilo com Gósen, Ramessés e Pitom">${g}</svg></div>`);
};

const NOMES_DG = {"planta-tabernaculo":"Planta do tabernáculo","vestes-sumo-sacerdote":"Vestes do sumo sacerdote","conversor-medidas":"Medidas da Bíblia","arca-da-alianca":"Arca da aliança","rota-exodo":"Rota do Êxodo","tabela-sacrificios":"Os cinco tipos de oferta","calendario-festas":"Calendário das festas","mapa-tribos-canaa":"As tribos em Canaã","acampamento-tribos":"O acampamento","candelabro":"O candelabro","tabela-animais":"Animais puros e impuros","tabela-dez-pragas":"As dez pragas","mapa-cidades-refugio":"Cidades de refúgio","mapa-egito-delta":"O delta do Nilo"};
const DG_EPOCA = {3:["rota-exodo","mapa-egito-delta","tabela-dez-pragas","planta-tabernaculo","arca-da-alianca","candelabro","vestes-sumo-sacerdote","tabela-sacrificios","tabela-animais","calendario-festas","acampamento-tribos","mapa-cidades-refugio","conversor-medidas"],4:["mapa-tribos-canaa"]};
