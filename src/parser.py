import os
import traceback
import base64
import datetime
import logging

from xml.etree.ElementTree import XML

from signxml import xmldsig


__all__ = ['AuthenticationError', 'parse_saml']


def decode_response(resp):
    return base64.b64decode(resp.encode('utf8'))


# Getters
def get_xmldoc(xmlstring):
    return XML(xmlstring)


def get_assertion(doc):
    return doc.find('{urn:oasis:names:tc:SAML:2.0:assertion}Assertion')


def get_assertion_attributes(assertion):
    ns = '{urn:oasis:names:tc:SAML:2.0:assertion}'
    attributes = {}
    for attr in assertion.find(
            '{}AttributeStatement'.format(ns)).getchildren():
        val = attr.find('{}AttributeValue'.format(ns))
        attributes[attr.attrib['Name']] = val.text
    return attributes


def get_conditions(assertion):
    ns = '{urn:oasis:names:tc:SAML:2.0:assertion}'
    return assertion.find('{}Conditions'.format(ns))


def strptime(dtstr):
    # Example dtstr: 2014-01-18T11:10:44.9568516Z
    return datetime.datetime.strptime(dtstr.split('.')[0], '%Y-%m-%dT%H:%M:%S')


# Verifications
def verify_ip(reported_ip, client_ip):
    logger = logging.getLogger('islykill')
    logger.debug('Reported ip "%s" - client_ip "%s"',
                 reported_ip, client_ip)
    return reported_ip == client_ip


def verify_date_is_after(reported_date, current_date):
    return reported_date < current_date


def verify_date_is_before(reported_date, current_date):
    return reported_date > current_date


# Helper methods for import
class AuthenticationError(Exception):
    pass


class SAMLResponse(object):
    def __init__(self, kt):
        self.kt = kt


def parse_saml(saml, ip, disable_checks=[], decode=True):
    logger = logging.getLogger('islykill')
    logger.debug('Starting SAML authentication process')
    logger.debug(saml)
    try:
        logger.debug(saml.__class__)
        if decode:
            dec_resp = decode_response(saml)
        else:
            dec_resp = saml

        logger.debug(dec_resp.__class__)

        ca_pem_loc = os.path.dirname(os.path.abspath(__file__))
        ca_pem_file = os.path.join(ca_pem_loc, 'Oll_kedjan.pem')

        logger.debug('Using ca_pem_file: %s' % ca_pem_file)

        xmldsig(dec_resp).verify(ca_pem_file=ca_pem_file)

        logger.debug('verify OK')

        xml = get_xmldoc(dec_resp)
        assertion = get_assertion(xml)
        attributes = get_assertion_attributes(assertion)
        conditions = get_conditions(assertion)

        logger.debug('all XML fetched...')

        now = datetime.datetime.now()

        if not verify_ip(attributes['IPAddress'], ip):
            checkError('verify_ip failed', disable_checks)
        if not verify_date_is_after(
                strptime(conditions.attrib['NotBefore']), now):
            checkError('verify_date_is_after failed', disable_checks)
        if not verify_date_is_before(
                strptime(conditions.attrib['NotOnOrAfter']), now):
            checkError('verify_date_is_before', disable_checks)
            logger.warning(
                'NotOnOrAfter: %s',
                conditions.attrib['NotOnOrAfter'])
            logger.warning(
                'Parsed date: %s',
                strptime(conditions.attrib['NotOnOrAfter']))
            logger.warning(
                'Current date: %s',
                now)
        kt = attributes['UserSSN']
        logger.debug('authenticated successfully: %s', kt)
        return SAMLResponse(kt)
    except AuthenticationError as e:
        logger.error('AuthenticationError: %s', e.message)
        raise e
    except Exception:
        logger.error('Unknown error occurred:')
        logger.error(traceback.format_exc())
        from django.core.mail import mail_admins
        mail_admins('SAML authentication error', traceback.format_exc())
        checkError('Unknown error', disable_checks)


def checkError(name, disable_checks=[]):
    if name not in disable_checks:
        raise AuthenticationError(name)
