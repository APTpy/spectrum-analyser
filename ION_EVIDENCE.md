# Literature-reported APT ions for Fe–Mn–C–Si–Al steels

Curated candidate list, version 0.2 (8 October 2026). This file records **ion
assignments reported by authors**, not proof that a particular ion is present
in another specimen. It is deliberately conservative. The search was broadened
and documented below, but it is **not yet a systematic or exhaustive review**.
The code in `cell1_core.py` does **not** yet use this list.

Scope: ion formulas contain only Fe, Mn, C, Si, and Al. The cited steel must
contain Fe–Mn–C; Si and Al may be present or absent, and additional alloying
elements are permitted but noted. Hydrogen-, oxygen-, gallium-, nitrogen-, and
other trace-element ions are outside this list. A precipitate formula such as
Fe₃C or M₆C is **not** itself an APT ion assignment.

Evidence classes:

- **Direct**: authors explicitly assigned this ion in an APT mass spectrum.
- **Overlap**: authors assigned or discussed this ion, but the cited peak has
  competing assignments; it must not be presented as uniquely identified.
- **Possible only**: a source names the ion as a possible contributor but did
  not range it as a distinct ion. Keep separate from the verified list.

## Verified reported candidates

The numbers below are approximate positions of the principal isotopologue on
the mass-to-charge axis, not every isotope peak. Exact positions and isotope
combinations must be calculated separately by the software. `Core` denotes a
closely related Fe–Mn–C–Si/Al steel; `Broader` denotes an Fe–Mn–C steel with
additional elements or a different alloy balance.

| Ion | Principal position | Evidence | Context | Exact evidence location | Important caveat |
| --- | ---: | --- | --- | --- | --- |
| C²⁺ | 6 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14]; [Kwok 2020, APT methods][kwok20] | Carbon monomer charge state. |
| C⁺ | 12 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14]; [Kwok 2020, APT methods][kwok20] | 12 Da may also admit C₂²⁺; [Niu 2024][niu24] uses C₂²⁺ only as an upper-bound alternative. |
| C₂⁺ | 24 | Overlap | Core | [Li 2011, “Mass spectrum analyses”][li11]; [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14]; [Seol 2016, “Mass spectrum”][seol16]; [Rementeria 2017, §3.3][rementeria17]; [Kwok 2020][kwok20] | 24–26 Da can overlap C₄²⁺ isotopologues. |
| C₃²⁺ | 18 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14]; [Seol 2016, “Mass spectrum”][seol16]; [Kwok 2020][kwok20] | The 18/18.5 Da peaks of `CCC+` in Kwok must be the doubly charged trimer. |
| C₃⁺ | 36 | Direct | Core | [Toji 2014, §2.3][toji14]; [Seol 2016, “Mass spectrum”][seol16]; [Kwok 2020][kwok20] | 36 Da can coincide with oxide species if O is considered later. |
| C₄²⁺ | 24 | Overlap | Core | [Li 2011, “Mass spectrum analyses”][li11]; [Toji 2014, §2.3][toji14]; [Toji 2015, APT mass-spectra paragraph][toji15]; [Rementeria 2017, §3.3][rementeria17]; [Kohne 2022, APT peak assignment][kohne22] | 24.5 Da mixed-isotope peak supports its contribution, but 24–26 Da also admits C₂⁺. |
| C₄⁺ | 48 | Direct | Core | [Toji 2016, APT mass-spectra paragraph][toji16] | Reported in a Fe–Mn–C–Si comparison steel; not automatically expected in every specimen. |
| Fe²⁺ | 28 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14] | ⁵⁴Fe²⁺ at 27 Da overlaps Al⁺. |
| Fe⁺ | 56 | Overlap | Core | [Wei 2021, Table 2][wei]; also [Wang 2024, Supplementary Table S1][wang24] | Wei co-assigns the Fe⁺ isotope region with FeH⁺. |
| Fe³⁺ | 18.7 | Direct | Broader | [Wang 2024, Supplementary Table S1][wang24]; [Rementeria 2017, §3.3][rementeria17] | Reported in steels with Mn and Si; may be minor in medium-Mn steel. |
| Mn²⁺ | 27.5 | Direct | Core | [Toji 2014, §2.3][toji14]; [Wang 2024, Supplementary Table S1][wang24] | ⁵⁵Mn is the stable isotope used for the principal position. |
| Mn⁺ | 55 | Direct | Core | [Wei 2021, Table 2][wei] | Distinct from Mn²⁺ at 27.5 Da. |
| Si²⁺ | 14 | Direct | Core | [Toji 2014, §2.3][toji14]; [Toji 2016, APT mass-spectra paragraph][toji16] | ²⁸Si²⁺ at 14 Da may overlap N⁺ if N is considered later. |
| Si⁺ | 28 | Overlap | Broader | [Wang 2024, Supplementary Table S1][wang24] | The 28–29 Da isotope region overlaps Fe²⁺; supplementary table also lists ³⁰Si⁺. |
| Al⁺ | 27 | Overlap | Core | [Kwok 2020, APT methods][kwok20]; [Zou 2026, APT methods][zou26]; [Aliabad 2026, APT analysis][aliabad26] | Reported by peak decomposition against ⁵⁴Fe²⁺; not a uniquely resolved 27 Da peak. |
| Al²⁺ | 13.5 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14]; [Kwok 2020][kwok20] | Aluminium has one stable isotope, ²⁷Al. |
| Al³⁺ | 9 | Direct | Core | [Wei 2021, Table 2][wei]; [Toji 2014, §2.3][toji14] | Aluminium has one stable isotope, ²⁷Al. |
| FeC₂²⁺ | 40 | Overlap | Core | [Wei 2021, Table 2 and text below it][wei]; [Kwok 2020, APT methods][kwok20] | Two studies assigned it; Wei's algorithm also offered CN₂⁺ and C₂O⁺ at 40 Da. |

