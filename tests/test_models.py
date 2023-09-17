import pytest
from django.core.validators import ValidationError  # type: ignore

from django_webhook.models import WebhookTopic, populate_topics_from_settings

pytestmark = pytest.mark.django_db


def test_validates_topic_name_regex():
    t = WebhookTopic(name="hello")
    with pytest.raises(ValidationError, match=r"Topic must match"):
        t.clean_fields()


def test_validates_topic_name_in_models(settings):
    settings.DJANGO_WEBHOOK = dict(MODELS=["tests.User"])
    t = WebhookTopic(name="tests.Country/update")
    with pytest.raises(
        ValidationError,
        match=r".*The topic: tests.Country/update is not in the whitelisted settings",
    ):
        t.clean_fields()


def test_populate_topics_from_settings(settings):
    populate_topics_from_settings()
    assert list(WebhookTopic.objects.values_list("name", flat=True)) == [
        "tests.User/create",
        "tests.User/update",
        "tests.User/delete",
        "tests.Country/create",
        "tests.Country/update",
        "tests.Country/delete",
    ]
    settings.DJANGO_WEBHOOK["MODELS"] = ["tests.Country"]
    populate_topics_from_settings()
    assert list(WebhookTopic.objects.values_list("name", flat=True)) == [
        "tests.User/create",
        "tests.User/update",
        "tests.User/delete",
        "tests.Country/create",
        "tests.Country/update",
        "tests.Country/delete",
    ]
