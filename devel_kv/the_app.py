import kavya as kv
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.datastructures import State

cookie_cfg_map, cookie_signer_secret_keys, cookie_initial_values = kv.load_cookie_configs()

print("The app session cookies called")

class InitRequestStateMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            #request = Request(scope)
            #request.state.form_data = {}
            state = scope["state"] = State()
            for name, initial_value in cookie_initial_values.items():
                setattr(state, name, dict(initial_value))  # clone default dict

            #setattr(state, "/form_submit", dict())
            await self.app(scope, receive, send)
                

app  = kv.build_app( cookie_cfg_map = cookie_cfg_map,
                     cookie_signer_secret_keys = cookie_signer_secret_keys,
                    middlewares=[Middleware(InitRequestStateMiddleware)
                                 ]
                    )
                    

