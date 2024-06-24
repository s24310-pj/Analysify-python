import pytest
import pandas as pd
from analysify.data_analyzer import DataAnalyzer

@pytest.fixture
def sample_data():
    data = {
        'Make': ['Ford', 'Chevrolet', 'Ford', 'BMW', 'Chevrolet'],
        'Engine HP': [450, 300, 300, 400, 350],
        'Engine Cylinders': [8, 6, 6, 8, 6],
        'Year': [2015, 2017, 2018, 2019, 2020],
        'MSRP': [55000, 40000, 42000, 75000, 65000],
        'highway MPG': [24, 27, 25, 22, 23]
    }
    return pd.DataFrame(data)

@pytest.fixture
def analyzer():
    return DataAnalyzer()

def test_load_data(analyzer, sample_data, tmp_path):
    file_path = tmp_path / "test_data.csv"
    sample_data.to_csv(file_path, index=False)
    analyzer.load_data(file_path)
    pd.testing.assert_frame_equal(analyzer.data, sample_data)

def test_get_summary(analyzer, sample_data):
    analyzer.data = sample_data
    summary = analyzer.get_summary()
    assert 'mean' in summary.index
    assert 'min' in summary.index
    assert 'max' in summary.index

def test_filter_data(analyzer, sample_data):
    analyzer.data = sample_data
    filtered_data = analyzer.filter_data('Make', 'Ford')
    assert len(filtered_data) == 2
    assert all(filtered_data['Make'] == 'Ford')

def test_convert_categorical(analyzer, sample_data):
    analyzer.data = sample_data
    result = analyzer.convert_categorical('Make')
    assert result is True
    assert analyzer.data['Make'].dtype.name == 'int8'

def test_plot_pie(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_pie('Make')
    except Exception as e:
        pytest.fail(f"plot_pie raised an exception: {e}")

def test_plot_line(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_line('Year', 'Engine HP')
    except Exception as e:
        pytest.fail(f"plot_line raised an exception: {e}")

def test_plot_bar(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_bar('Engine Cylinders', 'Engine HP')
    except Exception as e:
        pytest.fail(f"plot_bar raised an exception: {e}")

def test_plot_scatter(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_scatter('Engine HP', 'highway MPG')
    except Exception as e:
        pytest.fail(f"plot_scatter raised an exception: {e}")

def test_plot_bar_make_count(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_bar_make_count()
    except Exception as e:
        pytest.fail(f"plot_bar_make_count raised an exception: {e}")

def test_plot_bar_hp_cylinders(analyzer, sample_data):
    analyzer.data = sample_data
    try:
        analyzer.plot_bar_hp_cylinders()
    except Exception as e:
        pytest.fail(f"plot_bar_hp_cylinders raised an exception: {e}")
