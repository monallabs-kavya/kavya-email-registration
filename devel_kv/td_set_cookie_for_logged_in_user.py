#. The user will come in later ; lets first test cookie load/read/write


import kavya as kv

from py_tailwind_utils import * 
app = kv.load_app()

async def eh_set_cookie(dbref, msg, wp, request):
    state = request.state
    assert hasattr(state, "art_items")
    assert getattr(state, "art_items") == {"items": [], "total": 0}
        
    # Mutate to confirm memory references are live and interactive
    setattr(state, "art_items", {"aval": 999})
        
    pass






async def eh_get_cookie(dbref, msg, wp, request):
    state = request.state
    assert hasattr(state, "art_items")
    cookie_value = getattr(state, "art_items") 
    pass


cookie_setter_btn = kv.AC.Button(key="cookie_setter",
                                 text="Set Cookie: user logged in",
                                 on_click = eh_set_cookie,
                                 twsty_tags = [H/10, 
                                               ]
                                 )


cookie_getter_btn = kv.AC.Button(key="cookie_getter",
                                 text="Get Cookie",
                                 on_click = eh_get_cookie,
                                 twsty_tags = [H/10, 
                                               ]
                                 )

wp_endpoint = kv.create_endpoint(key="cookie_set_get",
                   childs = [cookie_setter_btn,
                             cookie_getter_btn
                             ],
                   rendering_type = "MutableSSR",
                   svelte_bundle_dir = "ssr",
                   )

kv.add_route("/", wp_endpoint)
