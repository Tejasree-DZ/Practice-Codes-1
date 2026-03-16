
class Urls:
    url_prefix = "/auth"
    urls_map = {
        "users_collection":      "%s/v1/users",
        "users":                 "%s/v1/users/{user_id}",
        "token":                 "%s/v1/token",
        "refresh_token":         "%s/v1/refresh_token",
        "assignments_collection":"%s/v1/assignments",
        "assignments":           "%s/v1/assignments/{assignment_id}",
    }
    def __init__(self):
        self.prefix = self.url_prefix
        for name, pattern in self.urls_map.items():
            setattr(self, name, pattern % self.url_prefix)

urls = Urls()