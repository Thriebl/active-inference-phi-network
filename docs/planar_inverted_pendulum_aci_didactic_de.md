<img src="conative_systems_logo.svg" align="right" width="125" style="float: right; margin-left: 20px; margin-bottom: 15px;" alt="Conative Systems Logo" />

# Active Conative Inference (ACI): Das Planare Invertierte Pendel
### Ein didaktischer Leitfaden zu Wahrnehmung, Handlung, Vitalität und Online-Lernen in einem planaren 2D-System

**Autor:** Thomas Riebl  
**Organisation:** Conative Systems S.à r.l.  
**Theoretische Grundlagen:** Active Conative Inference (ACI), Free Energy Principle (FEP), Integrated Information Theory ($\Phi$ / IIT 4.0, Giulio Tononi), Spinozas Conatus, Patent 01 & 11  
**Zielarchitektur:** Freistehendes ANSI C99 für Edge-Mikrocontroller (Zero Dynamic Heap)

---

## 1. Physikalische Anschauung: Das Besenstiel-Paradoxon & Planare Architektur

Bevor wir mathematische Formalismen oder Wahrscheinlichkeitsmatrizen definieren, verankern wir das System in der alltäglichen physikalischen Anschauung.

Stellen wir uns vor, einen langen Besenstiel senkrecht auf der offenen Handfläche zu balancieren:
* Wenn die Spitze des Stiels nach **rechts** kippt: Was muss die Hand tun?
* Die menschliche Intuition verleitet oft zu dem fatalen Reflex, die Hand nach links wegzuziehen. Die klassische Newton-Euler-Mechanik verlangt jedoch das genaue Gegenteil: Die Hand muss blitzschnell nach **RECHTS** schnellen, um den Drehpunkt direkt unter den fallenden Schwerpunkt (Center of Mass, CoM) zu schieben.
* Das resultierende Trägheitsmoment richtet den Stab wieder in die senkrechte Ruhelage ($0^\circ$) auf.

In diesem planaren 2D-System ist die Bewegung streng auf eine einzige vertikale Ebene beschränkt: Der Translationswagen fährt entlang der horizontalen $x$-Achse, und das Pendel kippt ausschließlich nach **Links** ($l$) oder **Rechts** ($r$). Vorne/Hinten-Freiheitsgrade sind mechanisch gesperrt.

---

### 1.1 Physikalisches Kinematik-Diagramm (Stufe 1: Das intuitive Cart-Pole)

Die folgende Vektorgrafik veranschaulicht den physikalischen Grundaufbau vor der Einführung diskreter Wahrscheinlichkeitsfächer oder Matrizen:

![1. Physikalisches System: Das Planare Invertierte Pendel](inverted_pendulum_step1_physics.svg)

#### Visuelle Elemente der physikalischen Bühne:
1. **Der mobile Translationswagen (Masse $M$):** Fährt streng linear entlang der horizontalen Schiene (Links ↔ Rechts). Keine Vorne/Hinten-Bewegungen.
2. **Der starre Balancestab (Länge $L$, Masse $m$):** Gelagert am reibungsarmen Drehpunkt $(x, 0)$ des Wagens, frei kippend um den Winkel $\theta$.
3. **Vertikale Soll-Lage ($\theta = 0^\circ$, grün gestrichelte Linie):** Die instabile Gleichgewichtslage, in welcher der Schwerpunkt exakt senkrecht über dem Drehpunkt steht.
4. **Das Besenstiel-Paradoxon:** Kippt der Stab nach rechts ($+\theta$), muss der Wagen blitzschnell nach **RECHTS** beschleunigen, um den Drehpunkt unter die fallende Masse zu schieben.

---

## 2. Der Geist des Reglers: Bayes' Theorem & Grundlegende Wahrscheinlichkeiten

Nachdem die Mechanik des Pendels greifbar vor Augen steht, wenden wir uns der Steuerung zu: **Wie nimmt der Agent wahr, was in der realen Welt geschieht?**

In klassischen Regelungstheorien wird oft angenommen, dass der exakte Winkel $\theta$ verzögerungsfrei und perfekt messbar sei. In der Realität sind Sensoren verrauscht, Encoder haben Quantisierungsrauschen und Luftzüge stören das System. Der Agent hat niemals direkten, allwissenden Zugriff auf den verborgenen Zustand der Außenwelt; er muss ihn kontinuierlich durch seine sensorische Grenze (das **Markov-Blanket**) hindurch erschließen.

### Grundlegende Notation: $s, o, a, P$

