from app.service.difference_finder import DifferenceFinder
from app.domain.field import Field
from app.domain.field_change import FieldChange


def test_should_find_deleted():
    old = {
        "a.b": "object",
        "c.d": "keyword"
    }

    new = {
        "a.b": "object"
    }

    removed = DifferenceFinder(old_mapping=old, new_mapping=new).get_difference().removed

    assert removed == [Field(name="c.d", type="keyword")]


def test_should_find_added():
    new = {
        "a.b": "object",
        "c.d": "keyword"
    }

    old = {
        "a.b": "object"
    }

    added = DifferenceFinder(old_mapping=old, new_mapping=new).get_difference().added

    assert added == [Field(name="c.d", type="keyword")]


def test_should_find_type_changes():
    new = {
        "a.b": "keyword",
        "c.d": "object"
    }

    old = {
        "a.b": "long",
        "c.d": "object"
    }

    changed = DifferenceFinder(old_mapping=old, new_mapping=new).get_difference().changed

    assert changed == [FieldChange(name="a.b", old_type="long", new_type="keyword")]
