def model_to_dict(queryset):
    result = []
    for row in queryset:
        d = row.__dict__.copy()
        del d['_sa_instance_state']
        d['uuid'] = str(d['uuid'])
        result.append(d)
    return result