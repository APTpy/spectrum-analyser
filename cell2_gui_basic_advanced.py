"""Cell 2: two-tab beginner interface for the published-ion catalogue.

Run cell1_core_basic_advanced.py first in the same Jupyter kernel.
Requires ipywidgets, plotly and APAV for EPOS plotting.
"""

from html import escape
from pathlib import Path
import csv
import io

import ipywidgets as widgets
from IPython.display import display

if "ION_CATALOG" not in globals():
    raise RuntimeError("Run cell1_core_basic_advanced.py first in this notebook.")


# No elements and no ions are selected by default.
element_widgets = {
    symbol: widgets.Checkbox(value=False, description=symbol, indent=False,
                             layout=widgets.Layout(width="70px"))
    for symbol in ELEMENT_ORDER
}
ion_widgets = {
    ion["key"]: widgets.Checkbox(value=False, description=ion["label"],
                                 indent=False,
                                 layout=widgets.Layout(width="100px"))
    for ion in ION_CATALOG
}
ion_rows = {}
group_rows = {}

for ion in ION_CATALOG:
    principal = principal_peak(ion)
    isotope_positions = isotope_position_summary(ion)
    source_url = escape(ion["source_url"], quote=True)
    source_name = escape(ion["source"])
    badge = " <span style='color:#B45309'>[tentative]</span>" if ion["evidence"] == "tentative only" else (
        " <span style='color:#A44336'>[overlap]</span>" if ion["evidence"] in ("overlap", "co-assigned") else ""
    )
    detail = widgets.HTML(
        value=(
            f"<span style='font-size:12px'>main <b>{principal['mass']:.6f}</b> Da/e; "
            f"isotopes (nominal m/z, Da/e): {escape(isotope_positions)}{badge}<br>"
            f"<a href='{source_url}' target='_blank'>{source_name}</a>"
            f" — {escape(ion['note'])}</span>"
        ),
        layout=widgets.Layout(width="calc(100% - 110px)"),
    )
    row = widgets.HBox(
        [ion_widgets[ion["key"]], detail],
        layout=widgets.Layout(width="100%", align_items="flex-start",
                              padding="6px 4px", border_bottom="1px solid #E5E7EB"),
    )
    ion_rows[ion["key"]] = row
    group_rows.setdefault((ion["tab"], ion["group"]), []).append(row)


def make_accordion(tab_name, ordered_groups):
    children = [widgets.VBox(group_rows[(tab_name, group)],
                             layout=widgets.Layout(width="100%"))
                for group in ordered_groups]
    accordion = widgets.Accordion(children=children,
                                  layout=widgets.Layout(width="100%"))
    for index, group in enumerate(ordered_groups):
        accordion.set_title(index, group)
    accordion.selected_index = 0 if tab_name == "Basic" else None
    return accordion


basic_accordion = make_accordion(
    "Basic", ("Atomic ions", "Carbon clusters", "Metal–carbon ion")
)
advanced_accordion = make_accordion(
    "Advanced", ("Other reported alloy states", "Hydrogen-related",
                 "Oxygen-related", "FIB/preparation signal",
                 "Tentative alternative")
)

def _selected_elements():
    return {symbol for symbol, control in element_widgets.items() if control.value}


def _selected_ions():
    elements = _selected_elements()
    return [ion for ion in ION_CATALOG
            if ion_widgets[ion["key"]].value and ion_is_available(ion, elements)]


def refresh_ion_rows(_=None):
    elements = _selected_elements()
    for ion in ION_CATALOG:
        available = ion_is_available(ion, elements)
        ion_rows[ion["key"]].layout.display = "" if available else "none"
        if not available and ion_widgets[ion["key"]].value:
            ion_widgets[ion["key"]].value = False


for control in element_widgets.values():
    control.observe(refresh_ion_rows, names="value")
for control in ion_widgets.values():
    control.observe(refresh_ion_rows, names="value")


