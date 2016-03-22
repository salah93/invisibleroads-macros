import datetime
import pytest
from dateutil.parser import parse as parse_date
from freezegun import freeze_time
from invisibleroads_macros.date import parse_date_safely


@freeze_time('2016-02-29')
def test_parse_date_safely():
    with pytest.raises(ValueError):
        parse_date('2017')
    assert parse_date_safely('2017') == datetime.datetime(2017, 1, 1)
