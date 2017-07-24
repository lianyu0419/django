#coding=utf-8
""" notification template tags
"""

from django import template
from django.template import Context



register = template.Library()


@register.tag("notification_list")
def do_notification_list(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, notifications, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0]) 
    return NotificationListNode(notifications, request)


class NotificationListNode(template.Node):
    def __init__(self, notifications, request): 
        self.notifications = template.Variable(notifications)
        self.request = template.Variable(request)
        
    def render(self, context):
        t = template.loader.get_template("notification/tags/list.html")
        new_context = Context({"notifications": self.notifications.resolve(context), 
                               "request": self.request.resolve(context)}, 
                              autoescape=context.autoescape)
        return t.render(new_context)
    
    
@register.tag("notification_alert")
def do_notification_alert(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag one argument" % token.contents.split()[0]) 
    return NotificationAlertNode(request)


class NotificationAlertNode(template.Node):
    def __init__(self, request): 
        self.request = template.Variable(request)
        
    def render(self, context):
        t = template.loader.get_template("notification/tags/alert.html")
        new_context = Context({"request": self.request.resolve(context)}, 
                              autoescape=context.autoescape)
        return t.render(new_context)
