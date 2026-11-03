# Modelet matematikore

Për problemet e realizueshmërisë, objektivi është të ulet numri i shkeljeve në zero.
Algoritmet këtu gjenerojnë vetëm gjendje të lejueshme dhe testi i qëllimit kërkon plotësim të plotë.
Funksioni i vlerësimit përshkruan progresin ose shkeljet; nuk përdoret si heuristikë A*.
MRV dhe renditja e kandidatëve janë përmirësime të renditjes; algoritmi i përshkimit mbetet ai i kërkuar.

## Social Golfers

1. **Përkufizimi:** n = gp lojtarë, g grupe me p lojtarë në javë, për w javë.
   Çdo çift mund të takohet më së shumti një herë.
2. **Gjendja:** tuple grupesh të plota, të renditura sipas javës. Brenda javës që po ndërtohet
   ruhen grupet e përfunduara; pjesa e mbetur llogaritet nga lojtarët e papërdorur.
3. **Zgjidhja:** wg grupe, të ndara në w javë. Shfaqja me ID nga 1 është vetëm transformim vizual.
4. **Variablat:** x[t,i] = grupi ku luan lojtari i në javën t.
5. **Domeni:** x[t,i] ∈ {0,…,g−1}.
6. **Kufizimet e forta:** çdo lojtar shfaqet një herë në javë; çdo grup ka p lojtarë;
   për i ≠ j, shuma e treguesve [x[t,i] = x[t,j]] mbi javët është ≤1.
7. **Kufizimet e buta:** asnjë në variantin bazë.
8. **Fillimi:** java e parë është ndarja kanonike (0,…,p−1), (p,…,2p−1), etj.
   Kjo nuk humbet zgjidhje: lojtarët mund të riemërtohen që çdo javë e parë të marrë këtë formë.
9. **Qëllimi:** wg grupe të plota; validuesi rikontrollon javët, madhësitë dhe çiftet nga fillimi.
10. **Tranzicioni:** lojtari më i vogël i pambuluar ankoron grupin tjetër; provohen kombinimet
    prej p−1 lojtarësh të tjerë. Refuzohen çiftet që janë takuar më parë.
    Ankorimi heq permutimet e grupeve pa eliminuar ndonjë ndarje të vlefshme.
11. **Objektivi:** për w të fiksuar, gjetja e një orari pa shkelje; në variantin e maksimizimit, max w.
12. **Vlerësimi:** numri i grupeve/javëve të plotësuara dhe çiftet e përdorura.
13. **Peizazhi:** një javë ka P = n!/((p!)^g g!) ndarje në grupe të paetiketuara.
    Fillimisht numërojmë n! renditje, pjesëtojmë me renditjet brenda grupeve dhe pastaj
    me renditjet e grupeve. P^w është hapësira naive e sekuencave, përpara kufizimeve ndërjavore.
    Me javën e parë të normalizuar mbetet jo më shumë se P^(w−1) sekuenca.
    Kjo është zgjedhje kombinatorike me rritje eksponenciale sipas javëve.
14. **Degëzimi:** kur mbeten r lojtarë, jo më shumë se C(r−1,p−1); krasitja e ul këtë vlerë.
15. **Thellësia maksimale:** (w−1)g tranzicione pas javës së parë. Stiva ka një kornizë shtesë për rrënjën.
16. **Koha:** eksponenciale në rastin më të keq, me kosto shtesë për formimin dhe kontrollin e çifteve;
    nuk jepet një numër i saktë nyjesh për instancat e mëdha.
17. **Hapësira:** stivë DFS lineare në thellësi për numrin e gjendjeve aktive; tuple-t dhe setet
    në secilën kornizë kanë kosto që varet nga n dhe wg.

Çdo lojtar takon p−1 lojtarë të rinj në javë, prandaj w(p−1) ≤ n−1 dhe
**w ≤ floor((n−1)/(p−1))**, për p>1. Për 32 lojtarë dhe p=4, kufiri është 10.
Për p=1 çiftesh nuk ka, ndaj nuk ekziston maksimum i fundëm javësh.
Një orar valid provon një kufi të poshtëm; një kufi teorik provon kufi të sipërm.
Vetëm kur ato përputhen ose kur një shterim i plotë përjashton javën pasuese provohet maksimumi.

## Sudoku

