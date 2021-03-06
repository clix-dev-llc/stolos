from __future__ import unicode_literals

import uuid

import django.contrib.auth.models

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import crypto
from rest_framework.authtoken.models import Token
from sshpubkeys import SSHKey
from sshpubkeys.exceptions import MalformedDataException


def _validate_public_key(value):
    """
    Validates that the given key is a valid SSH public key.
    """
    ssh_key = SSHKey(value, parse_options=False, strict_mode=True)
    try:
        ssh_key.parse()
    except MalformedDataException as exc:
        raise ValidationError(exc.message, code='invalid-key')


def _crypto_40_token():
    return crypto.get_random_string(40)


class APIToken(models.Model):
    """
    Authorization token, used to achieve multiple token authentication in
    Django Rest Framework.
    """
    key = models.CharField(
        max_length=40, primary_key=True, default=_crypto_40_token,
        editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class DockerCert(models.Model):
    """
    Model for storing user's docker certs common names.

    :param token: the key of the auth token, on which the certs are bound to
    :param cert_cn: the common name used to identify a set of certificates

    :type docker_ca_pem: string
    :type docker_cert_pem: string
    """
    owner = models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE,
    )
    token = models.ForeignKey(APIToken, on_delete=models.CASCADE)
    cert_cn = models.CharField(max_length=32, editable=False)

    class Meta:
        permissions = (
            ('view_dockercert', 'Can view Docker Certificate'),
        )


class SSHPublicKey(models.Model):
    """
    Model storing the SSH public keys of a user. This also includes their
    MD5, SHA256 and SHA512 fingerprints.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    public_key = models.TextField(unique=True,
                                  validators=[_validate_public_key])
    md5 = models.CharField(unique=True, max_length=256, editable=False)
    sha256 = models.CharField(unique=True, max_length=256, editable=False)
    sha512 = models.CharField(unique=True, max_length=256, editable=False)
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('name', 'owner',)
        permissions = (
            ('view_sshpublickey', 'Can view public key'),
        )

    def parse(self):
        """
        Cleans the key from comments and options and pulates the MD5, SHA256
        and SHA512 sums.
        """
        ssh_key = SSHKey(
            self.public_key, parse_options=False, strict_mode=True)
        ssh_key.parse()
        # Tiny hack, to get the clean key
        self.public_key = ' '.join(ssh_key._split_key(ssh_key.keydata))
        self.md5 = ssh_key.hash_md5()
        self.sha256 = ssh_key.hash_sha256()
        self.sha512 = ssh_key.hash_sha512()
