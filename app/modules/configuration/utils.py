def form_config(config_list):
    conf = {}
    param_links = config_list.params_links
    for i in param_links:
        conf[i.param.parameter_name] = i.value
    return conf