1. **Përkufizimi:** plotësim i rrjetit 9×9 me shifrat 1–9, duke ruajtur të dhënat fillestare.
2. **Gjendja:** tuple me 81 numra; 0 tregon një qelizë të paplotësuar.
3. **Zgjidhja:** tuple pa zero që kalon kontrollin e të 27 njësive dhe ruan çdo të dhënë.
4. **Variablat:** 81 variabla x[r,c].
5. **Domenet:** {1,…,9}; për të dhënat fillestare domeni është singleton.
6. **Kufizimet e forta:** AllDifferent për çdo rresht, kolonë dhe kuti 3×3; të dhënat nuk ndryshohen.
7. **Kufizimet e buta:** asnjë.
8. **Fillimi:** rrjeti i validuar, ku numrat janë të plotë 0–9 dhe nuk ka përsëritje të të dhënave.
9. **Qëllimi:** të gjitha qelizat janë mbushur. Kontrolli i pavarur verifikon setin 1–9 në çdo njësi.
10. **Tranzicioni:** zgjidhet qeliza me më pak kandidatë (MRV), me barazime sipas indeksit.
    Për çdo vlerë të lejueshme krijohet një fëmijë; radha FIFO zgjeron të gjithë nivelet sipas thellësisë.
    Domeni bosh e refuzon degën. Nuk bëhet thirrje rekursive DFS.
11. **Objektivi:** zero shkelje dhe plotësim i qelizave bosh.
12. **Vlerësimi:** numri i qelizave bosh dhe madhësia e domeneve për MRV.
13. **Peizazhi:** 9^81 ≈ 1.97×10^77 caktime të plota të pakufizuara; nuk është numri i Sudoku-ve valide.
    Me k qeliza bosh, jo më shumë se 9^k caktime që respektojnë të dhënat fillestare.
14. **Degëzimi:** nga 0 deri në 9; pas kufizimeve zakonisht më i ulët.
15. **Thellësia:** k, sepse çdo tranzicion mbush vetëm një qelizë.
16. **Koha:** O(9^k) nyje si kufi i përgjithshëm, me kosto kontrolli për gjendjen 81-qelizore.
17. **Hapësira:** eksponenciale, me front FIFO dhe tabelën e prindërve/gjendjeve të vizituara.

Backtracking në këtë pjesë nënkupton trajtimin e alternativave dhe refuzimin e degëve të pavlefshme.
Nuk nënkupton zëvendësimin e BFS me kthim rekursiv DFS. Numëruesi `backtracks` mbetet zero te BFS;
`rejected` regjistron kandidatët e refuzuar. Enigmat shoqërohen me etiketë pedagogjike vështirësie,
jo certifikim; numri i të dhënave nuk përcakton vetë vështirësinë njerëzore apo kohën e BFS.
Validimi i një zgjidhjeje nuk provon unikësinë e saj.

## Latin Square

1. **Përkufizimi:** një katror n×n me simbolet 1,…,n, pa përsëritje në rresht dhe kolonë.
2. **Gjendja:** prefiks row-major i qelizave të caktuara.
3. **Zgjidhja:** tuple prej n² vlerash që kalon validuesin e rreshtave dhe kolonave.
4. **Variablat:** x[r,c], për r,c = 0,…,n−1.
5. **Domeni:** {1,…,n}.
6. **Kufizimet e forta:** çdo rresht dhe kolonë është një permutim i 1,…,n.
7. **Kufizimet e buta:** asnjë.
8. **Fillimi:** prefiksi bosh; edhe qelizat e normalizuara caktohen përmes tranzicioneve.
9. **Qëllimi:** gjatësia n² dhe të gjitha kufizimet e plotësuara.
10. **Tranzicioni:** qeliza pasuese merr çdo simbol që mungon në rresht dhe kolonë.
    Normalizimi fikson rreshtin dhe kolonën e parë në 1,…,n. Çdo katror Latin mund të reduktohet
    në këtë formë duke riemërtuar simbolet dhe permutuar rreshtat; për kërkim ekzistence është i sigurt.
11. **Objektivi:** zero shkelje në një katror të plotë.
12. **Vlerësimi:** numri i qelizave të caktuara; nuk përdoret konstruksion ciklik për zgjidhjen.
13. **Peizazhi:** n^(n²) caktime të plota të pakufizuara. Shumica nuk janë katrorë Latinë.
    Ky nuk është numri i katrorëve Latinë; normalizimi ngushton më tej hapësirën e kërkimit.
14. **Degëzimi:** deri n, ose 1 në rreshtin/kolonën e parë, me refuzime nga kufizimet.
15. **Thellësia:** n². IDDFS ekzekuton 0,1,…,n²; shfaqet lista e kufijve të provuar realisht.
16. **Koha:** në kufirin e përgjithshëm O(n^(n²)), por kjo nuk parashikon matjet pas krasitjes.
    Për b>1 konstant, IDDFS ka të njëjtin rend asimptotik si DFS me thellësi d, duke përsëritur prefikset.
