---
name: Laboratori i kërkimit të painformuar
description: Ndërfaqe akademike e çelët për ekzekutim dhe krahasim rezultatesh.
colors:
  primary: "#256653"
  background: "#fbfcfe"
  secondary-background: "#eef3f7"
  text: "#172b3a"
  supporting-text: "#41566a"
typography:
  body:
    fontFamily: "sans-serif"
  table-header:
    fontWeight: 600
components:
  caption:
    textColor: "{colors.supporting-text}"
  table-header:
    textColor: "{colors.supporting-text}"
    typography: "{typography.table-header}"
---

# Design System: Laboratori i kërkimit të painformuar

## Overview

**Creative North Star: "Laboratori akademik i çelët"**

Ndërfaqja e miratuar i jep përparësi leximit të parametrave, rezultateve dhe krahasimeve në një ambient studimi me dritë. Identiteti mbështetet te sfondi i çelët, navigimi anësor, tabelat dhe pema pranë zgjidhjes në desktop. Modaliteti është Operate për ekzekutimin dhe Read për shpjegimet.

Ky dokument përshkruan ndërfaqen e ndërtuar nga kodi; nuk ka kompozim vizual të miratuar nga një imazh. Burimet autoritative janë tema në `.streamlit/config.toml` dhe paraqitja në `app.py`. Streamlit zotëron kontrollet, fokusin, gjendjet dhe sjelljen responsive. Aplikacioni shton rregullat për tekstin ndihmës dhe krerët e tabelave. Pamjet në `.impeccable/review/` ilustrojnë paraqitjen desktop dhe mobile.

**Key Characteristics:**

- Sipërfaqe të çelëta dhe theks i përmbajtur i gjelbër.
- Hierarki native, tabela të lexueshme dhe shpjegime në shqip.
- Zgjidhje dhe pemë në kolona të barabarta në desktop; njëra pas tjetrës në mobile.
- Status i shprehur me tekst dhe komponentët native të Streamlit.

## Colors

Paleta është e qetë, me neutrale të ftohta dhe një theks të gjelbër; vlerat normative janë në frontmatter.

### Primary

- **E gjelbër e laboratorit** (`primary`): theksi i temës për veprimet kryesore, përzgjedhjet dhe kontrollet aktive. Gjendjet ndërvepruese përllogariten nga Streamlit.

### Neutral

- **Letër e çelët** (`background`): sfondi i zonës kryesore.
- **Sipërfaqe e ftohtë** (`secondary-background`): paneli anësor dhe sipërfaqet dytësore të kontrolleve sipas temës native.
- **Bojë e errët** (`text`): tekstet dhe titujt kryesorë.
- **Tekst ndihmës i theksuar** (`supporting-text`): përshkrimet e vogla, përfshirë ato në panelin anësor, dhe krerët e tabelave në zonën kryesore. Përshkrimet kanë opacitet të plotë (`opacity: 1`); krerët kanë peshën e dokumentuar në frontmatter.

**The Kontrasti i shpjegimeve Rule.** Teksti ndihmës mbetet plotësisht opak; mos e zbeh për ta dalluar nga teksti kryesor.

Ngjyrat semantike të mesazheve vijnë nga Streamlit. Legjenda e pemës përdor blu për fillimin, gjelbër për rrugën/qëllimin dhe kuqe për refuzimin e regjistruar; këto nuk zëvendësojnë tekstin shpjegues dhe nuk janë thekse të përgjithshme të ndërfaqes.

## Typography

Familja e konfiguruar është sans-serif. Familja konkrete, madhësitë, lartësitë e rreshtave dhe pjesa tjetër e shkallës tipografike menaxhohen nga Streamlit. Projekti nuk deklaron font të jashtëm ose shkallë numerike të personalizuar.

- Titulli i seksionit përdor titullin kryesor native.
- Nëntitujt ndajnë matjet, zgjidhjen dhe pemën.
- Etiketat vendosen pranë kontrolleve; përshkrimet shpjegojnë kufijtë dhe interpretimin e rezultateve.
- Tabelat ruajnë etiketat e kolonave dhe paraqitjen numerike native për krahasim.

## Layout

Faqja përdor konfigurimin e gjerë të Streamlit. Paneli anësor përmban emrin e laboratorit, përshkrimin e shkurtër, navigimin me zgjedhje radio dhe seksionin e hapur të kufijve të kërkimit. Zona kryesore nis me titullin, parametrat dhe veprimin e ekzekutimit.

Rezultati shfaq statusin dhe matjet përpara dy kolonave të barabarta: zgjidhja majtas, pema e kufizuar dhe eksportet e saj djathtas. Shkarkimi JSON ndjek këtë bllok. Grafiku i pemës dhe tabela e analizës shtrihen sipas hapësirës së disponueshme.

Në pamjen mobile me gjerësi të vëzhguar (390px), paneli anësor hapet nga kontrolli native, ndërsa zgjidhja dhe pema renditen vertikalisht. Kjo është sjellje native e Streamlit, jo breakpoint i deklaruar nga projekti. Tabelat ruajnë sjelljen e tyre native kur kolonat tejkalojnë gjerësinë.

Tabela e dëshmisë Social Golfers qëndron brenda seksionit të saj të zgjerueshëm. Në mobile, lëvizja horizontale për kolonat e shumta mbetet e përmbajtur në tabelë; faqja dhe kontrollet ruajnë gjerësinë e ekranit.

