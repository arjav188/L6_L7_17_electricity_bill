import pytest
from electricity_bill import energy_charge, late_fee, subsidy

@pytest.mark.parametrize("units,conn,expected", [
    (0, "domestic", 50), (50, "domestic", 200), (100, "domestic", 350),
    (101, "domestic", 355), (200, "domestic", 850), (300, "domestic", 1350),
    (301, "domestic", 1358), (400, "domestic", 2150),
    (50, "commercial", 450), (400, "commercial", 4350),
])
def test_energy_charge(units, conn, expected):
    assert energy_charge(units, conn) == expected

def test_unknown_connection():
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(10, "industrial")

def test_negative_units():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")

@pytest.mark.parametrize("bill,days,expected", [
    (500, 0, 0), (500, -3, 0), (500, 5, 50), (500, 15, 50),
    (1000, 16, 100), (2000, 20, 100), (3000, 20, 250),
])
def test_late_fee(bill, days, expected):
    assert late_fee(bill, days) == expected

@pytest.mark.parametrize("units,senior,solar,expected", [
    (50, True, False, 50), (100, True, False, 50), (50, False, False, 0),
    (150, True, False, 0), (50, True, True, 150), (200, False, True, 100),
    (300, False, True, 100), (400, False, True, 0),
])
def test_subsidy(units, senior, solar, expected):
    assert subsidy(units, senior, solar) == expected
