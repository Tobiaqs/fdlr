def as_of_qs(history, date):
    # Partially borrowed from https://github.com/jazzband/django-simple-history/blob/e790fd66dd4035f956b114c1018f355304070775/simple_history/manager.py#L106
    # PSQL ONLY
    qs = history.filter(history_date__lte=date)

    latest_pk_attr_historic_ids = (
        qs.order_by('id', '-history_date', '-pk')
        .distinct('id')
        .values_list('pk', flat=True)
    )
    latest_historics = qs.filter(
        history_id__in=latest_pk_attr_historic_ids
    )

    return latest_historics.exclude(history_type='-').order_by('id')
