# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os
import shutil
import json
import uuid
from knack.util import CLIError
from azure.mgmt.botservice.models import Bot, BotProperties, Sku
from azure.cli.core._profile import Profile  # pylint: disable=unused-import

def get_auth_token(cli_ctx):
    profile = Profile(cli_ctx=cli_ctx)
    creds, subscription, tenant = profile.get_raw_token()
    return 'bearer {0}'.format(creds[1])

def get_request_headers(cli_ctx, bots):
    header_parameters = {}
    header_parameters['Accept'] = 'application/json'
    header_parameters['Content-Type'] = 'application/json; charset=utf-8'
    header_parameters['customAuthToken'] = get_auth_token(cli_ctx)
    if bots.config.generate_client_request_id:
        header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
    if bots.config.accept_language is not None:
        header_parameters['accept-language'] = bots._serialize.header("self.config.accept_language", bots.config.accept_language, 'str')
    
    return header_parameters


def get_manifest(cmd, client, resource_group_name, resource_name, manifest_path=None, overwrite_if_exists=False):
    import os
    manifest_path = manifest_path or os.getcwd()
    import uuid
    bots = client.bots
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/manifest'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'

    # Construct headers
    header_parameters = get_request_headers(cmd.cli_ctx, bots)

    # Construct and send request
    request = bots._client.get(url, query_parameters, header_parameters)
    response = bots._client.send(request, stream=False)

    if response.status_code not in [200]:
        raise CLIError('request failed with response code {0}'.format(response.status_code))
    import json
    response_json = json.loads(response.content)
    blob_url = response_json['properties']['manifestUrl']

    import requests
    response = requests.get(blob_url)
    manifest_file = os.path.join(manifest_path, '{0}_manifest.json'.format(resource_name))
    if os.path.exists(manifest_file) and not overwrite_if_exists:
        raise CLIError('{0} already exists. Please delete the file and run the command again'.format(manifest_file))
    with open(manifest_file, 'w+') as f:
        json.dump(json.loads(response.text), f, indent=4)
    return {'manifestPath': manifest_file}


def put_manifest(cmd, client, resource_group_name, resource_name, manifest_path=None):
    import os
    manifest_path = manifest_path or os.path.join( os.getcwd(), '{0}_manifest.json'.format(resource_name))
    if not os.path.exists(manifest_path):
        raise CLIError('{0} does not exist. Please provide a valid path'.format(manifest_path))
    import uuid
    bots = client.bots
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/manifest'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'

    # Construct headers
    header_parameters = get_request_headers(cmd.cli_ctx, bots)
    data = None
    with open(manifest_path, 'rb') as f:
        data = f.read()
    # Construct and send request
    request = bots._client.put(url, query_parameters, header_parameters, data)
    response = bots._client.send(request, stream=False)
    if response.status_code not in [200]:
        response_json = json.loads(response.content)
        error_string = response_json['properties']['errorMessage']
        raise CLIError('Error encountered while updating manifest - {0}'.format(error_string))
    return json.loads(response.text)


def get_cortana(cmd, client, resource_group_name, resource_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/channels/CortanaChannel'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    bots = client.bots
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'
    profile = Profile(cli_ctx=cmd.cli_ctx)
    creds, subscription, tenant = profile.get_raw_token()
    query_parameters['customAuthToken'] = 'bearer {0}'.format(creds[0])
    # Construct headers
    header_parameters = get_request_headers(cmd.cli_ctx, bots)
    from azure.mgmt.botservice.models import BotChannel
    botChannel = BotChannel(
        location='global',
        properties=CortanaChannel()
    )
    request = bots._client.get(url, query_parameters, header_parameters)
    response = bots._client.send(request, stream=False)
    return json.loads(response.text)

def delete_cortana(cmd, client, resource_group_name, resource_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/channels/CortanaChannel'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    bots = client.bots
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'
    profile = Profile(cli_ctx=cmd.cli_ctx)
    creds, subscription, tenant = profile.get_raw_token()
    query_parameters['customAuthToken'] = 'bearer {0}'.format(creds[0])
    # Construct headers
    header_parameters = get_request_headers(cmd.cli_ctx, bots)
    from azure.mgmt.botservice.models import BotChannel
    botChannel = BotChannel(
        location='global',
        properties=CortanaChannel()
    )
    request = bots._client.delete(url, query_parameters, header_parameters)
    response = bots._client.send(request, stream=False)
    if response.status_code not in [204]:
        raise CLIError('Delete request failed with status code {0}'.format(response.status_code))

from azure.mgmt.botservice.models import Channel
class CortanaChannel(Channel):
    def __init__(self, **kwargs):
        self.channel_name='CortanaChannel'

class CortanaChannelProperties:
    def __init__(self, **kwargs):
        self.isEnabled=True

def create_cortana(cmd, client, resource_group_name, resource_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/channels/CortanaChannel'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    bots = client.bots
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'
    # Construct headers
    header_parameters = get_request_headers(cmd.cli_ctx, bots)

    from azure.mgmt.botservice.models import BotChannel
    botChannel = BotChannel(
        location='global',
        properties=CortanaChannel()
    )
    body_content = bots._serialize.body(botChannel, 'BotChannel')
    request = bots._client.put(url, query_parameters, header_parameters, body_content)
    response = bots._client.send(request, stream=False)
    return json.loads(response.text)

def get_resource(cmd, client, url):
    bots = client.bots
    query_parameters = {}
    query_parameters['api-version'] = '2018-07-12'
    request = bots._client.get(url, query_parameters)
    response = bots._client.send(request, stream=False)
    return json.loads(response.text)

def list_bots(cmd, client, resource_group_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices'.format(client.bots.config.subscription_id, resource_group_name)
    return get_resource(cmd, client, url)

def list_channels(cmd, client, resource_group_name, resource_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices/{2}/channels'.format(client.bots.config.subscription_id, resource_group_name, resource_name)
    return get_resource(cmd, client, url)

def list_channel_skus(cmd, client, resource_group_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices'.format(client.bots.config.subscription_id, resource_group_name)
    return get_resource(cmd, client, url)

def list_skus(cmd, client, resource_group_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices'.format(client.bots.config.subscription_id, resource_group_name)
    return get_resource(cmd, client, url)

def list_authsetting_skus(cmd, client, resource_group_name):
    url = '/subscriptions/{0}/resourceGroups/{1}/providers/Microsoft.BotService/botServices'.format(client.bots.config.subscription_id, resource_group_name)
    return get_resource(cmd, client, url)