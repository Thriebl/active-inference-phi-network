# Kapitel 9: Mathematischer Anhang, Quellcode & Bibliographie

---

## Anhang A: Mathematische Formalismen

### 1. Das POMDP-Tupel
$$\mathcal{M} = \big\langle \mathcal{S}, \mathcal{O}, \mathcal{U}, A, B, C, D, \gamma \big\rangle$$

* **Likelihood:** $A = P(o_\tau \mid s_\tau) \in \mathbb{R}^{N_o \times N_s}$
* **Übergangstensor:** $B = P(s_{\tau+1} \mid s_\tau, u_\tau) \in \mathbb{R}^{N_s \times N_s \times N_u}$
* **Präferenzen:** $C = \ln P(o) \in \mathbb{R}^{N_o}$
* **Startverteilung:** $D = P(s_1) \in \mathbb{R}^{N_s}$

### 2. Zustandsschätzung (Perzeptuelle Inferenz)
$$q(s_t) = \sigma\Big( \ln A_{o_t, :} + \ln \big( B(u_{t-1}) \cdot q(s_{t-1}) \big) \Big)$$

### 3. Erwartete Freie Energie ($\mathbf{G}$) über Horizont $H$
$$\mathbf{G}(\pi) = \sum_{\tau = t+1}^{t+H} \delta^{\tau - t} \cdot \mathbf{G}(\pi, \tau)$$

$$\mathbf{G}(\pi, \tau) = \sum_{o_\tau} Q(o_\tau \mid \pi) \cdot \Big(\ln Q(o_\tau \mid \pi) - C(o_\tau)\Big) + \sum_{s_\tau} Q(s_\tau \mid \pi) \cdot \mathcal{H}\big(A_{:, s_\tau}\big)$$

### 4. Boltzmann-Politik-Auswahl
$$P(\pi) = \frac{\exp\big(-\gamma \cdot \mathbf{G}(\pi)\big)}{\sum_{\pi'} \exp\big(-\gamma \cdot \mathbf{G}(\pi')\big)}$$

---

## Anhang B: Alphabetisches Glossar der Fachbegriffe

