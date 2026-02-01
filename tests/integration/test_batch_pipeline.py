"""Integration tests for batch pipeline."""

import pytest


class TestBatchPipeline:
    """Integration tests for batch data pipeline."""

    @pytest.mark.skip(reason="Requires Airflow running")
    def test_brewery_sync_dag(self):
        """Test brewery sync DAG execution."""
        pass

    @pytest.mark.skip(reason="Requires Airflow running")
    def test_daily_aggregations_dag(self):
        """Test daily aggregations DAG execution."""
        pass

    @pytest.mark.skip(reason="Requires Airflow and MLflow running")
    def test_ml_training_pipeline(self):
        """Test ML training pipeline execution."""
        pass