Projekti nuk deklaron shkallë të vetën hapësirash, gjerësi fikse të panelit anësor ose breakpoint CSS. Ruani rrjedhën dhe hapësirat native.

## Elevation & Depth

Hierarkia mbështetet te sipërfaqet tonale, titujt, hapësira dhe vijat e tabelave e të kontrolleve. Nuk ka hije ose efekte shtresëzimi të personalizuara. Gjendjet dhe shtresat e kontrolleve native mbeten përgjegjësi e Streamlit.

## Shapes

Kontrollet, mesazhet dhe tabelat përdorin qoshet dhe kufijtë native të Streamlit. Projekti nuk deklaron shkallë rrezesh, forma të posaçme ose prerje dekorative; mos nxirrni vlera numerike nga pamjet si tokenë të rinj.

## Components

### Navigimi

Zgjedhësi radio në panelin anësor ka shtatë seksione: Paneli, Social Golfers, Sudoku, Latin Square, Pemët e kërkimit, Analiza e performancës dhe Shpjegimet matematikore. Ruani etiketat dhe përzgjedhjen native, përfshirë hapjen e panelit në mobile.

### Fushat dhe veprimet

Parametrat përdorin fusha numerike, zgjedhës, fusha JSON dhe rrëshqitës native me etiketa të dukshme. Butoni kryesor nis kërkimin; butonat dytësorë dhe të shkarkimit përdorin variantet native. Gjendjet hover, focus, active dhe disabled nuk kanë stil të personalizuar.

Zgjedhësi i shembullit Sudoku paraqet nivelet në shqip: E lehtë, Mesatare dhe E vështirë.

### Statusi dhe shpjegimet

Mesazhi i suksesit dallon zgjidhjen e validuar nga optimaliteti i provuar. Paralajmërimi për kufijtë shpjegon se ndërprerja nuk provon pamundësi; informacioni mbulon shterimin dhe udhëzimet. Spinner-i shfaq ekzekutimin, ndërsa gabimet e parametrave përdorin mesazhin native të gabimit.

Shpjegimet matematikore përdorin një zgjedhës dokumentesh dhe paraqitje Markdown native. Përveç modeleve, kompleksitetit dhe raportit, përfshihen përputhja me lëndën (`course_alignment`) dhe prova e optimalitetit Social Golfers (`golfers_optimality`).

### Dëshmia nga literatura

Për konfigurimin me 8 grupe dhe nga 4 lojtarë, Social Golfers paraqet seksionin native të zgjerueshëm “Përgjigjja e provuar: 10 javë — dëshmia nga literatura”, përpara kontrolleve të kërkimit. Brenda tij, mesazhi i suksesit shpjegon arritjen e kufirit të sipërm. Prejardhja e dukshme dhe lidhja e tabelës origjinale të Alejandro Aguado-s e identifikojnë dëshminë e botuar, të transkriptuar dhe të verifikuar lokalisht.

Statistikat paraqesin 480 çifte të ndryshme, zero përsëritje dhe 30 kundërshtarë të ndryshëm për lojtar; pas tyre vjen tabela e plotë 10-javore dhe shkarkimi i dëshmisë me verifikimin JSON. Përshkrimi shpjegon ID-të 0–31 dhe se kontrollet e kërkimit më poshtë ekzekutojnë DFS të pavarur nga dëshmia. Shpjegimi matematikor dallon kufirin e sipërm nga dëshmia e ekzistencës. Kjo paraqitje përdor të njëjtën paletë, tipografi dhe komponentë native, pa shtuar variant vizual.

### Tabelat

Tabelat paraqesin katalogun e problemeve, rrjetet e zgjidhjeve, oraret dhe matjet. Krerët në zonën kryesore përdorin tokenin `supporting-text` dhe peshën e dokumentuar; përmbajtja dhe vijat mbeten native. Analiza përdor tabelën interaktive pa indeks të dukshëm dhe grafik shtyllor.

### Pema dhe eksportet

Pema Graphviz është mostër e kufizuar, me legjendë të dukshme që sqaron edhe degët e lëna jashtë. Butoni DOT është menjëherë nën figurë; PNG dhe SVG bëhen të shkarkueshme pas përgatitjes. Rezultati dhe metrikat eksportohen edhe në JSON. Paraqitja nuk pretendon se pema e kufizuar është hapësira e plotë e kërkimit.

## Do's and Don'ts

### Do:

- **Do** ruaj sfondin e çelët, navigimin anësor dhe hierarkinë akademike të miratuar.
- **Do** ruaj zgjidhjen dhe pemën pranë njëra-tjetrës në desktop dhe vertikalisht në mobile.
- **Do** përdor tokenin e tekstit ndihmës me opacitet të plotë për përshkrimet dhe krerët e tabelave sipas kodit.
- **Do** shpjego statusin me tekst dhe ruaj legjendën e pemës.
- **Do** përdor kontrollet dhe sjelljet native të Streamlit.
- **Do** mbaj të dukshme prejardhjen e dëshmisë nga literatura dhe dallimin e saj nga ekzekutimet DFS.

### Don't:

- **Don't** shto dekorime ose lëvizje që pengojnë vëzhgimin e rezultateve.
- **Don't** zëvendëso tabelat krahasuese me karta dekorative.
- **Don't** deklaro font, rreze, hije, hapësira ose breakpoint të personalizuar pa burim në implementim.
- **Don't** paraqit ndërprerjen nga kufijtë si provë pamundësie ose pemën e kufizuar si pemë të plotë.
- **Don't** paraqit dëshminë e botuar si rezultat të DFS të këtij projekti.
