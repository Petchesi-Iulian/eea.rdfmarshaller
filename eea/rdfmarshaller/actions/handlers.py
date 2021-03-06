""" Handlers for object moved events
"""
from zope.event import notify
from zope.lifecycleevent.interfaces import IObjectAddedEvent, \
                                            IObjectRemovedEvent
from Acquisition import aq_inner, aq_parent
from eea.rdfmarshaller.actions.events import ObjectMovedOrRenamedEvent
from eea.rdfmarshaller.actions.interfaces import IObjectMovedOrRenamedEvent
from plone.app.contentrules.handlers import is_portal_factory, execute
from plone.app.discussion.interfaces import IComment
from Products.CMFCore.interfaces import IContentish

def moved(event):
    """ When an object is renamed/moved,
    execute rules assigned to its new parent."""
    obj = event.object
    if (not event.oldParent or not
            event.newParent or
            getattr(obj, "_at_creation_flag", None)):
        return
    if is_portal_factory(obj):
        return
    elif IContentish.providedBy(obj):
        execute(event.newParent, event)
    else:
        return

def copied(event):
    """When an object is copied, execute rules assigned to its parent
    """
    obj = event.object
    if not (IContentish.providedBy(obj) or IComment.providedBy(obj)):
        return

    if is_portal_factory(obj):
        return

    execute(aq_parent(aq_inner(event.original)), event)

def forwardevent(obj, event):
    """ Trigger an ObjectMovedOrRenamedEvent only
    if it's not an ObjectAddedEvent or an ObjectRemovedEvent"""
    if IObjectAddedEvent.providedBy(event) \
        or IObjectRemovedEvent.providedBy(event) \
        or IObjectMovedOrRenamedEvent.providedBy(event):
        return
    notify(ObjectMovedOrRenamedEvent(event.object,
                                event.oldParent,
                                event.oldName,
                                event.newParent,
                                event.newName))