* **$s$ (Verborgener Zustand / Hidden State):** Der wahre, unberührbare physikalische Zustand der Welt (z. B. der tatsächliche Kippwinkel $\theta \in \mathcal{S}$).
* **$o$ (Beobachtung / Observation):** Der verrauschte Messwert, den die Sensoren am Markov-Blanket registrieren ($o \in \mathcal{O}$).
* **$a$ (Handlung / Action):** Die physikalische Intervention oder der Steuerbefehl an die Motoren (z. B. Wagenbeschleunigung $a \in \mathcal{A}$).
* **$P$ (Wahrscheinlichkeit):** Der mathematische Wert für den Grad der Gewissheit, des Glaubens oder der Übergangshäufigkeit eines konkreten Ereignisses oder Zustands ($P \in [0, 1]$). *(Hinweis zur mathematischen Konvention: Großes $P$ bezeichnet die konkrete Wahrscheinlichkeit eines Zustands, während kleines $p(s)$ die gesamte Wahrscheinlichkeitsverteilung über alle Zustände und $q(s)$ den internen Glauben des Agenten darstellt.)*
* **Der Bedingungsstrich ($\mid$):** Gelesen als **„gegeben“**. Beispielsweise liest sich $P(s \mid o)$ als: *„Die Wahrscheinlichkeit des Zustands $s$, **gegeben** die Beobachtung $o$“*.

---

### Bayes' Theorem in der Wahrnehmung

Das Theorem von Bayes liefert das mathematische Gesetz, wie ein interner Glaube unter Einbeziehung neuer sensorischer Evidenz optimal aktualisiert wird:

