def get_contentful_cookie(request):
    """
    Returns the Contentful authentication token from a request

    @param request: the request that contains the cookie
    """
    return request.cookies.get('contentful_token')


def check_has_contentful_cookie(request):
    """
    Checks if a request has a Contentful authentication cookie

    @param request: the request that contains the cookie
    @return: True if the request has a contentful cookie, False otherwise
    """
    return get_contentful_cookie(
        request) is not None  # todo more robust check here
