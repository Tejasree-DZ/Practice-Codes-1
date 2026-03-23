class Urls:
    url_prefix = "/core"
    urls_map = {
        "organizations_collection": "%s/v1/organizations",
        "organizations":            "%s/v1/organizations/{organization_id}",
        "organization_teams":       "%s/v1/organization/{organization_id}/teams",
        "teams":                    "%s/v1/teams/{team_id}",
        "team_members":             "%s/v1/teams/{team_id}/members",
        "members":                  "%s/v1/members/{member_id}",
    }

    def __init__(self):
        self.prefix = self.url_prefix
        for name, pattern in self.urls_map.items():
            setattr(self, name, pattern % self.url_prefix)


urls = Urls()