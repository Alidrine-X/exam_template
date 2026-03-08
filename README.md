# Examination

Individuell examinationsuppgift i kursen Programmering med Python.

Börja läs igenom game.py - det är där projektet startas.

## Starta projektet

```commandline
python -m src.game
```

Fruit Loop är ett terminalbaserat äventyrsspel där spelaren navigerar på ett rutnätsbaserat spelbräde. Målet är att samla alla ursprungliga ätbara föremål, undvika fällor, använda verktyg och eventuellt placera och detonera bomber för att röja väggar eller hinder. När alla ätbara föremål är upplockade kan spelaren nå utgången (E) för att vinna spelet.

Vad spelaren kan göra

Rörelse:

Gå: W, A, S, D (1 steg)

Hoppa: JW, JA, JS, JD (2 steg)

Samla föremål till inventory:

Ätbart: ger poäng och gratis steg (grace-period)

Verktyg (spade): kan riva innerväggar

Nycklar: låser upp kistor

Bomb: kan placeras och explodera i 3×3-rutor

Interaktion med objekt:

Ätbart: ökar poäng och grace-period

Verktyg: kan användas för att riva innerväggar

Nyckel: låser upp kistor

Kistor: ger poäng

Bomb: kan placeras och explodera i 3×3-område

Fällor: ger minuspoäng, kan desarmeras med kommando T

Exit: kan användas när alla ursprungliga ätbara föremål är upplockade med kommando E

Poäng och spelmekanik

Spelaren börjar med 10 poäng.

Poängen minskar med 1 per steg, men stoppar under grace-period (5 steg) när ett ätbart föremål plockas upp.

Varje steg ökar spelarens fertile_soil, vilket genererar ett nytt ätbart föremål efter 25 steg.

Bomb-timer startar när bomben placeras i spelvärlden och exploderar efter att spelaren tagit 3 steg.
