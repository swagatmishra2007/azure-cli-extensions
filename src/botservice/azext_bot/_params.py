# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.arguments import CLIArgumentType

from azure.cli.core.commands.parameters import (
    resource_group_name_type,
    get_enum_type,
    get_three_state_flag,
    tags_type)

name_arg_type = CLIArgumentType(metavar='NAME', configured_default='botname')


# pylint: disable=line-too-long,too-many-statements
def load_arguments(self, _):
    with self.argument_context('bot') as c:
        c.argument('resource_group_name', arg_type=resource_group_name_type)
        c.argument('resource_name', options_list=['--name', '-n'], help='the Resource Name of the bot.', arg_type=name_arg_type)

    with self.argument_context('bot manifest get') as c:
        c.argument('manifest_path', options_list=['--path'], help='path to the manifest file')
        c.argument('overwrite_if_exists', options_list=['--overwrite'], help='If True, the existing manifest file gets overwritten.')
    
    with self.argument_context('bot manifest update') as c:
        c.argument('manifest_path', options_list=['--path'], help='path to the manifest file')