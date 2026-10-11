"""Cell 1: evidence-led APT candidates for Fe-Mn-C-Si-Al steels.

Run this file before cell2_gui_basic_advanced.py in JupyterLab.
The catalogue is deliberately finite: isotope variants are generated from a
selected published ion, not offered as separate ion-selection checkboxes.
"""

from __future__ import annotations

from html import escape
from itertools import product
from math import isfinite, log10
from pathlib import Path
import json
import os
import re
import tempfile


# NIST Atomic Weights and Isotopic Compositions; fractions are terrestrial
# natural values, not measured APT peak heights. 2H (D) is included.
ISOTOPES = {
    "H": ((1, 1.00782503223, 0.999885), (2, 2.01410177812, 0.000115)),
    "C": ((12, 12.0, 0.9893), (13, 13.00335483507, 0.0107)),
    "O": ((16, 15.99491461957, 0.99757), (17, 16.99913175650, 0.00038), (18, 17.99915961286, 0.00205)),
    "Al": ((27, 26.98153853, 1.0),),
    "Si": ((28, 27.97692653465, 0.92223), (29, 28.97649466490, 0.04685), (30, 29.973770136, 0.03092)),
    "Mn": ((55, 54.93804391, 1.0),),
    "Fe": ((54, 53.93960899, 0.05845), (56, 55.93493633, 0.91754), (57, 56.93539284, 0.02119), (58, 57.93327443, 0.00282)),
    "Ga": ((69, 68.9255735, 0.60108), (71, 70.92470258, 0.39892)),
}
ELECTRON_MASS_U = 0.0005485799090441  # NIST 2022 CODATA
ISOTOPE_SOURCE = "https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"
ELECTRON_SOURCE = "https://physics.nist.gov/cgi-bin/cuu/Value?meu"

SOURCES = {
    "Wei 2021": "https://doi.org/10.1016/j.patter.2020.100192",
    "Toji 2014": "https://doi.org/10.1016/j.actamat.2013.10.064",
    "Toji 2016": "https://doi.org/10.1016/j.actamat.2016.06.044",
    "Kwok 2020": "https://doi.org/10.1016/j.msea.2020.139258",
    "Rementeria 2017": "https://doi.org/10.1016/j.actamat.2016.12.013",
    "Wang 2024": "https://doi.org/10.1038/s41529-024-00528-9",
    "Marceau 2013": "https://doi.org/10.1016/j.ultramic.2013.01.010",
    "Niu 2024": "https://doi.org/10.1016/j.actamat.2024.120327",
}


def _ion(key, label, formula, charge, tab, group, source, locator, evidence,
         note=""):
    return {
        "key": key,
        "label": label,
        "formula": formula,
        "charge": charge,
        "tab": tab,
        "group": group,
        "source": source,
        "source_url": SOURCES[source],
        "locator": locator,
        "evidence": evidence,
        "note": note,
    }


