# Examination

Individuell examinationsuppgift i kursen Programmering med Python.

Börja läs igenom game.py - det är där projektet startas.

## Starta projektet

```commandline
python -m src.game
```

Spelets beskrivning

Fruit Loop är ett terminalbaserat spel där spelaren navigerar i en spelvärld representerad av ett rutnät. Målet är att samla upp alla ursprungliga ätbara föremål, undvika fällor, använda verktyg och eventuellt placera och detonera bomber för att röja väggar eller hinder. När alla ätbara föremål är upplockade kan spelaren gå till utgången (E) för att vinna.

Vad spelaren kan göra:

Rörelse: Gå (WASD) eller hoppa (JWASD) över 1–2 rutor.

Samla föremål: Ätbart, verktyg (spade), nycklar, bomb.

Interagera med objekt:

Ätbart ökar poäng och grace-period.

Verktyg kan riva innerväggar.

Nyckel låser upp kistor.

Kistor ger poäng.

Bomb kan placeras och explodera i 3x3-område.

Fällor ger minuspoäng, kan desarmeras med kommando T.

Exit kan användas när alla ursprungliga ätbara föremål är upplockade med kommando E

Poäng och mekanik:

Spelaren får 10 poäng vid start. Poäng minskas med ett per steg, men poäng stoppas 5 steg under grace-period när ätbart föremål plockats upp.

Steg som tas ökar “fertile_soil”, vilket genererar något nytt ätbart efter 25 steg.

Bomb-timer startas då bomb placerats ut io spelvärlden och exploderar när spelare tagit 3 steg.
