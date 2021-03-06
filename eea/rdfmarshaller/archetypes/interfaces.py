""" Archetypes Interfaces
"""
from zope.interface import Interface, Attribute
from Products.Archetypes.interfaces import IField
from eea.rdfmarshaller.interfaces import IGenericObject2Surf


class IArchetype2Surf(IGenericObject2Surf):
    """ IObject2Surf implementations for Archetype objects

    This interface is only used to describe the Archetype2Surf
    implementation. The IObject2Surf interface should be used as
    adapter interface
    """

    dc_map = Attribute(u"Mapping of field names to rdf names, for which  "
                       u"the prefix will be dcterms")
    field_map = Attribute(u"Mapping of fields to rdf names. It can be used "
                          u"to remap the field names in the rdf output ")
    blacklist_map = Attribute(u"A list of field names for fields that "
                              u"won't be exported")


class IATField2Surf(Interface):
    """ Extract values from Fields, to store them in the surf session """

    def value(context):
        """ Returns the value in RDF format """

    exportable = Attribute("Is this field exportable to RDF?")


class IATVocabulary(Interface):
    """ Marker interface for ATVocabularyManager Simple Vocabulary """


class IATVocabularyTerm(Interface):
    """ Marker interface for ATVocabularyManager Simple Term """


class IReferenceField(IField):
    """ Marker interface for Products.Archetypes.Field.ReferenceField """


class ITextField(IField):
    """ Marker interface for Products.Archetypes.Field.TextField """