epos_widget = widgets.Text(
    value="", description="EPOS file:",
    placeholder="Paste the full path to your .epos or .EPOS file",
    layout=widgets.Layout(width="100%"),
)
lower_widget = widgets.FloatText(value=0.0, description="Lower m/z:")
upper_widget = widgets.FloatText(value=200.0, description="Upper m/z:")
bin_widget = widgets.FloatText(value=0.01, description="Bin width:")
scale_widget = widgets.ToggleButtons(
    options=[("Linear", "linear"), ("Logarithmic", "log")],
    value="log", description="Y-axis:",
)
manual_widget = widgets.Textarea(
    value="",
    placeholder=("Unknown peak: 37.123; possible ion: 44.987\n"
                 "One peak per line or separate with semicolons. Manual peaks are not literature-verified."),
    layout=widgets.Layout(width="100%", height="78px"),
)
save_folder_widget = widgets.Text(
    value="", description="Save folder:",
    placeholder="All files use the EPOS filename; blank saves beside EPOS, or enter another folder.",
    layout=widgets.Layout(width="100%"),
)
project_file_widget = widgets.Text(
    value="", description="Project file:",
    placeholder="Save/resume project: paste full .json path to load; blank saves new project beside EPOS.",
    layout=widgets.Layout(width="100%"),
)
save_project_button = widgets.Button(description="Save project", icon="save",
                                     button_style="success")
load_project_button = widgets.Button(description="Load project", icon="folder-open")
project_status = widgets.HTML(value="Project not saved yet.")
blank_button = widgets.Button(description="Plot spectrum only",
                              button_style="info", icon="line-chart")
candidate_button = widgets.Button(description="Plot selected ions",
                                  button_style="success", icon="line-chart")
export_button = widgets.Button(description="Save plot, spectrum and ion list",
                               button_style="primary", icon="download")
status_output = widgets.Output()
plot_output = widgets.Output()

_cached_roi = None
_cached_signature = None
_last_plot_mode = None
_active_project_path = None
_applying_project = False


def _project_message(message, *, error=False):
    color = "#B42318" if error else "#176B45"
    project_status.value = f"<span style='color:{color}'>{escape(message)}</span>"


def _project_path():
    path_text = project_file_widget.value.strip()
    return (Path(path_text).expanduser() if path_text else
            default_project_path(epos_widget.value.strip())).absolute()


def _project_state():
    return {
        "format": PROJECT_FORMAT,
        "version": PROJECT_VERSION,
        "epos_file": epos_widget.value,
        "selected_elements": [symbol for symbol, control in element_widgets.items()
                              if control.value],
        "selected_ion_keys": [ion["key"] for ion in ION_CATALOG
                              if ion_widgets[ion["key"]].value],
        "manual_peaks": manual_widget.value,
        "lower_mz": lower_widget.value,
        "upper_mz": upper_widget.value,
        "bin_width": bin_widget.value,
        "y_scale": scale_widget.value,
        "save_folder": save_folder_widget.value,
    }


def _save_project(_):
    global _active_project_path, _applying_project
    try:
        path = _project_path()
        save_project_file(path, _project_state(),
                          overwrite=(path == _active_project_path))
        _active_project_path = path
        _applying_project = True
        try:
            project_file_widget.value = str(path)
        finally:
            _applying_project = False
        _project_message(f"Project saved: {path}")
    except Exception as error:
        _project_message(f"{type(error).__name__}: {error}", error=True)


def _load_project(_):
    global _active_project_path, _applying_project
    global _last_plot_mode
    try:
        path = _project_path()
        state = load_project_file(path)
        _last_plot_mode = None  # Loading must not redraw a previous project's plot.
        _applying_project = True
        try:
            for control in ion_widgets.values():
                control.value = False
            for symbol, control in element_widgets.items():
                control.value = symbol in state["selected_elements"]
            for key in state["selected_ion_keys"]:
                ion_widgets[key].value = True
            epos_widget.value = state["epos_file"]
            manual_widget.value = state["manual_peaks"]
            lower_widget.value = state["lower_mz"]
            upper_widget.value = state["upper_mz"]
            bin_widget.value = state["bin_width"]
            scale_widget.value = state["y_scale"]
            save_folder_widget.value = state["save_folder"]
            project_file_widget.value = str(path)
            refresh_ion_rows()
        finally:
            _applying_project = False
        _active_project_path = path
        with plot_output:
            plot_output.clear_output()
        _project_message(f"Project loaded: {path}. Click a plot button to redraw the spectrum.")
    except Exception as error:
        _project_message(f"{type(error).__name__}: {error}", error=True)


