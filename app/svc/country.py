def get_offset(country):
    """
        Get the offset of time of a country
        @param country m.Country the country to get the timezone offset
        @return int the offset, if no offset found return 0
    """
    if not country:
        return 0
    
    if country.timezone:
        return country.timezone
    
    return 0