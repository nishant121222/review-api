def get_google_review_link(business):
    """
    Returns Google Review link for a business if `google_location_id` exists.
    """
    if getattr(business, 'google_location_id', None):
        return f"https://search.google.com/local/writereview?placeid={business.google_location_id}"
    return None
