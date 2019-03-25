# -*- coding: utf-8 -*-

from django import template

from hitcount.templatetags import hitcount_tags

register = template.Library()


def get_hit_count_from_obj_variable(context, obj_variable, tag_name):
    """
    Helper function to return a HitCount for a given template object variable.
    Raises TemplateSyntaxError if the passed object variable cannot be parsed.
    """
    from popularity.tasks import HitCountJob

    error_to_raise = template.TemplateSyntaxError(
        "'%(a)s' requires a valid individual model variable "
        "in the form of '%(a)s for [model_obj]'.\n"
        "Got: %(b)s" % {'a': tag_name, 'b': obj_variable}
    )

    try:
        obj = obj_variable.resolve(context)
    except template.VariableDoesNotExist:
        raise error_to_raise
    
    opts, pk = obj._meta, obj.pk

    hit_count = HitCountJob().get(opts.app_label, opts.model_name, pk)

    return hit_count


class GetHitCount(hitcount_tags.GetHitCount):

    def render(self, context):
        hit_count = get_hit_count_from_obj_variable(context, self.obj_variable, 'get_hit_count')

        if self.period:  # if user sets a time period, use it
            try:
                hits = hit_count.hits_in_last(**self.period)
            except TypeError:
                raise template.TemplateSyntaxError(
                    "'get_hit_count for [obj] within [timedelta]' requires "
                    "a valid comma separated list of timedelta arguments. "
                    "For example, ['days=5,hours=6']. "
                    "Got these instead: %s" % self.period
                )
        else:
            hits = hit_count.hits

        if self.as_varname:  # if user gives us a variable to return
            context[self.as_varname] = str(hits)
            return ''
        else:
            return str(hits)


def get_hit_count(parser, token):
    return GetHitCount.handle_token(parser, token)

register.tag('get_hit_count', get_hit_count)
