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

## Akademische Bibliographie (Auswahl)

1. **Chalmers, D. J. (1995).** *Facing up to the problem of consciousness.* Journal of Consciousness Studies, 2(3), 200–219.
2. **Eigen, M. (1971).** *Selforganization of matter and the evolution of biological macromolecules.* Die Naturwissenschaften, 58(10), 465–523.
3. **Fountas, Z., Sajid, N., Mediano, P. A. M., & Friston, K. (2020).** *Deep active inference agents using Monte-Carlo methods.* NeurIPS 2020, 33, 11662–11675.
4. **Friston, K. (2010).** *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience, 11(2), 127–138.
5. **Husserl, E. (1928).** *Vorlesungen zur Phänomenologie des inneren Zeitbewusstseins.* Max Niemeyer Verlag.
6. **Kastrup, B. (2019).** *The Idea of the World.* Iff Books.
7. **Metzinger, T. (2009).** *The Ego Tunnel.* Basic Books.
8. **Monod, J. (1970).** *Le Hasard et la Nécessité.* Éditions du Seuil.
9. **Riebl, T. (2026).** *The Conative-Integrative Framework (CIF).* Master Monographie, Luxemburg.
10. **Roth, G. (2021).** *Wie das Gehirn die Seele macht.* Klett-Cotta.
11. **Schopenhauer, A. (1819).** *Die Welt als Wille und Vorstellung.* F. A. Brockhaus.
12. **Spinoza, B. (1677).** *Ethica, ordine geometrico demonstrata.*
13. **Tononi, G., Albantakis, L., et al. (2023).** *Integrated Information Theory (IIT) 4.0.* PLOS Computational Biology, 19(10), e1011465.

---

## Tool Attribution & Colophon

> [!NOTE]
> **Tooling Colophon:**  
> Diese theoretische Abhandlung, philosophische Architektur und wissenschaftliche Monographie wurden von **Thomas Riebl** (Luxemburg) im Rahmen des **Conative-Integrative Framework (CIF)** konzipiert und verfasst.  
> Die formale Modellierung, Simulationsskripte, Vektordiagramme und die mehrformatige Buchkompilierung (Amazon KDP Print-PDF $6 \times 9''$, Word `.docx`) wurden mit Unterstützung von **Google Gemini (Antigravity Advanced Agentic Coding System)** (September 2026) realisiert.
