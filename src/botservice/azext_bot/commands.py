# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import CliCommandType
from azure.cli.command_modules.botservice._client_factory import (
    get_botservice_management_client)
from azure.cli.command_modules.botservice._exception_handler import bot_exception_handler


def load_command_table(self, _):
    botOperations_commandType = CliCommandType(
        operations_tmpl='azext_bot.botservice.operations.bots_operations#BotsOperations.{}',  # pylint: disable=line-too-long
        client_factory=get_botservice_management_client,
        exception_handler=bot_exception_handler
    )

    # with self.command_group('bot', botOperations_commandType) as g:
    #     g.custom_command('create', 'create')
    #     g.custom_command('show', 'get_bot')
    #     g.custom_command('download', 'download_app')
    #     g.custom_command('publish', 'publish_app')

    with self.command_group('bot manifest', botOperations_commandType) as g:
        g.custom_command('get', 'get_manifest')
        g.custom_command('update', 'put_manifest')

    with self.command_group('bot cortana') as g:
        g.custom_command('create', 'create_cortana')
        g.custom_command('show', 'get_cortana')
        g.custom_command('delete', 'delete_cortana')

    with self.command_group('bot', botOperations_commandType) as g:
        g.custom_command('list', 'list_bots')
        g.custom_command('list-channels', 'list_channels')
        g.custom_command('list-channel-skus', 'list_channel_skus')
        g.custom_command('list-skus', 'list_skus')
        g.custom_command('list-authsetting-skus', 'list_authsetting_skus')
