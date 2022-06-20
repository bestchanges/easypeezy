import pytest
import requests_cache


@pytest.fixture(scope="module")
def cached_requests_fixture(request):
    test_function_name = request.node.name
    requests_cache.install_cache(
        cache_name=f'tests_cached_requests/{test_function_name}',
        backend='filesystem',
        serializer='json',
        expire_after=-1,
        allowable_methods=['GET', 'POST'],
    )
    yield True
    requests_cache.uninstall_cache()
