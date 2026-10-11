"""Dependency-light checks for the two-tab candidate implementation."""

import math
import runpy
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import cell1_core_basic_advanced as core


class FakeFigure:
    def __init__(self):
        self.traces = []
        self.yaxis = {}
        self.annotations = []

    def add_trace(self, trace):
        self.traces.append(trace)

    def add_annotation(self, **kwargs):
        self.annotations.append(kwargs)

    def update_layout(self, **kwargs):
        self.layout = kwargs

    def update_xaxes(self, **kwargs):
        self.xaxis = kwargs

    def update_yaxes(self, **kwargs):
        self.yaxis = kwargs


class FakeRoi:
    def mass_histogram(self, **_):
        return [11.5, 12.0, 12.5, 13.0], [100, 1000, 500, 50]


def fake_plotly_modules():
    plotly = types.ModuleType("plotly")
    graph_objects = types.ModuleType("plotly.graph_objects")
    graph_objects.Figure = FakeFigure
    graph_objects.Scattergl = lambda **kwargs: {"kind": "spectrum", **kwargs}
    graph_objects.Scatter = lambda **kwargs: {"kind": "candidate", **kwargs}
    plotly.graph_objects = graph_objects
    return {"plotly": plotly, "plotly.graph_objects": graph_objects}


def fake_widget_modules():
    class Layout:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class Widget:
        def __init__(self, value=None, layout=None, **kwargs):
            self._value = value
            self.layout = layout or Layout()
            self.__dict__.update(kwargs)
            self._observers = []
            self._click_callbacks = []

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, new):
            if new != self._value:
                old, self._value = self._value, new
                for callback in self._observers:
                    callback({"name": "value", "old": old, "new": new})

        def observe(self, callback, names=None):
            self._observers.append(callback)

        def on_click(self, callback):
            self._click_callbacks.append(callback)

        def click(self):
            for callback in self._click_callbacks:
                callback(self)

        def set_title(self, *_):
            pass

        def clear_output(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return False

    ipywidgets = types.ModuleType("ipywidgets")
    ipywidgets.Layout = Layout
    for name in ("Checkbox", "Text", "FloatText", "ToggleButtons", "Textarea",
                 "Button", "Output", "HTML", "VBox", "HBox", "Accordion", "Tab"):
        setattr(ipywidgets, name, Widget)
    ipython = types.ModuleType("IPython")
    ipython_display = types.ModuleType("IPython.display")
    ipython_display.display = lambda *_: None
    ipython.display = ipython_display
    return {"ipywidgets": ipywidgets, "IPython": ipython,
            "IPython.display": ipython_display}


class CandidateTests(unittest.TestCase):
    def test_catalogue_and_charge_division(self):
        self.assertEqual(len(core.ION_CATALOG), 28)
        self.assertEqual(sum(i["tab"] == "Basic" for i in core.ION_CATALOG), 16)
        self.assertAlmostEqual(core.principal_peak(core.ION_BY_KEY["Fe2"])["mass"],
                               27.966919585, places=6)
        self.assertAlmostEqual(core.principal_peak(core.ION_BY_KEY["FeC2_2"])["mass"],
                               39.966919585, places=6)
        for ion in core.ION_CATALOG:
            self.assertAlmostEqual(sum(p["abundance"] for p in core.isotope_peaks(ion)),
                                   100, places=6)

    def test_all_isotope_positions_are_displayed_to_one_decimal(self):
        silicon = core.isotope_position_summary(core.ION_BY_KEY["Si2"])
        self.assertEqual(silicon, "28Si: 14.0; 29Si: 14.5; 30Si: 15.0")
        for ion in core.ION_CATALOG:
            displayed = core.isotope_position_summary(ion).split("; ")
            self.assertEqual(len(displayed), len(core.isotope_peaks(ion)))
            for item, peak in zip(displayed, core.isotope_peaks(ion)):
                self.assertEqual(item, f"{peak['isotopes']}: {peak['nominal_mz']:.1f}")

    def test_log_axis_changes_visual_candidate_height(self):
        peaks = core.selected_candidate_peaks(["C1"])
        with patch.dict(sys.modules, fake_plotly_modules()):
            linear = core.make_spectrum_plot(FakeRoi(), peaks, 0, 14, 0.01,
                                             logarithmic_y=False)
            logarithmic = core.make_spectrum_plot(FakeRoi(), peaks, 0, 14, 0.01,
                                                  logarithmic_y=True)
        linear_lines = [t for t in linear.traces if t["kind"] == "candidate"]
        log_lines = [t for t in logarithmic.traces if t["kind"] == "candidate"]
        self.assertEqual(len(linear_lines), 2)
        self.assertEqual(logarithmic.yaxis["type"], "log")
        self.assertEqual(linear.yaxis["type"], "linear")
        # Same physical abundance ratio, but a log y-axis makes the minor
        # isotope visibly taller than its 1%-of-height linear presentation.
        linear_ratio = linear_lines[1]["y"][1] / linear_lines[0]["y"][1]
        log_floor = log_lines[1]["y"][0]
        log_ratio = ((math.log10(log_lines[1]["y"][1]) - math.log10(log_floor)) /
                     (math.log10(log_lines[0]["y"][1]) - math.log10(log_floor)))
        self.assertGreater(log_ratio, linear_ratio)
        self.assertFalse(logarithmic.annotations)

    def test_export_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            epos = root / "sample.EPOS"
            epos.touch()
            self.assertEqual(core.output_paths_for_epos(epos),
                             (root / "sample.html", root / "sample.txt", root / "sample.csv"))
            (root / "sample.html").touch()
            self.assertEqual(core.output_paths_for_epos(epos),
                             (root / "sample_2.html", root / "sample_2.txt", root / "sample_2.csv"))
            elsewhere = root / "elsewhere"
            elsewhere.mkdir()
            self.assertEqual(core.output_paths_for_epos(epos, str(elsewhere)),
                             (elsewhere / "sample.html", elsewhere / "sample.txt", elsewhere / "sample.csv"))
            (elsewhere / "sample.csv").touch()
            self.assertEqual(core.output_paths_for_epos(epos, str(elsewhere)),
                             (elsewhere / "sample_2.html", elsewhere / "sample_2.txt", elsewhere / "sample_2.csv"))

    def test_spectrum_export_uses_plot_histogram(self):
        mass, counts = core.spectrum_histogram(FakeRoi(), 0, 14, 0.01)
        with patch.dict(sys.modules, fake_plotly_modules()):
            figure = core.make_spectrum_plot(FakeRoi(), [], 0, 14, 0.01)
        self.assertEqual(figure.traces[0]["x"], mass)
        self.assertEqual(figure.traces[0]["y"], counts)

    def test_project_save_load_and_overwrite_protection(self):
        state = {
            "format": core.PROJECT_FORMAT,
            "version": core.PROJECT_VERSION,
            "epos_file": "/data/example.epos",
            "selected_elements": ["Fe", "C"],
            "selected_ion_keys": ["Fe2", "C1"],
            "manual_peaks": "unknown: 31.2",
            "lower_mz": 0.0,
            "upper_mz": 100.0,
            "bin_width": 0.01,
            "y_scale": "log",
            "save_folder": "/data/results",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.apt-project.json"
            self.assertEqual(core.default_project_path("/data/example.epos"),
                             Path("/data/example.apt-project.json"))
            core.save_project_file(path, state)
            self.assertEqual(core.load_project_file(path), state)
            with self.assertRaises(FileExistsError):
                core.save_project_file(path, {**state, "manual_peaks": "other: 50"})
            self.assertEqual(core.load_project_file(path), state)
            changed = {**state, "manual_peaks": "other: 50"}
            core.save_project_file(path, changed, overwrite=True)
            self.assertEqual(core.load_project_file(path), changed)

    def test_project_rejects_unknown_or_unavailable_ions(self):
        state = {
            "format": core.PROJECT_FORMAT,
            "version": core.PROJECT_VERSION,
            "epos_file": "",
            "selected_elements": ["Fe"],
            "selected_ion_keys": ["Fe2"],
            "manual_peaks": "",
            "lower_mz": 0.0,
            "upper_mz": 200.0,
            "bin_width": 0.01,
            "y_scale": "linear",
            "save_folder": "",
        }
        self.assertIs(core.validate_project_state(state), state)
        with self.assertRaises(ValueError):
            core.validate_project_state({**state, "selected_ion_keys": ["not-in-catalogue"]})
        with self.assertRaises(ValueError):
            core.validate_project_state({**state, "selected_ion_keys": ["FeC2_2"]})
        with self.assertRaises(ValueError):
            core.validate_project_state({**state, "version": 99})

    def test_gui_project_save_and_reload_without_autosave(self):
        gui_path = str(Path(__file__).with_name("cell2_gui_basic_advanced.py"))
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, fake_widget_modules()):
            epos = Path(directory) / "sample.epos"
            project = Path(directory) / "sample.apt-project.json"
            first = runpy.run_path(gui_path, init_globals=vars(core).copy())
            first["epos_widget"].value = str(epos)
            first["element_widgets"]["Fe"].value = True
            first["ion_widgets"]["Fe2"].value = True
            first["manual_widget"].value = "Unknown: 31.2"
            first["save_project_button"].click()
            self.assertTrue(project.is_file())
            first["manual_widget"].value = "Unknown: 32.2"
            self.assertEqual(core.load_project_file(project)["manual_peaks"], "Unknown: 31.2")
            first["save_project_button"].click()
            self.assertEqual(core.load_project_file(project)["manual_peaks"], "Unknown: 32.2")

            second = runpy.run_path(gui_path, init_globals=vars(core).copy())
            self.assertNotIn("autosave_widget", second)
            self.assertIn("paste full .json path", second["project_file_widget"].placeholder)
            self.assertIn("One peak per line", second["manual_widget"].placeholder)
            self.assertIn("All files use the EPOS filename", second["save_folder_widget"].placeholder)
            second["project_file_widget"].value = str(project)
            second["save_project_button"].click()
            self.assertIn("FileExistsError", second["project_status"].value)
            second["load_project_button"].click()
            self.assertTrue(second["element_widgets"]["Fe"].value)
            self.assertTrue(second["ion_widgets"]["Fe2"].value)
            self.assertEqual(second["manual_widget"].value, "Unknown: 32.2")
            self.assertEqual(second["epos_widget"].value, str(epos))

    def test_manual_peak_parsing_and_plotting(self):
        manual = core.parse_manual_candidates("Unknown-1: 37.123; possible FeC: 44.987\n")
        self.assertEqual([p["mass"] for p in manual], [37.123, 44.987])
        self.assertEqual([p["ion"] for p in manual], ["Unknown-1", "possible FeC"])
        self.assertEqual([p["evidence"] for p in manual], ["manual (unverified)"] * 2)
        with self.assertRaises(ValueError):
            core.parse_manual_candidates("bad: NaN")
        with patch.dict(sys.modules, fake_plotly_modules()):
            figure = core.make_spectrum_plot(FakeRoi(), manual, 0, 50, 0.01,
                                             logarithmic_y=True)
        lines = [t for t in figure.traces if t["kind"] == "candidate"]
        self.assertEqual(len(lines), 2)
        self.assertTrue(all("User-entered m/z" in line["hovertemplate"]
                            for line in lines))


if __name__ == "__main__":
    unittest.main()
