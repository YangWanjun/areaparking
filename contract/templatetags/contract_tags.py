from django import template

from contract import biz


register = template.Library()


@register.tag(name='year_month_filter')
def year_month_filter(parser, token):
    try:
        if len(token.split_contents()) == 3:
            tag_name, context_year, context_month = token.split_contents()
            label_text1 = u"対象年"
            label_text2 = u"対象月"
        else:
            tag_name, context_year, context_month, label_text1, label_text2 = token.split_contents()
            label_text1 = label_text1[1:-1]
            label_text2 = label_text2[1:-1]
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    # if not (year_name[0] == year_name[-1] and year_name[0] in ('"', "'")) or \
    #         not (month_name[0] == month_name[-1] and month_name[0] in ('"', "'")):
    #     raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    # if not re.match(r"[0-9]{4}", year_name) or not re.match(r"[0-9]{2}", month_name):
    #     raise template.TemplateSyntaxError("%s or %s is illegal year or month" % (year_name, month_name))

    return GenerateFilterTag(context_year, context_month, label_text1, label_text2)


class GenerateFilterTag(template.Node):
    def __init__(self, context_year, context_month, label_text1, label_text2):
        self.context_year = context_year
        self.context_month = context_month
        self.label_text1 = label_text1
        self.label_text2 = label_text2
        self.year_name = "_year"
        self.month_name = "_month"

    def render(self, context):
        year_list = biz.get_year_list()
        html = ""
        nodes = []
        current_year = context.get(self.context_year, None)
        current_month = context.get(self.context_month, None)
        if year_list and current_year and current_month:
            nodes.append('<div class="input-field col s6" style="padding: 0px;">')
            nodes.append(u'<select id="{0}" name="{0}" class="browser-default" style="border: none;border-bottom: 1px solid gray;">'.format(self.year_name))
            for y in year_list:
                if "%04d" % y == current_year:
                    nodes.append(u'<option selected value="{0}">{0}</option>'.format(y))
                else:
                    nodes.append(u'<option value="{0}">{0}</option>'.format(y))
            nodes.append(u'</select>')
            nodes.append(u"<label for='{1}' class='active'>{0}：</label>".format(self.label_text1, self.year_name))
            nodes.append('</div>')
            nodes.append('<div class="input-field col s6" style="padding: 0px;">')
            nodes.append(u'<select id="{0}" name="{0}" class="browser-default" style="border: none;border-bottom: 1px solid gray;">'.format(self.month_name))
            for m in range(1, 13):
                if "%02d" % m == current_month:
                    nodes.append(u'<option selected value="{0:02d}">{0:02d}</option>'.format(m))
                else:
                    nodes.append(u'<option value="{0:02d}">{0:02d}</option>'.format(m))
            nodes.append(u'</select>')
            nodes.append(u"<label for='{1}' class='active'>{0}：</label>".format(self.label_text2, self.month_name))
            nodes.append('</div>')

            html = "".join(nodes)
        return html
