import json
import os
import tempfile
from pathlib import Path

import pytest

from djx.djx import load_config, load_json, load_yaml, save_json, save_yaml


class TestLoadConfig:
    """Test loading configuration files in different formats."""

    def test_load_yaml_file(self, tmp_path):
        """Test loading a YAML configuration file."""
        yaml_file = tmp_path / "config.yml"
        yaml_file.write_text(
            """
meta:
  project_id: test_project
config:
  model_args:
    n_estimators: 100
    max_depth: 2
"""
        )
        data = load_config(str(yaml_file))
        assert data["meta"]["project_id"] == "test_project"
        assert data["config"]["model_args"]["n_estimators"] == 100

    def test_load_yaml_file_with_yaml_extension(self, tmp_path):
        """Test loading a YAML file with .yaml extension."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text(
            """
meta:
  project_id: test_yaml
"""
        )
        data = load_config(str(yaml_file))
        assert data["meta"]["project_id"] == "test_yaml"

    def test_load_json_file(self, tmp_path):
        """Test loading a JSON configuration file."""
        json_file = tmp_path / "config.json"
        json_data = {
            "meta": {"project_id": "test_json"},
            "config": {"model_args": {"n_estimators": 100, "max_depth": 2}},
        }
        json_file.write_text(json.dumps(json_data, indent=2))

        data = load_config(str(json_file))
        assert data["meta"]["project_id"] == "test_json"
        assert data["config"]["model_args"]["n_estimators"] == 100

    def test_load_unsupported_format(self, tmp_path):
        """Test that loading unsupported format raises an error."""
        txt_file = tmp_path / "config.txt"
        txt_file.write_text("some text")

        with pytest.raises(ValueError, match="Unsupported config file format"):
            load_config(str(txt_file))


class TestSaveConfig:
    """Test saving configuration files in different formats."""

    def test_save_yaml(self, tmp_path):
        """Test saving data as YAML."""
        yaml_file = tmp_path / "output.yml"
        data = {"meta": {"project_id": "test"}, "config": {"value": 42}}

        save_yaml(data, str(yaml_file))

        # Verify file was created and can be loaded
        loaded = load_yaml(str(yaml_file))
        assert loaded["meta"]["project_id"] == "test"
        assert loaded["config"]["value"] == 42

    def test_save_json(self, tmp_path):
        """Test saving data as JSON."""
        json_file = tmp_path / "output.json"
        data = {"meta": {"project_id": "test"}, "config": {"value": 42}}

        save_json(data, str(json_file))

        # Verify file was created and can be loaded
        loaded = load_json(str(json_file))
        assert loaded["meta"]["project_id"] == "test"
        assert loaded["config"]["value"] == 42

        # Verify it's properly formatted
        content = json_file.read_text()
        assert '"project_id": "test"' in content or '"project_id":"test"' in content


class TestJSONWithPlaceholders:
    """Test that JSON configs work with placeholder system."""

    def test_json_with_placeholders(self, tmp_path):
        """Test JSON config with placeholder strings."""
        json_file = tmp_path / "config.json"
        json_data = {
            "define": {
                "config_file": "<<cwd>>/experiments/<<project_id>>/<<job_idx>>/config.json",
                "log_file": "<<cwd>>/logs/<<datetime>>.log",
            },
            "meta": {"project_id": "test_project"},
            "config": {
                "output_path": "<<cwd>>/results/<<exp_uid>>/output.json",
                "model_args": {
                    "max_depth": "<<int:depth>>",
                    "learning_rate": "<<float:lr>>",
                },
            },
        }
        json_file.write_text(json.dumps(json_data, indent=2))

        data = load_config(str(json_file))

        # Verify placeholders are preserved as strings in the loaded data
        assert "<<cwd>>" in data["define"]["config_file"]
        assert "<<project_id>>" in data["define"]["config_file"]
        assert "<<datetime>>" in data["define"]["log_file"]
        assert "<<int:depth>>" in data["config"]["model_args"]["max_depth"]


class TestRealExamples:
    """Test with actual example files from the repository."""

    def test_iris_json_example_loads(self):
        """Test that the iris.json example file loads correctly."""
        example_path = Path(__file__).parent.parent / "example" / "config" / "iris.json"
        if not example_path.exists():
            pytest.skip("iris.json example not found")

        data = load_config(str(example_path))

        # Verify structure
        assert "define" in data
        assert "meta" in data
        assert "config" in data
        assert data["meta"]["project_id"] == "iris_json_test"

    def test_iris_yaml_example_loads(self):
        """Test that the iris.yml example file loads correctly."""
        example_path = Path(__file__).parent.parent / "example" / "config" / "iris.yml"
        if not example_path.exists():
            pytest.skip("iris.yml example not found")

        data = load_config(str(example_path))

        # Verify structure
        assert "define" in data
        assert "meta" in data
        assert "config" in data
        assert data["meta"]["project_id"] == "iris_test"


class TestFormatEquivalence:
    """Test that YAML and JSON produce equivalent results."""

    def test_equivalent_data_structures(self, tmp_path):
        """Test that same data saved/loaded in YAML and JSON is equivalent."""
        test_data = {
            "define": {"config_file": "<<cwd>>/config.yml"},
            "meta": {"project_id": "test", "name": "experiment"},
            "config": {
                "model_args": {
                    "n_estimators": 100,
                    "max_depth": 3,
                    "learning_rate": 0.01,
                },
                "features": ["a", "b", "c"],
            },
            "grid": [{"model_args.max_depth": [2, 3, 4]}],
        }

        # Save as both formats
        yaml_file = tmp_path / "config.yml"
        json_file = tmp_path / "config.json"

        save_yaml(test_data, str(yaml_file))
        save_json(test_data, str(json_file))

        # Load both
        yaml_data = load_config(str(yaml_file))
        json_data = load_config(str(json_file))

        # Compare
        assert yaml_data == json_data
        assert yaml_data["meta"]["project_id"] == json_data["meta"]["project_id"]
        assert yaml_data["config"]["model_args"] == json_data["config"]["model_args"]
        assert yaml_data["grid"] == json_data["grid"]


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_config(self, tmp_path):
        """Test loading empty or minimal configs."""
        json_file = tmp_path / "empty.json"
        json_file.write_text("{}")

        data = load_config(str(json_file))
        assert data == {}

    def test_nested_structures(self, tmp_path):
        """Test deeply nested data structures."""
        json_file = tmp_path / "nested.json"
        nested_data = {"level1": {"level2": {"level3": {"level4": {"value": "deep"}}}}}
        json_file.write_text(json.dumps(nested_data))

        data = load_config(str(json_file))
        assert data["level1"]["level2"]["level3"]["level4"]["value"] == "deep"

    def test_special_characters_in_json(self, tmp_path):
        """Test JSON with special characters."""
        json_file = tmp_path / "special.json"
        special_data = {
            "path": "/home/user/data",
            "regex": "\\d+",
            "unicode": "Hello 世界",
            "quote": 'He said "hello"',
        }
        json_file.write_text(json.dumps(special_data))

        data = load_config(str(json_file))
        assert data["path"] == "/home/user/data"
        assert data["regex"] == "\\d+"
        assert data["unicode"] == "Hello 世界"