## Possible contributor, not a clean verified assignment

| Ion | Position | Source | Why separated |
| --- | ---: | --- | --- |
| C₂²⁺ | 12 | [Li 2011, “Mass spectrum analyses”][li11]; [Niu 2024, Fig. 2 and text][niu24] | Both papers discuss C₂²⁺ at the ambiguous 12 Da peak; Niu assigned it entirely to C₂²⁺ only in an intentionally upper-bound carbon estimate, while their lower-bound model assigned it to C⁺. It is not uniquely demonstrated; [Yao thesis, §2.2.4][yao-thesis] reports negligible C₂²⁺ in another Fe–Mn–Al–C dataset based on absent mixed-isotope support. |

## Deliberately excluded from the verified set

FeC⁺, FeC²⁺, MnC⁺, MnC₂⁺, SiC⁺, AlC⁺, C₅⁺,
Fe₃C⁺, and M₆C⁺ are **not included merely because their formulas can be
generated or a carbide phase is present**. They can be re-evaluated if a
published APT assignment in an in-scope Fe–Mn–C specimen is documented with an
exact figure, table, or passage. FeC²⁺ is discussed in a thesis on other steels,
which is not sufficient evidence for this restricted peer-reviewed set.

## Reference keys

[wei]: https://doi.org/10.1016/j.patter.2020.100192 "Wei et al. (2021), Machine-learning-enhanced time-of-flight mass spectrometry analysis, Patterns 2, 100192. Fe–Mn–C–Al alloy, Table 2."
[toji14]: https://doi.org/10.1016/j.actamat.2013.10.064 "Toji et al. (2014), Atomic-scale analysis of carbon partitioning between martensite and austenite by atom probe tomography and correlative transmission electron microscopy, Acta Materialia 65, 215–228."
[toji15]: https://doi.org/10.1016/j.actamat.2014.11.049 "Toji et al. (2015), Carbon partitioning during quenching and partitioning heat treatment accompanied by carbide precipitation, Acta Materialia 86, 137–147."
[toji16]: https://doi.org/10.1016/j.actamat.2016.06.044 "Toji et al. (2016), Effect of Si on the acceleration of bainite transformation by pre-existing martensite, Acta Materialia 116, 250–262."
[seol16]: https://doi.org/10.1016/j.actamat.2016.01.007 "Seol et al. (2016), Combined atom probe tomography and density functional theory investigation of the Al off-stoichiometry of κ-carbides in an austenitic Fe–Mn–Al–C low density steel, Acta Materialia 106, 229–238."
[wang24]: https://doi.org/10.1038/s41529-024-00528-9 "Wang et al. (2024), Systematic quantification of hydrogen in pipeline steel by atom probe tomography after ambient charging and transfer, npj Materials Degradation 8, 119; Supplementary Table S1."
[aliabad26]: https://doi.org/10.1016/j.matdes.2026.115582 "Aliabad et al. (2026), Decoding the role of pre-existing austenite in transformation pathways during slow heating of cold-rolled medium-Mn steel for process design, Materials & Design 263, 115582."
[kwok20]: https://doi.org/10.1016/j.msea.2020.139258 "Kwok et al. (2020), Design of a high strength, high ductility 12 wt% Mn medium manganese steel with hierarchical deformation behaviour, Materials Science and Engineering A 782, 139258; APT methods, mass-to-charge peak list. [Author-uploaded online full text](https://www.researchgate.net/publication/340041515_Design_of_a_high_strength_high_ductility_12_wt_Mn_medium_manganese_steel_with_hierarchical_deformation_behaviour)."
[rementeria17]: https://doi.org/10.1016/j.actamat.2016.12.013 "Rementeria et al. (2017), Carbon concentration measurements by atom probe tomography in the ferritic phase of high-silicon steels, Acta Materialia 125, 359–368; §3.3. [Author-uploaded online full text](https://www.researchgate.net/publication/312167644_Carbon_concentration_measurements_by_atom_probe_tomography_in_the_ferritic_phase_of_high-silicon_steels)."
[niu24]: https://doi.org/10.1016/j.actamat.2024.120327 "Niu et al. (2024), Hydrogen-enhanced deformation in pearlite, Acta Materialia 281, 120327; Fig. 2 and corresponding text."
[zou26]: https://doi.org/10.1002/srin.202501305 "Zou et al. (2026), Near-Atomic Investigation on the Elemental Redistribution During Coprecipitation of Nano-Sized Kappa-Type and B2 Precipitates in an Al-Alloyed Lightweight Steel, steel research international; APT methods."
[marceau13]: https://doi.org/10.1016/j.ultramic.2013.01.010 "Marceau et al. (2013), Understanding the detection of carbon in austenitic high-Mn steel using atom probe tomography, Ultramicroscopy 132, 239–247; mass-spectrum section."
[li11]: https://doi.org/10.1016/j.ultramic.2010.11.010 "Li et al. (2011), Atom probe tomography characterization of heavily cold drawn pearlitic steel wire, Ultramicroscopy 111, 628–632; mass spectrum analyses."
[kohne22]: https://doi.org/10.3390/ma15196653 "Kohne et al. (2022), Correlation of Heterogeneous Local Martensite Tetragonality and Carbon Distribution in High Carbon Steel, Materials 15, 6653; APT peak assignment."
[yao-thesis]: https://publications.rwth-aachen.de/record/689464 "Yao, κ-carbide in a high-Mn light-weight steel, thesis, §2.2.4; contextual evidence, not counted as a peer-reviewed ion source."