* **Active Inference (Aktive Inferenz):** Das normative mathematische Framework der theoretischen Neurobiologie, das besagt, dass lebendige Organismen ihre Existenz sichern, indem sie Handlungen ausführen, die die erwartete freie Energie ($\mathbf{G}$) minimieren, um sensorische Beobachtungen mit angeborenen Präferenzen in Einklang zu bringen.
* **Alter (Dissoziiertes Bewusstseinszentrum):** Im Analytischen Idealismus ein individueller lebendiger Organismus, der durch die topologische Dissoziation von Mind-at-Large entsteht und durch eine statistische Markov-Decke abgegrenzt ist.
* **Analytischer Idealismus:** Die von Bernardo Kastrup formulierte nicht-duale, ontologisch sparsame Monismus-Lehre, nach der die Wirklichkeit fundamental erfahrungsbasiert ist (*Mind-at-Large*) und physikalische Materie das äußere Erscheinungsbild universaler mentaler Prozesse darstellt.
* **Autopoiese:** Die fundamentale Eigenschaft lebendiger Systeme, ihr eigenes strukturelles und organisatorisches Netzwerk kontinuierlich selbst zu regenerieren und gegen den thermodynamischen Zerfall zu behaupten.
* **Conatus (Der Existenzwille):** Das angeborene Streben jedes Seienden, in seiner Existenz zu verharren und der Zerstörung zu widerstehen (Spinoza). Im CIF formalisiert als Sollzustand $\Phi > 0$.
* **Das 6. Axiom des Bewusstseins:** Das Axiom der *Autopoietischen Kausalkonstanz*, das festlegt, dass echtes Bewusstsein zwingend ein aktives Handeln zur Erhaltung der integrierten Ursache-Wirkungs-Macht über die Zeit erfordert: $\mathbb{E}[\Phi(t+1) \mid \pi^*] \ge \Phi(t)$ (Riebl).
* **Erklärungslücke (*Explanatory Gap*):** Die unüberwindbare Kluft im Physikalismus zwischen quantitativen objektiven Hirnprozessen und qualitativem subjektiven Erleben (Levine).
* **Erwartete Freie Energie ($\mathbf{G}$):** Eine zukunftsgerichtete Metrik zur Bewertung von Handlungsoptionen über einen Planungshorizont $H$, bestehend aus pragmatischem Wert (Zielerfüllung) und epistemischem Wert (Neugier / Ambiguitätsabbau).
* **Integrierte Information ($\Phi$):** Das quantitative Maß für die intrinsische Ursache-Wirkungs-Macht eines maximal irreduziblen physikalischen Substrats über die Minimum Information Partition (Tononi, IIT 4.0).
* **Kritikalität (*Edge of Chaos*):** Der Phasenübergang zwischen starrer Ordnung und chaotischer Turbulenz, an dem Informationstransfer und Integrierte Information ($\Phi$) ihr globales Maximum erreichen.
* **Markov-Decke (*Markov Blanket*):** Eine statistische Trennfläche, die ein System in interne ($\mu$), sensorische ($s$), aktive ($a$) und externe Zustände ($\eta$) unterteilt und das Innere bedingt unabhängig vom Äußeren macht.
* **Mind-at-Large:** Das universale, transpersonale Feld reinen Bewusstseins, das den fundamentalen ontologischen Urgrund der Wirklichkeit bildet (Spinoza, Kastrup).
* **Minimum Information Partition (MIP):** Diejenige Zweiteilung eines Systems, die den geringsten Kausalitätsverlust verursacht; dient zur Berechnung der System-Irreduzibilität $\Phi$.
* **Phänomenales Selbstmodell (PSM):** Eine transparente, kontinuierliche innere Simulation des prädiktiven Gehirns, die die 1.-Person-Perspektive eines stabilen „Ich“ erzeugt (Metzinger).
* **POMDP (Partially Observable Markov Decision Process):** Mathematischer Formalismus für Entscheidungsfindung unter Unsicherheit, definiert durch die Tensoren $A$ (Likelihood), $B$ (Übergänge), $C$ (Werte) und $D$ (Startpriors).
* **Protention:** Die antizipatorische Zukunftserwartung innerhalb der Specious Present, entsprechend Top-Down-Vorhersagen (Husserl).
* **Retention:** Das im Arbeitsgedächtnis festgehaltene unmittelbare Vergangene innerhalb der Specious Present, entsprechend synaptischen Priors (Husserl).
* **Schweres Problem des Bewusstseins (*Hard Problem*):** Die Frage, warum und wie physikalische Informationsverarbeitung jemals subjektives inneres Erleben (*Qualia*) hervorbringen sollte (Chalmers).
* **Specious Present (Gefühlte Gegenwart):** Die triadische, nicht-ausdehnungslose zeitliche Dauer des subjektiven Erlebens ($\sim 500\,\text{ms} - 3\,\text{s}$), die Retention, Urimpression und Protention vereint (James, Husserl).
* **Temporale Tiefe ($H$):** Die Reichweite des kontrafaktischen Planungshorizonts, über den ein Agent Übergangstensoren ($B$) und erwartete freie Energie ($\mathbf{G}$) evaluiert.
* **Theorem der temporalen Mindesttiefe:** Die mathematische Notwendigkeitsbedingung, dass phänomenales Selbstbewusstsein mehrstufige kontrafaktische Planung ($H > 1$) erfordert, um einen Kausalitätskollaps ($\Phi \to 0$) abzuwenden (Riebl).
* **Urimpression:** Die gegenwärtige sensorische Störung an der Markov-Decke, entsprechend dem eingehenden Vorhersagefehler (Husserl).
* **Variationale Freie Energie ($F$):** Eine berechenbare Obergrenze für sensorische Überraschung ($-\ln P(o)$), die während der Wahrnehmung minimiert wird.

---

## Akademische Bibliographie (Auswahl)

