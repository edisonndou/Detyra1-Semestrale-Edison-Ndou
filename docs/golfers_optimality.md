# Social Golfers: maksimumi i provuar është 10 javë

Për 32 lojtarë në 8 grupe me nga 4, maksimumi është **10 javë**.
Ky përfundim mbështetet në një kufi të sipërm dhe një dëshmi ekzistence të kontrolluar.

## Kufiri i sipërm

Çdo lojtar takon 3 lojtarë të tjerë në javë. Pa përsëritje, pas w javësh duhet të ketë
3w kundërshtarë të ndryshëm. Janë vetëm 31 lojtarë të tjerë, prandaj 3w≤31 dhe w≤10.
Vetëm ky argument nuk provon se java e dhjetë mund të realizohet.

## Dëshmia e ekzistencës

Alejandro Aguado botoi tabelën [A 10 Days Solution to the Social Golfer Problem](https://www.mathpuzzle.com/MAA/54-Golf%20Tournaments/socgolf1.pdf).
Tabela I e origjinalit ka një kolonë për ditë/javë. Të dhënat numerike janë transpozuar
në `data/golfers/aguado_8_4_10.json`: çdo rresht JSON është një javë me 8 grupe.
Burimi dhe prejardhja ruhen në të njëjtin skedar. Artikulli lidhet edhe nga
[rezultatet e CSPLib për problemin 010](https://www.csplib.org/Problems/prob010/results/).

Verifikuesi lokal kontrollon:

1. Saktësisht 10 javë, 8 grupe për javë dhe 4 lojtarë për grup.
2. Çdo javë është një ndarje e të gjithë lojtarëve 0–31, pa mungesa ose përsëritje.
3. Të 480 çiftet që takohen janë të ndryshme: 10×8×C(4,2)=480.
4. Çdo lojtar takon saktësisht 30 kundërshtarë të ndryshëm.
5. Mbeten 16 çifte të papërdorura nga C(32,2)=496, pa shkelur asnjë kufizim.

Përveç validuesit të orarit, kontrolli për çdo lojtar rindërton kundërshtarët e tij.
Testi i regresionit ndërton në mënyrë të pavarur edhe një matricë 32×32 të takimeve.
Modifikimi i dëshmisë për të përsëritur një javë duhet të refuzohet.

## Çfarë provon kjo dhe çfarë ekzekuton programi

Orari i validuar provon w≥10; argumenti i sipërm provon w≤10. Pra **w*=10**.
Nuk ka nevojë për shterim të të gjithë hapësirës së orareve për këtë provë.

Ky është një **certifikim i një dëshmie nga literatura**, i ndarë shprehimisht nga kërkimi.
Nuk është një rezultat i koduar paraprakisht që paraqitet si rezultat i DFS.
`Golfers.solve()` dhe `--maximize` vazhdojnë të përdorin vetëm DFS me Backtracking dhe
krasitjen e çifteve. Nuk lexojnë dëshminë dhe nuk e përdorin si renditje të fshehur kandidatësh.
Kërkimi i tyre i kufizuar për 10 javë mund të kthejë `limit`, edhe pse problemi ka zgjidhje të njohur.
Ky dallim është i domosdoshëm për një raport eksperimental të ndershëm.

```powershell
# Kërkim real DFS, me kufizime të deklaruara
python main.py golfers --groups 8 --players 4 --weeks 10 --seconds 3

# Kontroll i veçantë i dëshmisë, me burimin dhe provën e maksimumit
python main.py golfers --certificate --output outputs/results/golfers-optimality.json
```

Orari i plotë shfaqet në Streamlit te Social Golfers → “Përgjigjja e provuar: 10 javë”,
dhe mund të shkarkohet si JSON së bashku me raportin e verifikimit.