def _project_file_changed(change):
    global _active_project_path
    if _applying_project or _active_project_path is None:
        return
    if change["new"].strip() != str(_active_project_path):
        _active_project_path = None
        _project_message("Project path changed. Click Save project or Load project.")


save_project_button.on_click(_save_project)
load_project_button.on_click(_load_project)
project_file_widget.observe(_project_file_changed, names="value")


def _settings():
    if lower_widget.value >= upper_widget.value:
        raise ValueError("Lower m/z must be smaller than upper m/z.")
    if bin_widget.value <= 0:
        raise ValueError("Bin width must be positive.")


def _load_roi():
    global _cached_roi, _cached_signature
    path_text = epos_widget.value.strip()
    if not path_text:
        raise ValueError("Enter the full path to your EPOS file.")
    path = Path(path_text).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"EPOS file not found: {path}")
    stat = path.stat()
    signature = (str(path.resolve()), stat.st_mtime_ns, stat.st_size)
    if signature != _cached_signature:
        import apav as ap
        _cached_roi = ap.Roi.from_epos(str(path))
        _cached_signature = signature
    return _cached_roi


def _build_figure(with_candidates):
    _settings()
    selected_ions = _selected_ions() if with_candidates else []
    manual_peaks = parse_manual_candidates(manual_widget.value) if with_candidates else []
    if with_candidates and not selected_ions and not manual_peaks:
        raise ValueError("Select an ion or enter a manual peak, or use 'Plot spectrum only'.")
    roi = _load_roi()
    candidates = selected_candidate_peaks(ion["key"] for ion in selected_ions)
    candidates.extend(manual_peaks)
    figure = make_spectrum_plot(
        roi=roi,
        candidates=candidates,
        lower_mass=lower_widget.value,
        upper_mass=upper_widget.value,
        bin_width=bin_widget.value,
        logarithmic_y=scale_widget.value == "log",
        show_labels=False,
    )
    return figure, selected_ions, candidates


def _plot(with_candidates):
    global _last_plot_mode
    with status_output:
        status_output.clear_output()
        try:
            figure, selected_ions, candidates = _build_figure(with_candidates)
            with plot_output:
                plot_output.clear_output()
                figure.show(config={"scrollZoom": True, "displaylogo": False,
                                    "responsive": True})
            _last_plot_mode = with_candidates
            manual_count = sum(peak["evidence"].startswith("manual") for peak in candidates)
            print(f"Plotted {len(selected_ions)} ion families, {manual_count} manual peaks, "
                  f"and {len(candidates)} candidate lines.")
        except Exception as error:
            print(f"{type(error).__name__}: {error}")


blank_button.on_click(lambda _: _plot(False))
candidate_button.on_click(lambda _: _plot(True))


def _refresh_scale(change):
    # A toggle changes the displayed guide heights immediately; no second
    # click on the plot button is needed. The EPOS data are reused from cache.
    if change["name"] == "value" and _last_plot_mode is not None:
        _plot(_last_plot_mode)


scale_widget.observe(_refresh_scale, names="value")


ACKNOWLEDGMENT = """Acknowledgment and citation

If this software contributes to a publication, presentation, thesis, or other research output, please acknowledge the author and cite the project repository.

Suggested acknowledgment:
The authors acknowledge Roohallah Surki Aliabad for developing APTpy — Spectrum Analyser, a publicly available JupyterLab tool for candidate-ion generation and mass-spectrum visualization based on APAV.

Suggested software citation:
Roohallah Surki Aliabad. APTpy — Spectrum Analyser. https://github.com/R-Surki/apt-candidate-list-maker. Accessed [DATE].

Please also cite APAV separately when it is used in the analysis:
Smith, J. D., & Young, M. L. (2023). APAV: An Open-Source Python Package for Mass Spectrum Analysis in Atom Probe Tomography. Journal of Open Source Software, 8(83), 4862. https://doi.org/10.21105/joss.04862
"""


