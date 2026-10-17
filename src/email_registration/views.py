

email_ = kv.LabeledInput("email",
                         "Email",
                         "me@mine.mydomain",
                         data_validators = [kv.validator.InputRequired(),
                                            kv.validator.Email(), 
                                            ],
                         on_change = on_input_change
                         )
        
wp_endpoint = kv.create_endpoint(key="expose_session_id",
                                 childs = [alabel,
                                           btn,
                                           #session_clear_btn 
                                           ],
                                 title="Expose session id",
                                 rendering_type="MutableSSR",
                                 svelte_bundle_dir="ssr"
                                 )






#@oj.csrfprotect
def register_new_user(request):
    # RequestNewVerificationEmail
    # csrf_token, form, and a button
    session_manager = oj.get_session_manager(request.session_id)
    def on_input_change(dbref, msg):
        # we need dummy event handler for correct functioning of react
        pass

    User = oj.aci.get_user_model()
    #@ojr.CfgLoopRunner
    def on_submit_click(dbref, msg, form_inputs_value_dict):
        print ("on_submit_click")
        print (form_inputs_value_dict)
        # the user model doesnot 1:1 map with the form
        # form has confirm password
        # but user model doesn't.
        # it seems tricky to build a model agnostic page
        
        #form_inputs_value_dict.pop("confirm_password")
        
        # add user in db and take actions
        val = User(**form_inputs_value_dict)
        val = User(**form_inputs_value_dict)
        print ("new user = ", str(val.id), val.email)
        #return "/new_user", User(**form_inputs_value_dict)
        return "/new_user", val
        
        #print (msg)

        #stop_validation = self._run_validation_chain(data, chain)
        # print(dbref.spathMap)
        # for cpath, cbref in dbref.spathMap.items():
        print ("form on_submit called")
        #     print (cpath, cbref)
        
        pass
    
    with oj.sessionctx(session_manager):
    # Technically, we should inspect the fields of the user; 
    # for now hardwiring to default user with email, first name, last, name, password
    
        email_ = oj.LabeledInput_("email",
                         "Email",
                         "me@mine.mydomain",
                         data_validators = [oj.validator.InputRequired(),
                                            oj.validator.Email(), 
                                            ]
                         ).event_handle(oj.change, on_input_change)




        # in Django-Verify-Email, first get the user_model, peek into meta, get the field,
        # and then get the verbose_name, along with help_text and then render out the form
        # things are bit manual here. You build your form by yourself

        first_name_ = oj.LabeledInput_("first_name",
                                        "First Name",
                                        "Mary",
                                        data_validators = [oj.validator.InputRequired(),
                                                           oj.validator.Length(max=128), # this should come from the user model only
                                                           ]).event_handle(oj.change,
                                                                           on_input_change

                                                                           )

        last_name_ = oj.LabeledInput_("last_name",
                                        "Last Name",
                                        "Fernandes",
                                        data_validators = [oj.validator.InputRequired(),
                                                           oj.validator.Length(max=128), # this should come from the user model only
                                                           ]).event_handle(oj.change,
                                                                                               on_input_change
                                                                                               )


        password_ = oj.LabeledInput_("password",
                                     "password",
                                     "Enter Password",
                                     input_type="password",
                                     data_validators=[oj.validator.InputRequired()]
                                     ).event_handle(oj.change, on_input_change)

        confirm_password_ = oj.LabeledInput_("confirm_password",
                                             "confirm_password",
                                             "Confirm Password",
                                             input_type="password",
                                             data_validators=[oj.validator.InputRequired(),
                                                              oj.validator.EqualTo(password_.spath)]
                                             ).event_handle(oj.change, on_input_change)

        all_inputs_ = oj.StackV_("all_inputs",
                                     cgens = [email_,
                                              first_name_,
                                              last_name_,
                                              password_,
                                              confirm_password_,
                                              ]
                                     )

        btn_ = oj.Button_("mybtn", text="Submit", type="submit")
        target_ = oj.Form_("myform",
                           all_inputs_,
                           btn_,
                           stubStore = session_manager.stubStore
                           ).event_handle(oj.submit, on_submit_click)


        wp_ = oj.WebPage_("register user",
                          cgens =[target_],
                          WPtype= ojr.WebPage,
                          use_websockets= False,
                          ui_app_trmap_iter = ui_app_keymap,
                          action_module = actions,
                          session_manager = session_manager,
                          title="Register new user"
                          )
        
    wp = wp_()
    
    print ("wp.use_websockets = ", wp.use_websockets)
    # TODO: need to figure this out
    # place some cookies; let signing cookie middleware do some work
    # request.state.messages.data = {'A Title': 'The message',
    #                                'Another title': 'With another msg',
    #                                }
    wp.session_manager = session_manager
    return wp