$$P(s \mid o) = \frac{P(o \mid s) \cdot P(s)}{P(o)} = \frac{P(o \mid s) \cdot P(s)}{\sum_{s'} P(o \mid s') \cdot P(s')}$$

---

#### Anschauliches Alltagsbeispiel: Das Regen-Paradoxon ($s = \text{Regen}$, $o = \text{Straße nass}$)

Um das Zusammenspiel dieser probabilistischen Terme und die unverzichtbare Rolle des Nenners $P(o)$ vorab intuitiv zu begreifen, hilft ein einfaches Alltagsszenario:

* **Verborgener Weltzustand $s$ (Das Wetter draußen):**
  * $s_1 = \text{Regen}$ (Vorab-Glaube / Prior: $P(\text{Regen}) = 0{,}20$ bzw. $20\,\%$)
  * $s_2 = \text{Ohne Regen}$ (Vorab-Glaube / Prior: $P(\text{ohne Regen}) = 0{,}80$ bzw. $80\,\%$)
* **Sensorische Beobachtung $o$ (Blick aus dem Fenster):**
  * $o = \text{Die Straße ist nass}$

**Warum kann die Straße nass sein? (Zwei konkurrierende Kausalpfade):**
1. **Pfad 1 (Echter Regen):** Wenn es regnet, ist die Straße fast garantiert nass: $P(\text{nass} \mid \text{Regen}) = 0{,}99$ ($99\,\%$).
2. **Pfad 2 (Sensor-Mehrdeutigkeit / Falscher Alarm):** Es herrscht kein Regen, aber ein Straßenreinigungsfahrzeug fuhr vorbei oder der Rasensprenger des Nachbarn lief: $P(\text{nass} \mid \text{ohne Regen}) = 0{,}05$ ($5\,\%$).

**Berechnung der marginalen Evidenz $P(o)$ (Gesamtwahrscheinlichkeit einer nassen Straße):**

$$\begin{aligned}
P(\text{nass}) &= \underbrace{P(\text{nass} \mid \text{Regen}) \cdot P(\text{Regen})}_{\text{Nass durch Regen } (0{,}99 \cdot 0{,}20 = 0{,}198)} + \underbrace{P(\text{nass} \mid \text{ohne Regen}) \cdot P(\text{ohne Regen})}_{\text{Nass durch Rasensprenger } (0{,}05 \cdot 0{,}80 = 0{,}040)} \\
&= 0{,}198 + 0{,}040 = \mathbf{0{,}238} \; (23{,}8\,\%)
\end{aligned}$$

**Anwendung des Bayes-Theorems (Regnet es wirklich da draußen?):**  
Sobald du aus dem Fenster blickst und siehst, dass die Straße nass ist ($o$), aktualisiert sich dein Glaube:

$$P(\text{Regen} \mid \text{nass}) = \frac{P(\text{nass} \mid \text{Regen}) \cdot P(\text{Regen})}{P(\text{nass})} = \frac{0{,}198}{0{,}238} \approx \mathbf{83{,}2\,\%}$$

* Der Nenner $P(o) = 0{,}238$ normiert das Ergebnis.
* Die Beobachtung der nassen Straße lässt die Regenwahrscheinlichkeit von zuvor $20\,\%$ auf $83{,}2\,\%$ steigen – aber eben nicht auf $100\,\%$, weil Bayes den alternativen Kausalpfad (Rasensprenger) mathematisch exakt mit einrechnet!
* In Theons Invertiertem Pendel erfüllt $P(o)$ exakt dieselbe mathematische Funktion: Es gewichtet Vorab-Erwartungen dynamisch gegen verrauschte Sensor-Encoder.

---

## 3. Abbildung der physikalischen Welt auf Active Inference: Vier intuitive Objekte

Durch die Beschränkung auf die Ebene vereinfacht sich unser generatives Modell auf exakt **5 Zustände** und **2 Aktionen**:

1. **Wo müssen wir sein? $\to \mathbf{C}$ (Phänotypische Präferenz):**  
   Das autopoietische Verlangen des Systems. Die aufrechte Ruhelage ($s_0$) bedeutet minimale Überraschung ($C_0 = 0.0$). Leichte Neigungen tragen kleine Strafen ($C = -1.5$). Katastrophales Kippen bedeutet existenzielle Bedrohung ($C = -8.0$).
2. **Wo glauben wir zu starten? $\to \mathbf{D}$ (Prior-Glaube):**  
   Die Ausgangshypothese vor der ersten Messung ($92\%$ Gewissheit für aufrechte Balance bei $t = 0$).
3. **Wie präzise sehen wir den Stab? $\to \mathbf{A}$ (Likelihood-Matrix):**  
   Eine transparente $5 \times 5$-Matrix für die Sensorzuverlässigkeit ($92\%$ Diagonalschärfe, $4\%$ Nachbarstreuung).
4. **Was bewirkt die Wagenbewegung? $\to \mathbf{B}(a)$ (Kausale Übergangstensoren):**  
   Zwei intuitive $5 \times 5$-Matrizen ($\mathbf{B}(l)$ und $\mathbf{B}(r)$), welche die Newton-Euler-Physik kodieren: Bei Schräglage rechts ($r_1$) stellt ein Rechtsruck ($a = r$) die Ruhelage ($s_0$) mit $88\%$ Wahrscheinlichkeit wieder her.

---

### Die vier Kernkomponenten von Bayes' Theorem (Formale Matrizen-Zuordnung)

Mit den vier intuitiven Objekten ($\mathbf{C}, \mathbf{D}, \mathbf{A}, \mathbf{B}$) und dem Regen-Paradoxon lässt sich nun formal beschreiben, wie Bayes' Theorem im Regler rechnet:

1. **Prior-Glaube $P(s)$ (A-priori-Erwartung vor der Messung $\to \mathbf{D}$):**  
   Was der Agent über den Zustand glaubt, **bevor** er die neue Messung auswertet. Beim Pendel ist dies entweder der Ausgangsvektor $\mathbf{D} = P(s_0)$ oder die Bewegungsvorhersage:
   $$s_{\text{pred}} = \mathbf{B}(a_{t-1}) \cdot s_{t-1}$$
   *(Im Regen-Beispiel: Vorab-Wahrscheinlichkeit $P(\text{Regen}) = 20\,\%$.)*
2. **Likelihood $P(o \mid s)$ (Matrix $\mathbf{A}$ — Sensorpräzision):**  
   Die generative Abbildung: *„Wenn der Stab tatsächlich im Zustand $s$ stünde: Wie wahrscheinlich ist es dann, dass unser Sensor die Beobachtung $o$ meldet?“* (Erfasst Sensorpräzision $\gamma_s$ und Rauschen $\varepsilon$).  
   *(Im Regen-Beispiel: $P(\text{nass} \mid \text{Regen}) = 99\,\%$ vs. $P(\text{nass} \mid \text{ohne Regen}) = 5\,\%$.)*
3. **Posterior-Glaube $P(s \mid o)$ (A-posteriori-Zustand $\to$ Interne Dichte $q(s)$):**  
   Der aktualisierte, optimale Glaube über den Weltzustand $s$ **nach** Verarbeitung der Beobachtung $o$. Wahrnehmung in Active Inference ist die Minimierung der Diskrepanz (Variational Free Energy $F$) zwischen diesem Posterior und der internen Dichte $q(s)$.  
   *(Im Regen-Beispiel: $P(\text{Regen} \mid \text{nass}) = 83{,}2\,\%$.)*
4. **Marginale Evidenz $P(o)$ (Normierung & Phänotypische Präferenz $\to \mathbf{C}$):**  
   Die Gesamtwahrscheinlichkeit der Beobachtung $o$, gemittelt über alle denkbaren Zustände. Ihr Logarithmus $\ln P(o)$ bildet den phänotypischen Präferenzvektor $\mathbf{C}$.  
   *(Im Regen-Beispiel: $P(\text{nass}) = 23{,}8\,\%$.)*

---

## 4. Formale mathematische 5-Zustände-Spezifikation & Zustands-Kompass

### 1.2 Architektur des Zustandsraums (Stufe 2: Diskretisierung & Conatus-Grenze)

Zur Konstruktion eines berechenbaren Modells diskretisieren wir den kontinuierlichen Winkel $\theta$ in **5 conative Zustände** ($\mathcal{S}$) und definieren die **Conatus-Überlebensgrenze**:

![2. Diskreter Zustandsraum & Conatus-Überlebensbarriere](inverted_pendulum_step2_states.svg)

#### Die 5 diskreten Zustände & physikalischen Schwellenwerte:
* **Zustand $s_0 = 0$ (Grün):** Aufrechte Gleichgewichtslage ($|\theta| \le 3^\circ$). Homeostatischer Attraktor ($C_0 = 0.0$, $\Phi = 1.00$).
* **Zustände $s_1 = l_1, s_3 = r_1$ (Bernstein):** Leichte Neigung links oder rechts ($3^\circ < |\theta| \le 15^\circ$). Mühelos stabilisierbar ($C = -1.5$, $\Phi = 0.70$).
* **Zustände $s_2 = l_2, s_4 = r_2$ (Rot):** Kritisches Kippen links oder rechts ($15^\circ < |\theta| < 35^\circ$). Starkes Gegensteuern erforderlich ($C = -8.0$, $\Phi = 0.15$).
* **Conatus-VETO-Grenze (Rot gestrichelt bei $\pm 35^\circ$):** Point of No Return. Exkursionen über $\pm 35^\circ$ können vom Motor nicht mehr abgefangen werden; jede dahin führende Politik löst ein sofortiges Conatus-Veto aus ($G^* \to +\infty$).

### Diskreter Zustandsraum ($|\mathcal{S}| = 5$) und Aktionsraum ($|\mathcal{A}| = 2$)

* **Zustände:** $\mathcal{S} = \{0, l_1, l_2, r_1, r_2\}$
  * $s_0 = 0$: Aufrechte Soll-Lage (Balanciert / Attraktor)
  * $s_1 = l_1$: Leichte Linksauslenkung ($\theta \approx -12^\circ$)
  * $s_2 = l_2$: Starker Sturz nach Links ($\theta \approx -26^\circ$)
  * $s_3 = r_1$: Leichte Rechtsauslenkung ($\theta \approx +12^\circ$)
  * $s_4 = r_2$: Starker Sturz nach Rechts ($\theta \approx +26^\circ$)
* **Aktionen:** $\mathcal{A} = \{l, r\}$
  * $a = 0$ ($l$): Wagen beschleunigt nach LINKS ⬅
  * $a = 1$ ($r$): Wagen beschleunigt nach RECHTS ➔

---

### Prior-Vektor $\mathbf{D}$ (Ausgangszustand)

$$\mathbf{D} = P(s_0) = \begin{pmatrix} 0.92 \\ 0.04 \\ 0.00 \\ 0.04 \\ 0.00 \end{pmatrix} \begin{matrix} (0) \\ (l_1) \\ (l_2) \\ (r_1) \\ (r_2) \end{matrix}$$

* $P(s = 0) = 0.92$: Hohe Sicherheit für den aufrechten Start.
* Geringe Restmasse ($0.04$) auf Stufe 1 verhindert numerische Nullfallen.
* Null Wahrscheinlichkeit ($0.00$) für sofortigen Absturz (Stufe 2).

---

### Phänotypischer Präferenzvektor $\mathbf{C}$ (Conatus-Attraktor & Die Log-Softmax-Brücke)

$$\mathbf{C} = \ln P(o) = \begin{pmatrix} 0.0 \\ -1.5 \\ -8.0 \\ -1.5 \\ -8.0 \end{pmatrix} \begin{matrix} (o_0) \\ (o_{l1}) \\ (o_{l2}) \\ (o_{r1}) \\ (o_{r2}) \end{matrix}$$

* $\mathbf{C}_0 = 0.0$: Maximale Präferenz (minimale Freie Energie / Null Überraschung in stabiler Balance).
* $\mathbf{C}_{\text{Stufe 1}} = -1.5$: Leichte Aversion gegen Schräglagen (erzeugt Regelantrieb).
* $\mathbf{C}_{\text{Stufe 2}} = -8.0$: Katastrophal negative Bewertung (existenzielle Gefahrenzone / Tipping-Barriere).

#### 💡 Mathematische Fundierung: Warum ist $\mathbf{C}$ negativ, während $\mathbf{A}, \mathbf{B}, \mathbf{D}$ strikt positiv sind?
Eine fundamentale mathematische Unterscheidung, an der viele Ingenieure und Einsteiger hängenbleiben:
* **Der Wahrscheinlichkeits-Raum ($\mathbf{A}, \mathbf{B}, \mathbf{D}$):**  
  In der Sensormatrix $\mathbf{A}$, den Übergangstensoren $\mathbf{B}(a)$ und dem Prior-Vektor $\mathbf{D}$ stehen **reine Wahrscheinlichkeiten** ($P \in [0, 1]$). Jeder einzelne Eintrag ist strikt positiv (nicht-negativ) und jede Spalte summiert sich exakt zu **$1{,}0$ ($100\,\%$)**, damit keine Wahrscheinlichkeitsmasse verloren geht (stochastische Spaltennormierung).
* **Der Log-Präferenz-Raum ($\mathbf{C}$ in Nats):**  
  Der Vektor $\mathbf{C}$ speichert keine Rohwahrscheinlichkeiten, sondern lebt im **logarithmischen Informationsraum**: $\mathbf{C} = \ln P(o)$.  
  Da jede Wahrscheinlichkeit $P \le 1{,}0$ ist, ist ihr natürlicher Logarithmus **immer kleiner oder gleich 0 (also negativ)**:
  $$\ln(1{,}0) = \mathbf{0{,}0} \quad (\text{Maximale Präferenz / Null Überraschung})$$
  $$\ln(0{,}223) \approx \mathbf{-1{,}5} \quad (\text{Leichte Auslenkung})$$
  $$\ln(0{,}00033) \approx \mathbf{-8{,}0} \quad (\text{Existenzielle Bedrohung})$$
* **Die Softmax-Brücke:**  
  Wie gelangt man von conativen Bewertungen $\mathbf{C}$ zurück zu einer echten, normierten Wahrscheinlichkeitsverteilung $P(o)$?  
  Genau über die **Softmax-Funktion** (die Boltzmann-/Gibbs-Verteilung):
  $$P(o_i) = \sigma(\mathbf{C})_i = \frac{e^{C_i}}{\sum_j e^{C_j}}$$
  Die Exponentialfunktion $e^{C_i}$ überführt jede noch so negative Zahl wieder in einen **strikt positiven Wert**, und die Division durch die Summe $\sum e^{C_j}$ stellt sicher, dass sich alle Werte exakt zu **$1{,}0$ ($100\,\%$)** aufsummieren!

---

### Beobachtungsmatrix $\mathbf{A}$ (Sensorpräzision)

Die Matrix $\mathbf{A} \in \mathbb{R}^{5 \times 5}$ bildet den Weltzustand $s$ auf die Beobachtungen $o$ ab: $P(o \mid s)$.

Bei Sensorschärfe $\gamma_s = 0.92$ und Nachbarstreuung $\varepsilon = 0.04$:

$$\mathbf{A} = P(o \mid s) = \begin{pmatrix}
0.92 & 0.04 & 0.00 & 0.04 & 0.00 \\
0.04 & 0.92 & 0.04 & 0.00 & 0.00 \\
0.00 & 0.04 & 0.96 & 0.00 & 0.00 \\
0.04 & 0.00 & 0.00 & 0.92 & 0.04 \\
0.00 & 0.00 & 0.00 & 0.04 & 0.96
\end{pmatrix}$$

* Die Hauptdiagonale dominiert mit über $92\%$ Zuverlässigkeit.
* Sensorungenauigkeiten treten nur in direkt benachbarte Neigungsstufen auf ($4\%$).

---

### Übergangstensoren $\mathbf{B}(a)$ (Kausaldynamik)

Für die beiden Aktionen $a \in \{l, r\}$ beschreibt $\mathbf{B}(a) \in \mathbb{R}^{5 \times 5}$ die Übergänge $P(s_{t+1} \mid s_t, a)$.

#### Aktion $a = r$ (Wagen beschleunigt nach rechts)

$$\mathbf{B}(r) = P(s' \mid s, a = r) = \begin{pmatrix}
0.15 & 0.00 & 0.00 & 0.88 & 0.00 \\
0.85 & 0.10 & 0.00 & 0.02 & 0.00 \\
0.00 & 0.90 & 1.00 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.10 & 0.85 \\
0.00 & 0.00 & 0.00 & 0.00 & 0.15
\end{pmatrix}$$

* Aus $s = r_1$ (leichte Neigung rechts): Rechtsruck $\to$ stellt Ruhelage $0$ mit $P = 0.88$ wieder her.
* Aus $s = r_2$ (starker Sturz rechts): Rettet das System von $r_2$ zurück nach $r_1$ mit $P = 0.85$.
* Aus $s = 0$ (bereits balanciert): Überflüssiger Rechtsruck kippt das Pendel nach links ($l_1$, $P = 0.85$).
* Aus $s = l_1$ (bereits nach links gekippt): Rechtsruck beschleunigt den Absturz nach links ($l_2$, $P = 0.90$).

#### Aktion $a = l$ (Wagen beschleunigt nach links – symmetrisch invertiert)

$$\mathbf{B}(l) = P(s' \mid s, a = l) = \begin{pmatrix}
0.15 & 0.88 & 0.00 & 0.00 & 0.00 \\
0.00 & 0.10 & 0.85 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.15 & 0.00 & 0.00 \\
0.85 & 0.02 & 0.00 & 0.10 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.90 & 1.00
\end{pmatrix}$$

---

### 5. Die conative ACI-Differenzierung (Thomas Riebl)

Klassisches Active Inference ($H = 1$) handelt kurzsichtig und optimiert lediglich den nächsten Zeitschritt.

Unter Active Conative Inference gilt:
* **Temporale Tiefe $H \ge 2$:** Der Agent antizipiert Überschwingen. Zu starkes Gegensteuern bei $r_1$ erzeugt bei $t+2$ einen unkontrollierbaren Gegenschwung nach $l_2$.
* **Systemische Vitalitätsüberwachung $\Phi(s)$ (Integrated Information Theory / IIT 4.0, Giulio Tononi):**
  * $\Phi(0) = 1.00\text{ nats}$ (Maximale systemische Kohärenz und autopoietische Gesundheit)
  * $\Phi(l_1, r_1) = 0.70\text{ nats}$ (Leichte Auslenkung)
  * $\Phi(l_2, r_2) = 0.15\text{ nats}$ (Kritische Gefahrenzone)
* **Conatus-VETO:** Fällt die prognostizierte Vitalität unter $\Phi < 0.25\text{ nats}$, sperrt das Conatus-Veto den schädlichen Steuerbefehl sofort und erzwingt stabilisierende Dämpfung.

---

## 5. Handlungsplanung ($G^*$-Minimierung) & Der Gesamte Regelkreis

### 1.3 Der vollständige geschlossene Regelkreis (Stufe 3: Kräfte, Handlungen & Tensoren)

Aus der Synthese von Cart-Pole-Mechanik (Stufe 1) und diskretem Zustands-Kompass (Stufe 2) entsteht die vollständige geschlossene Architektur:

![3. Vollständiges Planares ACI-System: Kinematik, Kräfte & 5x5-Tensoren](inverted_pendulum_step3_complete.svg)

#### Dynamische Elemente des Regelkreises:
* **Kippmoment $\tau_{\text{grav}} = m g L \sin\theta$:** Bei Auslenkung zieht die Schwerkraft $\vec{F}_g$ den Schwerpunkt abwärts.
* **Wiederherstellende Beschleunigung $\vec{a}_{\text{base}}$:** Der Agent setzt die Aktion $a = r$ (Rechtsbeschleunigung), um den Drehpunkt unter die Masse zu fahren.
* **Erwartete Freie Energie ($G^*$):** Die Aktionsauswahl minimiert künftige Überraschung und schützt die systemische Vitalität $\Phi$ über den Zeithorizont $H \ge 2$:

$$G^*(a) = G_{\text{pragmatisch}}(a) - \lambda_\Phi \cdot \Phi(a, H) \cdot \sqrt{H} + \Omega_{\text{conatus\_veto}}$$

* **Pragmatischer Term:** $-\mathbb{E}_{q(s_{t+1})}[\mathbf{C}]$ (Abstand zum phänotypischen Attraktor $s_0$).
* **Conativer Vitalitätsterm:** Prognostizierte Integrität $\Phi$, gewichtet mit Zeittiefe $\sqrt{H}$.
* **Conatus-Veto:** Sinkt die Vitalität unter $\Phi < 0.25\text{ nats}$, springt $G^* \to +\infty$ und blockiert gefährliche Steuerimpulse.

---

## 6. Online-Lernen — Erfahrungszähler (Kausales Gedächtnis)

### Wie der Agent Ursache und Wirkung lernt: Das Strichlisten-Prinzip

Traditionelle neuronale Netze und Reinforcement Learning benötigen Millionen Trainingsschritte, GPU-Cluster und leiden unter katastrophalem Vergessen („Catastrophic Forgetting“).

In Active Inference lernt das System physikalische Kausalgesetze so transparent wie das Führen einer **Erfahrungs-Strichliste**:

1. **Das Erfahrungsfach $\beta$:**  
   Für jede Kombination aus Ausgangszustand $s$, Aktion $a$ und Folgezustand $s'$ besitzt der Agent einen einfachen Zähler $\beta_{s', s, a}$.
2. **Echtzeit-Inkrementierung:**  
   Befindet sich das Pendel in Zustand $s$ (z. B. $r_1$), setzt der Wagen Aktion $a = r$ und landet das Pendel in $s'$ (Ruhelage $s_0$), erhält dieses Fach sofort einen Zählerpunkt:
   $$\beta_{s', s, a} \leftarrow \beta_{s', s, a} + 1$$
3. **Von Zählern zu Wahrscheinlichkeiten:**  
   Zur Vorhersage künftiger Übergänge $\mathbf{B}(a)$ berechnet der Agent schlicht den relativen Anteil:
   $$\mathbf{B}_{s', s, a} = P(s' \mid s, a) = \frac{\text{Beobachtete Häufigkeit von }(s \xrightarrow{a} s')}{\text{Gesamte Erfahrungen in Zustand } s \text{ mit Aktion } a} = \frac{\beta_{s', s, a}}{\sum_{s''} \beta_{s'', s, a}}$$

#### Industrielle Vorteile für Edge- und Mikrocontroller-Steuerungen:
* **Sofortiges Lernen in einem Schritt ($O(1)$):** Keine Gradientenabstiegsschleifen oder Backpropagation; sofortige Aktualisierung bei mechanischen Veränderungen.
* **Kein katastrophales Vergessen:** Frühere physikalische Erfahrungen bleiben in ihren Zählfächern sicher konserviert.
* **Deterministisch & C99-bereit:** Reines Hochzählen von Ganz- oder Gleitkommazahlen ohne Speicherallokation (`malloc`).

*(In der mathematischen Statistik wird dieses Zählverfahren als Dirichlet-Verteilung formalisiert – physikalisch ist es schlicht empirische Erfahrungsspeicherung.)*

---

## 7. Grundsatzfragen & Didaktische FAQ

### FAQ 1: Was macht dieses System „intelligent“?
Intelligenz ist in diesem Framework **weder passive statistische Textvorhersage (LLMs) noch blinde Belohnungsjagd (Reinforcement Learning)**.  
Intelligenz ist **aktive Homeostase und vorausschauende Autopoiese unter Rauschen und Störungen**:
* **Inferenz statt Reflex:** Statt wie ein PID-Regler blind auf Messfehler zu reagieren, pflegt der Agent eine interne generative Hypothese. Er filtert Rauschen heraus, rekonstruiert den wahren Zustand $s$ und plant über Zeithorizonte $H \ge 2$ voraus.
* **Autopoietischer Selbsterhalt (Conatus):** Der Regler jagt keinen von Menschen vorgegebenen Punktestand; sein Antrieb entspringt dem fundamentalen Schutz der eigenen Existenz und Systemvitalität ($\Phi$).

---

### FAQ 2: Was lernt der Agent?
Der Agent lernt die **wahren Kausalgesetze seiner Mechanik und Umwelt**:
* Er verfeinert den Tensor $\mathbf{B}(s' \mid s, a)$: *„Wenn ich im Zustand $s$ bin und Aktion $a$ ausführe: Mit welcher Wahrscheinlichkeit lande ich in $s'$?“*
* Ändert sich die Schienenreibung oder die Stablänge, passt sich das Kausalmodell im Betrieb sofort an.

---

### FAQ 3: Wie lernt der Agent?
Über **exakte Bayes'sche Zähler-Updates (Erfahrungs-Strichlisten)** statt über Gradientenabstiege:
* Der Agent führt Pseudocount-Matrizen $\beta_{s', s, a}$.
* Jede reale Beobachtung verfeinert die Übergangsmatrix $\mathbf{B}$ unmittelbar.
* **Vorteil:** Numerisch exakt, sofort wirksam und ohne Speicherüberlauf.

---

### FAQ 4: Was ist das Weltmodell in diesem Beispiel?
Das **Weltmodell** ist die generative Repräsentation der Umwelt im Agenten:
* **Zustandskompass $\mathcal{S}$:** $\{0, l_1, l_2, r_1, r_2\}$ für die wahre Auslenkung.
* **Sensormodell $\mathbf{A}$:** Abbildung von realem Zustand auf verrauschte Messung.
* **Kausaldynamik $\mathbf{B}(a)$:** Übergangstensor für die Wirkung der Motorbeschleunigung.

---

### FAQ 5: Was ist das Generative Modell in diesem Beispiel?
Die vollständige Verbundwahrscheinlichkeitsverteilung über Beobachtungen, Zustände, Handlungen und Präferenzen:
$$P(o, s, a) = P(o \mid s) \cdot P(s \mid s_{t-1}, a) \cdot P(s_0) \cdot P_{\text{prior}}(a)$$
ergänzt um den conativen Phänotypvektor $\mathbf{C} = \ln P(o)$ und die systemische Vitalität $\Phi(s)$. Es gestattet das geistige Durchspielen alternativer Zukünfte vor dem Auslösen von Motorströmen.

---

### FAQ 6: Klassischer PID vs. Active Conative Inference (ACI) — Unterschiede, Schwächen und Vorteile

#### 1. Was klassischer PID ist und wie er arbeitet
* **Proportional (P):** Stellkraft proportional zum aktuellen Regelfehler $e(t) = \theta_{\text{soll}} - \theta_{\text{ist}}$.
* **Integral (I):** Summiert vergangene Abweichungen auf $\int e(\tau) d\tau$.
* **Derivative (D):** Dämpft die Änderungsgeschwindigkeit $\frac{de(t)}{dt}$.

#### 2. Schwächen klassischer PID-Regler
* **Kein Kausalmodell:** PID weiß nichts über Ursache und Wirkung; er kann nicht zwei Schritte in die Zukunft blicken.
* **Rauschempfindlichkeit (D-Term-Verstärkung):** Das Differenzieren verstärkt Sensorrauschen extrem und führt zu Motorflattern.
* **Integral-Windup:** Bei starken Störungen läuft der I-Speicher voll und verursacht extremes Überschwingen.
* **Kein Selbsterhalt:** PID steuert selbst dann mit Vollgas weiter, wenn das System mechanisch bricht.

#### 3. Vorteile klassischer PID-Regler
* Minimaler Rechenaufwand (~10 Fließkommaoperationen).
* Bewährt und intuitiv für einfache lineare Arbeitspunkte.

#### 4. Vorteile von Active Conative Inference (ACI)
* **Optimales Bayes-Filtern:** Trennt Sensorrauschen von physikalischer Realität über Matrix $\mathbf{A}$.
* **Vorausschauende Planung ($H \ge 2$):** Verhindert Überschwingen, bevor es entsteht.
* **Autonomer Conatus-Schutz:** Conatus-Veto verhindert Motorschäden und Getriebebrüche.
* **Echtzeit-Adaption:** Passt sich veränderten Reibungswerten im Betrieb ohne manuelles Nachtrimmen an.

---

### FAQ 7: Wie arbeitet das Conatus-Veto am Invertierten Pendel konkret?

#### 1. Das Problem: Peitscheneffekt (Whiplash)
Beim schnellen Aufrichten aus starker Neigung erzeugt die Massenträgheit hohe kinetische Energie. Ein kurzsichtiger Regler ($H = 1$) reißt den Wagen zurück, wodurch der Stab auf die Gegenseite durchschlägt und abstürzt.

#### 2. Die conative Invariante: Vitalitätsabbildung $\Phi(s)$
Nach Spinozas Conatus-Prinzip strebt jedes autopoietische System nach Selbsterhalt. Über IIT 4.0 (Giulio Tononi) wird dies messbar:
* Aufrecht ($s_0$): Maximale Systemvitalität $\Phi = 1.00\text{ nats}$.
* Leichte Neigung ($l_1, r_1$): Stabiler Vitalitätsbereich $\Phi = 0.70\text{ nats}$.
* Gefahrenzone ($l_2, r_2$): Starker Vitalitätsabfall auf $\Phi = 0.15\text{ nats}$.

#### 3. Auslösen des Conatus-Vetos
Das Conatus-Prinzip besagt, dass der Schutz des Systems und der Erhalt der physischen Integrität absoluten Vorrang vor Aufgabenanforderungen haben.
* Vor jedem Steuerimpuls prüft der Agent die prognostizierte Vitalität über $H = 2$:
$$\Phi_{\text{prognose}}(a) < 0.25\text{ nats} \implies G^*(a) \to +\infty$$
* Der zerstörerische Befehl wird verworfen; stattdessen greift eine stabilisierende Notdämpfung.

---

### FAQ 8: Warum kein Python in harter Echtzeit — und wie löst ACI dies auf Edge-Hardware?

#### 1. Python als didaktischer Prototyp vs. natives C99 in Produktion
Dieses Dokument und das begleitende Jupyter-Notebook sind ein didaktischer Simulator für Übersicht und mathematische Klarheit.

In der industriellen Robotik (patentiert durch Conative Systems S.à r.l.):
* **Kein Python im Feld:** Null Python, null PyTorch, keine externen Bibliotheken.
* **Reiner ANSI-C99-Kern:** Der gesamte Inferenz- und Planungskern läuft in freistehendem C99.

#### 2. Die Pfeiler der nativen C99-ACI-Engine
* **Kein dynamischer Heap (`malloc`/`free` verboten):** Alle Tensoren, Vektoren und Arbeitsbereiche liegen fest im statischen Speicher. Keine Fragmentierung, keine Latenzsprünge.
* **Deterministische Ausführung unter $50\,\mu\text{s}$:** Garantiert feste Rechenzeiten, passend für $1\,\text{kHz}$- oder $10\,\text{kHz}$-Regeltakte.
* **Bare-Metal-Portabilität:** Kompiliert auf ARM Cortex-M4/M7, STM32, ESP32, RISC-V sowie Industrie-SPS via CANopen oder EtherCAT.
* **Funktionale Sicherheit (MISRA-C-Konformität):** Vollständig verifizierbar nach ISO 26262 und IEC 61508.

---

### FAQ 9: Wie beherrscht man die Mathematik ohne händisches Coden von Tensoren?

#### Die Lösung: Die Conative Studio IDE
Zur Überbrückung der Hürde zwischen theoretischer Neuro-Kybernetik und deterministischem Embedded-Code entwickelte Conative Systems die **Conative Studio IDE**:
* **Visuelle Modellierung:** Zustandsräume, Beobachtungen und Kausaltensoren werden grafisch definiert.
* **Formale Verifikation:** Automatische Prüfung auf Ergodizität, Normalisierung und zuverlässiges Greifen des Conatus-Vetos vor Code-Generierung.
* **1-Klick-C99-Codegenerierung:** Erzeugt optimierte, freistehende Quelldateien (`aci_core.h`, `aci_core.c`) ohne externe Abhängigkeiten.
* **Hardware-in-the-Loop-Simulation:** Echtzeit-Testlauf gegen digitale Zwillinge vor dem Aufspielen auf die Zielhardware.

---

### FAQ 10: Tritt das „Dark Room Problem“ beim Invertierten Pendel auf?

#### 1. Was ist das „Dark Room Problem“?
In der Kognitionswissenschaft lautet eine klassische Kritik am Free Energy Principle:  
*„Wenn ein System nur sensorische Überraschung minimiert: Warum setzt es sich nicht einfach in einen dunklen, leeren Raum, schließt die Augen und bleibt regungslos stehen?“*

Am Invertierten Pendel entspräche der „Dark Room“ dem **Umkippen auf den Tisch und Abschalten des Motors**:
* Liegt der Stab flach am Boden, bewegt sich nichts mehr.
* Die Messwerte sind absolut vorhersehbar und frei von Überraschungen ($F \approx 0$).
* Ein naiver Algorithmus ohne Conatus würde diesen Zustand anstreben.

#### 2. Wie Conatus und Systemvitalität $\Phi(s)$ das Problem lösen
Active Conative Inference schließt dieses Fehlverhalten kategorisch aus:
1. **Phänotypische Präferenz ($\mathbf{C}$):** Flach auf dem Boden zu liegen ist mit katastrophaler Aversion belegt ($\mathbf{C} = -8.0$).
2. **Vitalitätsmaximierung ($\Phi$):** Regungslos am Boden zu liegen bedeutet $\Phi \approx 0.0\text{ nats}$ (Verlust der systemischen Integration).
3. **Der Conatus-Imperativ:** Das System existiert, um aktiv gegen die Entropie anzukämpfen. Das Aufrechtstehen gegen die Schwerkraft ist der physische Beweis dieser Lebendigkeit.
