import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoints(client):
    assert client.get('/admin/login/').status_code == 200
    # API root should exist after including router
    assert client.get('/api/').status_code in (200, 403)  # 403 when unauthenticated


