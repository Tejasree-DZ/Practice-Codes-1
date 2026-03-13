
#contraints should be based on the user input data validation
#ref:  https://github.com/hystax/optscale/blob/integration/rest_api/rest_api_server/models/types.py

from sqlalchemy import Index, UniqueConstraint
class Urls:
    
    
    url_prefix: str = "/auth"

    urls_map: dict[str, str] = {
        
        "users_collection":       "%s/users",
        "users":                  "%s/users/{user_id}",

       
        "token":                  "%s/token",
        "refresh_token":          "%s/refresh_token",

        "assignments_collection": "%s/assignments",
        "assignments":            "%s/assignments/{assignment_id}",

        
        "roles_collection":       "%s/roles",
        "roles":                  "%s/roles/{role_id}",

        
        "types_collection":       "%s/types",
        "types":                  "%s/types/{type_id}",
    }

    def __init__(self) -> None:
        # Expose the prefix itself so routers can reference it directly
        self.prefix: str = self.url_prefix

        # Build every named path attribute from the map
        for name, pattern in self.urls_map.items():
            setattr(self, name, pattern % self.url_prefix)

    def __repr__(self) -> str:
        routes = {k: getattr(self, k) for k in self.urls_map}
        return f"<{self.__class__.__name__} prefix={self.url_prefix!r} routes={routes}>"


class UrlsV1(Urls):
    
    url_prefix: str = "/auth/v1"

urls_v1 = UrlsV1()
IDX_USER_MAIL = Index(
    "ix_user_mail",
    "mail",
    unique=True,
)

IDX_ASSIGNMENT_USER_ID = Index(
    "ix_assignment_user_id",
    "user_id",
)

IDX_ASSIGNMENT_RESOURCE_ID = Index(
    "ix_assignment_resource_id",
    "resource_id",
)

UQ_ASSIGNMENT_ACTIVE = UniqueConstraint(
    "user_id",
    "resource_id",
    "role_id",
    "type_id",
    name="uq_assignment_user_role_resource",
)