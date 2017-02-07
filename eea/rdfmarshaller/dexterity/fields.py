from Acquisition import aq_base
from Products.CMFPlone import log
from eea.rdfmarshaller.archetypes.fields import Value2Surf
from eea.rdfmarshaller.archetypes.interfaces import IFieldDefinition2Surf
from eea.rdfmarshaller.dexterity.interfaces import IDXField2Surf
from eea.rdfmarshaller.interfaces import ISurfSession
from eea.rdfmarshaller.marshaller import GenericObject2Surf
from plone.app.textfield.value import RichTextValue
from zope.component import adapts
from zope.interface import implements, Interface
from zope.schema.interfaces import IField
import rdflib
import surf
import sys


class DXField2Surf(object):
    """Base implementation of IDXField2Surf """

    implements(IDXField2Surf)
    # adapts(IField, Interface, ISurfSession)
    adapts(Interface, Interface, ISurfSession)

    exportable = True
    prefix = None   # override the prefix for this predicate
    name = None     # this will be the predicate name (fieldname)

    def __init__(self, field, context, session):
        self.field = field
        self.context = context
        self.session = session

        self.name = self.field.__name__

    def value(self):
        """ Value """
        value = getattr(aq_base(self.context), self.name, None)
        try:
            if callable(value):
                value = value()
            print "Returning '{}' for field {}".format(value, self.name)
            return value
        except Exception:
            log.log('RDF marshaller error for context[field]'
                    '"%s[%s]": \n%s: %s' %
                    (self.context.absolute_url(), self.name,
                     sys.exc_info()[0], sys.exc_info()[1]),
                    severity=log.logging.WARN)

            return None


class RichValue2Surf(Value2Surf):
    adapts(RichTextValue)

    def __init__(self, value):
        self.value = value.output


class DexterityField2RdfSchema(GenericObject2Surf):
    """IFieldDefinition2Surf implemention for Fields;

    This is used to define rdfs schemas for objects,
    extracting their field definitions
    """

    implements(IFieldDefinition2Surf)
    adapts(IField, Interface, ISurfSession)

    _namespace = surf.ns.RDFS
    _prefix = 'rdfs'

    def __init__(self, context, fti, session):
        super(DexterityField2RdfSchema, self).__init__(context, session)
        self.fti = fti

    @property
    def portalType(self):
        """ portal type """
        return u'Property'

    @property
    def rdfId(self):
        """ rdf id """
        return self.context.getName().replace(' ', '')

    @property
    def subject(self):
        """ subject """
        return '%s#%s' % (self.fti.absolute_url(), self.context.getName())

    def modify_resource(self, resource, *args, **kwargs):
        """ Schema to Surf """
        context = self.context

        # TODO: use dexterity mechanism to get widget
        widget_label = (context.title, u'en')
        widget_description = (context.description, u'en')
        fti_title = rdflib.URIRef(u'#%s' % self.fti.Title())

        setattr(resource, 'rdfs_label', widget_label)
        setattr(resource, 'rdfs_comment', widget_description)
        setattr(resource, 'rdf_id', self.rdfId)
        setattr(resource, 'rdf_domain', fti_title)
        return resource
