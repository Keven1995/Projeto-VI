from viz_api_project.facades.visualization_facade import VisualizationFacade


def test_visualization_facade_builds_generic_clean_dataset() -> None:
    class Config:
        source = "generic"
        api = None
        tmdb = None
        records_path = "items"
        local_data_path = "data/sample_dataset.json"

    dataset = VisualizationFacade().build_clean_dataset(Config())

    assert dataset.source == "generic"
    assert dataset.records_count > 0
