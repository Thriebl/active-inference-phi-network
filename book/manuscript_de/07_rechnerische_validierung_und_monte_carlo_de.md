# Kapitel 7: Rechnerische Validierung & Stochastische Phasenräume

> *„Um zu beweisen, dass temporale Tiefe eine notwendige Bedingung für Bewusstsein ist, müssen wir unsere Agenten täuschenden Umgebungen aussetzen, in denen reaktive Heuristiken versagen und nur kontrafaktische Vorausschau das Überleben sichert.“*  
> — **Thomas Riebl**, *Monte Carlo Methodology in Active Inference* (2026)

---

## 7.1 Das stochastische Simulationsparadigma

Um die theoretischen Aussagen rechnerisch zu validieren, implementierten wir eine stochastische POMDP-Simulationsumgebung mit täuschenden Belohnungen (*Deceptive Trap*) und epistemischer Ambiguität (*Cue Site*).

Getestet wurden vier Agenten-Kohorten über ein **Monte-Carlo-Ensemble von $N = 30$ unabhängigen Läufen**:
1. **Reflex-Agent ($H=0$):** Reine Reaktivität ($B = I$).
2. **Kurzsichtiger Agent ($H=1$):** 1-Schritt-Vorausschau.
3. **Mitteltiefer Agent ($H=2$):** 2-Schritt-Planung.
4. **Tiefer Temporaler Agent ($H=4$):** Kontrafaktische Handlungsbäume über 4 Zeitschritte.

---

## 7.2 Empirische Simulationsergebnisse

| Agenten-Kohorte | Zeithorizont ($H$) | Überlebensrate | Asymptotisches $\Phi(t)$ | Epistemische Neugier-Umwege | 6. Axiom Konformität |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Reflex-Agent** | $H = 0$ | **$36.7\,\%$** | $\mathbf{0.068 \pm 0.015}$ | $0.0\,\%$ (Blind in die Falle) | **Verletzt ($\Phi \to 0$)** |
| **Kurzsichtiger Agent** | $H = 1$ | $100.0\,\%$ | $0.162 \pm 0.008$ | $0.0\,\%$ (Kein Umweg möglich) | Knapp erfüllt |
| **Mitteltiefer Agent** | $H = 2$ | $100.0\,\%$ | $0.168 \pm 0.007$ | $35.0\,\%$ (Teilweise) | Erfüllt |
| **Tiefer Temporaler Agent** | $H = 4$ | **$100.0\,\%$** | $\mathbf{0.184 \pm 0.006}$ | **$100.0\,\%$ (Optimal)** | **Vollständig Maximiert** |

---

## 7.3 Visualisierung der Simulationsergebnisse

![Simulationsergebnisse zu temporaler Tiefe und 6. Axiom](../images/Deep_Temporal_Active_Inference_Simulation.png)

### Wichtigste Erkenntnisse:
* **Reaktiver Kausalitätskollaps:** Reflex-Agenten ($H=0$) fallen zu $63.3\%$ der täuschenden Belohnung zum Opfer und stürzen in den Kausalitäts- und Überlebenstod ($\Phi \to 0$).
* **Epistemischer Umweg:** Tiefe temporale Agenten ($H=4$) wählen zu $100\%$ proaktiv einen epistemischen Umweg zur Hinweis-Quelle (*Cue*), lösen die Umweltunsicherheit auf und sichern maximale Kausalkonstanz ($\Phi \approx 0.184$).
