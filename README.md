# APTpy — Spectrum Analyser

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23296361.svg)](https://doi.org/10.5281/zenodo.23296361)

APTpy is an open-source project intended to grow into a practical, accessible
toolbox for atom-probe tomography (APT) data analysis. **APTpy — Spectrum
Analyser** is the first component of that larger project.

This release provides a JupyterLab interface for exploring candidate ions in
APT mass spectra. It reads EPOS data through [APAV](https://gitlab.com/jesseds/apav),
generates literature-informed atomic and molecular-ion candidates, displays
their expected mass-to-charge positions and natural-isotope fingerprints, and
exports candidate lists and spectrum data for further analysis.

The initial scientific focus is Fe–C–Mn–Al–Si-based alloys, including the
broader advanced high-strength steel (AHSS) literature centred on Fe–C–Mn
systems. The catalogue also includes selected H-, O- and Ga-related signals
that can be useful when considering hydrogen charging, surface chemistry,
residual gas, or FIB/preparation effects.

## Why APTpy?

APT mass spectra can contain overlapping isotope patterns, multiple charge
states, molecular ions, and signals whose origin depends on the specimen and
the analysis conditions. A candidate list is therefore most useful when it
shows not only a calculated mass-to-charge position, but also the evidence and
limitations behind that candidate.

The starting point for APTpy is a literature review of reported APT ion
assignments in Fe–C–Mn–Al–Si and related AHSS. The reviewed candidates were
organised into an evidence-led catalogue with three important distinctions:

- **Reported/direct** — an ion was explicitly assigned by the source.
- **Overlap/co-assigned** — the ion was reported or discussed, but its peak
  also has competing assignments.
- **Tentative or condition-dependent** — the ion was suggested only under
  particular conditions, in supplementary material, or as an alternative
  interpretation.

These distinctions are displayed in the project files and are intended to keep
the interface scientifically useful without implying that every listed ion is
uniquely present in every specimen.

## Relationship to APAV

APTpy — Spectrum Analyser is an independent, complementary JupyterLab tool
built on top of [APAV](https://gitlab.com/jesseds/apav). It does not replace
APAV and is not an official APAV interface.

The project follows the direction described in the APAV FAQ, **“Why is there
no GUI for APAV?”** APAV is intended to be used as a Python library; a GUI may
exist alongside APAV, but not as a replacement. APAV already provides custom
interactive plotting tools for selected computations. APTpy explores how a
user-friendly interface can be added alongside that library and, in the longer
term, developed into a broader free APT data-analysis toolbox.

Please cite APAV separately when it is used in an analysis:

> Smith, J. D., & Young, M. L. (2023). APAV: An Open-Source Python Package
> for Mass Spectrum Analysis in Atom Probe Tomography. *Journal of Open Source
> Software, 8*(83), 4862. <https://doi.org/10.21105/joss.04862>

## Current scientific scope

The literature-informed core catalogue is based on reported ions in steels
containing Fe–Mn–C, with closely related Fe–C–Mn–Al–Si and AHSS studies used
where relevant. The current interface is organised as follows:

### Basic ions

- Atomic ions of Fe, Mn, C, Si and Al, with literature-supported charge states.
- Carbon clusters such as C₂, C₃ and C₄ in the reported charge states.
- The mixed FeC₂²⁺ candidate.

### Advanced ions

- Other reported alloy states, including selected Fe³⁺ and Si⁺ candidates.
- Hydrogen-related candidates such as H⁺, H₂⁺ and FeH⁺.
- Oxygen-related candidates such as O⁺, OH⁺, O₂⁺ and FeO²⁺.
- Ga⁺ and Ga²⁺ as possible FIB/preparation-related signals.
- Explicitly tentative alternatives such as C₂²⁺ at the 12 Da position.

The catalogue is deliberately finite and conservative. It is not intended to
generate every chemically possible formula. A formula is not treated as an
APT assignment merely because a compound or precipitate with that formula is
known. New candidates should be added only after their APT evidence and exact
source location have been checked.

## Main workflow

The intended analysis sequence is:

```text
EPOS data
    → literature-informed candidate generation
    → isotope fingerprints and overlap review
    → spectrum overlay and colour-coded ion families
    → candidate-list and spectrum export
```

The interface supports:

- Loading an EPOS file once and reusing it while candidate selections change.
- Choosing candidates through beginner-friendly Basic and Advanced tabs.
- Showing isotope fingerprints beside molecular-ion choices.
- Linking each catalogue entry to its literature source and evidence status.
- Showing the selected ion families in distinct colours on the spectrum.
- Saving and loading a project configuration as JSON.
- Adding manual candidate peaks for hypotheses not yet in the catalogue.
- Exporting an interactive Plotly HTML spectrum.
- Exporting measured spectrum data and the selected candidate positions.
- Exporting a tab-separated candidate list containing ion name, charge and
  mass-to-charge information.

## Scientific interpretation and limitations

APTpy — Spectrum Analyser is a candidate-generation and spectrum-exploration
tool. It does not automatically prove the identity of a peak, determine the
phase from which an ion evaporated, or replace expert interpretation.

Reported ions may behave differently depending on alloy composition, local
chemistry, crystallographic environment, specimen preparation, laser or
voltage pulsing, hydrogen charging, detection conditions and background
signals. Isotope fingerprints are calculated reference patterns; their
relative intensities should not be interpreted as a complete prediction of
APT peak intensities.

In particular, overlapping assignments such as C⁺/C₂²⁺ near 12 Da,
C₂⁺/C₄²⁺ in the 24–26 Da region, Al⁺/Fe²⁺ near 27 Da, and C₃⁺/FeO²⁺ near
36 Da should be evaluated using the complete isotope pattern, experimental
context and the original literature.

The accompanying evidence files are a curated literature record rather than a
systematic or exhaustive review. Before using the catalogue as publication
evidence, verify each assignment against the version of record and document
any additions or changes.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Run in JupyterLab

Start JupyterLab:

```bash
jupyter lab
```

Run the two Python cells in the same Jupyter kernel, in this order:

```python
%run cell1_core_basic_advanced.py
```

```python
%run cell2_gui_basic_advanced.py
```

Alternatively, open `APTpy_Spectrum_Analyser.ipynb` and run its cells from top
to bottom. Enter the path to your own EPOS file in the interface. EPOS data
files are not included in this repository.

## Repository contents

- `APTpy_Spectrum_Analyser.ipynb` — notebook version of the complete workflow.
- `cell1_core_basic_advanced.py` — isotope calculations, evidence-led ion
  catalogue, candidate generation and plotting functions.
- `cell2_gui_basic_advanced.py` — Basic/Advanced Jupyter widgets, project
  save/load, plotting callbacks and export controls.
- `ION_EVIDENCE.md` — human-readable literature review and evidence notes.
- `ion_evidence.json` — machine-readable evidence catalogue.
- `test_basic_advanced_core.py` — basic tests for catalogue and calculations.
- `requirements.txt` — Python dependencies.
- `LICENSE` — GNU General Public License version 3 or later.

## Literature basis

The initial catalogue was assembled from literature covering medium-Mn,
high-Mn, pearlitic, high-silicon and related AHSS studied by APT. Representative
sources include:

- Wei et al. (2021), *Patterns*, 2, 100192. [doi:10.1016/j.patter.2020.100192](https://doi.org/10.1016/j.patter.2020.100192)
- Toji et al. (2014), *Acta Materialia*, 65, 215–228. [doi:10.1016/j.actamat.2013.10.064](https://doi.org/10.1016/j.actamat.2013.10.064)
- Toji et al. (2016), *Acta Materialia*, 116, 250–262. [doi:10.1016/j.actamat.2016.06.044](https://doi.org/10.1016/j.actamat.2016.06.044)
- Kwok et al. (2020), *Materials Science and Engineering A*, 782, 139258. [doi:10.1016/j.msea.2020.139258](https://doi.org/10.1016/j.msea.2020.139258)
- Rementeria et al. (2017), *Acta Materialia*, 125, 359–368. [doi:10.1016/j.actamat.2016.12.013](https://doi.org/10.1016/j.actamat.2016.12.013)
- Wang et al. (2024), *npj Materials Degradation*, 8, 119. [doi:10.1038/s41529-024-00528-9](https://doi.org/10.1038/s41529-024-00528-9)
- Marceau et al. (2013), *Ultramicroscopy*, 132, 239–247. [doi:10.1016/j.ultramic.2013.01.010](https://doi.org/10.1016/j.ultramic.2013.01.010)
- Niu et al. (2024), *Acta Materialia*, 281, 120327. [doi:10.1016/j.actamat.2024.120327](https://doi.org/10.1016/j.actamat.2024.120327)

The complete evidence notes, source locations and qualifications are maintained
in `ION_EVIDENCE.md` and `ion_evidence.json`.

## Status and future direction

APTpy is an actively developing research tool. This release establishes the
first APTpy component: a literature-informed, transparent candidate workflow
for APT spectrum analysis. Future development may add more automated spectrum
assistance, broader alloy systems, improved validation, reusable Python
modules, worked examples and additional analysis tools under the APTpy
umbrella.

## Acknowledgment and citation

If APTpy — Spectrum Analyser contributes to a paper, thesis, presentation,
report or other research output, users are kindly requested to acknowledge the
author and cite the software repository. Please also cite the original
literature sources relevant to the ion assignments used in the analysis, and
cite APAV separately.

Suggested acknowledgment:

> The authors acknowledge Roohallah Surki Aliabad for developing APTpy —
> Spectrum Analyser, an open-source JupyterLab tool for literature-informed
> candidate-ion generation, isotope-fingerprint inspection and APT mass-
> spectrum visualization based on APAV.

Suggested software citation:

> Aliabad, R. S. (2026). *APTpy — Spectrum Analyser* (Version 1.0.1)
> [Computer software]. Zenodo.
> <https://doi.org/10.5281/zenodo.23296361>

Suggested APAV citation:

> Smith, J. D., & Young, M. L. (2023). APAV: An Open-Source Python Package
> for Mass Spectrum Analysis in Atom Probe Tomography. *Journal of Open Source
> Software, 8*(83), 4862. <https://doi.org/10.21105/joss.04862>

## License and attribution

This project is distributed under the
[GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.html).

APTpy — Spectrum Analyser is an independent companion tool built on APAV. It
does not replace APAV. Please retain the APAV attribution and license notices
when using or redistributing this work, and verify license compatibility before
redistributing modified or combined software.
