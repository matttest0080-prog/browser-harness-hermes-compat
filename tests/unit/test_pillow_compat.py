"""Security floor and actual image paths used by the unchanged browser code."""
import importlib.metadata
import io

import pytest
from PIL import Image

from browser_harness.video_render import contact_sheet, masked_frame


def test_runtime_uses_fixed_pillow():
    assert int(importlib.metadata.version("Pillow").split(".")[0]) >= 13


@pytest.mark.parametrize("mode", ["RGB", "L", "CMYK"])
def test_jpeg_decode_and_contact_sheet(mode, tmp_path):
    path = tmp_path / "capture.jpg"
    Image.new(mode, (800, 400)).save(path, format="JPEG")
    with Image.open(path) as decoded:
        decoded.load()
        assert decoded.size == (800, 400)
    output = tmp_path / "sheet.jpg"
    contact_sheet([{"path": str(path), "label": "owned fixture", "time": 0}], output, "Compatibility")
    with Image.open(output) as sheet:
        sheet.load()
        assert sheet.width > 800 and sheet.height > 225


def test_mask_preserves_dimensions_and_hides_selected_pixels(tmp_path):
    Image.new("RGB", (100, 100), "red").save(tmp_path / "frame.png")
    comp = {"viewport": {"w": 100, "h": 100},
            "redact": {"frame.png": [{"x": 20, "y": 20, "w": 40, "h": 40, "fill": "#000000", "pad": 1}]}}
    masked = masked_frame(tmp_path, comp, "frame.png")
    assert masked.size == (100, 100)
    assert masked.getpixel((40, 40)) == (0, 0, 0)
    assert masked.getpixel((90, 90)) == (255, 0, 0)


def test_invalid_image_is_not_accepted():
    from PIL import UnidentifiedImageError
    with pytest.raises(UnidentifiedImageError):
        Image.open(io.BytesIO(b"not an image")).load()