# Display order is intentional. No ion is selected by default in Cell 2.
ION_CATALOG = [
    # BASIC — matrix and solute atomic ions.
    _ion("Fe2", "Fe²⁺", {"Fe": 1}, 2, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported", "⁵⁴Fe²⁺ can overlap Al⁺."),
    _ion("Fe1", "Fe⁺", {"Fe": 1}, 1, "Basic", "Atomic ions", "Wei 2021", "Table 2", "co-assigned", "Fe⁺ / FeH⁺ region is co-assigned."),
    _ion("Mn2", "Mn²⁺", {"Mn": 1}, 2, "Basic", "Atomic ions", "Toji 2014", "Section 2.3", "reported"),
    _ion("Mn1", "Mn⁺", {"Mn": 1}, 1, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported"),
    _ion("C1", "C⁺", {"C": 1}, 1, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported", "12 Da can also admit C₂²⁺ as an alternative."),
    _ion("C2charge", "C²⁺", {"C": 1}, 2, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported"),
    _ion("Si2", "Si²⁺", {"Si": 1}, 2, "Basic", "Atomic ions", "Toji 2014", "Section 2.3", "reported", "²⁸Si²⁺ can overlap ¹⁴N⁺."),
    _ion("Al2", "Al²⁺", {"Al": 1}, 2, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported"),
    _ion("Al1", "Al⁺", {"Al": 1}, 1, "Basic", "Atomic ions", "Kwok 2020", "APT mass-to-charge peak list", "overlap", "27 Da can overlap ⁵⁴Fe²⁺."),
    _ion("Al3", "Al³⁺", {"Al": 1}, 3, "Basic", "Atomic ions", "Wei 2021", "Table 2", "reported"),
    # BASIC — carbon clusters and the published mixed carbide ion.
    _ion("C2cluster1", "C₂⁺", {"C": 2}, 1, "Basic", "Carbon clusters", "Toji 2014", "Section 2.3", "overlap", "Some peaks overlap C₄²⁺ isotopologues."),
    _ion("C3cluster1", "C₃⁺", {"C": 3}, 1, "Basic", "Carbon clusters", "Toji 2014", "Section 2.3", "reported"),
    _ion("C3cluster2", "C₃²⁺", {"C": 3}, 2, "Basic", "Carbon clusters", "Wei 2021", "Table 2", "reported"),
    _ion("C4cluster1", "C₄⁺", {"C": 4}, 1, "Basic", "Carbon clusters", "Toji 2016", "APT mass-spectra paragraph", "reported"),
    _ion("C4cluster2", "C₄²⁺", {"C": 4}, 2, "Basic", "Carbon clusters", "Toji 2014", "Section 2.3", "overlap", "Some peaks overlap C₂⁺ isotopologues."),
    _ion("FeC2_2", "FeC₂²⁺", {"Fe": 1, "C": 2}, 2, "Basic", "Metal–carbon ion", "Kwok 2020", "APT mass-to-charge peak list", "overlap", "Wei 2021 also assigns it; other formulas can contribute near 40 Da."),
    # ADVANCED — other verified alloy charge states.
    _ion("Fe3", "Fe³⁺", {"Fe": 1}, 3, "Advanced", "Other reported alloy states", "Rementeria 2017", "Section 3.3", "reported", "Broader Fe–Mn–C–Si steel context."),
    _ion("Si1", "Si⁺", {"Si": 1}, 1, "Advanced", "Other reported alloy states", "Wang 2024", "Supplementary Table S1", "overlap", "Reported in pipeline steel; isotope region can overlap Fe²⁺."),
    # ADVANCED — diagnostic hydrogen, oxygen and preparation-related ions.
    _ion("H1", "H⁺", {"H": 1}, 1, "Advanced", "Hydrogen-related", "Wang 2024", "Hydrogen mass-spectrum discussion", "reported", "A 1 Da signal can originate from residual-gas background."),
    _ion("H2", "H₂⁺", {"H": 2}, 1, "Advanced", "Hydrogen-related", "Wei 2021", "Table 2", "reported", "Check background and preparation controls."),
    _ion("FeH1", "FeH⁺", {"Fe": 1, "H": 1}, 1, "Advanced", "Hydrogen-related", "Wei 2021", "Table 2", "co-assigned", "Co-assigned with Fe⁺ in the cited region."),
    _ion("O1", "O⁺", {"O": 1}, 1, "Advanced", "Oxygen-related", "Wei 2021", "Table 2", "reported"),
    _ion("OH1", "OH⁺", {"O": 1, "H": 1}, 1, "Advanced", "Oxygen-related", "Wei 2021", "Table 2 (HO⁺ notation)", "reported"),
    _ion("O2", "O₂⁺", {"O": 2}, 1, "Advanced", "Oxygen-related", "Wei 2021", "Table 2", "reported"),
    _ion("FeO2charge", "FeO²⁺", {"Fe": 1, "O": 1}, 2, "Advanced", "Oxygen-related", "Wei 2021", "Table 2", "reported"),
    _ion("Ga1", "Ga⁺", {"Ga": 1}, 1, "Advanced", "FIB/preparation signal", "Marceau 2013", "APT mass spectra section", "reported", "Possible gallium implantation during FIB preparation."),
    _ion("Ga2", "Ga²⁺", {"Ga": 1}, 2, "Advanced", "FIB/preparation signal", "Marceau 2013", "APT mass spectra section", "reported", "Possible gallium implantation during FIB preparation."),
    # Explicitly not a verified default candidate.
    _ion("C2cluster2", "C₂²⁺", {"C": 2}, 2, "Advanced", "Tentative alternative", "Niu 2024", "Figure 2 and text", "tentative only", "Upper-bound alternative to C⁺ at 12 Da; not uniquely demonstrated."),
]
ION_BY_KEY = {item["key"]: item for item in ION_CATALOG}
ELEMENT_ORDER = ("Fe", "C", "Mn", "Si", "Al", "H", "O", "Ga")


def ion_is_available(ion, selected_elements):
    """Only display a formula when all its elements have been chosen."""
    return set(ion["formula"]).issubset(set(selected_elements))


def isotope_peaks(ion):
    """Enumerate every stable-isotope combination for one selected ion.

    Identical atoms are aggregated by isotopologue; their probabilities sum,
    so C₂ with one ¹³C is counted twice and remains one plotted peak.
    """
    atom_symbols = [symbol for symbol, count in ion["formula"].items()
                    for _ in range(count)]
    combined = {}
    for combination in product(*(ISOTOPES[s] for s in atom_symbols)):
        isotope_ids = tuple(sorted((symbol, item[0])
                                   for symbol, item in zip(atom_symbols, combination)))
        probability = 1.0
        for item in combination:
            probability *= item[2]
        if isotope_ids not in combined:
            combined[isotope_ids] = {
                "mass_u": sum(item[1] for item in combination),
                "probability": 0.0,
                "nominal_mass": sum(item[0] for item in combination),
            }
        combined[isotope_ids]["probability"] += probability

    peaks = []
    charge = ion["charge"]
    for isotope_ids, record in combined.items():
        isotope_label = "·".join(f"{mass_number}{symbol}"
                                 for symbol, mass_number in isotope_ids)
        exact_mz = (record["mass_u"] - charge * ELECTRON_MASS_U) / charge
        peaks.append({
            "ion_key": ion["key"],
            "ion": ion["label"],
            "isotopes": isotope_label,
            "charge": charge,
            "mass": exact_mz,
            "nominal_mz": record["nominal_mass"] / charge,
            "integer_mz": round(exact_mz),
            "abundance": 100.0 * record["probability"],
            "source_url": ion["source_url"],
            "evidence": ion["evidence"],
            "category": ion["group"],
            "family": ion["label"],
            "label": ion["label"],
        })
    return sorted(peaks, key=lambda peak: peak["mass"])


def principal_peak(ion):
    return max(isotope_peaks(ion), key=lambda peak: peak["abundance"])


def isotope_position_summary(ion):
    """Show every isotope combination at its one-decimal nominal m/z.

    Keeping the isotope labels distinguishes combinations that share the same
    nominal position. Exact masses remain available in plots and exports.
    """
    return "; ".join(
        f"{peak['isotopes']}: {peak['nominal_mz']:.1f}"
        for peak in isotope_peaks(ion)
    )


def selected_candidate_peaks(selected_keys):
    """Create all isotope lines for checked ion families, in catalogue order."""
    selected_keys = set(selected_keys)
    return [peak for ion in ION_CATALOG if ion["key"] in selected_keys
            for peak in isotope_peaks(ion)]


def parse_manual_candidates(text):
    """Read `ion name: m/z` entries separated by newlines or semicolons.

    Manual peaks are single positions supplied by the user, not literature
    assignments or generated isotope families.
    """
    candidates = []
    for entry in re.split(r"[;\n]+", text):
        entry = entry.strip()
        if not entry:
            continue
        if ":" not in entry:
            raise ValueError(f"Manual peak needs 'ion name: m/z': {entry}")
        label, mass_text = entry.rsplit(":", 1)
        label = label.strip()
        if not label:
            raise ValueError("A manual peak needs an ion name before the colon.")
        try:
            mass = float(mass_text.strip())
        except ValueError as error:
            raise ValueError(f"Invalid m/z for manual peak {label!r}.") from error
        if not isfinite(mass) or mass <= 0:
            raise ValueError(f"Manual m/z must be a positive finite number: {label!r}.")
        candidates.append({
            "ion_key": f"manual-{len(candidates)}",
            "ion": label,
            "label": label,
            "isotopes": "user-entered position",
            "charge": "",
            "mass": mass,
            "nominal_mz": None,
            "integer_mz": round(mass),
            "abundance": 100.0,
            "source_url": "",
            "evidence": "manual (unverified)",
            "category": "Manual peaks",
            "family": label,
        })
    return candidates


def output_paths_for_epos(epos_filename, folder_text=""):
    """Return unused HTML/TXT/CSV paths named after the EPOS file.

    An empty folder uses the EPOS directory. A supplied folder redirects all
    outputs. Repeated exports receive matching _2, _3, ... suffixes.
    """
    epos_path = Path(epos_filename).expanduser()
    folder = Path(folder_text).expanduser() if folder_text.strip() else epos_path.parent
    if not folder.is_dir():
        raise FileNotFoundError(f"Save folder does not exist: {folder}")
    for number in range(1, 1001):
        suffix = "" if number == 1 else f"_{number}"
        html_path = folder / f"{epos_path.stem}{suffix}.html"
        txt_path = folder / f"{epos_path.stem}{suffix}.txt"
        csv_path = folder / f"{epos_path.stem}{suffix}.csv"
        if not any(path.exists() for path in (html_path, txt_path, csv_path)):
            return html_path, txt_path, csv_path
    raise FileExistsError("No unused output name found in the save folder.")


PROJECT_FORMAT = "apt-candidate-list-maker-project"
PROJECT_VERSION = 1


def default_project_path(epos_filename):
    """Suggest a project filename beside the EPOS file."""
    if not str(epos_filename).strip():
        raise ValueError("Enter an EPOS path or a project-file path first.")
    epos_path = Path(epos_filename).expanduser()
    return epos_path.with_name(f"{epos_path.stem}.apt-project.json")


def validate_project_state(state):
    """Validate a saved session without requiring APAV or a live EPOS file."""
    if not isinstance(state, dict) or state.get("format") != PROJECT_FORMAT:
        raise ValueError("This is not an APTpy — Spectrum Analyser project file.")
    if type(state.get("version")) is not int or state["version"] != PROJECT_VERSION:
        raise ValueError("Unsupported project-file version.")
    for name in ("selected_elements", "selected_ion_keys"):
        values = state.get(name)
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise ValueError(f"Project field {name!r} must be a list of names.")
        if len(values) != len(set(values)):
            raise ValueError(f"Project field {name!r} contains duplicates.")
    elements = set(state["selected_elements"])
    keys = set(state["selected_ion_keys"])
    if elements - set(ELEMENT_ORDER):
        raise ValueError(f"Unknown element(s) in project: {sorted(elements - set(ELEMENT_ORDER))}")
    if keys - set(ION_BY_KEY):
        raise ValueError(f"Unknown ion key(s) in project: {sorted(keys - set(ION_BY_KEY))}")
    if any(not ion_is_available(ION_BY_KEY[key], elements) for key in keys):
        raise ValueError("A selected ion requires an element not selected in this project.")
    for name in ("epos_file", "manual_peaks", "save_folder"):
        if not isinstance(state.get(name), str):
            raise ValueError(f"Project field {name!r} must be text.")
    for name in ("lower_mz", "upper_mz", "bin_width"):
        value = state.get(name)
        if type(value) not in (int, float) or not isfinite(value):
            raise ValueError(f"Project field {name!r} must be a finite number.")
    if state.get("y_scale") not in ("linear", "log"):
        raise ValueError("Project y-axis scale must be linear or log.")
    return state


def save_project_file(filename, state, *, overwrite=False):
    """Write a validated JSON project atomically; never silently replace one."""
    state = validate_project_state(state)
    path = Path(filename).expanduser()
    if path.suffix.lower() != ".json":
        raise ValueError("Project filename must end in .json.")
    if not path.parent.is_dir():
        raise FileNotFoundError(f"Project folder does not exist: {path.parent}")
    if path.exists() and not overwrite:
        raise FileExistsError(f"Project already exists: {path}. Load it, or choose a new filename.")
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", prefix=f".{path.name}.",
            suffix=".tmp", dir=path.parent, delete=False,
        ) as output:
            temporary_name = output.name
            json.dump(state, output, ensure_ascii=False, indent=2)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        if overwrite:
            os.replace(temporary_name, path)
        else:
            os.link(temporary_name, path)
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    return path


def load_project_file(filename):
    """Read and validate a JSON project before changing any GUI controls."""
    path = Path(filename).expanduser()
    with path.open("r", encoding="utf-8") as project_file:
        return validate_project_state(json.load(project_file))


def spectrum_histogram(roi, lower_mass, upper_mass, bin_width):
    """Return exactly the bins and counts used by the displayed spectrum."""
    mass, counts = roi.mass_histogram(
        bin_width=bin_width, lower=lower_mass, upper=upper_mass,
        multiplicity="all",
    )
    mass, counts = list(mass), list(counts)
    if len(mass) != len(counts):
        raise ValueError("APAV returned different lengths for m/z and counts.")
    return mass, counts


PALETTE = (
    "#2166AC", "#D73027", "#1B7837", "#762A83", "#E08214", "#008B8B",
    "#8C510A", "#C51B7D", "#4D4D4D", "#7FBC41", "#A6761D", "#1F78B4",
    "#B15928", "#6A3D9A", "#E31A1C", "#33A02C", "#FB9A99", "#CAB2D6",
    "#B2DF8A", "#FDBF6F", "#006D2C", "#08519C", "#A50F15", "#54278F",
)
DASHES = ("solid", "dash", "dot", "dashdot")


def _style_for(ion_key):
    if ion_key.startswith("manual-"):
        index = len(ION_CATALOG) + int(ion_key.split("-", 1)[1])
    else:
        index = next(i for i, ion in enumerate(ION_CATALOG) if ion["key"] == ion_key)
    return {
        "color": PALETTE[index % len(PALETTE)],
        "dash": DASHES[index // len(PALETTE) % len(DASHES)],
    }


def make_spectrum_plot(roi, candidates, lower_mass=0.0, upper_mass=200.0,
                       bin_width=0.01, logarithmic_y=False, show_labels=False):
    """Plot EPOS histogram and optional literature-backed isotope guide lines."""
    import plotly.graph_objects as go

    mass, counts = spectrum_histogram(roi, lower_mass, upper_mass, bin_width)
    if not mass or not counts or not any(value > 0 for value in counts):
        raise ValueError("No positive spectrum counts in this m/z interval.")
    positive = [value for value in counts if value > 0]
    y_max = float(max(positive))
    y_min = max(1.0, float(min(positive)))
    y_top_limit = y_max * 1.5 if y_max > 1 else 10.0
    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        x=mass, y=counts, mode="lines", name="Measured spectrum",
        line={"color": "#24292F", "width": 1}, showlegend=False,
        hovertemplate="m/z %{x:.5f}<br>Counts %{y:.0f}<extra></extra>",
    ))

    family_peaks = {}
    for candidate in candidates:
        if lower_mass <= candidate["mass"] <= upper_mass:
            family_peaks.setdefault(candidate["ion_key"], []).append(candidate)

    plotted_ions = list(ION_CATALOG)
    for key, peaks in family_peaks.items():
        if key.startswith("manual-"):
            plotted_ions.append({"key": key, "label": peaks[0]["ion"],
                                 "evidence": "manual (unverified)",
                                 "manual": True})

    def family_abundance_max(ion):
        if ion.get("manual"):
            return max(peak["abundance"] for peak in family_peaks[ion["key"]])
        return max(peak["abundance"] for peak in isotope_peaks(ion))

    # Candidate heights are proportional to isotope abundance in data units.
    # Plotly then applies the requested axis transform. Do not interpolate the
    # abundance fraction across the logarithmic screen height: that makes a
    # log plot's guides behave like a linear-abundance slider.
    reference_height = 0.84 * y_top_limit
    visible_tops = []
    for ion in plotted_ions:
        peaks = family_peaks.get(ion["key"], [])
        if peaks:
            largest = family_abundance_max(ion)
            visible_tops.extend(reference_height * p["abundance"] / largest
                                for p in peaks)
    log_floor = max(1e-12, min(y_min, min(visible_tops) * 0.5)) if visible_tops else y_min

    for ion in plotted_ions:
        peaks = family_peaks.get(ion["key"], [])
        if not peaks:
            continue
        peak_max = family_abundance_max(ion)
        style = _style_for(ion["key"])
        tallest = max(peaks, key=lambda peak: peak["abundance"])
        for peak in peaks:
            fraction = peak["abundance"] / peak_max
            line_base = log_floor if logarithmic_y else 0.0
            line_top = reference_height * fraction
            hover_text = (
                f"<b>{escape(ion['label'])}</b><br>"
                f"User-entered m/z: {peak['mass']:.6f} Da/e<br>"
                "Manual peak; not literature-verified<extra></extra>"
                if ion.get("manual") else
                f"<b>{escape(ion['label'])}</b><br>"
                f"Isotopes: {escape(peak['isotopes'])}<br>"
                f"Calculated m/z: {peak['mass']:.6f} Da/e<br>"
                f"Natural isotope share: {peak['abundance']:.5f}%<br>"
                f"Evidence: {escape(ion['evidence'])}<extra></extra>"
            )
            fig.add_trace(go.Scatter(
                x=[peak["mass"], peak["mass"]],
                y=[line_base, line_top], mode="lines", showlegend=False,
                line={"color": style["color"], "width": 2,
                      "dash": style["dash"]},
                hovertemplate=hover_text,
            ))
            if show_labels and peak is tallest:
                fig.add_annotation(
                    x=peak["mass"], y=line_top, text=escape(ion["label"]),
                    showarrow=False, yshift=8, font={"size": 10,
                    "color": style["color"]},
                )

    fig.update_layout(
        title="APT mass spectrum and selected candidate positions",
        template="plotly_white", height=750, hovermode="closest",
        showlegend=False, margin={"l": 75, "r": 40, "t": 75, "b": 80},
        dragmode="pan",
    )
    fig.update_xaxes(title="Mass-to-charge ratio (Da/e)",
                     range=[lower_mass, upper_mass], rangeslider_visible=True)
    fig.update_yaxes(title="Counts", type="log" if logarithmic_y else "linear",
                     range=[log10(log_floor), log10(max(y_top_limit, log_floor * 10))]
                     if logarithmic_y else [0, y_top_limit])
    return fig
