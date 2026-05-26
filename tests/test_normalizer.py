from viz_api_project.data.normalizer import extract_records, normalize_records


def test_extract_records_from_nested_payload() -> None:
    payload = {"data": {"items": [{"name": "A"}, {"name": "B"}]}}

    records = extract_records(payload, "data.items")

    assert records == [{"name": "A"}, {"name": "B"}]


def test_normalize_records_creates_dataframe_columns() -> None:
    dataframe = normalize_records([{"source": "A", "target": "B", "value": 10}])

    assert list(dataframe.columns) == ["source", "target", "value"]
    assert dataframe.loc[0, "value"] == 10