def export_selected_ions(_):
    with status_output:
        status_output.clear_output()
        try:
            _settings()
            selected_ions = _selected_ions()
            use_candidates = bool(selected_ions or manual_widget.value.strip())
            figure, _, peaks = _build_figure(use_candidates)
            html_path, txt_path, csv_path = output_paths_for_epos(
                epos_widget.value.strip(), save_folder_widget.value.strip()
            )
            mass, counts = spectrum_histogram(
                _load_roi(), lower_widget.value, upper_widget.value, bin_widget.value
            )
            buffer = io.StringIO()
            writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
            writer.writerow(["Ion", "Isotopes", "Charge", "m/z (Da/e)",
                             "Nearest integer", "Natural isotope share (%)",
                             "Evidence", "Source", "Source URL"])
            for peak in peaks:
                ion = ION_BY_KEY.get(peak["ion_key"])
                writer.writerow([
                    peak["ion"], peak["isotopes"], peak["charge"],
                    f"{peak['mass']:.8f}", peak["integer_mz"],
                    f"{peak['abundance']:.8f}" if ion else "",
                    ion["evidence"] if ion else "manual (unverified)",
                    ion["source"] if ion else "user-entered",
                    ion["source_url"] if ion else "",
                ])
            spectrum_buffer = io.StringIO()
            spectrum_writer = csv.writer(spectrum_buffer, lineterminator="\n")
            spectrum_writer.writerow(["m/z (Da/e)", "Counts"])
            spectrum_writer.writerows(zip(mass, counts))
            figure.write_html(str(html_path), include_plotlyjs=True, full_html=True)
            txt_path.write_text(buffer.getvalue(), encoding="utf-8")
            csv_path.write_text(spectrum_buffer.getvalue(), encoding="utf-8")
            print(f"Saved plot: {html_path}")
            print(f"Saved measured spectrum ({len(mass)} bins): {csv_path}")
            print(f"Saved {len(selected_ions)} published ion families and "
                  f"{sum(peak['ion_key'].startswith('manual-') for peak in peaks)} "
                  f"manual peaks: {txt_path}")
            print("\n" + ACKNOWLEDGMENT)
        except Exception as error:
            print(f"{type(error).__name__}: {error}")


export_button.on_click(export_selected_ions)


basic_tab = widgets.VBox([
    widgets.HTML("<b>Basic:</b> reported core-steel ions, ordered by element, then carbon clusters and FeC₂²⁺. Overlap notes do not hide candidates."),
    basic_accordion,
])
advanced_tab = widgets.VBox([
    widgets.HTML("<b>Advanced:</b> other published states, H/O/Ga diagnostics, and one explicitly tentative alternative. Isotopes are not separate checkboxes."),
    advanced_accordion,
])
tabs = widgets.Tab(children=[basic_tab, advanced_tab],
                   layout=widgets.Layout(width="100%"))
tabs.set_title(0, "Basic ions")
tabs.set_title(1, "Advanced ions")

interface = widgets.VBox([
    widgets.HTML("<h3>APTpy — Spectrum Analyser</h3>"),
    project_file_widget,
    widgets.HBox([save_project_button, load_project_button]),
    project_status,
    widgets.HTML("<b>1. Ion family selection</b><br>Choose elements, then check the ions you want to plot."),
    widgets.HBox(list(element_widgets.values())),
    tabs,
    widgets.HTML("<b>2 · Plot spectrum</b>"),
    epos_widget,
    widgets.HBox([lower_widget, upper_widget, bin_widget]),
    scale_widget,
    widgets.HTML("<b>Unknown ion peaks (ion name: Da)</b>"),
    manual_widget,
    widgets.HBox([blank_button, candidate_button]),
    widgets.HTML("<b>3 · Export spectrum and candidate positions</b>"),
    widgets.HTML("Save the interactive plot (.html), measured spectrum (.csv), and candidate positions (.txt)."),
    save_folder_widget,
    export_button,
    status_output,
    plot_output,
], layout=widgets.Layout(width="100%"))

refresh_ion_rows()
display(interface)
