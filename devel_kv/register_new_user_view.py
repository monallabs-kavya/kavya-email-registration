import kavya as kv
from py_tailwind_utils import *

app = kv.load_app()
async def on_input_change(dbref, msg, wp, request):
    # dummy event handler;
    # required

    pass

async def on_submit_click(dbref, msg, wp, request):
    print ("on_submit_click")
    abc = dbref.get_comp_value(request, "/input_email")
    print(abc)
    #print (form_inputs_value_dict)
    # the user model doesnot 1:1 map with the form
    # form has confirm password
    # but user model doesn't.
    # it seems tricky to build a model agnostic page

    #form_inputs_value_dict.pop("confirm_password")

    # add user in db and take actions
    # val = User(**form_inputs_value_dict)
    # val = User(**form_inputs_value_dict)
    #print ("new user = ", str(val.id), val.email)
    #return "/new_user", User(**form_inputs_value_dict)
    #return "/new_user", val

    # user_email 
    #return "/new_user_email",  user_email 
    #print (msg)

    #stop_validation = self._run_validation_chain(data, chain)
    # print(dbref.spathMap)
    # for cpath, cbref in dbref.spathMap.items():
    #print ("form on_submit called")
    #     print (cpath, cbref)

    pass
    
email_input  = kv.PD.Label(twsty_tags=[noop/label],
            childs = [kv.PC.Span(text="Email",
                                 twsty_tags=[noop/label_text]
                                 ),

                      kv.AC.TextInput(key="input_email",
                                  on_change=on_input_change,
                             value=kv.Validator.InvalidInput,
                             data_validators = [kv.Validator.InputRequired(),
                                                kv.Validator.Email(), 
                                                ], 
                                               
                             twsty_tags = [W/40]
                            )
                      ]
            )


submit_btn = kv.AC.Button(key="submit",
                          text="Submit",

                          )


user_registration_form = kv.AD.Form(key="register_new_user_form_submit",
                                    childs = [email_input,
                                              submit_btn],
                                    on_submit=on_submit_click
                                    )


def post_init_page_load(wp, session_manager=None):

    print("post init called with form_data initialized")
    assert session_manager is not None
    session_manager.state.form_data = {}
    session_manager.state.form_data["/register_new_user_form_submit"] = {}
    print("initialized form_data on session_manager.state ", id(session_manager))
    pass

        

# rest of the details will come later
# first verify the email 
# #. user model should dictate 
# name_input  = kv.PD.Label(twsty_tags=[noop/label],
#             childs = [kv.PC.Span(text="Full Name",
#                                  twsty_tags=[noop/label_text]
#                                  ),

#                       kv.AC.Input(key="full_name", on_change=on_input_change,
#                              value=kv.InvalidInput,
#                              data_validators = [oj.validator.InputRequired(),
#                                                 oj.validator.Length(max=128) # user model 
#                                                 ], 
                                               
#                              twsty_tags = [W/40]
#                             )
#                       ]
#             )

wp_endpoint = kv.create_endpoint(key="user_registration_form",
                                 childs = [user_registration_form,
                                           
                                           ],
                                 rendering_type = "MutableSSR",
                                 svelte_bundle_dir = "ssr",
                                 post_init_callback = post_init_page_load,
                                 )

kv.add_route("/", wp_endpoint)