17. **Hapësira:** O(d) korniza aktive, por kopjet e prefikseve kërkojnë deri O(d²) vlera në këtë implementim.

## 8-Puzzle

1. **Përkufizimi:** lëvizja e boshllëkut për të arritur renditjen e synuar në tabelën 3×3.
2. **Gjendja:** permutim immutable i 0,…,8; 0 është boshllëku.
3. **Zgjidhja:** rrugë gjendjesh dhe listë lëvizjesh nga fillimi te qëllimi.
4. **Variablat:** pozicioni i secilës pllakë ose vlerat e nëntë qelizave.
5. **Domeni:** simbolet 0–8 me kufizim AllDifferent.
6. **Kufizimet e forta:** çdo simbol shfaqet një herë; lejohet vetëm shkëmbimi i boshllëkut me një fqinj ortogonal.
7. **Kufizimet e buta:** asnjë; çdo lëvizje ka kosto 1.
8. **Fillimi:** si parazgjedhje (1,2,3,4,0,6,7,5,8), i konfigurueshëm.
9. **Qëllimi:** (1,2,3,4,5,6,7,8,0), ose qëllim i dhënë programatikisht.
10. **Tranzicioni:** Lart, Poshtë, Majtas, Djathtas sipas lëvizjes së boshllëkut.
    BFS përdor vizitim global; DFS i Puzzle përdor vizitim global; IDDFS kontrollon ciklet e rrugës
    dhe rifillon vizitimin për çdo limit, sepse rizgjerimi është pjesë e vetë metodës.
11. **Objektivi:** min numrin e lëvizjeve në krahasimin e rrugëve; BFS dhe IDDFS e garantojnë për kosto njësi
    kur përfundojnë. DFS kërkon një rrugë dhe nuk garanton minimum.
12. **Vlerësimi:** testi i barazisë me qëllimin; nuk përdoret heuristikë distance.
13. **Peizazhi:** 9! = 362880 permutime, por vetëm 9!/2 = 181440 janë të arritshme nga një qëllim fiks.
    Në gjerësi tek, pariteti i inversioneve të pllakave jo-zero ruhet; dy klasat kanë madhësi të barabartë.
14. **Degëzimi:** 2 në cep, 3 në anë, 4 në qendër; më i ulët pas refuzimit të cikleve.
15. **Thellësia:** kufiri përdoruesit m; për graf të fundëm një rrugë e thjeshtë ka jo më shumë se |V|−1 hapa.
    Ky kufi nuk është pretendim se BFS ka nevojë për kaq hapa në këtë instancë.
16. **Koha:** BFS dhe DFS me tabelë globale O(V+E) në përshkim të plotë pa ndërprerje;
    IDDFS ka kufi pemor O(b^d) me përsëritje midis iteracioneve.
17. **Hapësira:** BFS/DFS grafik ruajnë O(V) identifikues; DFS ruan edhe rrugën aktive.
    IDDFS ruan rrugën me kopje gjendjesh konstante dhe korniza O(d).

## Misionarët dhe Kanibalët

1. **Përkufizimi:** transportimi i 3 misionarëve dhe 3 kanibalëve me varkë dyvendëshe.
2. **Gjendja:** (M_left, C_left, B), ku B=0 majtas, B=1 djathtas.
3. **Zgjidhja:** rruga e kalimeve të sigurta deri te bregu tjetër.
4. **Variablat:** numri i secilit lloj në bregun e majtë dhe ana e varkës.
5. **Domenet:** M_left,C_left ∈ {0,1,2,3}, B ∈ {0,1}.
6. **Kufizimet e forta:** në secilin breg, nëse M>0 atëherë M≥C; varka merr 1–2 njerëz
    nga bregu ku ndodhet; numrat duhet të mbeten 0–3.
7. **Kufizimet e buta:** asnjë.
8. **Fillimi:** (3,3,0).
9. **Qëllimi:** (0,0,1).
10. **Tranzicionet:** ngarkesat (0,1),(0,2),(1,0),(1,1),(2,0), me shenjë sipas bregut dhe ndërrim të B.
11. **Objektivi:** min kalimet, me kosto 1. BFS jep rrugë minimale me 11 kalime.
12. **Vlerësimi:** kontrolli i sigurisë dhe barazia me qëllimin.
13. **Peizazhi:** 4×4×2 = 32 kombinime bruto. 20 plotësojnë sigurinë e brigjeve,
    por vetëm 16 janë të arritshme nga fillimi përmes ngarkesave të lejueshme.