1. **Bak, P. (1996).** *How Nature Works: The Science of Self-Organized Criticality.* Copernicus, Springer-Verlag.
2. **Beggs, J. M., & Plenz, D. (2003).** *Neuronal avalanches in neocortical circuits.* Journal of Neuroscience, 23(35), 11167–11177.
3. **Chalmers, D. J. (1995).** *Facing up to the problem of consciousness.* Journal of Consciousness Studies, 2(3), 200–219.
4. **Clark, A. (2016).** *Surfing Uncertainty: Prediction, Action, and the Embodied Mind.* Oxford University Press.
5. **Da Costa, L., Parr, T., Sajid, N., Veselic, S., Neacsu, V., & Friston, K. (2020).** *Active inference on discrete state-spaces: A synthesis.* Journal of Mathematical Psychology, 99, 102447.
6. **Eigen, M. (1971).** *Selforganization of matter and the evolution of biological macromolecules.* Die Naturwissenschaften, 58(10), 465–523.
7. **Fountas, Z., Sajid, N., Mediano, P. A. M., & Friston, K. (2020).** *Deep active inference agents using Monte-Carlo methods.* NeurIPS 2020, 33, 11662–11675.
8. **Friston, K. (2010).** *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience, 11(2), 127–138.
9. **Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., & Pezzulo, G. (2017).** *Active Inference: A Process Theory.* Neural Computation, 29(1), 1–49.
10. **Gershman, S. J. (2019).** *The generative adversary in brain and machine.* Trends in Cognitive Sciences, 23(1), 8–17.
11. **Husserl, E. (1928).** *Vorlesungen zur Phänomenologie des inneren Zeitbewusstseins.* Max Niemeyer Verlag.
12. **Jablonka, E., & Lamb, M. J. (2014).** *Evolution in Four Dimensions.* MIT Press.
13. **James, W. (1890).** *The Principles of Psychology.* Henry Holt and Company.
14. **Kastrup, B. (2019).** *The Idea of the World.* Iff Books.
15. **Kastrup, B. (2021).** *Science Ideated.* Iff Books.
16. **Levine, J. (1983).** *Materialism and qualia: The explanatory gap.* Pacific Philosophical Quarterly, 64(4), 354–361.
17. **Metzinger, T. (2003).** *Being No One: The Self-Model Theory of Subjectivity.* MIT Press.
18. **Metzinger, T. (2009).** *The Ego Tunnel.* Basic Books.
19. **Metzinger, T. (2024).** *The Elephant and the Blind.* MIT Press.
20. **Monod, J. (1970).** *Le Hasard et la Nécessité.* Éditions du Seuil.
21. **Panksepp, J. (1998).** *Affective Neuroscience.* Oxford University Press.
22. **Parr, T., & Friston, K. J. (2018).** *The anatomy of choice: active inference and agency.* Cognitive Neuroscience, 9(1-2), 11–27.
23. **Parr, T., Pezzulo, G., & Friston, K. J. (2022).** *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press.
24. **Riebl, T. (2026).** *The Conative-Integrative Framework (CIF).* Master Monographie, Luxemburg.
25. **Roth, G. (2003).** *Aus Sicht des Gehirns.* Suhrkamp Verlag.
26. **Roth, G. (2021).** *Wie das Gehirn die Seele macht: Emotionen, Bewusstsein, Unbewusstes.* Klett-Cotta.
27. **Schopenhauer, A. (1819/1844).** *Die Welt als Wille und Vorstellung.* F. A. Brockhaus.
28. **Seth, A. K. (2021).** *Being You: A New Science of Consciousness.* Dutton.
29. **Spinoza, B. (1677).** *Ethica, ordine geometrico demonstrata.*
30. **Tononi, G., Albantakis, L., Boly, M., Massimini, M., & Koch, C. (2023).** *Integrated information theory (IIT) 4.0.* PLOS Computational Biology, 19(10), e1011465.
31. **Tschantz, A., Millidge, B., Seth, A. K., & Buckley, C. L. (2020).** *Reinforcement learning through active inference.* arXiv:2002.12636.
32. **Yehuda, R., & Lehrner, A. (2018).** *Intergenerational transmission of trauma effects.* World Psychiatry, 17(3), 243–257.

---

## Tool Attribution & Colophon

> [!NOTE]
> **Tooling Colophon:**  
> Diese theoretische Abhandlung, philosophische Architektur und wissenschaftliche Monographie wurden von **Thomas Riebl** (Luxemburg) im Rahmen des **Conative-Integrative Framework (CIF)** konzipiert und verfasst.  
> Die formale Modellierung, Simulationsskripte, Vektordiagramme und die mehrformatige Buchkompilierung (Amazon KDP Print-PDF $6 \times 9''$, Word `.docx`) wurden mit Unterstützung von **Google Gemini (Antigravity Advanced Agentic Coding System)** (September 2026) realisiert.