## Search and screening notes (8 October 2026)

This update used web searches of publisher pages, PubMed, institutional pages,
and indexed author-uploaded online text; **no remote PDF was downloaded**.
Queries covered combinations of `Fe-Mn-C`, `Fe-Mn-Al-C`, `Fe-Mn-Si-C`,
`medium Mn`, `TWIP`, `bainite`, and `pearlite` with `atom probe`, `mass
spectrum`, `peak assignment`, `molecular ions`, plus targeted `FeC`, `MnC`,
`SiC`, `AlC`, `C2`, `C4`, and charge-state searches. Results were screened for
an Fe–Mn–C specimen and an actual APT ion assignment; search hits about
precipitate formulas alone were rejected. The exact number of records returned,
deduplication, and database coverage were **not** recorded, so this cannot be
described as a systematic review or as every published ion.

Newly inspected primary reports and their contribution:

| Source | Steel / focus | Screening outcome |
| --- | --- | --- |
| [Marceau 2013][marceau13] | Fe–22Mn–0.6C | Mass-spectra discussion confirms Fe and Mn charge peaks; carbon molecular ions are discussed but exact formulas require checking Fig. 1. |
| [Li 2011][li11] | Fe–0.98C–0.31Mn–0.20Si–0.20Cr pearlitic steel | Explicit 6–36 Da carbon peak list and C₂²⁺/C⁺ and C₄²⁺/C₂⁺ ambiguities. |
| [Rementeria 2017][rementeria17] | Three Fe–Mn–C–Si steels, with Cr/Ni/Mo variations | Explicit C monomer/dimer/trimer/tetramer, Fe³⁺, Si²⁺ and Mn²⁺ assignments; 24 Da C₂⁺/C₄²⁺ overlap. |
| [Kohne 2022][kohne22] | Fe–0.74C–1.2Mn–0.2Si–1.1Cr high-carbon steel | Explicit carbon peak groups, including C₄²⁺ at 24.5 Da. |
| [Kwok 2020][kwok20] | Fe–12Mn–4.8Al–2Si–0.32C–0.3V | Explicit multi-ion peak list; adds a second FeC₂²⁺ source and an actual Al⁺ overlap decomposition. |
| [Niu 2024][niu24] | Fe–Mn–C–Si pearlitic steel | C₂²⁺ was evaluated only as an upper-bound alternative, not a unique assignment. |
| [Zou 2026][zou26] | Fe–Al–Mn–Ni–C lightweight steel | Confirms Al⁺/⁵⁴Fe²⁺ overlap; does not add a new ion family. |
| [Aliabad 2026][aliabad26] | Fe–0.4C–6Mn–2Al–1Si–0.05Nb | Reports a 27 Da Al⁺/Fe²⁺ decomposition; full mass-spectrum definitions are in Supplement 2 and remain to be checked. |

Other located Fe–Mn–C APT studies (e.g. [Souza Filho 2019](https://doi.org/10.1016/j.actamat.2018.12.046), [Guo 2022](https://doi.org/10.1016/j.actamat.2021.117601), and [Sauvage et al.](https://map.materials-science.info/?detail-publ=https%3A%2F%2Fmap.materials-science.info%2Fwork%2Fftccsdartic_oai_hal_hal-01324531v1&person=https%3A%2F%2Fmap.materials-science.info%2Fperson%2F0000-0001-8247-803x&view=detail)) describe elemental partitioning or co-segregation in their readily accessible text, but no explicit *new* ion formula was extracted. They are not evidence for extra ions.

Before using this as a publication-quality review, a domain expert should check
each cited passage against the version of record, especially the supplementary
table column distinction for Si⁺ and the charge notation in older typeset
articles. Add a search protocol and a dated update process if claiming
systematic completeness. In particular, conduct a database search with stored
queries, dates, result counts and deduplicated records; inspect supplementary
peak tables and figures in every eligible paper; and seek a second independent
reviewer. No remote PDF was downloaded to create this file.