14. **Degëzimi:** deri 5 ngarkesa para kontrolleve dhe vizitimit.
15. **Thellësia:** për rrugë të thjeshta maksimumi 15 hapa në komponentin e arritshëm;
    BFS përfundon në thellësinë optimale 11.
16. **Koha:** O(V+E) për kërkimin grafik, këtu graf i vogël i fundëm.
17. **Hapësira:** O(V), për frontin, gjendjet e vizituara dhe prindërit.

## Planifikimi rrotullues i punonjësve

1. **Përkufizimi:** mbulimi i ndërrimeve të një horizonti javor. Parazgjedhja: 6 punonjës,
    7 ditë, 2 ndërrime/ditë, një punonjës për ndërrim, maksimum 4 ndërrime për punonjës,
    një ndërrim i lirë mes dy punëve, pa padisponueshmëri/preferenca të deklaruara.
    Nuk supozohet kohëzgjatje në orë apo rregull ligjor pune. Java është horizont i fundëm,
    jo cikël me kontroll të pushimit mes ditës së fundit dhe të parës; "rrotullues" këtu shpreh shpërndarjen e ngarkesës.
2. **Gjendja:** tuple ekipesh për prefiksin e ndërrimeve kronologjike.
3. **Zgjidhja:** T=D×S ekipe me madhësi të barabartë me kërkesën q[t].
4. **Variablat:** x[e,t] ∈ {0,1}, tregues nëse punonjësi e punon ndërrimin t.
5. **Domenet:** binare, ose në përfaqësimin e kërkimit nënbashkësi me q[t] punonjës.
6. **Kufizimet e forta:** shuma_e x[e,t]=q[t]; shuma_t x[e,t]≤L;
    punonjësi nuk caktohet kur është i padisponueshëm; dy caktime të tij duhet të kenë
    më shumë se R indekse largësi. Ekipi nuk përmban dublikime. R matet në ndërrime të plota të lira.
7. **Kufizimet e buta:** balancimi i ngarkesës dhe shmangia e ndërrimeve të papëlqyera.
8. **Fillimi:** asnjë ndërrim i caktuar.
9. **Qëllimi:** T ndërrime të mbuluara; validuesi rikontrollon kërkesën, ngarkesat,
    disponueshmërinë dhe largësitë pa përdorur gjeneratorin e pasardhësve.
10. **Tranzicioni:** zgjidhet një ekip prej q[t] punonjësish të lejueshëm për ndërrimin e radhës.
    Kandidatët renditen sipas kostos së pjesshme, pastaj ID-ve për determinizëm.
11. **Objektivi:** min F = shuma_e load[e]^2 + λ shuma_(e,t të papëlqyera) x[e,t].
    Për kërkesë totale fikse, minimizimi i shumës së katrorëve është ekuivalent me minimizimin
    e devijimit kuadratik nga ngarkesa mesatare.
12. **Vlerësimi/kufiri:** për kufi të poshtëm, vendosjet e mbetura shtohen te ngarkesa më e vogël,
    duke injoruar pushimin dhe disponueshmërinë. Shtohen vetëm penalitetet e preferencave tashmë të kryera.
    Relaksimi nuk mund të mbivlerësojë optimumin; nëse kufiri ≥ kostos më të mirë, dega pritet.
13. **Peizazhi:** produkti mbi t i C(E,q[t]) për ndërrime të etiketuara dhe ekipe të paetiketuara.
    Për kërkesë 1, parazgjedhja është 6^14 = 78364164096 orare bruto.
14. **Degëzimi:** deri C(E,q[t]), i ulur nga disponueshmëria, pushimi dhe kapaciteti.
15. **Thellësia:** T=14 në shembull; një tranzicion për ndërrim, edhe kur kërkesa është 0.
16. **Koha:** në rastin më të keq përshkon produktin e zgjedhjeve, me koston e kontrollit
    dhe renditjes së ekipeve. Branch-and-bound përmirëson praktikën, jo garancinë eksponenciale.
17. **Hapësira:** DFS me stivë eksplicite mban edhe motrat e paprovuara, afërsisht O(bT)
    gjendje në rastin uniform; kopjimi i rrugëve/ekipeve shton faktor sipas T dhe E.

Konfliktet evidente raportohen paraprakisht (kërkesë totale mbi kapacitet, ose mungesë punonjësish
të disponueshëm në një ndërrim). Për ndërveprime më të ndërlikuara, shterimi i plotë provon
pamundësinë; ndërprerja nga kufijtë nuk e provon atë. Një kandidat i ruajtur gjatë ndërprerjes
është valid, por optimaliteti mbetet i hapur.
