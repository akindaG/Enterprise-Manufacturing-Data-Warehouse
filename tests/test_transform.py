import pandas as pd

from etl_pipeline.transform import clean_frame


def test_clean_frame_normalizes_headers_trims_text_and_deduplicates():
    frame = pd.DataFrame(
        {
            " Product_ID ": [" P001 ", " P001 "],
            "Product_Name": ["Widget ", "Widget "],
        }
    )
    result = clean_frame(frame)
    assert list(result.columns) == ["product_id", "product_name"]
    assert len(result) == 1
    assert result.loc[0, "product_id"] == "P001"
    assert result.loc[0, "product_name"] == "Widget"
