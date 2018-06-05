def key_function_builder(search_keys_dict):
    def filter_function(task):
        for k,v in search_keys_dict.items():
            attr_val = task.try_get_attribute(k)
            if attr_val is None:
                return False
            if isinstance(v, list):
                for item in v:
                    if item not in attr_val:
                        return False
            elif attr_val != v:
                return False
        return True
    return filter_function


def task_editor_builder(changes_dict):
    def editor(task_to_edit):
        for k,v in changes_dict.items():
            if isinstance(v,list):
                task_to_edit.add_to_attribute(k,changes_dict[k])
            else:
                task_to_edit.set_attinute(k,changes_dict[k])
    return editor
